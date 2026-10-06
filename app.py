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
            st.write(answer)

        except Exception as e:
            st.error(f"Gemini error: {e}")
            st.stop()

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
