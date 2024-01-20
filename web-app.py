import streamlit as st
import requests


st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by local LLM")
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(key='chat'):
    st.chat_input(key='quiet', disabled=True)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message('user'):
        st.markdown(prompt)

    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        with requests.post("http://127.0.0.1:8000/model", stream=True, json=st.session_state.messages) as r:
            for chunk in r.iter_content(chunk_size=None):
                msg = chunk.decode()
                message_placeholder.markdown(msg)

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_input(disabled=False)
    st.rerun()
