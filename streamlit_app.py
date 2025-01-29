import streamlit as st
from functions import *
import base64
import pandas as pd

# Load necessary functions and classes
def load_streamlit_page():
    """
    Load the Streamlit page with the necessary inputs and explain the tool's purpose.
    """
    st.set_page_config(layout="wide", page_title="PDF Document Vector Store and Query Tool")

    # Design page layout with two columns: interactions on the left, details on the right.
    col1, col2 = st.columns([0.5, 0.5], gap="large")

    with col1:
        st.header("OpenAI API Key and PDF Upload")
        if 'api_key' not in st.session_state:
            st.session_state.api_key = st.text_input('Enter your OpenAI API Key:', type='password')
        uploaded_file = st.file_uploader("Please upload your PDF document:", type="pdf")

    with col2:
        st.header("Instructions")
        st.write("1. Enter your OpenAI API key.")
        st.write("2. Upload the PDF document you want to query.")
        st.write("3. After uploading, input your question in the provided text box to generate the query answer.")

    return col1, col2, uploaded_file

def display_pdf(uploaded_file):
    """
    Display a PDF file in Streamlit.
    """
    bytes_data = uploaded_file.getvalue()
    base64_pdf = base64.b64encode(bytes_data).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Setup the Streamlit page
col1, col2, uploaded_file = load_streamlit_page()

if uploaded_file is not None:
    with col2:
        display_pdf(uploaded_file)
    # Load and process the documents
    documents = get_pdf_text(uploaded_file)
    st.session_state.vector_store = create_vectorstore_from_texts(documents, 
                                                                  st.session_state.api_key,
                                                                  uploaded_file.name)

    # Input for the user query
    query = st.text_input("Enter your question:")
    if st.button("Generate answer"):
        with st.spinner("Generating answer..."):
            answer_df = query_document(st.session_state.vector_store, 
                                       query, 
                                       st.session_state.api_key)
            st.write(answer_df)
