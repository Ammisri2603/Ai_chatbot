
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load local environment variables
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
    st.error(
        "GEMINI_API_KEY is not configured. "
        "Please add it to your local .env file "
        "or Streamlit Cloud Secrets."
    )
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

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Message Chandu-Nexora...")

if prompt:
    # Display user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Build history from previous messages only
                history = []

                for msg in st.session_state.messages[:-1]:
                    role = (
                        "user"
                        if msg["role"] == "user"
                        else "model"
                    )

                    # Merge consecutive messages with the same role
                    if history and history[-1]["role"] == role:
                        history[-1]["parts"][0]["text"] += (
                            "\n" + msg["content"]
                        )
                    else:
                        history.append({
                            "role": role,
                            "parts": [
                                {"text": msg["content"]}
                            ]
                        })

                # Create one Gemini chat session
                chat = client.chats.create(
                    model="gemini-3.5-flash-lite",
                    history=history,
                    config={
                        "system_instruction": SYSTEM_INSTRUCTIONS
                    }
                )

                # Send the current question ONCE
                response = chat.send_message(prompt)

                answer = (
                    response.text
                    or "Sorry, I couldn't generate a response."
                )

            except Exception as e:
                error_text = str(e)

                if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                    answer = (
                        "⚠️ Gemini free quota is exhausted.\n\n"
                        "Please wait until your quota resets, then try again. "
                        "Changing the model does not guarantee another free quota."
                    )
                else:
                    answer = (
                        "Sorry, something went wrong. "
                        "Please check your API key, model availability, "
                        "and internet connection.\n\n"
                        f"Error details: {error_text}"
                    )

            st.markdown(answer)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )