# 🔬 ResearchFlow AI

ResearchFlow AI is a **Multi-Agent AI Research Assistant** built using **LangChain**, **Mistral AI**, **Tavily Search API**, and **Streamlit**.

The system uses multiple AI agents that collaborate together to:
- Search the web
- Scrape detailed information
- Generate structured research reports
- Critically review the generated report

It provides a beautiful futuristic Streamlit UI and an end-to-end automated research workflow.

---

# 🚀 Features

## ✅ Multi-Agent Architecture
The project uses specialized AI agents for different tasks:

| Agent | Responsibility |
|---|---|
| 🔍 Search Agent | Searches the web for recent & reliable information |
| 📄 Reader Agent | Scrapes and extracts deep content from URLs |
| ✍️ Writer Chain | Generates a professional research report |
| 🧐 Critic Chain | Reviews and scores the report |

---

## ✅ Modern Streamlit UI
- Futuristic dark theme UI
- Animated pipeline stages
- Real-time agent progress tracking
- Downloadable report generation

---

## ✅ AI Powered Research Workflow
The application automatically:
1. Searches latest information
2. Extracts useful content
3. Synthesizes findings
4. Creates structured reports
5. Critiques the report quality

---

# 🛠️ Tech Stack

## Frontend
- Streamlit
- Custom CSS

## Backend / AI
- LangChain
- Mistral AI
- Google Gemini (optional)
- Tavily Search API

## Web Scraping
- BeautifulSoup4
- Requests

---

# 📂 Project Structure

```bash
ResearchFlow-AI/
│
├── agents.py          # Agent & chain definitions
├── app.py             # Streamlit frontend
├── pipeline.py        # CLI pipeline execution
├── tools.py           # Search & scraping tools
├── requirements.txt
├── .env
└── README.md
