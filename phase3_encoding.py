import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def encode_categories_tab(df):
    st.subheader("Encode Categorical Variables")

    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    if not cat_cols:
        st.info("No categorical columns found.")
        return df

    selected_cols = st.multiselect("Select columns to encode", cat_cols)
    method = st.radio("Encoding method", ["One-Hot Encoding", "Label Encoding"])
    mode = st.radio("How to apply encoding?", ["Add new columns", "Replace original columns"])

    if st.button("Apply Encoding"):
        if not selected_cols:
            st.warning("Please select at least one column.")
            return df

        if method == "One-Hot Encoding":
            encoded_df = pd.get_dummies(df[selected_cols], prefix=selected_cols, drop_first=False)

            if mode == "Add new columns":
                df = pd.concat([df, encoded_df], axis=1)
            else:  # replace
                df.drop(columns=selected_cols, inplace=True)
                df = pd.concat([df, encoded_df], axis=1)

        elif method == "Label Encoding":
            for col in selected_cols:
                le = LabelEncoder()
                encoded = le.fit_transform(df[col].astype(str))
                if mode == "Add new columns":
                    df[col + "_label"] = encoded
                else:
                    df[col] = encoded

        st.success(f"Applied {method} to {len(selected_cols)} column(s).")
        st.dataframe(df.head())

        # Save back to memory
        st.session_state.df = df
        st.session_state.change_log.append(f"Encoded columns {selected_cols} using {method} ({mode}).")

    return df
