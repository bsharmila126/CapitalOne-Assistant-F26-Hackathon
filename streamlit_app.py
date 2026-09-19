import streamlit as st

st.set_page_config(
    page_title = "General Financial Advisor",
    layout = "centered",
    initial_sidebar_state = "collapsed"
)

app_title = st.title("Financial Advisor")
description = st.write("This app gives general financial advice about....")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask the chatbot a question.")

def ask_assistant(question):
    #dify API call 
    return "This is a temporary response"

if prompt: 
    st.session_state.messages.append (
        {
            "role": "user",
            "content": prompt
        }
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    response = ask_assistant(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append (
        {
            "role": "assistant",
            "content": response
        }
    )