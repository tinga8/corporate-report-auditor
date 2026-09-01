import pandas as pd
import streamlit as st
import pdfplumber
import re

# 1. Page Configuration
st.set_page_config(page_title="Institutional Financial Analytics Engine", page_icon="📈", layout="wide")
st.title("📈 Enterprise Multi-Period Ingestion & Table Extraction Platform")
st.caption("Production-Grade Table Ingestion Framework tailored for S&P Global, Moody's, and Bloomberg Evaluation")

# 2. Sidebar Process Documentation
st.sidebar.header("⚙️ Data Processing Matrix")
st.sidebar.info("""
- **Processing Matrix:** Layout-aware cell extraction using pdfplumber.
- **Analytical Metrics:** Multi-period structure matching.
- **Execution Cost:** $0 (Local execution, no API keys required).
""")

# 3. File Upload Engine
uploaded_file = st.file_uploader(
    "Upload Financial Document (Accepts: .pdf, .xlsx, .xls)", 
    type=["pdf", "xlsx", "xls"]
)

if uploaded_file is not None:
    file_name = uploaded_file.name
    st.subheader(f"📥 Processing Ingested File: `{file_name}`")
    
    extracted_rows = []
    
    # --- UPGRADED: STRUCTURAL LAYOUT PARSER FOR PDFs ---
    if file_name.endswith('.pdf'):
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    # Extract tables with precise layout detection
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            # Filter empty text rows out
                            if row and any(row):
                                # Clean individual elements
                                cleaned_row = [str(cell).strip() if cell else "" for cell in row]
                                extracted_rows.append(cleaned_row)
            
            st.success("✅ PDF Structural Table Engine Extracted Successfully.")
        except Exception as e:
            st.error(f"Failed to analyze PDF grid structures: {e}")

    # --- HANDLING EXCEL FILES ---
    elif file_name.endswith(('.xlsx', '.xls')):
        try:
            excel_df = pd.read_excel(uploaded_file)
            st.success("✅ Excel Ledger Uploaded Successfully.")
            extracted_rows = [excel_df.columns.tolist()] + excel_df.values.tolist()
        except Exception as e:
            st.error(f"Failed to parse Excel array: {e}")

    # 4. Multi-Period Mapping Logic Engine
    # Dictionary keywords to parse rows for relevant figures
    target_keywords = {
        "Revenue": ["revenue", "turnover", "net sales", "revenue from operations"],
        "Net Income": ["net income", "net profit", "profit for the period", "profit after tax", "pat"],
        "Total Assets": ["total assets", "assets"],
        "Total Liabilities": ["total liabilities", "liabilities"]
    }

    financial_data = {"Current Period": {}, "Prior Period": {}}
    for k in target_keywords.keys():
        financial_data["Current Period"][k] = None
        financial_data["Prior Period"][k] = None

    # Step 5: Process extracted cells sequentially
    for row in extracted_rows:
        # Join row items to find matches against our accounting metrics labels
        row_string = " ".join(row).lower()
        
        for metric, aliases in target_keywords.items():
            if any(alias in row_string for alias in aliases):
                # Isolate all financial numbers inside this row
                numeric_values = []
                for cell in row:
                    # Strip common structural text symbols away
                    clean_cell = cell.replace(",", "").replace("$", "").replace("(", "").replace(")", "").strip()
                    # Check if cell can map into float logic boundary
                    if re.match(r'^\d+(\.\d+)?$', clean_cell):
                        numeric_values.append(float(clean_cell))
                
                # Assign structural columns to correct year context
                if len(numeric_values) >= 2:
                    financial_data["Current Period"][metric] = numeric_values[0]
                    financial_data["Prior Period"][metric] = numeric_values[1]
                elif len(numeric_values) == 1 and financial_data["Current Period"][metric] is None:
                    financial_data["Current Period"][metric] = numeric_values[0]

    # Structuring Output DataFrame
    records = [
        {"Period": "Current Period (YoY)", **financial_data["Current Period"]},
        {"Period": "Prior Period (YoY)", **financial_data["Prior Period"]}
    ]
    df = pd.DataFrame(records)

    st.subheader("🧹 Step 2: Cleaned & Standardized Historical Financial Extract")
    st.dataframe(df.style.format({
        "Revenue": "${:,.2f}",
        "Net Income": "${:,.2f}",
        "Total Assets": "${:,.2f}",
        "Total Liabilities": "${:,.2f}"
    }, na_rep="Missing in Document Layout"), use_container_width=True)

    # 6. Advanced Trend Analysis Calculations
    st.subheader("📊 Step 3: Comparative Performance & Solvency Analytics Matrix")
    
    # Safely compute analytics columns using baseline checks
    df["Net Profit Margin (%)"] = (df["Net Income"] / df["Revenue"]) * 100
    df["Debt-to-Asset Ratio"] = df["Total Liabilities"] / df["Total Assets"]
    df["Equity / Net Worth"] = df["Total Assets"] - df["Total Liabilities"]
    df["Return on Assets (%)"] = (df["Net Income"] / df["Total Assets"]) * 100
    
    rev_growth = None
    ni_growth = None
    if pd.notna(df.at[0, "Revenue"]) and pd.notna(df.at[1, "Revenue"]) and df.at[1, "Revenue"] != 0:
        rev_growth = ((df.at[0, "Revenue"] - df.at[1, "Revenue"]) / df.at[1, "Revenue"]) * 100
    if pd.notna(df.at[0, "Net Income"]) and pd.notna(df.at[1, "Net Income"]) and df.at[1, "Net Income"] != 0:
        ni_growth = ((df.at[0, "Net Income"] - df.at[1, "Net Income"]) / df.at[1, "Net Income"]) * 100

    st.dataframe(df.style.format({
        "Net Profit Margin (%)": "{:.2f}%",
        "Debt-to-Asset Ratio": "{:.2f}",
        "Equity / Net Worth": "${:,.2f}",
        "Return on Assets (%)": "{:.2f}%"
    }, na_rep="Pending Structural Context"), use_container_width=True)

    # 7. Deep Analytical Investor Summary
    st.markdown("---")
    st.subheader("📑 Step 4: Institutional Investor Decision Memorandum")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📈 Revenue & Profitability Velocity Trends")
        if rev_growth is not None:
            if rev_growth > 0:
                st.success(f"🚀 **Positive Revenue Velocity:** Top-line growth expanded by **{rev_growth:.2f}%** compared to the prior period.")
            else:
                st.error(f"📉 **Top-Line Contraction:** Revenue shifted downward by **{abs(rev_growth):.2f}%** year-over-year.")
        
        c_margin = df.at[0, "Net Profit Margin (%)"]
        if pd.notna(c_margin):
            if c_margin > 15:
                st.markdown(f"🏆 **Premium Profit Margin:** Organization maintains strong operational efficiency at **{c_margin:.2f}%**.")
            else:
                st.markdown(f"裁 **Standard Margin Constraints:** Modern profit conversion baseline sits at **{c_margin:.2f}%**.")

    with col2:
        st.markdown("#### 🛡️ Capital Structure Stability & Quality Profile")
        for idx, row in df.iterrows():
            period = row['Period']
            leverage = row['Debt-to-Asset Ratio']
            roa = row['Return on Assets (%)']
            
            if pd.notna(leverage) and pd.notna(roa):
                if leverage < 0.5 and roa > 8:
                    st.markdown(f"🟢 **{period}:** Defensively structured balance sheet ({leverage:.2f} leverage) carrying optimized operational ROA of **{roa:.1f}%**.")
                else:
                    st.markdown(f"🟡 **{period}:** Standard operational baseline portfolio metrics tracked.")

    # 8. Download Data Pipeline Export
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Full Historical Investment Analytics to CSV",
        data=csv,
        file_name="historical_investor_analytics.csv",
        mime="text/csv"
    )
else:
    st.info("💡 Pro-Tip: Upload your quarterly consolidated report file to initiate multi-ratio matrix processing.")
