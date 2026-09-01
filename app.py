import re
import pandas as pd
import streamlit as st
import pdfplumber

# 1. Page Configuration
st.set_page_config(page_title="Institutional Financial Analytics Engine", page_icon="📈", layout="wide")
st.title("📈 Universal Multi-Period Ingestion & Spatial Analytics Platform")
st.caption("Production-Grade Table Ingestion Framework | Engineered for S&P Global, Moody's, and Bloomberg Standards")

# 2. Sidebar Process Documentation
st.sidebar.header("⚙️ Data Processing Matrix")
st.sidebar.info("""
- **Processing Engine:** Spatial layout-aware cell coordinates matrix mapping.
- **Dependencies:** None (Pure local calculations, no external API keys).
- **Core Function:** Standardized multi-period core ratio and performance velocity tracking.
""")

# 3. File Upload Ingestion
uploaded_file = st.file_uploader(
    "Upload Corporate Financial Report (Accepts: .pdf, .xlsx, .xls)", 
    type=["pdf", "xlsx", "xls"]
)

if uploaded_file is not None:
    file_name = uploaded_file.name
    st.subheader(f"📥 Processing Ingested File: `{file_name}`")
    
    extracted_rows = []
    
    # --- POSITIONAL COORDINATE BLOCK TABLE READER ---
    if file_name.endswith('.pdf'):
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    # Precise layout bounding box extraction captures actual multi-column structures
                    tables = page.extract_tables(settings={
                        "vertical_strategy": "lines",
                        "horizontal_strategy": "lines",
                        "snap_tolerance": 3,
                        "join_tolerance": 3,
                    })
                    
                    # Fallback strategy if table lacks distinct visible outer border lines
                    if not tables:
                        tables = page.extract_tables()
                        
                    for table in tables:
                        for row in table:
                            if row and any(row):
                                # Clean structural noise out of raw text blocks
                                cleaned_row = [str(cell).strip() if cell else "" for cell in row]
                                extracted_rows.append(cleaned_row)
        except Exception as e:
            st.error(f"Failed to analyze PDF grid structures: {e}")

    # Excel Parsing Track
    elif file_name.endswith(('.xlsx', '.xls')):
        try:
            excel_df = pd.read_excel(uploaded_file)
            extracted_rows = [excel_df.columns.tolist()] + excel_df.values.tolist()
            st.success("✅ Excel Ledger Array Imported Successfully.")
        except Exception as e:
            st.error(f"Failed to compile Excel tabular matrix: {e}")

    # 4. Multi-Synonym Fundamental Accounting Dictionary
    target_keywords = {
        "Revenue": ["revenue", "turnover", "net sales", "revenue from operations", "total revenue", "income"],
        "Net Income": ["net income", "net profit", "profit for the period", "profit after tax", "pat", "profit/(loss)"],
        "Total Assets": ["total assets", "assets", "balance sheet total"],
        "Total Liabilities": ["total liabilities", "liabilities", "total equity and liabilities"]
    }

    # Internal sequence mapping matrices
    financial_matrix = {k: [None, None] for k in target_keywords.keys()}

    # 5. Core Column Alignment Processing Loop
    for row in extracted_rows:
        # Join cell text elements to match row classifications
        row_string = " ".join(row).lower()
        
        for metric, aliases in target_keywords.items():
            if any(alias in row_string for alias in aliases) and financial_matrix[metric] == [None, None]:
                numeric_values = []
                
                for cell in row:
                    # Accounting Bracket Conversion Step: Check for parentheses wrapping negative values
                    is_negative = "(" in cell or "-" in cell
                    clean_cell = cell.replace(",", "").replace("$", "").replace("(", "").replace(")", "").replace("-", "").strip()
                    
                    if re.match(r'^\d+(\.\d+)?$', clean_cell):
                        val = float(clean_cell)
                        if val > 10:  # Exclude page coordinates, notes index keys, or simple padding values
                            numeric_values.append(-val if is_negative else val)
                
                # Align historical columns programmatically based on extracted token lengths
                if len(numeric_values) >= 2:
                    financial_matrix[metric] = [numeric_values[0], numeric_values[1]]
                elif len(numeric_values) == 1:
                    financial_matrix[metric] = [numeric_values[0], None]

    # Transpile the mapped metrics dictionary directly into structured tracking frames
    records = [
        {"Period": "Current Period", **{k: financial_matrix[k][0] for k in target_keywords.keys()}},
        {"Period": "Prior Period", **{k: financial_matrix[k][1] for k in target_keywords.keys()}}
    ]
    df = pd.DataFrame(records)

    st.subheader("🧹 Step 2: Cleaned & Standardized Historical Financial Extract")
    st.dataframe(df.style.format({
        "Revenue": "${:,.2f}",
        "Net Income": "${:,.2f}",
        "Total Assets": "${:,.2f}",
        "Total Liabilities": "${:,.2f}"
    }, na_rep="Missing in Document Layout"), use_container_width=True)

    # 6. Comprehensive Financial Results Ratio Analysis
    st.subheader("📈 Step 3: Comparative Financial Results Analysis")
    
    # Computes standard accounting performance metrics across the timeline rows
    df["Net Profit Margin (%)"] = (df["Net Income"] / df["Revenue"]) * 100
    df["Debt-to-Asset Ratio"] = df["Total Liabilities"] / df["Total Assets"]
    df["Equity / Shareholder Net Worth"] = df["Total Assets"] - df["Total Liabilities"]
    df["Return on Assets (%)"] = (df["Net Income"] / df["Total Assets"]) * 100
    
    # Calculate operational change parameters
    rev_growth = None
    ni_growth = None
    if pd.notna(df.at[0, "Revenue"]) and pd.notna(df.at[1, "Revenue"]) and df.at[1, "Revenue"] != 0:
        rev_growth = ((df.at[0, "Revenue"] - df.at[1, "Revenue"]) / df.at[1, "Revenue"]) * 100
    if pd.notna(df.at[0, "Net Income"]) and pd.notna(df.at[1, "Net Income"]) and df.at[1, "Net Income"] != 0:
        ni_growth = ((df.at[0, "Net Income"] - df.at[1, "Net Income"]) / df.at[1, "Net Income"]) * 100

    st.dataframe(df.style.format({
        "Net Profit Margin (%)": "{:.2f}%",
        "Debt-to-Asset Ratio": "{:.2f}",
        "Equity / Shareholder Net Worth": "${:,.2f}",
        "Return on Assets (%)": "{:.2f}%"
    }, na_rep="Awaiting Spatial Data"), use_container_width=True)

    # 7. Deep Scannable Performance Summary Memorandum
    st.markdown("---")
    st.subheader("📑 Step 4: Detailed Financial Performance Analytics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📊 Income Statement Metrics Velocity")
        if rev_growth is not None:
            if rev_growth > 0:
                st.markdown(f"• **Revenue Growth Trend:** Corporate top-line scale expanded by **{rev_growth:.2f}%** year-over-year.")
            else:
                st.markdown(f"• **Revenue Growth Trend:** Corporate top-line scaled downward by **{abs(rev_growth):.2f}%** against the history timeline.")
        
        if ni_growth is not None:
            if ni_growth > 0:
                st.markdown(f"• **Net Earnings Trend:** Bottom-line profits accelerated by **{ni_growth:.2f}%** compared to the prior period.")
            else:
                st.markdown(f"• **Net Earnings Trend:** Net margins compressed, with profits pulling back by **{abs(ni_growth):.2f}%** year-over-year.")
        
        for idx, row in df.iterrows():
            p = row['Period']
            m = row['Net Profit Margin (%)']
            if pd.notna(m):
                st.markdown(f"• **{p} Profitability:** Core net profit margin settled at **{m:.2f}%** for the interval.")

    with col2:
        st.markdown("#### 🛡️ Balance Sheet Position & Solvency Tracking")
        for idx, row in df.iterrows():
            p = row['Period']
            lev = row['Debt-to-Asset Ratio']
            roa = row['Return on Assets (%)']
            eq = row['Equity / Shareholder Net Worth']
            
            if pd.notna(lev) and pd.notna(roa) and pd.notna(eq):
                st.markdown(f"• **{p} Capital Structure:** Total debt-to-asset leverage score registered at **{lev:.2f}** with calculated total net worth capital base sitting at **${eq:,.2f}**.")
                st.markdown(f"• **{p} Capital Utilization Productivity:** Net Return on Assets (ROA) performance factor calculated at **{roa:.2f}%**.")

    # 8. Export Compiled Structure
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Full Performance Analytics Data Model to CSV",
        data=csv,
        file_name="financial_spatial_analytics.csv",
        mime="text/csv"
    )
else:
    st.info("💡 Pro-Tip: Drop any complex multi-period reporting file to isolate spatial matrix calculations instantly.")
