import streamlit as st
from backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage
import uuid

# ---------------------------------------- Utility Functions ----------------------------------------
def generate_thread_id():
    return str(uuid.uuid4())

def get_config(thread_identifier):
    return {"configurable": {"thread_id": thread_identifier}}

def reset_chat():
    new_thread_id = generate_thread_id()
    st.session_state['thread_id'] = new_thread_id
    add_thread(new_thread_id)
    st.session_state['message_history'] = []

def add_thread(thread_identifier):
    if thread_identifier not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_identifier)

def load_conversation(thread_identifier):
    state = chatbot.get_state(config=get_config(thread_identifier))
    if not state or not state.values:
        return []
    return state.values.get('messages', [])

# ---------------------------------------- Session State ----------------------------------------
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])

# ---------------------------------------- Sidebar UI ----------------------------------------
st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("Conversations List")

for existing_thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(existing_thread_id), key=f"thread-{existing_thread_id}"):
        st.session_state['thread_id'] = existing_thread_id
        messages = load_conversation(existing_thread_id)

        temp_messages = []
        for message in messages:
            if isinstance(message, HumanMessage):
                temp_messages.append({"role": "user", "content": message.content})
            else:
                temp_messages.append({"role": "assistant", "content": message.content})

        st.session_state['message_history'] = temp_messages

# ---------------------------------------- Main UI ----------------------------------------

# load the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content']) 

# User input
user_input = st.chat_input("Type here...")

if user_input:

    with st.chat_message("user"):
        st.text(user_input)
    st.session_state['message_history'].append({"role": "user", "content": user_input})

    CONFIG = {
        'configurable': {
            'thread_id': st.session_state['thread_id']
        },
        'metadata': {
            'thread_id': st.session_state['thread_id']
        },
        'run_name': "chat_turn"
    }

    with st.chat_message("assistant"):
        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            ):
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content
        ai_response = st.write_stream(ai_only_stream())
    st.session_state['message_history'].append({"role": "assistant", "content": ai_response})