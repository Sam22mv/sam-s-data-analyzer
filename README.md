# Sam's Data Analyzer

Sam's Data Analyzer is a fully interactive web-based tool for exploring, cleaning, visualizing, and preparing datasets for analysis and machine learning — all without writing code.

>  Live App: [Open on Streamlit Cloud](https://sam-s-data-analyzer-4ras42xdgv4bjkjhzrtbm4.streamlit.app/)  

>  GitHub Repo: [github.com/Sam22mv/sam-s-data-analyzer](https://github.com/Sam22mv/sam-s-data-analyzer)

>  Video Demo: [open google drive link](https://drive.google.com/file/d/1N5uJsJUbfW8K_p88yYBvqJbwJ5KILWBR/view?usp=sharing)  
---

## Features

### Phase 1: Analyze Dataset
- **Insights Tab**:
  - View dataset shape, null values, data types
  - Descriptive statistics
  - Correlation matrix with filter on high correlations
- **Visualization Tab**:
  - Line, Bar, Histogram, Pie, and Scatter charts
  - Dynamic axis selection with Plotly

### Phase 2: Clean and Explore
- **Clean Data**:
  - Drop nulls or duplicates
  - Fill missing values with Mean, Median, Mode, Constant, Zero, or Interpolation
- **Fix Data Types**:
  - Convert columns to integer, float, string, datetime, or categorical
  - Auto-handle garbage values like %, commas, and null placeholders
- **Outlier Detection**:
  - Box plot visualization
  - IQR-based detection with option to retain specific outlier rows
- **Explore Features**:
  - Univariate analysis with histogram and skewness
  - Bivariate scatter plots with correlation
  - Correlation matrix for numeric columns

### Phase 3: Preprocessing
- **Scaling**:
  - StandardScaler, MinMaxScaler, RobustScaler
- **Encoding**:
  - Label Encoding for categorical variables
- **Skewness Correction**:
  - Yeo-Johnson transformation for non-normal distributions

---

## Folder Structure
numerix_app.py # Main Streamlit app
├── insights.py # Insights (nulls, stats, correlations)
├── visualizer.py # Chart generation (Plotly)
├── report_generator.py # PDF report builder
├── phase2_cleaning.py # Drop/fill missing/duplicate rows
├── phase2_dtypes.py # Data type converter
├── phase2_outliers.py # Box plot + IQR outlier control
├── phase2_explore.py # Univariate and bivariate EDA
├── phase3_scaling.py # Feature scaling
├── phase3_encoding.py # Categorical encoding
├── phase3_skew_transform.py # Skewness transformation
└── requirements.txt # Required libraries

---

## Tech Stack

| Library         | Use Case                        |
|----------------|----------------------------------|
| Streamlit       | Web UI for interactive app       |
| Pandas          | Data manipulation and EDA        |
| NumPy           | Numerical operations             |
| Plotly          | Interactive charts               |
| Seaborn         | Correlation heatmaps             |
| Matplotlib      | Auxiliary visualizations         |
| FPDF            | PDF export of results            |
| Scikit-learn    | Preprocessing (scaling, encoding)|
| SciPy           | Yeo-Johnson transformation       |

---

## Run Locally

```bash
git clone https://github.com/Sam22mv/sam-s-data-analyzer.git
cd sam-s-data-analyzer
pip install -r requirements.txt
streamlit run numerix_app.py
