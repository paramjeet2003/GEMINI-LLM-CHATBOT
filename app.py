from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os
load_dotenv()

st.set_page_config(page_title="QnA Chatbot using Gemini Pro")
st.header("Gemini LLM Application")
api_key = st.sidebar.text_input("Enter the Google API Key: ", type='password')
genai.configure(api_key=api_key)

model = genai.GenerativeModel(model_name='gemini-pro')
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response
if api_key:
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    inputs = st.text_input("Input: ", key='inputs')
    submit = st.button("Ask the question")

    if submit and inputs:
        response = get_gemini_response(inputs)
        ## add userquery and response to session chat history
        st.session_state['chat_history'].append(("You", inputs))
        st.subheader("The Response is")
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))
    st.subheader("The Chat history is ")
    for role, text in st.session_state["chat_history"]:
        st.write(f"{role}:{text}")
