import re
import pandas as pd
import streamlit as st
from pypdf import PdfReader

# 1. UI Configuration
st.set_page_config(page_title="Financial Data Specialist Pipeline", page_icon="📊", layout="wide")
st.title("📊 Enterprise Financial Ingestion & Multi-Ratio Analytics Pipeline")
st.caption("Production-Grade Data Collection & Analysis Framework tailored for S&P Global, Moody's, and Bloomberg")

# 2. Sidebar Architecture Summary
st.sidebar.header("⚙️ Data Engineering Engine")
st.sidebar.info("""
- **Formats:** PDF Documents, Unstructured Text, Raw Excel Sheets.
- **Analytics:** Calculates key financial health and performance ratios.
- **Data Quality (DQ):** Mathematical logic guards.
- **Cost:** $0 (Zero API dependencies).
""")

# 3. Multi-Format File Ingestion
uploaded_file = st.file_uploader(
    "Upload Financial Document (Accepts: .pdf, .txt, .xlsx, .xls)", 
    type=["pdf", "txt", "xlsx", "xls"]
)

raw_text = ""

if uploaded_file is not None:
    file_name = uploaded_file.name
    st.subheader(f"📥 Processing Ingested File: `{file_name}`")
    
    # --- HANDLING PDF FILES ---
    if file_name.endswith('.pdf'):
        try:
            pdf_reader = PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text_content = page.extract_text()
                if text_content:
                    raw_text += text_content + "\n"
            st.success("✅ PDF Document Parsed Successfully.")
        except Exception as e:
            st.error(f"Failed to parse PDF: {e}")

    # --- HANDLING EXCEL FILES ---
    elif file_name.endswith(('.xlsx', '.xls')):
        try:
            excel_df = pd.read_excel(uploaded_file)
            st.success("✅ Excel Sheet Loaded Successfully.")
            raw_text = excel_df.to_string()
        except Exception as e:
            st.error(f"Failed to parse Excel: {e}")
            
    # --- HANDLING TEXT FILES ---
    else:
        raw_text = uploaded_file.read().decode("utf-8")
        st.success("✅ Text Report Loaded Successfully.")

    # 4. Expanded Fundamental Extraction Engine
    metrics = {
        "Revenue": [r"(?:Revenue|Total Revenue|Net Sales|Turnover)\s*(?::|—|-)?\s*\$?([\d,\.]+)\s*(?:billion|million|M|B)?"],
        "Net Income": [r"(?:Net Income|Net Profit|Net Earnings|Earnings Available)\s*(?::|—|-)?\s*\$?([\d,\.]+)\s*(?:billion|million|M|B)?"],
        "Total Assets": [r"(?:Total Assets|Assets)\s*(?::|—|-)?\s*\$?([\d,\.]+)\s*(?:billion|million|M|B)?"],
        "Total Liabilities": [r"(?:Total Liabilities|Liabilities)\s*(?::|—|-)?\s*\$?([\d,\.]+)\s*(?:billion|million|M|B)?"]
    }
    
    extracted_data = {}
    
    for metric, patterns in metrics.items():
        extracted_data[metric] = None
        for pattern in patterns:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                raw_val = match.group(1)
                clean_val = float(raw_val.replace(",", "").replace("$", "").strip())
                extracted_data[metric] = clean_val
                break

    df = pd.DataFrame([extracted_data])
    
    st.subheader("🧹 Step 2: Cleaned & Standardized Fundamental Output")
    st.dataframe(df.style.format(precision=2, na_rep="Missing Data"), use_container_width=True)
    
    # Extract scalar values for quick math
    rev = df.at[0, "Revenue"]
    ni = df.at[0, "Net Income"]
    assets = df.at[0, "Total Assets"]
    liab = df.at[0, "Total Liabilities"]
    
    # 5. NEW: Advanced Financial Analytics & Ratio Engine
    st.subheader("📈 Step 3: Stakeholder Financial Analysis & Decision Engine")
    
    # Compute metrics safely
    net_margin = (ni / rev) * 100 if pd.notna(ni) and pd.notna(rev) and rev != 0 else None
    debt_to_assets = (liab / assets) if pd.notna(liab) and pd.notna(assets) and assets != 0 else None
    equity = (assets - liab) if pd.notna(assets) and pd.notna(liab) else None
    return_on_assets = (ni / assets) * 100 if pd.notna(ni) and pd.notna(assets) and assets != 0 else None

    # Visualizing Analysis Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Net Profit Margin", value=f"{net_margin:.2f}%" if net_margin is not None else "N/A")
    with col2:
        st.metric(label="Debt-to-Asset Ratio", value=f"{debt_to_assets:.2f}" if debt_to_assets is not None else "N/A")
    with col3:
        st.metric(label="Calculated Shareholder Equity", value=f"${equity:,.2f}" if equity is not None else "N/A")
    with col4:
        st.metric(label="Return on Assets (ROA)", value=f"{return_on_assets:.2f}%" if return_on_assets is not None else "N/A")

    # 6. Automated Stakeholder Decision Summary
    st.markdown("### 📋 Executive Summary for Stakeholders")
    
    insights = []
    
    if net_margin is not None:
        if net_margin > 15:
            insights.append("🟢 **High Profitability:** The firm converts revenue into net profits efficiently, presenting strong operational stability.")
        elif net_margin > 5:
            insights.append("🟡 **Moderate Profitability:** Operating margins are stable, but optimization may be required to shield against market shifts.")
        else:
            insights.append("🔴 **Low Margin Warning:** Net margin is narrow, indicating high cost structures or weak pricing power.")

    if debt_to_assets is not None:
        if debt_to_assets > 0.7:
            insights.append("🔴 **High Leverage Risk:** Debt finances over 70% of company assets, increasing structural insolvency risks during capital shifts.")
        elif debt_to_assets > 0.3:
            insights.append("🟡 **Balanced Capital Structure:** The balance sheet demonstrates a healthy, standard mix of equity and debt financing.")
        else:
            insights.append("🟢 **Low Leverage Strength:** Highly conservative capital structure with minimal reliance on external liabilities.")

    if return_on_assets is not None:
        if return_on_assets > 10:
            insights.append("🟢 **Excellent Asset Efficiency:** Efficiently deploying capital assets to generate structural baseline returns.")
        else:
            insights.append("🟡 **Sub-Optimal Asset Utilization:** Asset returns are under historical benchmarks; evaluation of non-performing assets advised.")

    if insights:
        for insight in insights:
            st.markdown(insight)
    else:
        st.info("Insufficient data extracted from report text to build executive stakeholder insights.")

    # 7. Production Financial Logic Checks
    st.subheader("🚨 Step 4: Automated Data Quality Flags")
    valid_pipeline = True
    if pd.notna(rev) and pd.notna(ni) and ni > rev:
        st.error("❌ Data Quality Failure: Net Income mathematically exceeds Total Revenue.")
        valid_pipeline = False
    else:
        st.success("✅ Financial Logic Check Passed: Net Income limits fall within proper boundary.")

    if valid_pipeline:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Cleaned Dataset & Ratios to CSV",
            data=csv,
            file_name="standardized_financial_output.csv",
            mime="text/csv"
        )
else:
    st.info("💡 Pro-Tip: Upload an updated financial document containing both Income Statement and Balance Sheet lines to generate the automated stakeholder summary module.")
