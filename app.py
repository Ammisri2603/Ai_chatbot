import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(
    page_title="Chandu-Nexora AI",
    page_icon="🤖",
    layout="centered"
)

# Gemini API configuration
api_key = os.getenv("GEMINI_API_KEY")

st.title("🤖 Chandu-Nexora AI")
st.caption("Your personal AI assistant")

if not api_key:
    st.error("GEMINI_API_KEY is not configured. Please set it in your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

SYSTEM_INSTRUCTIONS = """
You are Chandu-Nexora, a helpful, friendly, intelligent AI assistant.
Answer questions clearly and naturally.
Help with education, coding, writing, general knowledge,
ideas, and everyday questions.
Use the conversation history to answer follow-up questions.
If you do not know an answer, be honest.
"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar settings
with st.sidebar:
    st.title("⚙️ Settings")
    st.caption("Powered by Google Gemini")

    if st.button("🗑️ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Display existing conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Message Chandu-Nexora...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Send conversation history to Gemini
                
                
                # Build conversation history from previous messages
                history = []

                for msg in st.session_state.messages[:-1]:
                    role = "user" if msg["role"] == "user" else "model"

                    # Gemini expects alternating user/model messages.
                    if history and history[-1]["role"] == role:
                        history[-1]["parts"][0]["text"] += "\n" + msg["content"]
                    else:
                        history.append({
                            "role": role,
                            "parts": [{"text": msg["content"]}]
                        })

                # Gemini chat session with previous messages
                chat = client.chats.create(
                    model="gemini-3.5-flash-lite",
                    history=history,
                    config={
                        "system_instruction": SYSTEM_INSTRUCTIONS
                    }
                )

                response = chat.send_message(prompt)
                answer = response.text or "Sorry, I couldn't generate a response."

                chat = client.chats.create(
                    model="gemini-3.8-flash",
                    history=[
                        {
                            "role": item["role"],
                            "parts": item["parts"]
                        }
                        for item in history
                    ],
                    config={
                        "system_instruction": SYSTEM_INSTRUCTIONS
                    }
                )

                response = chat.send_message(prompt)
                answer = response.text or "Sorry, I couldn't generate a response."

            except Exception as e:
                answer = (
                    "Sorry, something went wrong. "
                    "Please check your Gemini API key, model availability, "
                    "and API quota.\n\n"
                    f"Error details: {e}"
                )

            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )