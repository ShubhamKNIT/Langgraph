import streamlit as st
from backend import chatbot, CONFIG
from langchain_core.messages import HumanMessage

# ---------------------------------------- Session State ----------------------------------------
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

message_history = st.session_state['message_history']


# ---------------------------------------- Sidebar UI ----------------------------------------
st.sidebar.title("LangGraph Chatbot")
st.sidebar.button("New Chat")
st.sidebar.header("Conversations List")

# ---------------------------------------- Main UI ----------------------------------------

# load the conversation history
for message in message_history:
    with st.chat_message(message['role']):
        st.text(message['content']) 

# User input
user_input = st.chat_input("Type here...")

if user_input:

    with st.chat_message("user"):
        st.text(user_input)
    message_history.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        ai_response = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {
                    'messages': [HumanMessage(content=user_input)]
                },
                config=CONFIG,
                stream_mode='messages'
            )
        )
    message_history.append({"role": "assistant", "content": ai_response})