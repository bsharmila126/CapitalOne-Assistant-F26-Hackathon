import streamlit as st
import requests
import json


# =========================================================
# DIFY API
# =========================================================

DIFY_API_KEY = st.secrets["DIFY_API_KEY"]


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title= "ICICI Banking Financial Advisor",
    layout= "centered",
    initial_sidebar_state= "collapsed"
)


# =========================================================
# STYLING
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #FFF9F5;
}

h1 {
    color: #9B1C31;
    font-weight: 700;
}

h2, h3 {
    color: #B22222;
}

.stButton > button {
    background-color: #F47C20;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.5rem 1rem;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover {
    background-color: #B22222;
    color: white;
    border: none;
}

[data-testid="stChatMessage"] {
    background-color: white;
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 10px;
    border-left: 4px solid #F47C20;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# TITLE
# =========================================================

st.title("ICICI Banking Financial Advisor")

st.write(
    "Get personalized financial guidance based on your financial profile."
)


# =========================================================
# SESSION STATE
# =========================================================

if "chats" not in st.session_state:
    st.session_state.chats = {
        "Chat 1": {
            "messages": [],
            "conversation_id": "",
            "question_count": 0
        }
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"


MAX_QUESTIONS = 15


# =========================================================
# CREATE NEW CHAT
# =========================================================

def new_chat():

    chat_number = 1

    while f"Chat {chat_number}" in st.session_state.chats:
        chat_number += 1

    chat_name = f"Chat {chat_number}"

    st.session_state.chats[chat_name] = {
        "messages": [],
        "conversation_id": "",
        "question_count": 0
    }

    st.session_state.current_chat = chat_name


# =========================================================
# DELETE CHAT
# =========================================================

def delete_chat():

    chat_name = st.session_state.current_chat

    if chat_name in st.session_state.chats:
        del st.session_state.chats[chat_name]

    # Always keep at least one chat available
    if not st.session_state.chats:

        st.session_state.chats["Chat 1"] = {
            "messages": [],
            "conversation_id": "",
            "question_count": 0
        }

    st.session_state.current_chat = next(
        iter(st.session_state.chats)
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("Chats")

    if st.button("➕ New Chat"):
        new_chat()
        st.rerun()

    chat_names = list(st.session_state.chats.keys())

    selected_chat = st.radio(
        "Your Chats",
        chat_names,
        index=chat_names.index(
            st.session_state.current_chat
        )
    )

    st.session_state.current_chat = selected_chat

    if st.button("🗑️ Delete Chat"):
        delete_chat()
        st.rerun()


# =========================================================
# CURRENT CHAT
# =========================================================

current_chat = st.session_state.chats[
    st.session_state.current_chat
]


# =========================================================
# DIFY REQUEST
# =========================================================

def ask_assistant(question):

    url = "https://api.dify.ai/v1/chat-messages"

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": {},
        "query": question,
        "response_mode": "streaming",
        "conversation_id": current_chat["conversation_id"],
        "user": "financial-advisor-user"
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        stream=True,
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(
            f"Dify error {response.status_code}: {response.text}"
        )

    answer = ""

    for line in response.iter_lines():

        if not line:
            continue

        decoded_line = line.decode("utf-8")

        if decoded_line.startswith("data: "):

            event = json.loads(decoded_line[6:])

            if event.get("event") == "agent_message":
                answer += event.get("answer", "")

            if event.get("conversation_id"):
                current_chat["conversation_id"] = event[
                    "conversation_id"
                ]

    return answer


# =========================================================
# HANDLE USER QUESTION
# =========================================================

def handle_question(question):

    if current_chat["question_count"] >= MAX_QUESTIONS:
        return

    # Save user's question
    current_chat["messages"].append(
        {
            "role": "user",
            "content": question
        }
    )

    # Increase question count
    current_chat["question_count"] += 1

    # Display user's question immediately
    with st.chat_message("user"):
        st.markdown(question)

    try:

        # Display spinner while waiting for Dify
        with st.spinner("Thinking..."):
            response = ask_assistant(question)

    except Exception:
        response = (
            "Sorry, something went wrong. "
            "Please try again."
        )

    # Save assistant response
    current_chat["messages"].append(
        {
            "role": "assistant",
            "content": response
        }
    )


# =========================================================
# DISPLAY CURRENT CHAT
# =========================================================

for message in current_chat["messages"]:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================================================
# QUESTION LIMIT
# =========================================================

if current_chat["question_count"] >= MAX_QUESTIONS:

    st.warning(
        "Sorry, you have reached the 15 question limit for this chat."
    )


# =========================================================
# CHAT INPUT
# =========================================================

prompt = st.chat_input(
    "Ask the chatbot a question.",
    disabled=current_chat["question_count"] >= MAX_QUESTIONS
)


if prompt:

    handle_question(prompt)

    st.rerun()