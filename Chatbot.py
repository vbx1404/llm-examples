from openai import OpenAI
import streamlit as st
from streamlit_lottie import st_lottie

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    #"[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

col1, col2 = st.columns([1, 4])
with col1:
    st_lottie("https://lottie.host/88559120-c6dc-40b2-ab08-4de3f326aa57/xWPx9if7jC.json", height=120, width=120)

with col2:
    st.title("Personify Me")

#st.caption("💖 Connect with your plant using emotive AI")

st.subheader('✨ Connect with your plant using emotive AI', divider='rainbow')
#st.subheader('_Streamlit_ is :blue[cool] :sunglasses:')

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-4", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
