# 🏨 Simplotel Voice Concierge

An intelligent voice-enabled hotel assistant built for the Simplotel AI Intern assignment. 
This bot handles customer queries regarding room availability and pricing using real-time database lookups and tracks system performance.

## 🌟 Features
- **Voice-to-Voice Interaction:**   using Groq & Whisper.
- **Real-time Database:** Fetches live room inventory (SQLite) to prevent overbooking.
- **Performance Dashboard:** Tracks Total messages and User-queries in real-time.
- **Context Awareness:** Remembers conversation history for natural follow-ups.

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Speech-to-Text:** Groq (Whisper-Large-V3)
- **LLM:** Groq (Llama-3.1-8b-Instant)
- **Text-to-Speech:** gTTS (Google Text-to-Speech)
- **Database:** SQLite



## ⚙️ Installation & Run
1. Clone the repository.
2. Install dependencies:
   pip install -r requirements.txt
3.Create a .env file and add your Groq Key:
GROQ_API_KEY=your_key_here
4.Run the app:
streamlit run app.py
