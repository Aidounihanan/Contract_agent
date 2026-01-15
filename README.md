# Contract Review Expert (Agno)

A lightweight **AI-powered contract review application** built with **Agno** and **OpenAI**.  
It delivers a **client-ready contract review** through three complementary lenses:

- **Structure Review** – clarity, completeness, missing or inconsistent sections  
- **Legal & Compliance Review** – high-impact risks, unclear or missing clauses  
- **Negotiation Playbook** – redlines, negotiation points, fallback options  

>  **Disclaimer**: This tool provides informational assistance only and does **not** constitute legal advice.

---

## Features

- Upload contracts in **PDF / DOCX / TXT** format  
- Optional **user goal** (e.g. reduce liability, improve termination terms)  
- Clear and concise final report (no internal traces shown)  
- Two execution modes:
  - ✅ **Streamlit Web Interface**
  - ✅ **Telegram Bot Interface**

---

## 📁 Project Structure

```text
Contract_agent/
├── app_streamlit.py          # Streamlit web interface
├── app_telegram.py           # Telegram bot
├── core/
│   ├── __init__.py
│   ├── team.py               # Multi-agent logic (structure, legal, negotiation)
│   └── tools.py              # Contract text extraction utilities
├── assets/                   # Optional branding assets
│   └── logo.png
├── .env                      # Environment variables (not committed)
├── requirements.txt
└── venv/                     # Python virtual environment
🧩 Requirements
Python 3.10+ (recommended)

An OpenAI API key

Telegram Bot token (only for Telegram mode)

Supported on Windows, macOS, and Linux.

⚙️ Setup
1️⃣ Create and activate a virtual environment (Windows PowerShell)
python -m venv venv
.\venv\Scripts\Activate
2️⃣ Install dependencies
pip install -r requirements.txt
🔐 Environment Variables
Create a .env file at the project root:

env
OPENAI_API_KEY=your_openai_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
⚠️ Never commit .env to version control.

▶️ Run the Streamlit App
From the project root directory:

streamlit run app_streamlit.py
Streamlit will open automatically in your browser
(default: http://localhost:8501).

🤖 Run the Telegram Bot
From the project root directory:

python app_telegram.py
Then open your bot on Telegram and type:
/start
You can send:

Contract files (PDF / DOCX / TXT)

Optionally include a goal in the message or caption

