import streamlit as st
from streamlit_mic_recorder import mic_recorder
from groq import Groq
from gtts import gTTS
import os
from dotenv import load_dotenv
from database import init_db, get_hotel_status


load_dotenv()

#Groq client
if not os.getenv("GROQ_API_KEY"):
    st.error("Error: GROQ_API_KEY is missing from .env file.")
    st.stop()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#Database
init_db()

st.set_page_config(page_title="Simplotel Voice Concierge", page_icon="🏨", layout="wide")

#SIDEBAR
with st.sidebar:
    st.title("📊 Dashboard")

    metrics_placeholder = st.empty()
    
    st.markdown("---")
    st.success("System Status: Online 🟢")
    st.markdown("---")
    st.info("**Tech Stack:**\n- Groq (Fast AI)\n- Google TTS (Voice)\n- SQLite (Database)")

# UPDATE DASHBOARD
def update_dashboard():
    total_messages = len(st.session_state.messages)
    user_queries = sum(1 for m in st.session_state.messages if m["role"] == "user")
    

    with metrics_placeholder.container():
        col1, col2 = st.columns(2)
        col1.metric("Total Msgs", total_messages)
        col2.metric("User Queries", user_queries)

#MAIN CHAT INTERFACE
st.title("🏨 Simplotel Voice Concierge")
st.markdown("Ask about **room availability** or **prices**. The system checks the live database.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to Simplotel! How can I help you today?"}]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# FOOTER: VOICE INPUT 
footer_container = st.container()
with footer_container:
    st.write("---")
    col1, col2 = st.columns([1, 10])
    with col1:
        audio = mic_recorder(
            start_prompt="🎤 Speak",
            stop_prompt="⏹️ Stop",
            key='recorder',
            format="wav"
        )
    with col2:
        status_msg = st.empty()
        if audio:
            status_msg.write("Processing audio...")

# LOGIC ENGINE
if audio:
    with open("input.wav", "wb") as f:
        f.write(audio['bytes'])
    
    with st.spinner("Consulting the database..."):
        try:
            # 1. TRANSCRIPTION
            with open("input.wav", "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=("input.wav", file.read()),
                    model="whisper-large-v3",
                    response_format="json",
                    language="en",
                    temperature=0.0
                )
            user_text = transcription.text
            
            # Add User Message
            st.session_state.messages.append({"role": "user", "content": user_text})
            with st.chat_message("user"):
                st.markdown(user_text)
                
            # 2. INTELLIGENCE
            hotel_context = get_hotel_status()
            system_prompt = f"""
            You are a helpful hotel receptionist for Simplotel.
            Use the following real-time database info to answer questions:
            {hotel_context}
            Rules:
            1. Be polite and professional.
            2. Only offer rooms that are listed as available.
            3. Keep answers concise (MAX 2 sentences).
            4. Do not use formatting like asterisks.
            """
            chat_completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text}
                ],
                temperature=0.7,
                max_tokens=150
            )
            ai_response = chat_completion.choices[0].message.content
            
            # Add AI Response
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            with st.chat_message("assistant"):
                st.markdown(ai_response)
            
            # 3. AUDIO
            tts = gTTS(text=ai_response, lang='en', tld='co.in') 
            tts.save("output.mp3")
            status_msg.empty() 
            st.audio("output.mp3", format="audio/mp3", autoplay=True)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

# --- FINAL UPDATE ---
# This runs at the VERY END of the script every time.
# It ensures the numbers in the sidebar include the messages we just added above.
update_dashboard()