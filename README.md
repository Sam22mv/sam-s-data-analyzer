# Sam's Data Analyzer

Sam's Data Analyzer (formerly NumeriX) is a fully interactive web-based tool for exploring, cleaning, visualizing, and preparing datasets for analysis and machine learning — all without writing code.

>  Live App: [Open on Streamlit Cloud](https://sam-s-data-analyzer-4ras42xdgv4bjkjhzrtbm4.streamlit.app/)  
>  GitHub Repo: [github.com/Sam22mv/sam-s-data-analyzer](https://github.com/Sam22mv/sam-s-data-analyzer)
>  Video Demo: 
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

