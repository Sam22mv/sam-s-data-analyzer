import streamlit as st
import plotly.express as px

def generate_visualizations(df):
    st.subheader("Select Visualization Type")

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    chart_type = st.selectbox("Choose chart type", ["Line", "Bar", "Histogram", "Pie", "Scatter"])

    charts = []  # Collect figures for export

    if chart_type in ["Line", "Bar", "Scatter"]:
        x_col = st.selectbox("Select X-axis", df.columns)
        y_col = st.selectbox("Select Y-axis", numeric_cols)

        if chart_type == "Line":
            fig = px.line(df, x=x_col, y=y_col)
        elif chart_type == "Bar":
            fig = px.bar(df, x=x_col, y=y_col)
        elif chart_type == "Scatter":
            fig = px.scatter(df, x=x_col, y=y_col)

        st.plotly_chart(fig, use_container_width=True)
        charts.append(fig)

    elif chart_type == "Histogram":
        col = st.selectbox("Select column for histogram", numeric_cols)
        fig = px.histogram(df, x=col)
        st.plotly_chart(fig, use_container_width=True)
        charts.append(fig)

    elif chart_type == "Pie":
        col = st.selectbox("Select categorical column", categorical_cols)
        pie_data = df[col].value_counts().reset_index()
        pie_data.columns = [col, "Count"]
        fig = px.pie(pie_data, names=col, values="Count")
        st.plotly_chart(fig, use_container_width=True)
        charts.append(fig)

    return charts  # Return all created figures

