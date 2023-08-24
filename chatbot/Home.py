import streamlit as st

st.markdown("<h1 style='text-align: center;'>StudyCompanion</h1>", unsafe_allow_html=True)
st.divider()

st.subheader('Instructions')

st.markdown("1. Upload your PDF files [here](/Upload_Slides).")

st.markdown("2. Ask the Chatbot about your slides [here](/Chat). Choose your Prompt Strategy and Language.")

st.subheader("Prompt Strategies")

st.markdown("""
* **RetrievalQA** Simple semantic document retrieval. Context will be chosen from vector store based on your input. No context-sensitivity.
* **SummarizedConversationRetrievalQA** Advanced semantic document retrieval with chat context. For every input, a new question is generated and relevant elements of the previous conversation are included in the context. High context-sensitivity.
* **StandaloneQuestionConversationalRetrievalQA** Advanced semantic document retrieval with chat context. For every input, a new question is generated that captures context of the previous conversation and is used to retrieve relevant documents. Medium context-sensitivity. 
""")