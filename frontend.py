import streamlit as st
from test import chatbot

st.title('Test')

if ['messages'] not in st.session_state['messages']:
    st.session_state['messages'] == []

user_message = st.chat_input("Ask Anything")

CONFIG = {'configurable':{'thread_id':'1'}}

if user_message:
    
    #user
    user = st.chat_message(name="user",avatar='user')
    user.write(user_message)

    response = chatbot.invoke({'messages':user_message},config=CONFIG)

    #AI
    ai = st.chat_message(name="ai",avatar='assistant')
    ai.write(response['messages'].content)