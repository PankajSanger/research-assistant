import streamlit as st
from app import chatbot

st.title('Test')

user_message = st.text_input("Ask Anything")

CONFIG = {'configurable':{'thread_id':'1'}}

if st.button('Enter'):
    response = chatbot.invoke({'messages':user_message},config=CONFIG)
    st.text(response['messages'].content)