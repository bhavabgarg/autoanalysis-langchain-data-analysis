import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

def upload_data():
    st.sidebar.subheader("📥 Data Ingestion")
    option = st.sidebar.radio("Choose Input Method", ["Upload CSV", "Connect to SQL DB"])
    
    df = None
    if option == "Upload CSV":
        uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.sidebar.success("CSV Uploaded Successfully!")
            except Exception as e:
                st.sidebar.error(f"Error loading CSV: {e}")
    else:
        db_string = st.sidebar.text_input("SQLAlchemy Connection String", 
                                          placeholder="sqlite:///example.db")
        query = st.sidebar.text_area("SQL Query", placeholder="SELECT * FROM table_name")
        if st.sidebar.button("Connect & Query"):
            if db_string and query:
                try:
                    engine = create_engine(db_string)
                    df = pd.read_sql(query, engine)
                    st.sidebar.success("Query Executed Successfully!")
                except Exception as e:
                    st.sidebar.error(f"Database Error: {e}")
            else:
                st.sidebar.warning("Please provide both connection string and query.")
    return df
