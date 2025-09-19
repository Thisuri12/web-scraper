# 📬 Web Scraper 2.0

A Python-based tool that scrapes company websites for contact emails and phone numbers using the Brave Search API. Designed for academic and freelance automation, with a clean GUI and strict typing.

---

## 🚀 Features

- 🔍 Searches company websites using Brave Search API
- 📧 Extracts one valid email per company
- 📞 Extracts one phone number (9–12 digits, cleans `+` signs)
- 🌐 GUI built with Tkinter for easy file upload and progress tracking
- 🛡️ Keeps API keys and secrets out of source using `.env`

---

## Setup

### 1. Clone the repo

git clone https://github.com/Thisuri12/web-scraper
cd web-scraper

### 2. Create a virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

###4. Add your Brave API key to .env (This file is ignored by Git using .gitignore)
Create a .env file in the root directory:
BRAVE_API_KEY=your_actual_api_key_here

🖥️ How to Run-> python main.py

Use the GUI to:
-Upload your Excel file with Company and Region columns
-Select a country
-Start scraping and save results to a new Excel file

📁 Input Format
Your Excel file should have:
Company Region
Corp Milan
Ltd Berlin

✅ Output Format
Company Region Website Emails Phone Numbers
Corp Milan ... info@example.com 0123456789

🔐 Security Notes
-API keys are stored in .env and never committed to Git
-.gitignore protects .env, cache files, and OS artifacts

📄 License
MIT License. Feel free to fork, improve, and share.

🙌 Credits
Built by Thisuri with ❤️ and Python.
