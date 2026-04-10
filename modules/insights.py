import streamlit as st
import pandas as pd
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


def _build_data_context(df: pd.DataFrame) -> str:
    """Build a rich text summary of the dataframe to send as LLM context."""
    lines = []
    lines.append(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    lines.append(f"Columns: {list(df.columns)}")
    lines.append(f"\nData Types:\n{df.dtypes.astype(str).to_string()}")
    lines.append(f"\nNull Counts:\n{df.isnull().sum().to_string()}")

    numeric_df = df.select_dtypes(include="number")
    if not numeric_df.empty:
        lines.append(f"\nNumeric Summary:\n{numeric_df.describe().round(2).to_string()}")

    lines.append(f"\nFirst 5 rows:\n{df.head().to_string(index=False)}")
    return "\n".join(lines)


def run_ai_insights(df: pd.DataFrame, groq_api_key: str):
    if not groq_api_key:
        st.warning("Please provide a Groq API Key to generate insights.")
        return

    try:
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=groq_api_key)
        data_context = _build_data_context(df)

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        highest_numeric_col = numeric_cols[0] if numeric_cols else "any numeric column"

        questions = [
            "What are the top trends in this dataset?",
            "Which columns have the strongest correlations?",
            "Are there any outliers or anomalies?",
            f"What are the top 5 rows by highest {highest_numeric_col}?",
            "Give a plain-English business summary of this data.",
        ]

        st.subheader("💡 AI Auto-Insights")

        if "ai_insights_report" not in st.session_state:
            insights = []
            with st.spinner("Generating AI insights… This may take a moment."):
                for q in questions:
                    try:
                        prompt = ChatPromptTemplate.from_messages([
                            ("system",
                             "You are an expert data analyst. The user will give you a dataset summary "
                             "and ask a question. Answer clearly and concisely in plain English. "
                             "Do not ask for more data — work only with what is provided."),
                            ("user",
                             f"Dataset Summary:\n{data_context}\n\nQuestion: {q}"),
                        ])
                        chain = prompt | llm
                        response = chain.invoke({})
                        insights.append({"q": q, "a": response.content.strip()})
                    except Exception as e:
                        insights.append({"q": q, "a": f"Error generating insight: {e}"})
            st.session_state["ai_insights_report"] = insights

        # Display auto-insights
        for item in st.session_state["ai_insights_report"]:
            st.markdown(f'''
            <div class="insight-card">
                <h4>{item["q"]}</h4>
                <p>{item["a"]}</p>
            </div>
            ''', unsafe_allow_html=True)

        # Interactive Q&A
        st.markdown("### 💬 Ask anything about your data")
        user_query = st.text_input(
            "Type your question here…",
            placeholder="e.g., How many rows have a value > 100?",
            key="user_insight_query"
        )
        if user_query:
            with st.spinner("Analyzing…"):
                try:
                    prompt = ChatPromptTemplate.from_messages([
                        ("system",
                         "You are an expert data analyst. The user will give you a dataset summary "
                         "and ask a question. Answer clearly and concisely in plain English. "
                         "Do not ask for more data — work only with what is provided."),
                        ("user",
                         f"Dataset Summary:\n{data_context}\n\nQuestion: {user_query}"),
                    ])
                    chain = prompt | llm
                    response = chain.invoke({})
                    st.success(response.content.strip())
                except Exception as e:
                    st.error(f"Error: {e}")

    except Exception as e:
        st.error(f"Failed to initialize AI Insights: {e}")
