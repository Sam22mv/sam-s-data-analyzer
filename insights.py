import streamlit as st
import pandas as pd

def generate_insights(df):
    st.subheader("Dataset Insights")

    # 1. Shape
    st.markdown("#### Shape of Dataset")
    st.write(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")

    # 2. Descriptive Statistics
    st.markdown("#### Descriptive Statistics")
    st.dataframe(df.describe().T)

    # 3. Data Types
    st.markdown("#### Data Types")
    st.dataframe(df.dtypes.astype(str))

    # 4. Null Values
    st.markdown("#### Null Values")
    null_counts = df.isnull().sum()
    st.dataframe(null_counts[null_counts > 0])

    # 5. Top Null Columns (numeric only)
    st.markdown("#### Top Missing Value Columns (Numeric)")
    numeric_nulls = df.select_dtypes(include=['float64', 'int64']).isnull().sum().sort_values(ascending=False)
    st.dataframe(numeric_nulls[numeric_nulls > 0].head(5))

    # 6. Low-Variance Columns (useless features)
    st.markdown("#### Low-Variance Columns (Constant or Near-Constant)")
    low_var_cols = [col for col in df.columns if df[col].nunique() <= 1]
    if low_var_cols:
        st.write(low_var_cols)
    else:
        st.success("No constant-value columns detected.")

    # 7. High Correlation Pairs
    st.markdown("#### Highly Correlated Numeric Columns (> 0.85)")
    corr = df.select_dtypes(include=['float64', 'int64']).corr()
    high_corr = []
    for i in range(len(corr.columns)):
        for j in range(i):
            if abs(corr.iloc[i, j]) > 0.85:
                high_corr.append((corr.columns[i], corr.columns[j], corr.iloc[i, j]))
    if high_corr:
        for col1, col2, val in high_corr:
            st.write(f" {col1} ↔ {col2} → Correlation: {val:.2f}")
    else:
        st.info("No strongly correlated numeric columns.")

    # 8. Top 5 Categories in Object Columns
    st.markdown("#### Top Categories in Categorical Columns")
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(cat_cols) == 0:
        st.info("No categorical columns.")
    else:
        for col in cat_cols:
            st.write(f"**{col}**")
            st.write(df[col].value_counts().head(5))

    # 9. High Cardinality Columns
    st.markdown("#### High Cardinality Columns (Many Unique Values)")
    high_card_cols = [col for col in df.columns if df[col].nunique() > df.shape[0] * 0.9]
    if high_card_cols:
        st.warning(f"High cardinality columns: {', '.join(high_card_cols)}")
    else:
        st.success("No high-cardinality columns found.")
