# https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/#4-session-state
import time
import streamlit as st
from streamlit_chat import message
from chat.chat_controller import ChatController
from chat.prompt_strategy import PromptStrategyA
from chat.feedback_controller import FeedbackController

st.set_page_config(page_title="Chat")

# set prompt strategy to strategy A
prompt_strategy = PromptStrategyA()


@st.cache_resource(show_spinner=True)
def get_chat_controller():
    # Create a database session object that points to the URL.
    return ChatController(prompt_strategy)


get_chat_controller()

# load feedback elements
feedback_controller = FeedbackController(prompt_strategy)

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

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        with st.spinner(""):
            chat_controller = get_chat_controller()
            assistant_response = chat_controller.on_new_user_message(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response['content'], "sources": assistant_response['sources']})

        # Simulate stream of response content with milliseconds delay
        for chunk in assistant_response['content'].split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

        with st.expander("Sources"):
            st.write("\n\n".join(assistant_response['sources']))
        feedback_controller.load_st_component()