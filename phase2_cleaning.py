import streamlit as st
import pandas as pd
import numpy as np

def clean_data_tab(df):
    st.subheader("Clean Your Dataset")

    original_shape = df.shape
    st.markdown(f"**Original shape:** `{original_shape[0]}` rows × `{original_shape[1]}` columns")

    # --- Drop rows with null values ---
    if st.button("Drop Rows with Null Values"):
        before = df.shape[0]
        df.dropna(inplace=True)
        after = df.shape[0]
        dropped = before - after
        st.success(f"Dropped `{dropped}` rows with missing values.")
        st.markdown(f"**New shape:** `{df.shape[0]}` rows × `{df.shape[1]}` columns")
        if dropped > 0:
            st.session_state.change_log.append(f"Dropped {dropped} rows with missing values")

    # --- Drop duplicates ---
    if st.button("Drop Duplicate Rows"):
        before = df.shape[0]
        df.drop_duplicates(inplace=True)
        after = df.shape[0]
        dropped = before - after
        st.success(f"Dropped `{dropped}` duplicate rows.")
        st.markdown(f"**New shape:** `{df.shape[0]}` rows × `{df.shape[1]}` columns")
        if dropped > 0:
            st.session_state.change_log.append(f"Dropped {dropped} duplicate rows")

    st.markdown("---")
    st.subheader("Fill Missing Values (Advanced Options)")

    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # --- Fill numeric ---
    with st.expander("Fill Numeric Column"):
        num_col = st.selectbox("Select numeric column", num_cols, key="num_col")
        num_method = st.selectbox("Fill method", ["Mean", "Median", "Mode", "0", "Constant", "Interpolate"])

        const_num = None
        if num_method == "Constant":
            const_num = st.number_input("Enter constant value to fill with", value=0.0)

        if st.button("Apply Numeric Fill"):
            filled_count = df[num_col].isna().sum()
            if filled_count > 0:
                if num_method == "Mean":
                    df[num_col].fillna(df[num_col].mean(), inplace=True)
                elif num_method == "Median":
                    df[num_col].fillna(df[num_col].median(), inplace=True)
                elif num_method == "Mode":
                    df[num_col].fillna(df[num_col].mode()[0], inplace=True)
                elif num_method == "0":
                    df[num_col].fillna(0, inplace=True)
                elif num_method == "Constant":
                    df[num_col].fillna(const_num, inplace=True)
                elif num_method == "Interpolate":
                    df[num_col].interpolate(method='linear', inplace=True)

                st.success(f"Filled {filled_count} nulls in `{num_col}` using `{num_method}` method.")
                st.session_state.change_log.append(f"Filled {filled_count} nulls in '{num_col}' using {num_method}")
            else:
                st.info(f"No missing values found in `{num_col}`.")

    # --- Fill categorical ---
    with st.expander("Fill Categorical Column"):
        cat_col = st.selectbox("Select categorical column", cat_cols, key="cat_col")
        cat_method = st.selectbox("Fill method", ["Mode", "Constant"])

        const_cat = None
        if cat_method == "Constant":
            const_cat = st.text_input("Enter text to fill with", value="missing")

        if st.button("Apply Categorical Fill"):
            filled_count = df[cat_col].isna().sum()
            if filled_count > 0:
                if cat_method == "Mode":
                    df[cat_col].fillna(df[cat_col].mode()[0], inplace=True)
                elif cat_method == "Constant":
                    df[cat_col].fillna(const_cat, inplace=True)

                st.success(f"Filled {filled_count} nulls in `{cat_col}` using `{cat_method}` method.")
                st.session_state.change_log.append(f"Filled {filled_count} nulls in '{cat_col}' using {cat_method}")
            else:
                st.info(f"No missing values found in `{cat_col}`.")

    return df
