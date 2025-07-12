import streamlit as st
import plotly.express as px
import pandas as pd

def detect_outliers_tab(df):
    st.subheader("Outlier Detection with Box Plot")

    # --- Step 1: Select numeric column ---
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    if not num_cols:
        st.warning("No numeric columns available.")
        return df

    col = st.selectbox("Select numeric column", num_cols)

    # --- Step 2: Clean and plot ---
    clean_data = df[col].dropna()
    fig = px.box(clean_data, y=col, points="outliers", title=f"Box Plot of '{col}'")
    st.plotly_chart(fig, use_container_width=True)

    # --- Step 3: IQR calculation ---
    Q1 = clean_data.quantile(0.25)
    Q3 = clean_data.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outlier_rows = df[(df[col] < lower) | (df[col] > upper)]

    st.markdown("### Outlier Summary (IQR Method)")
    st.code(f"""
Q1  = {Q1:.2f}
Q3  = {Q3:.2f}
IQR = {IQR:.2f}

Lower Bound = {lower:.2f}
Upper Bound = {upper:.2f}

Outliers Detected = {outlier_rows.shape[0]}
    """)

    if outlier_rows.empty:
        st.success("No outliers detected.")
        return df

    # --- Step 4: Manage selection state ---
    outlier_indices = outlier_rows.index.tolist()
    key = f"selected_outliers_{col}"

    if key not in st.session_state:
        st.session_state[key] = outlier_indices  # default: all selected

    # 🛡 Ensure default values are valid
    valid_defaults = [i for i in st.session_state[key] if i in outlier_indices]

    # Buttons to update session state
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Select All Outliers"):
            st.session_state[key] = outlier_indices
            valid_defaults = outlier_indices
    with col2:
        if st.button("❌ Clear All Selection"):
            st.session_state[key] = []
            valid_defaults = []

    # --- Step 5: Multiselect UI ---
    selected_to_keep = st.multiselect(
        "Choose rows to keep (based on index):",
        options=outlier_indices,
        default=valid_defaults,
        key=f"multiselect_{col}"
    )

    st.dataframe(outlier_rows)

    # --- Step 6: Apply removal ---
    if st.button(f"Remove Unselected Outliers from `{col}`"):
        to_remove = outlier_rows[~outlier_rows.index.isin(selected_to_keep)].index
        before = df.shape[0]
        df = df.drop(index=to_remove)
        after = df.shape[0]
        removed = before - after
        st.success(f"Removed {removed} outlier rows from `{col}`.")
        st.markdown(f"**New shape:** `{after} rows × {df.shape[1]} columns`")

        # Log the change
        if removed > 0 and "change_log" in st.session_state:
            st.session_state.change_log.append(f"Removed {removed} outliers from '{col}'")

        # Clear state
        del st.session_state[key]

    return df


