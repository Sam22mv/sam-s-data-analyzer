import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.figure_factory as ff


def explore_features_tab(df):
    st.subheader("Feature Exploration Dashboard")

    st.markdown("### 🔹 Dataset Overview")
    st.markdown(f"- Rows: `{df.shape[0]}`  | Columns: `{df.shape[1]}`")

    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    date_cols = df.select_dtypes(include='datetime64').columns.tolist()

    st.markdown(f"- Numeric Columns: `{len(num_cols)}` | Categorical: `{len(cat_cols)}` | Date: `{len(date_cols)}`")

    # Constant Columns
    constant_cols = [col for col in df.columns if df[col].nunique() <= 1]
    if constant_cols:
        st.warning(f"⚠️ Constant columns (only 1 unique value): {constant_cols}")

    # High Nulls
    high_nulls = df.isnull().mean()
    high_null_cols = high_nulls[high_nulls > 0.5].index.tolist()
    if high_null_cols:
        st.warning(f"⚠️ Columns with >50% nulls: {high_null_cols}")

    # High Cardinality
    high_card_cols = [col for col in cat_cols if df[col].nunique() > 50]
    if high_card_cols:
        st.warning(f"⚠️ High-cardinality categorical columns (>50 unique): {high_card_cols}")

    st.markdown("---")
    st.subheader("Univariate Analysis")
    feature = st.selectbox("Select a column to explore:", df.columns)

    if feature in num_cols:
        st.markdown("**Histogram & Distribution:**")
        fig = px.histogram(df, x=feature, marginal="box", nbins=30)
        st.plotly_chart(fig, use_container_width=True)

        skew = df[feature].skew()
        st.info(f"Skewness: `{skew:.2f}`")

    elif feature in cat_cols:
        st.markdown("**Top Categories:**")
        vc = df[feature].value_counts().head(10)
        fig = px.bar(x=vc.index, y=vc.values, labels={'x': feature, 'y': 'Count'})
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Bivariate Analysis")
    col1 = st.selectbox("X-axis column:", df.columns, key="bivar_x")
    col2 = st.selectbox("Y-axis column:", df.columns, key="bivar_y")

    if col1 != col2:
        if df[col1].dtype in ['int64', 'float64'] and df[col2].dtype in ['int64', 'float64']:
            st.markdown("**Scatter Plot + Correlation:**")
            fig = px.scatter(df, x=col1, y=col2)
            st.plotly_chart(fig, use_container_width=True)
            corr = df[[col1, col2]].corr().iloc[0, 1]
            st.info(f"Correlation: `{corr:.2f}`")

        elif col1 in cat_cols and col2 in num_cols:
            st.markdown("**Box Plot:**")
            fig = px.box(df, x=col1, y=col2)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Correlation Matrix (Numeric Features Only)")
    if len(num_cols) >= 2:
        corr_matrix = df[num_cols].corr().round(2)
        fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r')
        st.plotly_chart(fig, use_container_width=True)

        high_corrs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i):
                val = corr_matrix.iloc[i, j]
                if abs(val) >= 0.7:
                    high_corrs.append(f"{corr_matrix.columns[i]} ↔ {corr_matrix.columns[j]}: {val:.2f}")

        if high_corrs:
            st.markdown("**Highly Correlated Pairs (|corr| > 0.7):**")
            st.code("\n".join(high_corrs))
        else:
            st.info("No strong correlations found.")

    else:
        st.warning("Not enough numeric columns for correlation analysis.")
