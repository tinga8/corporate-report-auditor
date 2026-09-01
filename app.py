import re
import pandas as pd
import streamlit as st
from pypdf import PdfReader

# 1. Page Configuration
st.set_page_config(page_title="Institutional Financial Analytics Engine", page_icon="📈", layout="wide")
st.title("📈 Enterprise Financial Ingestion & Investor Intelligence Platform")
st.caption("Advanced Analytical Framework engineered for Fundamental Data Specialist Evaluation")

# 2. Sidebar Process Documentation
st.sidebar.header("⚙️ Data Processing Matrix")
st.sidebar.info("""
- **Inbound Processing:** Multi-phased PDF string extraction.
- **Normalization Strategy:** Synonymous term mapping matrices.
- **Analytical Metrics:** Profitability, Capital Structure, Solvency.
- **Execution Cost:** $0 (Local execution).
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

    # 4. Multi-Synonym Fundamental Dictionary (Fixes the "None / N/A" Bug)
    metrics_dictionary = {
        "Revenue": [
            r"(?:Total Revenue|Revenue|Net Sales|Turnover|Revenue from Operations)\s*(?::|—|-)?\s*\$?([\d,\.]+)"
        ],
        "Net Income": [
            r"(?:Net Income|Net Profit|Net Earnings|Profit for the period|Profit after Tax|PAT|Profit/(Loss) for the period)\s*(?::|—|-)?\s*\$?([\d,\.]+)"
        ],
        "Total Assets": [
            r"(?:Total Assets|Assets|Total Non-Current Assets \+ Total Current Assets)\s*(?::|—|-)?\s*\$?([\d,\.]+)"
        ],
        "Total Liabilities": [
            r"(?:Total Liabilities|Liabilities|Total Equity and Liabilities)\s*(?::|—|-)?\s*\$?([\d,\.]+)"
        ]
    }
    
    extracted_data = {}
    
    # 5. Extraction and Context Conversion Engine
    for metric, patterns in metrics_dictionary.items():
        extracted_data[metric] = None
        for pattern in patterns:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                raw_val = match.group(1)
                # Stripping standard formatting variations
                clean_val = float(raw_val.replace(",", "").replace("$", "").strip())
                extracted_data[metric] = clean_val
                break

    df = pd.DataFrame([extracted_data])
    
    st.subheader("🧹 Step 2: Normalized Fundamental Accounting Extract")
    st.dataframe(df.style.format(precision=2, na_rep="Data Line Omitted in Source"), use_container_width=True)
    
    # Local variable unpacking for downstream computation
    rev = df.at[0, "Revenue"]
    ni = df.at[0, "Net Income"]
    assets = df.at[0, "Total Assets"]
    liab = df.at[0, "Total Liabilities"]
    
    # 6. Advanced Investor Ratios Matrix
    st.subheader("📊 Step 3: Comprehensive Investment Ratios Matrix")
    
    # Safe analytical calculations
    net_margin = (ni / rev) * 100 if pd.notna(ni) and pd.notna(rev) and rev != 0 else None
    debt_to_assets = (liab / assets) if pd.notna(liab) and pd.notna(assets) and assets != 0 else None
    equity = (assets - liab) if pd.notna(assets) and pd.notna(liab) else None
    debt_to_equity = (liab / equity) if pd.notna(liab) and pd.notna(equity) and equity != 0 else None
    roa = (ni / assets) * 100 if pd.notna(ni) and pd.notna(assets) and assets != 0 else None
    roe = (ni / equity) * 100 if pd.notna(ni) and pd.notna(equity) and equity != 0 else None

    # Visualizing Analysis Cards
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric(label="Net Profit Margin (Profitability)", value=f"{net_margin:.2f}%" if net_margin is not None else "N/A")
        st.metric(label="Return on Equity (ROE)", value=f"{roe:.2f}%" if roe is not None else "N/A")
    with m_col2:
        st.metric(label="Debt-to-Asset Ratio (Leverage)", value=f"{debt_to_assets:.2f}" if debt_to_assets is not None else "N/A")
        st.metric(label="Debt-to-Equity Ratio (Solvency)", value=f"{debt_to_equity:.2f}" if debt_to_equity is not None else "N/A")
    with m_col3:
        st.metric(label="Calculated Net Worth / Equity", value=f"${equity:,.2f}" if equity is not None else "N/A")
        st.metric(label="Return on Assets (ROA)", value=f"{roa:.2f}%" if roa is not None else "N/A")

    # 7. Deep Analytical Investor Summary
    st.markdown("---")
    st.subheader("📑 Step 4: Institutional Investor Decision Memorandum")
    
    left_memo, right_memo = st.columns(2)
    
    with left_memo:
        st.markdown("#### 🎯 Core Investment Thesis")
        if net_margin is not None and net_margin > 12:
            st.success("🏆 **Premium Operational Profile:** High profit margins confirm significant pricing power and structurally sound unit economics.")
        elif net_margin is not None and net_margin >= 0:
            st.warning("⚠️ **Baseline Operational Stability:** Capital conversion is within safety boundaries, but susceptible to margin compression from scaling overhead.")
        elif net_margin is not None:
            st.error("🚨 **Value-Destructive Margins:** The operation is running at a net loss. Capital allocation strategy should be evaluated immediately.")
        else:
            st.info("ℹ️ Profitability baseline unavailable due to missing core data rows in document.")

        if debt_to_equity is not None and debt_to_equity < 1.0:
            st.success("🛡️ **Strong Balance Sheet Cushion:** Debt is well below equity lines. Low risk of systemic default under macroeconomic headwinds.")
        elif debt_to_equity is not None and debt_to_equity <= 2.0:
            st.warning("⚡ **Gearing Utilization:** Moderate debt leverage balances risk and reward. Recommended to monitor current ratio trends.")
        elif debt_to_equity is not None:
            st.error("🔥 **Aggressive Capital Gearing:** Heavy reliance on credit capital increases structural insolvency risks if cash generation slows down.")

    with right_memo:
        st.markdown("#### ⚙️ Efficiency & Allocation Quality")
        if roe is not None and roe > 15:
            st.markdown("🟢 **Top-Tier Equity Productivity:** The organization generates strong value on shareholder funds, exceeding baseline corporate cost matrices.")
        else:
            st.markdown("🟡 **Sub-Optimal Equity Yields:** Returns on capital call for strategic adjustments to turn around underperforming assets.")
            
        if roa is not None and roa > 8:
            st.markdown("🟢 **Strong Capital Asset Deployment:** Fixed and current capital blocks are highly optimized toward immediate baseline cash flows.")
        else:
            st.markdown("🟡 **Underutilized Fixed Capital Block:** Current asset configurations show extended recovery horizons.")

    # 8. Automated Verification Flags
    st.subheader("🚨 Step 5: Data Pipeline Verification Checks")
    valid_pipeline = True
    if pd.notna(rev) and pd.notna(ni) and ni > rev:
        st.error("❌ Fatal Error: Net Income mathematically exceeds Total Revenue. Ingestion halted.")
        valid_pipeline = False
    else:
        st.success("✅ Operational Boundary Passed: Base metrics align cleanly with core accounting guidelines.")

    if valid_pipeline:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Institutional Analytics to CSV",
            data=csv,
            file_name="investor_analytics_export.csv",
            mime="text/csv"
        )
else:
    st.info("💡 Pro-Tip: Upload your quarterly consolidated report file (`.pdf`) to initiate multi-ratio computational metrics.")
