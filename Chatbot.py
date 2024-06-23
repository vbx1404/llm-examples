from openai import OpenAI
import streamlit as st
from streamlit_lottie import st_lottie
import requests
import cv2
import av
# from streamlit_webrtc import webrtc_streamer
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
import threading
from typing import Union
import numpy as np

from PIL import Image


with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    #"[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"

col1, col2 = st.columns([1, 4])
with col1:
    st_lottie("https://lottie.host/88559120-c6dc-40b2-ab08-4de3f326aa57/xWPx9if7jC.json", height=100, width=100)

with col2:
    st.title("Pair.ai")

st.subheader('✨ Breathe life into everyday objects with emotive AI', divider='rainbow')

picture = st.camera_input("Take a picture")

if picture:
    st.image(picture)
    
    with open("tmp.jpg", "wb") as f:
        f.write(picture.getvalue())
        
    file = {'file': open('tmp.jpg', 'rb')}
    response = requests.post("https://ae6e-146-152-225-40.ngrok-free.app/upload/image/", files=file)
    
    prompt = st.text_input("enter your prompt")
    if prompt:
        data = {"name": prompt}
        response = requests.post("https://ae6e-146-152-225-40.ngrok-free.app/llava_api/prompt/", json=data)
        
        if response:
            st.chat_message("assistant").write(response.text)
    


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
