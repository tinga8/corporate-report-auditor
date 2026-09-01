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
                    # Attempt 1: Extract standard structural text
                    text_content = page.extract_text()
                    if text_content:
                        raw_text += text_content + "\n"
                    
                    # Attempt 2: Fallback to table layout text boundaries if standard extraction layout is tight
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

    # 4. Universal Fuzzy Synonym Lists
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
        {"Period": "Current Period", **{k: v[0] for k, v in extracted_metrics.items()}},
        {"Period": "Prior Period", **{k: v[1] for k, v in extracted_metrics.items()}}
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
    
    # --- NEW ADDITION: STEP 4 DETAILED VERDICT & MEMORANDUM ---
    st.markdown("---")
    st.subheader("🎯 Step 4: Final Investment Verdict & Solvency Memorandum")
    
    # Capture metrics for algorithmic grading logic rules
    c_margin = df.at[0, "Net Profit Margin (%)"]
    c_leverage = df.at[0, "Debt-to-Asset Ratio"]
    c_roa = df.at[0, "Return on Assets (%)"]
    
    score = 0
    total_checks = 0
    
    # Automated Logic Evaluation Flags
    if pd.notna(c_margin):
        total_checks += 1
        if c_margin > 10: score += 1
    if pd.notna(c_leverage):
        total_checks += 1
        if c_leverage < 0.6: score += 1
    if pd.notna(c_roa):
        total_checks += 1
        if c_roa > 5: score += 1
    if rev_growth is not None:
        total_checks += 1
        if rev_growth > 0: score += 1

    # Visual Metric Card Containers
    card_col1, card_col2 = st.columns([1, 2])
    
    with card_col1:
        if total_checks > 0:
            rating_percentage = (score / total_checks) * 100
            if rating_percentage >= 75:
                st.success("🟩 FINAL VERDICT: STRONG FINANCIAL POSITION")
            elif rating_percentage >= 50:
                st.warning("🟨 FINAL VERDICT: STABLE / CAUTIOUS POSITION")
            else:
                st.error("🟥 FINAL VERDICT: WEAK / DISTRESSED FINANCIAL POSITION")
        else:
            st.info("ℹ️ Unable to generate structural score due to missing column mappings.")

    with card_col2:
        st.markdown("#### 🗒️ Credit Analyst Assessment Summary")
        insights = []
        if pd.notna(c_margin):
            if c_margin > 10: insights.append("✅ **Profitability Strength:** Strong net profit metrics confirm solid operational health.")
            else: insights.append("⚠️ **Profitability Constraint:** Sub-10% net margins leave the enterprise exposed to operating cash friction.")
        if pd.notna(c_leverage):
            if c_leverage < 0.6: insights.append("✅ **Balance Sheet Health:** Gearing is inside safe parameters. The asset base insulates liabilities comfortably.")
            else: insights.append("❌ **High Credit Risk Leverage:** Liabilities swallow a large share of corporate asset values, raising default warning risks.")
        if rev_growth is not None:
            if rev_growth > 0: insights.append(f"📈 **Positive Trajectory:** Revenue grew by {rev_growth:.1f}% year-over-year.")
            else: insights.append(f"📉 **Top-Line Decay:** Core scale contracted by {abs(rev_growth):.1f}% over the prior comparative tracking layout.")
            
        for insight in insights:
            st.markdown(insight)

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
