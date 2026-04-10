import streamlit as st
import pandas as pd
import os
import time
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AutoAnalyst AI", layout="wide", page_icon="⚡")

st.markdown("""
<style>
:root {
    --bg-color: #0f1117;
    --accent: #4f8ef7;
    --success: #00d09c;
    --warning: #f7a84f;
    --card-bg: #1e2130;
}
.stApp {
    background-color: var(--bg-color);
}
div[data-testid="stMetricValue"] {
    color: var(--accent);
}
.metric-card {
    border-left: 5px solid var(--accent);
    padding: 10px;
    background-color: var(--card-bg);
    border-radius: 5px;
    margin-bottom: 10px;
}
.insight-card {
    border: 2px solid transparent;
    border-radius: 8px;
    background: linear-gradient(var(--card-bg), var(--card-bg)) padding-box, 
                linear-gradient(135deg, var(--accent), var(--success)) border-box;
    padding: 20px;
    margin-bottom: 15px;
    color: white;
}
.insight-card h4 {
    margin-top: 0;
    color: var(--success);
}
</style>
""", unsafe_allow_html=True)

from modules import ingest, profiler, cleaner, insights, dashboard

st.sidebar.title("⚡ AutoAnalyst AI")
st.sidebar.markdown("Fully automated data analysis web application.")

api_key = st.sidebar.text_input(
    "Groq API Key", 
    type="password", 
    value=os.getenv("GROQ_API_KEY", ""),
    help="Enter your Groq API key here or place it in the .env file."
)

if not api_key:
    st.sidebar.warning("⚠️ Groove API Key missing. Data cleaning & AI insights will be disabled.")

raw_df = ingest.upload_data()

if raw_df is not None:
    # State Management: reset state if new data is uploaded
    if "raw_df" not in st.session_state or not st.session_state.raw_df.equals(raw_df):
        st.session_state.raw_df = raw_df
        st.session_state.cleaned_df = None
        st.session_state.cleaning_plan = None
        if "ai_insights_report" in st.session_state:
            del st.session_state.ai_insights_report
            
        progress_text = "Processing your data..."
        my_bar = st.progress(0, text=progress_text)
        time.sleep(0.5)
        my_bar.progress(20, text="[Ingesting] Complete")
        
        with st.spinner("Generating AI Cleaning Plan..."):
            plan = cleaner.get_cleaning_plan(raw_df, api_key)
            st.session_state.cleaning_plan = plan
            st.session_state.cleaned_df = cleaner.clean_data(raw_df, plan)
            
        my_bar.progress(60, text="[Profiling & Cleaning] Complete")
        time.sleep(0.5)
        my_bar.progress(100, text="[Dashboard Ready]")
        time.sleep(0.5)
        my_bar.empty()
        
    st.title("AutoAnalyst AI Dashboard Overview")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Data Profile", 
        "🧹 Clean & Preview", 
        "🤖 AI Insights", 
        "📈 Charts", 
        "💾 Export"
    ])
    
    with tab1:
        profiler.profile_data(st.session_state.raw_df)
        
    with tab2:
        st.subheader("🧹 Data Cleaning Pipeline")
        if st.session_state.cleaning_plan:
            with st.expander("AI Recommended Cleaning Plan (JSON)"):
                st.json(st.session_state.cleaning_plan)
        else:
            if api_key:
                 st.info("No AI cleaning steps recommended.")
            else:
                 st.warning("Provide API key for AI Cleaning.")
                 # If no AI plan, default fallback cleaned_df to raw_df
                 if st.session_state.cleaned_df is None:
                     st.session_state.cleaned_df = st.session_state.raw_df.copy()
            
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Original Data (Header)**")
            st.dataframe(st.session_state.raw_df.head(), use_container_width=True)
            
        # Apply manual cleaning overrides right before display
        st.session_state.cleaned_df = cleaner.manual_cleaning_ui(st.session_state.cleaned_df)
        
        with col2:
            st.markdown("**Processed / Cleaned Data (Preview)**")
            st.dataframe(st.session_state.cleaned_df.head(), use_container_width=True)
            
        # CSV Export shortcut in this tab
        csv_quick = st.session_state.cleaned_df.to_csv(index=False).encode('utf-8')
        st.download_button("↓ Quick Download Clean CSV", csv_quick, "cleaned_data.csv", "text/csv")
            
    with tab3:
        if api_key:
            insights.run_ai_insights(st.session_state.cleaned_df, api_key)
        else:
            st.warning("Please provide Groq API Key to enable AI Insights.")
            
    with tab4:
        dashboard.render_dashboard(st.session_state.cleaned_df)
        
    with tab5:
        st.subheader("💾 Export Center")
        
        csv_full = st.session_state.cleaned_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download Cleaned CSV File",
            data=csv_full,
            file_name='cleaned_data.csv',
            mime='text/csv',
            use_container_width=True
        )
        
        if "ai_insights_report" in st.session_state:
            report_text = "=== AutoAnalyst AI Insights Report ===\n\n"
            for item in st.session_state.ai_insights_report:
                report_text += f"[Q]: {item['q']}\n[A]: {item['a']}\n\n"
            
            st.download_button(
                label="📝 Download AI Insights Report (.txt)",
                data=report_text.encode('utf-8'),
                file_name='autoanalyst_insights.txt',
                mime='text/plain',
                use_container_width=True
            )
            
        st.markdown("**Clean Data Viewer**")
        st.dataframe(st.session_state.cleaned_df, use_container_width=True)

else:
    st.info("👈 Please use the sidebar to upload a dataset or connect to an SQL database to begin.")
