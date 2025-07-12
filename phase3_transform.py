import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import yeojohnson

def transform_skew_tab(df):
    st.subheader("🔃 Transform Skewed Numeric Features")

    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    if not num_cols:
        st.info("No numeric columns found.")
        return df

    skew_df = df[num_cols].skew().sort_values(ascending=False)
    skewed_cols = skew_df[abs(skew_df) > 0.7].index.tolist()

    if not skewed_cols:
        st.success("No significantly skewed columns found.")
        return df

    st.markdown(f"**Detected Skewed Columns (|skew| > 0.7):**")
    st.dataframe(skew_df[abs(skew_df) > 0.7].round(2))

    col = st.selectbox("Select a column to transform", skewed_cols)
    method = st.selectbox("Select transformation", ["Log", "Square Root", "Yeo-Johnson"])
    mode = st.radio("How to apply?", ["Add as new column", "Replace original"])

    if st.button("Apply Transformation"):
        transformed = df[col].copy()

        try:
            if method == "Log":
                transformed = np.log1p(transformed)
            elif method == "Square Root":
                transformed = np.sqrt(transformed)
            elif method == "Yeo-Johnson":
                transformed, _ = yeojohnson(transformed.fillna(0))  # Replace NaN temporarily

            if mode == "Add as new column":
                df[col + f"_{method.lower()}"] = transformed
            else:
                df[col] = transformed

            st.success(f"Applied {method} transformation to `{col}`.")
            st.plotly_chart(px.histogram(transformed, nbins=30, title=f"{col} after {method} transformation"))

            # Save to session state
            st.session_state.df = df
            st.session_state.change_log.append(f"Transformed `{col}` using `{method}` ({mode}).")

        except Exception as e:
            st.error(f"❌ Transformation failed: {e}")

    return df
