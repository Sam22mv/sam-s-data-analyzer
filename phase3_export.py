import streamlit as st

def export_final_tab(df):
    st.subheader("Export Final Dataset")

    st.markdown("You can now download the updated dataset after all preprocessing steps.")

    st.dataframe(df.head())

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="⬇️ Download Final CSV",
        data=csv,
        file_name="numerix_processed.csv",
        mime="text/csv"
    )
