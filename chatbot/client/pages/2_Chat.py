# https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/#4-session-state

import streamlit as st
import time
from streamlit_chat import message
from chatbot.pipeline.vectorstore_controller import VectorstoreController

@st.cache_resource(show_spinner=False)
def get_vectorstore_controller():
    # Create a database session object that points to the URL.
    return VectorstoreController()

get_vectorstore_controller()

st.set_page_config(page_title="Chat")

# Store chat messages
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

#User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner(""):
            vectorstore_controller = get_vectorstore_controller()
            response = vectorstore_controller.query_vectorstore(st.session_state.messages[-1]["content"], k=1)
            st.write(response[0].page_content)
    message = {"role": "assistant", "content": response[0].page_content}
    st.session_state.messages.append(message)
