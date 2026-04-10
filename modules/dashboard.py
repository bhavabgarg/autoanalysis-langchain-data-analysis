import streamlit as st
import plotly.express as px

def render_dashboard(df):
    st.subheader("📈 Visual Dashboard")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category', 'string', 'bool']).columns.tolist()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if cat_cols:
            st.markdown(f"**Top 10 values of {cat_cols[0]}**")
            first_cat = cat_cols[0]
            val_counts = df[first_cat].value_counts().head(10).reset_index()
            val_counts.columns = [first_cat, 'Count']
            fig_bar = px.bar(val_counts, x=first_cat, y='Count', title=f"Top 10 {first_cat}", template="plotly_dark", color_discrete_sequence=["#4f8ef7"])
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No categorical columns available for bar chart.")
            
        if len(numeric_cols) >= 2:
            st.markdown("**Scatter plot of top 2 correlated numeric columns**")
            corr_matrix = df[numeric_cols].corr()
            corr_pairs = corr_matrix.abs().unstack().sort_values(ascending=False).drop_duplicates()
            corr_pairs = corr_pairs[corr_pairs < 1]
            if not corr_pairs.empty:
                col_x, col_y = corr_pairs.index[0]
                fig_scatter = px.scatter(df, x=col_x, y=col_y, title=f"Scatter: {col_x} vs {col_y}", template="plotly_dark", color_discrete_sequence=["#00d09c"])
                st.plotly_chart(fig_scatter, use_container_width=True)
            else:
                st.info("Could not find correlated numeric columns for scatter plot.")
        else:
            st.info("Need at least 2 numeric columns for scatter plot.")
                
    with col2:
        if numeric_cols:
            st.markdown(f"**Line chart: {numeric_cols[0]}**")
            first_num = numeric_cols[0]
            dt_cols = df.select_dtypes(include=['datetime']).columns.tolist()
            x_axis = dt_cols[0] if dt_cols else df.index
            fig_line = px.line(df, x=x_axis, y=first_num, title=f"Line Chart of {first_num}", template="plotly_dark", color_discrete_sequence=["#f7a84f"])
            st.plotly_chart(fig_line, use_container_width=True)
            
            st.markdown("**Histogram: Distribution of numeric column**")
            sel_col = st.selectbox("Select numeric column", numeric_cols, key="hist_select")
            fig_hist = px.histogram(df, x=sel_col, title=f"Distribution of {sel_col}", template="plotly_dark", color_discrete_sequence=["#4f8ef7"])
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("No numeric columns available for line and histogram charts.")
            
    if len(numeric_cols) > 1:
        st.markdown("**Correlation Heatmap**")
        corr = df[numeric_cols].corr()
        fig_corr = px.imshow(corr, title="Correlation Heatmap", template="plotly_dark", 
                             color_continuous_scale="RdBu_r", text_auto=True, aspect="auto")
        st.plotly_chart(fig_corr, use_container_width=True)
