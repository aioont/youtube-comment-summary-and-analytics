import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import TokenTextSplitter
from langchain.chains.summarize import load_summarize_chain
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access Gemini API key from Streamlit secrets
gemini_api_key = st.secrets['GEMINI_API_KEY']

def get_summary(text, gemini_api_key):
    """
    Generates a summary of the input text using Google's Gemini API.

    Args:
        text (str): The input text to be summarized.
        gemini_api_key (str): The API key for accessing Google's Gemini API.

    Returns:
        str: The summarized text.
    """
    # Tokenization
    text_splitter = TokenTextSplitter(
        chunk_size=1000, 
        chunk_overlap=10
    )
    chunks = text_splitter.create_documents([text])

    # Summarization
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=gemini_api_key
    )
    
    chain = load_summarize_chain(
        llm, 
        chain_type="map_reduce"
    )

    # Invoke Chain
    response = chain.invoke(chunks)

    return response['output_text']
