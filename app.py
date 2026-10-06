import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="My Free AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 My Free AI Chatbot")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is not configured.")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
       try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    answer = response.text

except Exception as e:
    st.error(f"Gemini error: {e}")
    st.stop()

        answer = response.text
        st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
