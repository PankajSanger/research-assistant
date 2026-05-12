import streamlit as st
from app import chatbot

st.title('Test')

user_message = st.text_input("Ask Anything")

if st.button('Enter'):
    response = chatbot.invoke({'messages':user_message})
    st.text(response['messages'].content)