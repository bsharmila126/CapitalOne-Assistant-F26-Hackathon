import streamlit as st

st.set_page_config(
    page_title = "General Financial Advisor",
    layout = "centered",
    initial_sidebar_state = "collapsed"
)

st.title("Financial Advisor")
st.write("This app gives general financial advice about....")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "question_count" not in st.session_state:
    st.session_state.question_count = 0

MAX_QUESTIONS = 15

def ask_assistant(question):
    #dify API call 
    return f"I received your question: '{question}'. This is a temporary response."

def handle_question(question):
    if st.session_state.question_count >= MAX_QUESTIONS: 
        return
    
    st.session_state.messages.append (
        {
            "role": "user",
            "content": question
        }
    )

    st.session_state.question_count += 1

    try:
        with st.spinner("Thinking..."):
            response = ask_assistant(question)
    except Exception:
        response = "Sorry, something went wrong. Please try again."
    
    st.session_state.messages.append (
        {
            "role": "assistant",
            "content": response
        }
    )

st.subheader("Quick Questions")

if st.button("Where am I spending the most?"):
    handle_question("Where am I spending the most?")
    st.rerun()

if st.button("How am I doing against my budget?"):
    handle_question("How am I doing against my budget?")
    st.rerun()

if st.button("Where can I save money?"):
    handle_question("Where can I save money?")
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.question_count >= MAX_QUESTIONS:
    st.warning("Sorry, you have reached the 15 question limit for this session.")

prompt = st.chat_input(
    "Ask the chatbot a question.",
    disabled=st.session_state.question_count >= MAX_QUESTIONS
)

if prompt:
    handle_question(prompt)
    st.rerun()

st.subheader("Overview of Finances")
st.caption("This chart displays your finances.")