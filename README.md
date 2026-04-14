# AutoAnalyst AI ⚡
A fully automated data analysis web application powered by Streamlit, LangChain, and Groq LLMs.

## Architecture
+---------------+     +---------------+     +-----------------+
|               |     |               |     |                 |
| Data Ingest   +---->+ Auto Profiling+---->+ AI Data Cleaning|
| (CSV / SQL)   |     | (Pandas)      |     | (LangChain/Groq)|
|               |     |               |     |                 |
+---------------+     +---------------+     +--------+--------+
                                                     |
+---------------+     +---------------+              |
|               |     |               |              |
| Export / D/L  |<----+ Interactive   |<-------------+
|               |     | Dashboard     |              |
+---------------+     +---------------+
                          ^
                          | (SQL Agent)
                    +-----+-------+
                    | AI Insights |
                    +-------------+

## Setup Instructions
1. Clone this repository to your local machine.
2. Navigate to the project directory: `cd autoanalyst`
3. Install dependencies: `pip install -r requirements.txt`
4. Add your Groq API key to `.env`: `GROQ_API_KEY=your_key_here`
5. Run the Streamlit app: `streamlit run app.py`

## Screenshots
<img width="805" height="438" alt="image" src="https://github.com/user-attachments/assets/1d9e6b5e-f6de-41df-8cb4-c0cf2db5594d" />


## Tech Stack
- **Frontend/Framework**: Streamlit
- **Data Manipulation**: Pandas
- **Visualization**: Plotly
- **AI Orchestration**: LangChain
- **LLM**: Groq (Llama-3-70b-8192)
- **Database (In-memory)**: SQLAlchemy & SQLite

## License
MIT License
