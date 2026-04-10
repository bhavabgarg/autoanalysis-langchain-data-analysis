import streamlit as st
import pandas as pd
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

def get_cleaning_plan(df, groq_api_key):
    if not groq_api_key:
        return None
    
    try:
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=groq_api_key)
        
        dtypes_str = df.dtypes.astype(str).to_dict()
        nulls_str = df.isnull().sum().to_dict()
        shape_str = str(df.shape)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert data science assistant. Given a dataset profile, suggest a cleaning plan in JSON format. The JSON should match this schema EXACTLY:\n{{\n  \"fill_nulls\": {{\"column_name\": 0_or_string}},\n  \"drop_columns\": [\"col1\"],\n  \"convert_to_int\": [\"col2\"],\n  \"convert_to_datetime\": [\"col3\"],\n  \"drop_duplicates\": true\n}}\nIf a step is not needed, leave it empty. Reply ONLY with complete and valid JSON. Do not write markdown backticks or any other text."),
            ("user", f"Dataset Profiling:\\nTypes: {dtypes_str}\\nNulls: {nulls_str}\\nShape: {shape_str}\\nSuggest a cleaning plan.")
        ])
        
        chain = prompt | llm
        response = chain.invoke({})
        content = response.content.strip()
        
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
            
        plan = json.loads(content)
        return plan
    except Exception as e:
        # Failsafe or silent error log
        # st.error(f"Error generating cleaning plan: {e}")
        return None

def clean_data(df, plan):
    df_cleaned = df.copy()
    
    if plan:
        if plan.get("drop_duplicates"):
            df_cleaned = df_cleaned.drop_duplicates()
            
        for col in plan.get("drop_columns", []):
            if col in df_cleaned.columns:
                df_cleaned = df_cleaned.drop(columns=[col])
                
        fill_nulls = plan.get("fill_nulls", {})
        if fill_nulls:
            for col, val in fill_nulls.items():
                if col in df_cleaned.columns:
                    df_cleaned[col] = df_cleaned[col].fillna(val)
                    
        for col in plan.get("convert_to_int", []):
            if col in df_cleaned.columns:
                try:
                    df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce').fillna(0).astype(int)
                except:
                    pass
                    
        for col in plan.get("convert_to_datetime", []):
            if col in df_cleaned.columns:
                try:
                    df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors='coerce')
                except:
                    pass
                    
    return df_cleaned

def manual_cleaning_ui(df_cleaned):
    st.markdown("### 🎛️ Manual Override")
    
    drop_cols = st.multiselect("Select columns to drop", df_cleaned.columns)
    if drop_cols:
        df_cleaned = df_cleaned.drop(columns=drop_cols)
        
    drop_dupes = st.checkbox("Drop Duplicate Rows", value=False)
    if drop_dupes:
        df_cleaned = df_cleaned.drop_duplicates()
        
    st.markdown("**Fill Missing Values**")
    col1, col2 = st.columns(2)
    with col1:
        col_to_fill = st.selectbox("Select column to fill nulls", ["None"] + list(df_cleaned.columns))
    with col2:
        fill_value = st.text_input("Fill value (string or number)")
        
    if col_to_fill != "None" and fill_value:
        try:
            if fill_value.replace('.', '', 1).isdigit():
                val = float(fill_value) if '.' in fill_value else int(fill_value)
            else:
                val = fill_value
            df_cleaned[col_to_fill] = df_cleaned[col_to_fill].fillna(val)
        except:
             df_cleaned[col_to_fill] = df_cleaned[col_to_fill].fillna(fill_value)
             
    return df_cleaned
