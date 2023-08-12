import streamlit as st
from pipeline.pipeline_controller import PipelineController
import tempfile
import os
import time

st.set_page_config(page_title="Upload Slides")


st.subheader('Upload your PDF Files')

@st.cache_resource(show_spinner=True)
def get_pipeline_controller():
    # Create a database session object that points to the URL.
    return PipelineController()


get_pipeline_controller()

uploaded_files = st.file_uploader(
    label="empty-label", type="PDF", accept_multiple_files=True, label_visibility='hidden')
for uploaded_file in uploaded_files:
    file_name = uploaded_file.name
    print(file_name)
    bytes_data = uploaded_file.read()

    with tempfile.TemporaryDirectory() as temp_dir:
        path = os.path.join(temp_dir, file_name)
        file = open(path, 'w+b')
        file.write(bytes_data)
        pipeline_controller = get_pipeline_controller()
        start_time = time.time()
        with st.spinner(text="Ingesting file"):
            pipeline_controller.ingest_pdf(path)
        print("Ingestion time: ", time.time() - start_time, "seconds")

        success = st.success("Successfully ingested files! You can now chat with the bot.")