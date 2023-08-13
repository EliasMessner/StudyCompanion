# https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/#4-session-state
import time
import streamlit as st
from streamlit_chat import message
from chat.chat_controller import ChatController
from chat.feedback_controller import FeedbackController

st.set_page_config(page_title="Chat")


@st.cache_resource(show_spinner=True)
def get_chat_controller():
    # Create a database session object that points to the URL.
    return ChatController()


get_chat_controller()

# let user select chat options
if strategy_option := st.selectbox('Prompt Strategy', ('RetrievalQA', 'SummarizedConversationRetrievalQA', 'StandaloneQuestionConversationalRetrievalQA')):
    get_chat_controller().set_prompt_strategy(strategy_option)

if language_option := st.selectbox('Language', ('English', 'German')):
    get_chat_controller().set_language(language_option)

# load feedback elements
feedback_controller = FeedbackController(get_chat_controller().prompt_strategy)

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
            # show thumbs up/down feedback
            user_question = st.session_state.messages[idx-1]['content']
            scores = message['scores']
            feedback_controller.load_st_component(
                key=idx, prompt_question=user_question, prompt_answer=message["content"], scores=scores)

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
            assistant_response = get_chat_controller(
            ).on_new_user_message(st.session_state.messages)
            st.session_state.messages.append(assistant_response)

        # Simulate stream of response content with milliseconds delay
        for chunk in assistant_response['content'].split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

        with st.expander("Sources"):
            st.write("\n\n".join(assistant_response['sources']))

         # show thumbs up/down feedback
        user_question = st.session_state.messages[-1]['content']
        scores = st.session_state.messages[-1]['scores']
        feedback_controller.load_st_component(key=str(len(
            st.session_state.messages)-1), prompt_question=user_question, prompt_answer=assistant_response['content'], scores=scores)
