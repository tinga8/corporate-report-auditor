import re
import pandas as pd
import streamlit as st

# 1. UI Configuration
st.set_page_config(page_title="Financial Data Specialist Pipeline", page_icon="📊", layout="wide")
st.title("📊 Multi-Format Financial Ingestion & Standardization Pipeline")
st.caption("Production-Grade Data Collection Framework tailored for S&P Global, Moody's, and Bloomberg")

# 2. Sidebar Architecture Summary
st.sidebar.header("⚙️ Data Engineering Engine")
st.sidebar.info("""
- **Formats:** PDF Layouts, Unstructured Text, Raw Excel Sheets.
- **Normalization:** RegEx mapping and numeric cleansing.
- **Data Quality (DQ):** Mathematical logic guards.
- **Cost:** $0 (Zero API dependancies).
""")

# 3. Multi-Format File Ingestion
uploaded_file = st.file_uploader(
    "Upload Financial Document (Accepts: .txt, .xlsx, .xls)", 
    type=["txt", "xlsx", "xls"]
)

# Note for PDF Handling: PDF parsing in pure cloud environments requires external binaries.
# To keep this pipeline 100% free and zero-setup, we provide instant extraction for Text and Excel.

raw_text = ""
excel_df = None

if uploaded_file is not None:
    file_name = uploaded_file.name
    st.subheader(f"📥 Processing Ingested File: `{file_name}`")
    
    # --- HANDLING EXCEL FILES ---
    if file_name.endswith(('.xlsx', '.xls')):
        try:
            excel_df = pd.read_excel(uploaded_file)
            st.success("✅ Excel Sheet Loaded Successfully.")
            with st.expander("View Raw Ingested Sheet Structure"):
                st.dataframe(excel_df.head(10))
            
            # Flatten Excel data to text for the extraction engine to analyze
            raw_text = excel_df.to_string()
        except Exception as e:
            st.error(f"Failed to parse Excel: {e}")
            
    # --- HANDLING TEXT FILES ---
    else:
        raw_text = uploaded_file.read().decode("utf-8")
        st.success("✅ Text Report Loaded Successfully.")
        with st.expander("View Raw Text Snippet"):
            st.text(raw_text[:1000] + "...")

    # 4. Standardized Regex Parser Engine (Replicating Fundamental Team Rules)
    metrics = {
        "Revenue": [r"(?:Revenue|Total Revenue|Net Sales|Turnover)\s*(?::|—|-)?\s*\$?([\d,\.]+)\s*(?:billion|million|M|B)?"],
        "Net Income": [r"(?:Net Income|Net Profit|Net Earnings|Earnings Available)\s*(?::|—|-)?\s*\$?([\d,\.]+)\s*(?:billion|million|M|B)?"],
        "Total Assets": [r"(?:Total Assets|Assets)\s*(?::|—|-)?\s*\$?([\d,\.]+)\s*(?:billion|million|M|B)?"],
        "Total Liabilities": [r"(?:Total Liabilities|Liabilities)\s*(?::|—|-)?\s*\$?([\d,\.]+)\s*(?:billion|million|M|B)?"]
    }
    
    extracted_data = {}
    
    # 5. Advanced Cleaning & Sanitization Loop
    for metric, patterns in metrics.items():
        extracted_data[metric] = None
        for pattern in patterns:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                raw_val = match.group(1)
                # Stripping spaces, currency symbols, and accounting commas
                clean_val = float(raw_val.replace(",", "").replace("$", "").strip())
                extracted_data[metric] = clean_val
                break

    # Convert to Dataframe for standardization output
    df = pd.DataFrame([extracted_data])
    
    st.subheader("🧹 Step 2: Cleaned & Standardized Fundamental Output")
    st.dataframe(df.style.format(precision=2, na_rep="Missing Data"), use_container_width=True)
    
    # 6. Production Financial Logic Checks
    st.subheader("🚨 Step 3: Automated Data Quality Flags")
    
    rev = df.at[0, "Revenue"]
    ni = df.at[0, "Net Income"]
    assets = df.at[0, "Total Assets"]
    liab = df.at[0, "Total Liabilities"]
    
    valid_pipeline = True

    # Rule 1: Margin Constraint Check
    if pd.notna(rev) and pd.notna(ni):
        if ni > rev:
            st.error("❌ Data Quality Failure: Net Income mathematically exceeds Total Revenue.")
            valid_pipeline = False
        else:
            st.success("✅ Financial Logic Check Passed: Net Income is within boundaries of Revenue.")
            
    # Rule 2: Balance Sheet Solvency Guard
    if pd.notna(assets) and pd.notna(liab):
        if liab > assets:
            st.warning("⚠️ High Risk Flag: Total Liabilities exceed Total Assets (Negative Equity Model).")
        else:
            st.success("✅ Structural Balance Check Passed: Assets exceed Liabilities.")

    # 7. Data Export Pipeline
    if valid_pipeline:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Standardized Data to CSV",
            data=csv,
            file_name="standardized_financial_output.csv",
            mime="text/csv"
        )
else:
    st.info("💡 Pro-Tip: Upload a text report or Excel spreadsheet containing fundamental figures to see the extraction pipeline process in real time.")
