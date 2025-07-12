import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

def scale_features_tab(df):
    st.subheader("Feature Scaling")

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if not numeric_cols:
        st.warning("No numeric columns found.")
        return df

    selected_cols = st.multiselect("Select columns to scale", numeric_cols)
    method = st.selectbox("Select scaling method", ["StandardScaler", "MinMaxScaler", "RobustScaler"])
    mode = st.radio("How to apply scaling?", ["Replace original columns", "Add new columns (suffix: _scaled)"])

    if st.button("Apply Scaling"):
        if not selected_cols:
            st.warning("Please select at least one column.")
            return df

        scaler = None
        if method == "StandardScaler":
            scaler = StandardScaler()
        elif method == "MinMaxScaler":
            scaler = MinMaxScaler()
        elif method == "RobustScaler":
            scaler = RobustScaler()

        scaled_data = scaler.fit_transform(df[selected_cols])
        scaled_df = pd.DataFrame(scaled_data, columns=selected_cols)

        if mode == "Add new columns (suffix: _scaled)":
            for col in selected_cols:
                df[col + "_scaled"] = scaled_df[col]
        else:
            for col in selected_cols:
                df[col] = scaled_df[col]

        st.success(f"Applied {method} to {len(selected_cols)} column(s).")
        st.dataframe(df[selected_cols if mode == 'Replace original columns' else [col + "_scaled" for col in selected_cols]].head())

        # Update global state
        st.session_state.df = df
        st.session_state.change_log.append(f"Scaled columns {selected_cols} using {method} ({mode}).")

    return df

