import re
import json
import pandas as pd
import streamlit as st
import pdfplumber
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Universal Financial Intelligence Engine", page_icon="📈", layout="wide")
st.title("📈 Universal Multi-Year Financial Ingestion & Investor Platform")
st.caption("Production-Grade Data Collection Engine | Engineered for S&P Global, Moody's, and Bloomberg Assessment Standards")

# 2. Sidebar Process Documentation & Secure Token Session
st.sidebar.header("🔑 Engine Authentication Matrix")
user_token = st.sidebar.text_input("Gemini API Key (Optional)", type="password", help="Input your free Google AI Studio token to unlock universal semantic processing. Leave blank for fallback heuristic logic.")

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Data Processing Matrix")
st.sidebar.info("""
- **Primary AI Processing Mode:** Semantic Structure Normalization via Gemini.
- **Fallback Processing Mode:** Offline Multi-Line Lookahead Layout Tokenization.
- **Security Profile:** 100% Secure (Keys remain volatile in browser session memory).
- **Execution Cost:** $0 (Free Tier Frameworks Only).
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
    
    # PDF Parser Loop using layout bounding box character tracking
    if file_name.endswith('.pdf'):
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    text_content = page.extract_text()
                    if text_content:
                        raw_text += text_content + "\n"
                    
                    # Layout fallback matching matrix rows
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            if row:
                                raw_text += " ".join([str(cell) for cell in row if cell]) + "\n"
            st.success("✅ PDF Text Layout Array Unpacked Successfully.")
        except Exception as e:
            st.error(f"Failed to process PDF text matrix layout: {e}")

    # Excel Parser Loop
    elif file_name.endswith(('.xlsx', '.xls')):
        try:
            excel_df = pd.read_excel(uploaded_file)
            st.success("✅ Excel Ledger Uploaded Successfully.")
            raw_text = excel_df.to_string()
        except Exception as e:
            st.error(f"Failed to parse Excel tabular matrices: {e}")
            
    # Text Parser Loop
    else:
        raw_text = uploaded_file.read().decode("utf-8")
        st.success("✅ Raw String Payload Processed.")

    # 4. Multi-Path Processing Gateway
    parsed_json_data = None
    
    # --- PATH A: INTELLECTUAL AI SEMANTIC MAPPING ENGINE ---
    if user_token and raw_text.strip():
        st.info("🤖 Primary Mode Activated: Executing Semantic Mapping over document layout...")
        try:
            genai.configure(api_key=user_token)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            ai_prompt = f"""
            You are an elite fundamental data curation specialist at S&P Global. Analyze this corporate text.
            Your task is to identify and extract side-by-side historical columns for the main report lines.
            
            Target Variables:
            1. Revenue (or turnover, operational sales)
            2. Net Income (or profit for the period, net earnings, PAT). Ensure losses inside parentheses are negative floats!
            3. Total Assets
            4. Total Liabilities
            
            OUTPUT RULES:
            - Return STRICTLY a valid JSON list of dictionaries. No text explanations, notes, or markdown wrappers.
            - Format numbers as clean numeric floats. Keep losses as negative balances.
            
            Expected JSON Output Structure:
            [
                {{"Period": "Prior Period", "Revenue": 150000.0, "Net Income": -12000.0, "Total Assets": 450000.0, "Total Liabilities": 19000.0}},
                {{"Period": "Current Period", "Revenue": 185000.0, "Net Income": 24000.0, "Total Assets": 520000.0, "Total Liabilities": 21000.0}}
            ]
            
            Document Text Segment:
            {raw_text[:45000]}
            """
            response = model.generate_content(ai_prompt)
            clean_text = response.text.strip().replace("```json", "").replace("```", "")
            parsed_json_data = json.loads(clean_text)
        except Exception as e:
            st.warning(f"AI Core processing error out, defaulting to fallback engine profile... Details: {e}")

    # --- PATH B: OFFLINE HEURISTIC BLOCK TOKENIZER (FALLBACK) ---
    if parsed_json_data is None and raw_text.strip():
        st.info("⚙️ Secondary Mode Activated: Executing Local Lookahead Tokenizer...")
        keywords = {
            "Revenue": ["revenue", "sales", "turnover", "operations", "income"],
            "Net Income": ["net income", "profit", "earnings", "pat", "loss", "profit/(loss)"],
            "Total Assets": ["assets", "property", "equipment", "balance sheet total"],
            "Total Liabilities": ["liabilities", "obligations", "equity and liabilities"]
        }
        extracted_metrics = {k: [None, None] for k in keywords.keys()}
        lines = raw_text.split("\n")
        
        for idx, line in enumerate(lines):
            line_lower = line.lower()
            for metric, aliases in keywords.items():
                if any(alias in line_lower for alias in aliases) and extracted_metrics[metric] == [None, None]:
                    search_block = " ".join(lines[idx:idx+3])
                    raw_tokens = re.findall(r'\(?\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b\)?', search_block)
                    tokens = []
                    for token in raw_tokens:
                        is_negative = "(" in token or ")" in token or "-" in token
                        clean_token = token.replace(",", "").replace("(", "").replace(")", "").replace("-", "").strip()
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
                        
        parsed_json_data = [
            {"Period": "Current Period", **{k: (v[0] if v else None) for k, v in extracted_metrics.items()}},
            {"Period": "Prior Period", **{k: (v[1] if v else None) for k, v in extracted_metrics.items()}}
        ]

    # 5. DataFrame Compilation & Presentation Layer
    if parsed_json_data:
        df = pd.DataFrame(parsed_json_data)
        
        st.subheader("🧹 Step 2: Cleaned & Standardized Historical Financial Extract")
        st.dataframe(df.style.format({
            "Revenue": "${:,.2f}",
            "Net Income": "${:,.2f}",
            "Total Assets": "${:,.2f}",
            "Total Liabilities": "${:,.2f}"
        }, na_rep="Missing Data Segment"), use_container_width=True)
        
        # 6. Advanced Financial Ratio Calculations
        st.subheader("📊 Step 3: Comparative Performance & Solvency Analytics Matrix")
        
        # Helper computation wrappers to insulate against missing text data rows
        def calc_margin(row): return (row["Net Income"] / row["Revenue"]) * 100 if pd.notna(row["Net Income"]) and pd.notna(row["Revenue"]) and row["Revenue"] != 0 else None
        def calc_leverage(row): return row["Total Liabilities"] / row["Total Assets"] if pd.notna(row["Total Liabilities"]) and pd.notna(row["Total Assets"]) and row["Total Assets"] != 0 else None
        def calc_equity(row): return row["Total Assets"] - row["Total Liabilities"] if pd.notna(row["Total Assets"]) and pd.notna(row["Total Liabilities"]) else None
        def calc_roa(row): return (row["Net Income"] / row["Total Assets"]) * 100 if pd.notna(row["Net Income"]) and pd.notna(row["Total Assets"]) and row["Total Assets"] != 0 else None

        df["Net Profit Margin (%)"] = df.apply(calc_margin, axis=1)
        df["Debt-to-Asset Ratio"] = df.apply(calc_leverage, axis=1)
        df["Equity / Net Worth"] = df.apply(calc_equity, axis=1)
        df["Return on Assets (%)"] = df.apply(calc_roa, axis=1)
        
        rev_growth = None
        if len(df) > 1 and pd.notna(df.at[0, "Revenue"]) and pd.notna(df.at[1, "Revenue"]) and df.at[1, "Revenue"] != 0:
            rev_growth = ((df.at[0, "Revenue"] - df.at[1, "Revenue"]) / df.at[1, "Revenue"]) * 100

        st.dataframe(df.style.format({
            "Net Profit Margin (%)": "{:.2f}%",
            "Debt-to-Asset Ratio": "{:.2f}",
            "Equity / Net Worth": "${:,.2f}",
            "Return on Assets (%)": "{:.2f}%"
        }, na_rep="Awaiting Alignment"), use_container_width=True)
        
        # --- STEP 4 EXPERT RE-STRUCTURED SUMMARY VERDICT ---
        st.markdown("---")
        st.subheader("🎯 Step 4: Executive Performance Summary Verdict")
        
        ni = df.at[0, "Net Income"]
        assets = df.at[0, "Total Assets"]
        liab = df.at[0, "Total Liabilities"]
        
        summary_bullets = []
        is_healthy = True
        
        if pd.notna(ni):
            if ni > 0:
                summary_bullets.append("✅ **Operational Performance:** The company is fully **profitable** and successfully generating positive net returns.")
            else:
                is_healthy = False
