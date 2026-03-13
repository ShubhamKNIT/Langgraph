import streamlit as st
from backend import chatbot, CONFIG
from langchain_core.messages import HumanMessage

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

message_history = st.session_state['message_history']


user_input = st.chat_input("Type here...")

if user_input:

    # first add message to the message history
    # then display the UI

    message_history.append({"role": "user", "content": user_input})

    response = chatbot.invoke({
        "messages": [HumanMessage(content=user_input)]
    }, config=CONFIG)

    ai_response = response['messages'][-1].content

    message_history.append({"role": "assistant", "content": ai_response})

# loading conversation history
for message in message_history:
    with st.chat_message(message['role']):
        st.text(message['content'])