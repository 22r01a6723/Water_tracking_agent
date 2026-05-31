💧 Water Tracker (AI Powered)
AI-powered Water Tracker using FastAPI, Uvicorn, SQLite, and Streamlit with Gemini/OpenAI integration. It logs water intake, stores history, and generates AI-based hydration insights. The dashboard visualizes daily and weekly trends and supports data-driven health tracking.

🚀 Features
📌 Log daily water intake via API/UI
🗄️ SQLite database for persistent storage
🧠 AI-generated hydration insights (Gemini/OpenAI)
📊 Streamlit dashboard for trend visualization
👥 Multi-user tracking support
📈 Daily & weekly consumption analysis
🔍 Debug-friendly logging system
🛠️ Tech Stack
FastAPI (Backend APIs)
Uvicorn (Server)
Streamlit (Dashboard UI)
SQLite (Database)
Gemini / OpenAI API (AI Insights)
Python (Core logic)

📁 Project Structure
WATERTRACKER/
│
├── src/
│   ├── api.py          # FastAPI endpoints
│   ├── agent.py        # AI logic (Gemini/OpenAI)
│   ├── database.py     # SQLite operations
│   ├── logger.py       # Logging utilities
│   ├── dashboard.py    # Streamlit UI
│
├── water_tracker.db    # SQLite database
├── image.png           # UI assets
├── requirements.txt    # Dependencies
⚙️ Setup & Installation
1️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Add environment variables

Create .env file:

GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
🚀 Run Project
▶ Start FastAPI backend
uvicorn src.api:app --reload
▶ Start Streamlit dashboard
streamlit run src/dashboard.py

🔄 Workflow
User → FastAPI → SQLite → AI Agent → Streamlit Dashboard → Insights & Trends

🧠 AI Features
.Hydration behavior analysis
.Personalized suggestions
.Trend-based feedback
.Smart recommendations
📊 Output
.Daily intake tracking
.Weekly trend graphs
.AI hydration suggestions
.User-wise history logs
🐛 Common Issues
.Ensure uvicorn is running before opening dashboard
.Check .env keys for AI API errors
.Delete water_tracker.db if schema breaks
💡 Goal
To transform simple water logging into an AI-powered health insight system with real-time analytics.
