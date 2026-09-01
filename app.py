import pandas as pd
import streamlit as st
import pdfplumber
import google.generativeai as genai
import json

# 1. Page Configuration
st.set_page_config(page_title="Universal Financial Analytics Platform", page_icon="📈", layout="wide")
st.title("📈 Universal Multi-Year Financial Ingestion & Investor Engine")
st.caption("AI-Assisted Fundamental Data Pipeline Tailored for S&P Global, Moody's, and Bloomberg Interview Readiness")

# 2. Sidebar Process Documentation & Secure Input
st.sidebar.header("🔑 Engine Authentication")
user_api_key = st.sidebar.text_input("Enter Gemini API Key", type="password", help="Input your free Google AI Studio token to process this document.")

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Data Processing Matrix")
st.sidebar.info("""
- **AI Core:** Generative Mapping Layer (Gemini Flash).
- **Security Profile:** 100% Client-Side Isolated (Key is never stored or logged).
- **Execution Cost:** $0 (Using Google's Free Tier token).
""")

# 3. File Ingestion Engine
uploaded_file = st.file_uploader(
    "Upload Any Corporate Financial Report (Accepts: .pdf, .txt)", 
    type=["pdf", "txt"]
)

raw_text = ""

if uploaded_file is not None:
    if not user_api_key:
        st.warning("🔒 Session Authentication Required: Please enter your free Gemini API key in the left sidebar to unlock the universal intelligence engine.")
    else:
        file_name = uploaded_file.name
        st.subheader(f"📥 Processing Ingested File: `{file_name}`")
        
        # Robust PDF Layout Character Unpacker
        if file_name.endswith('.pdf'):
            try:
                with pdfplumber.open(uploaded_file) as pdf:
                    for page in pdf.pages:
                        text_content = page.extract_text()
                        if text_content:
                            raw_text += text_content + "\n"
                st.success("✅ Layout Extraction Phase Complete.")
            except Exception as e:
                st.error(f"Failed to unpack document characters: {e}")
        else:
            raw_text = uploaded_file.read().decode("utf-8")
            st.success("✅ Text String Matrix Loaded.")

        if raw_text:
            # Configure Google Generative AI Session Environment
            genai.configure(api_key=user_api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # 4. Strict Financial Data Engineering Extraction Prompt
            ai_prompt = f"""
            You are an expert fundamental data extraction specialist at S&P Global. Analyze this corporate text.
            Your objective is to find the core side-by-side multi-year financial numbers (such as Current Year vs Prior Year, or consecutive quarters).
            
            Isolate the main rows for:
            1. Total Revenue (or Operational Income/Turnover)
            2. Net Income (or Net Profit After Tax/PAT/Profit for the Period)
            3. Total Assets
            4. Total Liabilities
            
            CRITICAL RULES:
            - Disregard small intermediate line-item adjustments, taxes, or micro sub-components. Capture the main high-level consolidated metrics.
            - Ensure Revenue and Assets are positive numbers representing real scale.
            - Output your final structured table lines STRICTLY as a raw, valid JSON list of dictionaries. 
            - Do not return markdown wraps, trailing notes, or conversational sentences.
            
            JSON Blueprint Output Target:
            [
                {{"Period": "Prior Period", "Revenue": 150000000.0, "Net Income": 12000000.0, "Total Assets": 450000000.0, "Total Liabilities": 190000000.0}},
                {{"Period": "Current Period", "Revenue": 185000000.0, "Net Income": 19000000.0, "Total Assets": 520000000.0, "Total Liabilities": 210000000.0}}
            ]
            
            Filing Document Segment:
            {raw_text[:45000]}
            """
            
            with st.spinner("🤖 AI Orchestration Layer Mapping Varied Disclosures into Standard Schema..."):
                try:
                    response = model.generate_content(ai_prompt)
                    # Safe cleaning of standard text response outputs
                    clean_text = response.text.strip().replace("```json", "").replace("```", "")
                    parsed_json = json.loads(clean_text)
                    
                    df = pd.DataFrame(parsed_json)
                    
                    st.subheader("🧹 Step 2: Cleaned & Standardized Historical Financial Extract")
                    st.dataframe(df.style.format({
                        "Revenue": "${:,.2f}",
                        "Net Income": "${:,.2f}",
                        "Total Assets": "${:,.2f}",
                        "Total Liabilities": "${:,.2f}"
                    }, na_rep="Metric Omitted"), use_container_width=True)
                    
                    # 5. Advanced Trend Analytics Module
                    st.subheader("📊 Step 3: Comparative Performance & Solvency Analytics Matrix")
                    
                    df["Net Profit Margin (%)"] = (df["Net Income"] / df["Revenue"]) * 100
                    df["Debt-to-Asset Ratio"] = df["Total Liabilities"] / df["Total Assets"]
                    df["Equity / Net Worth"] = df["Total Assets"] - df["Total Liabilities"]
                    df["Return on Assets (%)"] = (df["Net Income"] / df["Total Assets"]) * 100
                    
                    # Horizontal Growth Changes
                    if len(df) > 1:
                        df["Revenue Growth (%)"] = df["Revenue"].pct_change() * 100
                        df["Net Income Growth (%)"] = df["Net Income"].pct_change() * 100
                    else:
                        df["Revenue Growth (%)"] = None
                        df["Net Income Growth (%)"] = None

                    st.dataframe(df.style.format({
                        "Net Profit Margin (%)": "{:.2f}%",
                        "Debt-to-Asset Ratio": "{:.2f}",
                        "Equity / Net Worth": "${:,.2f}",
                        "Return on Assets (%)": "{:.2f}%",
                        "Revenue Growth (%)": "{:.2f}%",
                        "Net Income Growth (%)": "{:.2f}%"
                    }, na_rep="Context Bound"), use_container_width=True)
                    
                    # 6. Deep Analytical Investor Summary
                    st.markdown("---")
                    st.subheader("📑 Step 4: Institutional Investor Decision Memorandum")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("#### 📈 Revenue Velocity & Profit Realization")
                        for idx, row in df.iterrows():
                            p = row['Period']
                            m = row['Net Profit Margin (%)']
                            g = row['Revenue Growth (%)']
                            g_text = f" (YoY Shift: {g:.1f}%)" if pd.notna(g) else ""
                            
                            if pd.notna(m):
                                if m > 15:
                                    st.markdown(f"🏆 **{p}:** Superior structural margin sitting at **{m:.1f}%**{g_text}. Strong competitive defenses.")
                                elif m >= 0:
                                    st.markdown(f"名 **{p}:** Balanced profit conversion at **{m:.1f}%**{g_text}. Stable core volume baseline.")
                                else:
                                    st.markdown(f"⚠️ **{p}:** Structural loss margins logged (**{m:.1f}%**){g_text}. Operational costs require review.")

                    with col2:
                        st.markdown("#### 🛡️ Capital Architecture Safety Grading")
                        for idx, row in df.iterrows():
                            p = row['Period']
                            lev = row['Debt-to-Asset Ratio']
                            roa = row['Return on Assets (%)']
                            
                            if pd.notna(lev) and pd.notna(roa):
                                if lev < 0.5 and roa > 8:
                                    st.markdown(f"🟢 **{p}:** Highly defensive risk structure ({lev:.2f} leverage) matched with clean asset tracking productivity of **{roa:.1f}%**.")
                                else:
                                    st.markdown(f"🟡 **{p}:** Standard capital leverage patterns tracked. Performance within historic normal boundaries.")
                                    
                    # 7. Data Export Execution Link
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Export Full Historical Investment Analytics to CSV",
                        data=csv,
                        file_name="universal_investor_analytics.csv",
                        mime="text/csv"
                    )
                    
                except Exception as e:
                    st.error(f"Failed to map structured finance outputs: {e}")
                    st.info("💡 Pro-Tip: Make sure your key is valid and the file contains text-based characters.")
