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
<img width="1914" height="853" alt="Screenshot 2026-04-14 181657" src="https://github.com/user-attachments/assets/d3111e06-651e-4bbd-a4b2-8bfd8d56a017" />

<img width="1887" height="843" alt="Screenshot 2026-04-14 181811" src="https://github.com/user-attachments/assets/b8a48d43-2fa5-4104-a471-885148ed5f33" />


## Tech Stack
- **Frontend/Framework**: Streamlit
- **Data Manipulation**: Pandas
- **Visualization**: Plotly
- **AI Orchestration**: LangChain
- **LLM**: Groq (Llama-3-70b-8192)
- **Database (In-memory)**: SQLAlchemy & SQLite

