from fpdf import FPDF
import tempfile
import pandas as pd
import plotly.io as pio
import os
import time

pio.kaleido.scope.default_format = "png"

class PDFReport(FPDF):
    def header(self):
        if self.page_no() == 1:
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, "NumeriX Report", ln=True, align="C")
            self.ln(10)

    def section_title(self, title):
        self.ln(5)
        self.set_font("Arial", "B", 12)
        self.set_text_color(33, 37, 41)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def section_body(self, text):
        self.set_font("Arial", "", 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 6, text)
        self.ln()

def generate_pdf_report(df, charts: list, dataset_name="Unnamed Dataset"):
    pdf = PDFReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Dataset Name
    pdf.section_title("Dataset Name")
    pdf.section_body(dataset_name)

    # Dataset Info
    pdf.section_title("Dataset Info")
    shape_info = f"Rows: {df.shape[0]}\nColumns: {df.shape[1]}"
    pdf.section_body(shape_info)

    # Data Types
    pdf.section_title("Data Types")
    try:
        dtypes_str = df.dtypes.astype(str).to_string()
        pdf.section_body(dtypes_str)
    except Exception as e:
        pdf.section_body(f"Could not extract data types: {e}")

    # Null Values
    pdf.section_title("Null Values")
    nulls = df.isnull().sum()
    nulls_present = nulls[nulls > 0]
    if not nulls_present.empty:
        pdf.section_body(nulls_present.to_string())
    else:
        pdf.section_body("No missing values.")

    # Descriptive Statistics
    pdf.add_page()
    pdf.section_title("Descriptive Statistics")
    try:
        desc_stats = df.describe().T.round(2).to_string()
        pdf.section_body(desc_stats)
    except Exception as e:
        pdf.section_body(f"Could not compute statistics: {e}")

    # Correlation Matrix
    pdf.section_title("Correlation Matrix (|corr| > 0.85)")
    try:
        corr = df.select_dtypes(include='number').corr()
        pairs = []
        for i in range(len(corr.columns)):
            for j in range(i):
                val = corr.iloc[i, j]
                if abs(val) > 0.85:
                    pairs.append(f"{corr.columns[i]} <-> {corr.columns[j]}: {val:.2f}")
        corr_text = "\n".join(pairs) if pairs else "No strong correlations."
        pdf.section_body(corr_text)
    except Exception as e:
        pdf.section_body(f"Could not calculate correlation matrix: {e}")

    # Visualizations
    if charts:
        pdf.add_page()
        pdf.section_title("Visualizations")
        for fig in charts:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                    tmpfile_path = tmpfile.name
                fig.write_image(tmpfile_path, format="png", scale=2)
                pdf.image(tmpfile_path, w=180)
                time.sleep(0.1)
                os.unlink(tmpfile_path)
            except Exception as e:
                pdf.section_body(f"[Error rendering chart: {e}]")

    # Save final PDF to temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        pdf.output(f.name)
        return f.name

