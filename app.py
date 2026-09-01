import re
import pandas as pd
import streamlit as st
from pypdf import PdfReader

# 1. Page Configuration
st.set_page_config(page_title="Institutional Financial Analytics Engine", page_icon="📈", layout="wide")
st.title("📈 Enterprise Year-over-Year Ingestion & Investor Analytics Platform")
st.caption("Advanced Rule-Based Multi-Period Fundamental Data Pipeline tailored for S&P Global, Moody's, and Bloomberg Evaluation")

# 2. Sidebar Process Documentation
st.sidebar.header("⚙️ Data Processing Matrix")
st.sidebar.info("""
- **Processing Matrix:** Local multi-period regex tokenization.
- **Analytical Metrics:** YoY Growth, Capital Structure, Solvency.
- **Execution Cost:** $0 (Zero API dependancies / No Keys Required).
""")

# 3. File Upload Engine
uploaded_file = st.file_uploader(
    "Upload Financial Document (Accepts: .pdf, .txt, .xlsx, .xls)", 
    type=["pdf", "txt", "xlsx", "xls"]
)

raw_text = ""

if uploaded_file is not None:
    file_name = uploaded_file.name
    st.subheader(f"📥 Processing Ingested File: `{file_name}`")
    
    # PDF Parser Loop
    if file_name.endswith('.pdf'):
        try:
            pdf_reader = PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text_content = page.extract_text()
                if text_content:
                    raw_text += text_content + "\n"
            st.success("✅ PDF Document Structure Extracted Successfully.")
        except Exception as e:
            st.error(f"Failed to parse PDF binary matrix: {e}")

    # Excel Parser Loop
    elif file_name.endswith(('.xlsx', '.xls')):
        try:
            excel_df = pd.read_excel(uploaded_file)
            st.success("✅ Excel Ledger Uploaded Successfully.")
            raw_text = excel_df.to_string()
        except Exception as e:
            st.error(f"Failed to parse Excel array: {e}")
            
    # Text Parser Loop
    else:
        raw_text = uploaded_file.read().decode("utf-8")
        st.success("✅ Raw String Payload Processed.")

    # 4. Advanced Multi-Period Tokenizing Dictionary
    # Matches lines with labels and extracts multiple consecutive numeric columns (e.g. FY26, FY25)
    multi_period_patterns = {
        "Revenue": r"(?:Total Revenue|Revenue|Net Sales|Turnover|Revenue from Operations)\s*(?::|—|-)?\s*([\d,\.\s]+)",
        "Net Income": r"(?:Net Income|Net Profit|Net Earnings|Profit for the period|Profit after Tax|PAT)\s*(?::|—|-)?\s*([\d,\.\s]+)",
        "Total Assets": r"(?:Total Assets|Assets)\s*(?::|—|-)?\s*([\d,\.\s]+)",
        "Total Liabilities": r"(?:Total Liabilities|Liabilities)\s*(?::|—|-)?\s*([\d,\.\s]+)"
    }
    
    # Storage structures for multiple periods
    period_data = {"Current Period": {}, "Prior Period": {}}
    
    for metric, pattern in multi_period_patterns.items():
        match = re.search(pattern, raw_text, re.IGNORECASE)
        if match:
            # Extract raw numbers block from the line matching the financial line item
            numbers_block = match.group(1).strip()
            # Tokenize individual spatial string segments into numeric sequences
            tokens = [float(t.replace(",", "")) for t in re.split(r'\s+', numbers_block) if re.match(r'^[\d,\.]+$', t)]
            
            # Map values to appropriate historical matrix fields based on column indexing rules
            if len(tokens) >= 2:
                period_data["Current Period"][metric] = tokens[0]
                period_data["Prior Period"][metric] = tokens[1]
            elif len(tokens) == 1:
                period_data["Current Period"][metric] = tokens[0]
                period_data["Prior Period"][metric] = None
            else:
                period_data["Current Period"][metric] = None
                period_data["Prior Period"][metric] = None
        else:
            period_data["Current Period"][metric] = None
            period_data["Prior Period"][metric] = None

    # Convert mapping schema directly into structured comparative records
    records = [
        {"Period": "Current Period (YoY)", **period_data["Current Period"]},
        {"Period": "Prior Period (YoY)", **period_data["Prior Period"]}
    ]
    df = pd.DataFrame(records)
    
    st.subheader("🧹 Step 2: Normalized Multi-Period Financial Extract")
    st.dataframe(df.style.format({
        "Revenue": "${:,.2f}",
        "Net Income": "${:,.2f}",
        "Total Assets": "${:,.2f}",
        "Total Liabilities": "${:,.2f}"
    }, na_rep="Omitted in Source Table"), use_container_width=True)
    
    # 5. Advanced Trend Analysis Calculations
    st.subheader("📊 Step 3: Comparative Performance & Solvency Analytics Matrix")
    
    # Calculate performance ratios safely across all records
    df["Net Profit Margin (%)"] = (df["Net Income"] / df["Revenue"]) * 100
    df["Debt-to-Asset Ratio"] = df["Total Liabilities"] / df["Total Assets"]
    df["Equity / Net Worth"] = df["Total Assets"] - df["Total Liabilities"]
    df["Return on Assets (%)"] = (df["Net Income"] / df["Total Assets"]) * 100
    
    # Compute horizontal Year-over-Year metric shifts if two periods exist
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
    }, na_rep="Insufficient Context"), use_container_width=True)
    
    # 6. Deep Analytical Investor Summary
    st.markdown("---")
    st.subheader("📑 Step 4: Institutional Investor Decision Memorandum")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Revenue & Profitability Velocity Trends")
        if rev_growth is not None:
            if rev_growth > 0:
                st.success(f"🚀 **Positive Revenue Velocity:** Top-line growth accelerated by **{rev_growth:.2f}%** compared to the prior period, expanding operational scale.")
            else:
                st.error(f"📉 **Top-Line Contraction:** Revenue declined by **{abs(rev_growth):.2f}%** year-over-year, indicating potential market contraction or operational friction.")
        
        if ni_growth is not None:
            if ni_growth > 0:
                st.success(f"💰 **Net Earnings Expansion:** Profitability expanded by **{ni_growth:.2f}%** year-over-year, reflecting strong expense controls.")
            else:
                st.error(f"⚠️ **Earnings Compression:** Net earnings pulled back by **{abs(ni_growth):.2f}%**, warning investors of margin pressures.")
                
        # Current period baseline checks
        c_margin = df.at[0, "Net Profit Margin (%)"]
        if pd.notna(c_margin):
            if c_margin > 15:
                st.markdown(f"🏆 **Premium Profit Margin:** Modern operations yield a high **{c_margin:.2f}%** profit margin, showing strong pricing power.")
            else:
                st.markdown(f"🟡 **Standard Margin Constraints:** Modern margins sit at **{c_margin:.2f}%**, sensitive to changes in volume.")

    with col2:
        st.markdown("#### 🛡️ Capital Structure Stability & Quality Profile")
        for idx, row in df.iterrows():
            period = row['Period']
            leverage = row['Debt-to-Asset Ratio']
            roa = row['Return on Assets (%)']
            
            if pd.notna(leverage) and pd.notna(roa):
                if leverage < 0.5 and roa > 8:
                    st.markdown(f"🟢 **{period}:** Conservative health profile. Low default risk ({leverage:.2f} leverage) paired with efficient asset deployment yielding **{roa:.1f}%**.")
                elif leverage <= 0.7:
                    st.markdown(f"🟡 **{period}:** Standard corporate leverage baseline ({leverage:.2f}). Capital asset efficiency sits at **{roa:.1f}%**.")
                else:
                    st.markdown(f"🔴 **{period}:** High balance sheet leverage risk ({leverage:.2f}). Vulnerable to changes in macro credit terms.")

    # 7. Download Data Pipeline Export
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Full Historical Investment Analytics to CSV",
        data=csv,
        file_name="historical_investor_analytics.csv",
        mime="text/csv"
    )
else:
    st.info("💡 Pro-Tip: Upload your quarterly consolidated report file to initiate multi-ratio computational metrics.")
