import streamlit as st
import pandas as pd
from insights import generate_insights
from visualizer import generate_visualizations
from report_generator import generate_pdf_report

from phase2_cleaning import clean_data_tab
from phase2_dtypes import fix_data_types_tab
from phase2_outliers import detect_outliers_tab
from phase2_explore import explore_features_tab
from phase3_scaling import scale_features_tab
from phase3_encoding import encode_categories_tab
from phase3_transform import transform_skew_tab
from phase3_export import export_final_tab


#--------------------------------------------------------------Page configuration
st.set_page_config(page_title="Sam's", layout="wide")
st.title("Become a Data Analyst")

#--------------------------------------------------------------File Upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

#--------------------------------------------------------------Show instructions only when file not uploaded
if not uploaded_file:
    with st.expander("Instructions & Upload Guidelines", expanded=True):
        st.markdown("""
### File Upload Rules

**A) Supported File Format**
- Only `.csv` files allowed.

**B) File Requirements**
- First row must contain column headers.
- Each column should have a **unique name**.
- Avoid merged cells or inconsistent column types.
- Recommended encoding: **UTF-8** (default in most tools).

**C) Common Issues to Avoid**
- Missing headers → dropdowns won't work.
- Mixed data types in one column → errors in visualization.
- Blank rows or extra unnamed columns may lead to crashes.

---

**Features of NumeriX**

- **Insight Tab**:
  - Dataset shape, nulls, types, stats
  - High correlation detection
  - Low-variance column detection
  - Top categories & high cardinality warnings

- **Visualization Tab**:
  - Line, Bar, Histogram, Pie, Scatter (via Plotly)
  - Customizable axes for numeric/categorical data
""", unsafe_allow_html=True)

#--------------------------------------------------------Proceed when file is uploaded
if uploaded_file:
    # Initialize session state once
    if 'df' not in st.session_state:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.session_state.change_log = []

    df = st.session_state.df
    dataset_name = uploaded_file.name

    #----------------------------------------------------Reset button
    if st.button("Reset Dataset"):
        st.session_state.df = pd.read_csv(uploaded_file)
        st.session_state.change_log = []
        st.success("Dataset reset to original.")
        df = st.session_state.df

    #-----------------------------------------------------Preview
    st.subheader("Data Preview")
    st.dataframe(df.head())

    # Phase 1 Tabs
    tab1, tab2 = st.tabs(["Insights", "Visualizations"])

    with tab1:
        generate_insights(df)

    with tab2:
        charts = generate_visualizations(df)

    #-----------------------------------------------------Download report
    if st.button("Download Full Report (PDF)"):
        if charts:
            pdf_path = generate_pdf_report(df, charts, dataset_name=dataset_name)
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download Full Report", f, file_name="numerix_report.pdf", mime="application/pdf")
        else:
            st.warning("No charts generated yet. Please generate at least one chart.")

    # Phase 2 Tabs
    st.markdown("---")
    st.subheader("Phase 2: Clean & Explore Your Data")

    tab_clean, tab_dtypes, tab_outliers, tab_eda = st.tabs([
        "Clean Data",
        "Fix Data Types",
        "Outlier Detection",
        "Explore Features"
    ])

    with tab_clean:
        df = clean_data_tab(df)
        st.session_state.df = df

    with tab_dtypes:
        df = fix_data_types_tab(df)
        st.session_state.df = df

    with tab_outliers:
        df = detect_outliers_tab(df)
        st.session_state.df = df

    with tab_eda:
        explore_features_tab(df)

    st.markdown("---")
    st.subheader("Phase 3: Feature Transformation & Scaling")

    tab_scaling, tab_encoding, tab_transform, tab_export = st.tabs([
        "Feature Scaling",
        "Encode Categories",
        "Transform Skew",
        "Export Final Data"
    ])    


    with tab_scaling:
        df = scale_features_tab(df)

    with tab_encoding:
        df = encode_categories_tab(df)

    with tab_transform:
        df = transform_skew_tab(df)    

    with tab_export:
        export_final_tab(df)

    #-----------------------------------------------------Summary Log of Changes
    if st.session_state.change_log:
        st.markdown("---")
        st.subheader("Dataset Modification Summary")
        for entry in st.session_state.change_log:
            st.markdown(f"- {entry}")

else:
    st.info("Please upload a CSV file to proceed.")
