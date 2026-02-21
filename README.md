PO Classification System – LLM Powered
📌 Project Overview

PO Classification System is an AI-driven application that automatically classifies Purchase Order (PO) descriptions into predefined categories using a Large Language Model (LLM).
Instead of traditional ML training, the system relies on prompt-based reasoning via the Groq API.

🚀 Problem Statement

Organizations process large volumes of purchase orders.
Manual classification is:

• Time-consuming
• Error-prone
• Difficult to scale

An intelligent automated solution is needed to improve efficiency and accuracy.

✅ Solution

This project implements an LLM-based classification system that:

• Accepts PO descriptions from users
• Constructs optimized prompts
• Sends requests to the Groq LLM endpoint
• Returns predicted classification labels

No dataset training or feature engineering required.

🛠️ Tech Stack

Language
• Python

Frontend / UI
• Streamlit (interactive web interface)

AI / Model Backend
• Groq API
• Model: openai/gpt-oss-120b

Core Libraries
• streamlit
• groq

🏗️ Project Architecture

• UI Layer → app.py (Streamlit interface)
• Logic Layer → classifier.py (classification workflow)
• Prompt Management → prompts.py
• Category Definitions → taxonomy.py
• Configuration → settings.py

⚙️ How It Works

User enters a PO description

Input is processed and validated

Prompt is dynamically generated

Prompt sent to Groq API

LLM predicts classification category

Result displayed in UI

✨ Key Features

✔ LLM-powered classification
✔ No model training required
✔ Lightweight & fast
✔ Clean modular structure
✔ Easily extendable taxonomy

🎯 Use Cases

• Procurement automation
• Enterprise workflow optimization
• Intelligent document processing
• AI-based categorization systems

📦 Installation & Setup

1️⃣ Clone Repository

git clone <your-repo-url>
cd PO_Classification

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Configure API Key

Add your Groq API key inside Streamlit secrets:

.streamlit/secrets.toml

Example:

GROQ_API_KEY = "your_api_key_here"

4️⃣ Run Application

streamlit run app.py
📈 Future Improvements

✔ Add file / PDF input support
✔ Improve prompt optimization
✔ Add logging & analytics
✔ Deploy as API service
✔ Multi-label classification

👨‍💻 Author

Developed for learning, experimentation, and AI-based automation exploration.
