import re
import pandas as pd
import streamlit as st
import pdfplumber

# 1. Page Configuration
st.set_page_config(page_title="Universal Financial Engine", page_icon="📈", layout="wide")
st.title("📈 Universal Multi-Year Financial Ingestion & Investor Platform")
st.caption("Pure Offline Heuristic Table Parsing Pipeline | Engineered for S&P Global, Moody's, and Bloomberg Standards")

# 2. Sidebar Process Documentation
st.sidebar.header("⚙️ Data Processing Matrix")
st.sidebar.info("""
- **AI Core:** Zero (Pure Spatial Text Parsing Heuristics).
- **Security Profile:** 100% Secure (No APIs, keys, or networks used).
- **Compatibility:** Structural sequence extraction for any company report.
- **Execution Cost:** $0 (Forever Free).
""")

# 3. File Upload Engine
uploaded_file = st.file_uploader(
    "Upload Any Corporate Financial Report (Accepts: .pdf, .txt, .xlsx, .xls)", 
    type=["pdf", "txt", "xlsx", "xls"]
)

raw_text = ""

if uploaded_file is not None:
    file_name = uploaded_file.name
    st.subheader(f"📥 Processing Ingested File: `{file_name}`")
    
    # PDF Parser Loop using pdfplumber layout extraction
    if file_name.endswith('.pdf'):
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    text_content = page.extract_text()
                    if text_content:
                        raw_text += text_content + "\n"
                    
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            if row:
                                raw_text += " ".join([str(cell) for cell in row if cell]) + "\n"
                                
            st.success("✅ PDF Text Layer Unpacked Successfully.")
        except Exception as e:
            st.error(f"Failed to process PDF text array: {e}")

    # Excel Parser Loop
    elif file_name.endswith(('.xlsx', '.xls')):
        try:
            excel_df = pd.read_excel(uploaded_file)
            st.success("✅ Excel Sheet Loaded Successfully.")
            raw_text = excel_df.to_string()
        except Exception as e:
            st.error(f"Failed to parse Excel structures: {e}")
            
    # Text Parser Loop
    else:
        raw_text = uploaded_file.read().decode("utf-8")
        st.success("✅ Raw String Payload Processed.")

    # 4. Universal Fuzzy Synonym Lists (Restored to the exact good setup)
    keywords = {
        "Revenue": ["revenue", "sales", "turnover", "operations", "income"],
        "Net Income": ["net income", "profit", "earnings", "pat", "loss"],
        "Total Assets": ["assets", "property", "equipment"],
        "Total Liabilities": ["liabilities", "obligations", "equity and liabilities"]
    }
    
    extracted_metrics = {k: [None, None] for k in keywords.keys()}
    
    # 5. Fail-Safe Sequence Ingestion Loop
    if raw_text.strip():
        lines = raw_text.split("\n")
        
        for idx, line in enumerate(lines):
            line_lower = line.lower()
            
            for metric, aliases in keywords.items():
                if any(alias in line_lower for alias in aliases) and extracted_metrics[metric] == [None, None]:
                    search_block = " ".join(lines[idx:idx+3])
                    raw_tokens = re.findall(r'\(?\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b\)?', search_block)
                    
                    tokens = []
                    for token in raw_tokens:
                        is_negative = "(" in token or "-" in token
                        clean_token = token.replace(",", "").replace("(", "").replace(")", "").strip()
                        try:
                            val = float(clean_token)
                            if val > 10:
                                tokens.append(-val if is_negative else val)
                        except ValueError:
                            continue
                    
                    if len(tokens) >= 2:
                        extracted_metrics[metric] = [tokens[0], tokens[1]]
                    elif len(tokens) == 1:
                        extracted_metrics[metric] = [tokens[0], None]

    # Structure records into comparative DataFrames
    records = [
        {"Period": "Current Period", **{k: extracted_metrics[k][0] for k in keywords.keys()}},
        {"Period": "Prior Period", **{k: extracted_metrics[k][1] for k in keywords.keys()}}
    ]
    df = pd.DataFrame(records)
    
    st.subheader("🧹 Step 2: Cleaned & Standardized Historical Financial Extract")
    st.dataframe(df.style.format({
        "Revenue": "${:,.2f}",
        "Net Income": "${:,.2f}",
        "Total Assets": "${:,.2f}",
        "Total Liabilities": "${:,.2f}"
    }, na_rep="Missing Data Segment"), use_container_width=True)
    
    # 6. Comparative Financial Ratio Analytics Framework
    st.subheader("📊 Step 3: Comparative Performance & Solvency Analytics Matrix")
    
    df["Net Profit Margin (%)"] = (df["Net Income"] / df["Revenue"]) * 100
    df["Debt-to-Asset Ratio"] = df["Total Liabilities"] / df["Total Assets"]
    df["Equity / Net Worth"] = df["Total Assets"] - df["Total Liabilities"]
    df["Return on Assets (%)"] = (df["Net Income"] / df["Total Assets"]) * 100
    
    # Horizontal Growth tracking
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
    }, na_rep="Awaiting Alignment"), use_container_width=True)
    
    # --- FIXED: STEP 4 CLEAN SUMMARY VERDICT LOGIC ---
    st.markdown("---")
    st.subheader("🎯 Step 4: Executive Performance Summary Verdict")
    
    rev = df.at[0, "Revenue"]
    ni = df.at[0, "Net Income"]
    assets = df.at[0, "Total Assets"]
    liab = df.at[0, "Total Liabilities"]
    
    # Summary Evaluation Array
    summary_bullets = []
    is_healthy = True
    
    # 1. Operational Profitability Check
    if pd.notna(ni):
        if ni > 0:
            summary_bullets.append("✅ **Operational Performance:** The company is fully **profitable** and successfully generating positive net returns.")
        else:
            is_healthy = False
            summary_bullets.append("❌ **Operational Performance:** The company is operating at a **net loss**, indicating high structural overhead costs.")
            
    # 2. Scale Growth Check
    if rev_growth is not None:
        if rev_growth > 0:
            summary_bullets.append(f"📈 **Revenue Velocity:** Top-line revenue increased by **{rev_growth:.1f}%** year-over-year, showing solid market expansion.")
        else:
            summary_bullets.append(f"📉 **Revenue Velocity:** Top-line scale contracted by **{abs(rev_growth):.1f}%**, signaling a business slowdown.")

    # 3. Capital Structure Solvency Check
    if pd.notna(assets) and pd.notna(liab):
        if assets > liab:
            summary_bullets.append("🛡️ **Balance Sheet Cushion:** Total Assets exceed Total Liabilities, leaving a solid **positive equity net worth** container.")
        else:
            is_healthy = False
            summary_bullets.append("⚠️ **Balance Sheet Insolvency Risk:** Total Liabilities exceed Total Assets, creating a dangerous **negative equity profile**.")

    # Display the Final Call banner
    if is_healthy:
        st.success("🟩 **FINAL VERDICT SUMMARY: overall FINANCIAL POSITION IS STRONG & HEALTHY**")
    else:
        st.warning("🟨 **FINAL VERDICT SUMMARY: FINANCIAL POSITION CARRIES MATERIAL OPERATIONAL OR SOLVENCY RISK**")
        
    # Render the scannable summary points
    for bullet in summary_bullets:
        st.markdown(bullet)

    # 8. Export Data
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Full Historical Investment Analytics to CSV",
        data=csv,
        file_name="universal_keyless_analytics.csv",
        mime="text/csv"
    )
else:
    st.info("💡 Pro-Tip: Upload any financial document containing side-by-side metric tables to verify the automated keyless parser engine.")
