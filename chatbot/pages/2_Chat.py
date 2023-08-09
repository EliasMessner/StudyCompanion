# https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/#4-session-state

import streamlit as st
import time
from streamlit_chat import message
from chat.chat_controller import ChatController

@st.cache_resource(show_spinner=False)
def get_chat_controller():
    # Create a database session object that points to the URL.
    return ChatController()

get_chat_controller()

st.set_page_config(page_title="Chat")

# Store chat messages
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant" and idx != 0:
            with st.expander("Sources"):
                st.write("\n\n".join(message['sources']))

#User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner(""):
            chat_controller = get_chat_controller()
            response = chat_controller.on_new_user_message(st.session_state.messages)
            st.write(response['content'])
            with st.expander("Sources"):
                st.write("\n\n".join(response['sources']))
    st.session_state.messages.append(response)
