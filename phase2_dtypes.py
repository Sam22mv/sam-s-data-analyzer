import streamlit as st
import pandas as pd
import numpy as np

def fix_data_types_tab(df):
    st.subheader("Convert Data Types")

    column = st.selectbox("Select column to convert", df.columns)
    dtype_options = ["int", "float", "str", "datetime", "category"]
    target_dtype = st.selectbox("Convert to", dtype_options)

    # Skip conversion if already that type
    if str(df[column].dtypes) == target_dtype:
        st.info(f" Column `{column}` is already of type `{target_dtype}`.")
        return df

    if st.button("Convert Data Type"):
        try:
            original_series = df[column].copy()

            # Step 1: Clean garbage
            cleaned = original_series.astype(str).str.strip()
            cleaned = cleaned.str.replace('%', '', regex=False)
            cleaned = cleaned.str.replace(',', '', regex=False)
            cleaned = cleaned.replace(["", " ", "NaN", "nan", "None", "null", "--"], np.nan)

            # Step 2: Conversion
            if target_dtype == "datetime":
                year_only = cleaned.str.match(r"^\d{4}(\.0)?$")
                cleaned.loc[year_only] = cleaned.loc[year_only].str.extract(r"(\d{4})")[0] + "-01-01"
                df[column] = pd.to_datetime(cleaned, errors='coerce', infer_datetime_format=True)

                if df[column].isna().all():
                    st.warning(f"⚠️ All values in `{column}` failed to convert to datetime.")

            elif target_dtype == "category":
                df[column] = cleaned.astype("category")

            elif target_dtype == "int":
                df[column] = pd.to_numeric(cleaned, errors='coerce').fillna(0).astype(int)

            elif target_dtype == "float":
                df[column] = pd.to_numeric(cleaned, errors='coerce')

            elif target_dtype == "str":
                df[column] = original_series.astype(str)

            # Step 3: Success output
            st.success(f" `{column}` converted to `{target_dtype}`.")
            st.code(f"New dtype: {df[column].dtypes}")
            st.markdown("**Sample values after conversion:**")
            st.dataframe(df[[column]].dropna().head(10))

            # Log the change
            st.session_state.change_log.append(f"Converted '{column}' to {target_dtype}")

        except Exception as e:
            st.error(f"❌ Conversion failed: {e}")
            return df

    # 🔍 Dataset Summary
    st.markdown("---")
    st.subheader("Dataset Summary After Conversion")

    st.markdown("**🔹 Shape:**")
    st.code(f"{df.shape[0]} rows × {df.shape[1]} columns")

    st.markdown("**🔹 Data Types:**")
    st.dataframe(df.dtypes.astype(str).reset_index().rename(columns={"index": "Column", 0: "Dtype"}))

    st.markdown("**🔹 Null Values per Column:**")
    nulls = df.isna().sum()
    st.dataframe(nulls[nulls > 0].reset_index().rename(columns={"index": "Column", 0: "Null Count"}))

    # Save changes
    st.session_state.df = df
    return df
