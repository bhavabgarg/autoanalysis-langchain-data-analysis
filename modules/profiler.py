import streamlit as st
import pandas as pd

def profile_data(df):
    st.subheader("📊 Data Profiling Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Rows", value=df.shape[0])
    with col2:
        st.metric(label="Total Columns", value=df.shape[1])
    with col3:
        st.metric(label="Duplicate Rows", value=df.duplicated().sum())

    with st.expander("Column Data Types"):
        dtypes_df = pd.DataFrame(df.dtypes, columns=["Data Type"]).reset_index()
        dtypes_df.rename(columns={"index": "Column Name"}, inplace=True)
        dtypes_df['Data Type'] = dtypes_df['Data Type'].astype(str)
        st.dataframe(dtypes_df, use_container_width=True)

    with st.expander("Missing Values (Nulls)"):
        nulls_df = pd.DataFrame(df.isnull().sum(), columns=["Null Count"]).reset_index()
        nulls_df.rename(columns={"index": "Column Name"}, inplace=True)
        st.dataframe(nulls_df, use_container_width=True)

    with st.expander("Statistical Summary"):
        # describe(include='all') to include categorical data
        desc_df = df.describe(include='all').T.reset_index()
        desc_df.rename(columns={"index": "Column Name"}, inplace=True)
        st.dataframe(desc_df, use_container_width=True)
