import os
import requests
import openai
import streamlit as st
import pdfplumber
from io import BytesIO
from dotenv import load_dotenv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from helper_functions.utility import check_password 

# Load environment variables (OpenAI API key)
load_dotenv('.env')
# Load environment variables (OpenAI API key)
if load_dotenv('.env'):
   # for local development
   OPENAI_KEY = os.getenv('OPENAI_API_KEY')
else:
   OPENAI_KEY = st.secrets['OPENAI_API_KEY']

# Pass the API Key to the OpenAI Client
client = openai.OpenAI(api_key=OPENAI_KEY)
# Some other code here are omitted for brevity

# Streamlit UI Setup
st.set_page_config(page_title="Skills Demand for the Future Economy 2023/24 report", layout="centered")
st.title("📊 Skills Demand for the Future Economy 2023/24 report")
st.subheader("Dive into the Skills Demand for the Future Economy 2023/24 report and discover key trends, industry shifts, and the skills you need to stay ahead!")
st.write("Whether you're planning to boost your current career or pivot to a new opportunity, this tool will help you find actionable insights in a fun and engaging way! 🔍✨")

# Check if the password is correct.  
if not check_password():  
    st.stop() 

# Example questions section
st.markdown("### Find Out More About the Report:")
st.write("- What are the key findings of the report?")
st.write("- What are the emerging industry trends?")
st.write("- What skills should I develop to pivot to growth sectors?")         

# Step 1: Download PDF Data
pdf_url = "https://www.skillsfuture.gov.sg/docs/default-source/skills-report-2023/sdfe-2023.pdf"

def download_pdf(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to download PDF: {e}")
        return None

# Step 2: Extract Text from PDF

def extract_text_from_pdf(pdf_file):
    try:
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + ""
        return text
    except Exception as e:
        st.error(f"Failed to extract text from PDF: {e}")
        return ""

# Helper function to split text into manageable chunks
def chunk_text(text, max_tokens=2000):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(" ".join(current_chunk)) > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# Step 3: Process Query and Generate Response using LLM with concurrency
def generate_response(user_message, extracted_text):
    # Chunk the extracted text
    text_chunks = chunk_text(extracted_text, max_tokens=2000)
    
    # Limit to processing top N chunks (e.g., top 2 chunks)
    top_chunks = text_chunks[:2]

    responses = []

    # Use ThreadPoolExecutor for concurrent processing of text chunks
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_to_chunk = {
            executor.submit(process_chunk, chunk, user_message): chunk
            for chunk in top_chunks 
        }
        for future in as_completed(future_to_chunk):
            try:
                response_content = future.result()
                responses.append(response_content)
            except Exception as e:
                print(f"Exception occurred: {e}")

    # Combine responses from each chunk
    full_response = "\n".join(responses)

    # Step 4: Generate Summary of Response
    summary_prompt = f"""
    Based on the detailed response below, provide a concise summary to guide the reader in making informed choices 
    about upskilling to either stay relevant at their current workplace or to pivot to job opportunities with growth potential. 
    
    Must remind users in that response is based on information from the Skills Demand for the Future Economy 2023/24 report. 
    Important to inform users for detailed information, refer to https://www.skillsfuture.gov.sg/docs/default-source/skills-report-2023/sdfe-2023.pdf.
    
    Detailed Response:
    {full_response}
    
    Please focus the summary on key insights for individuals to make informed decisions on jobs and skills matters.
    """
    try:
        summary_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{'role': 'system', 'content': summary_prompt}],
            max_tokens=512,
            temperature=0.7
        )
        summary = summary_response.choices[0].message.content.strip()
    except Exception as e:
        summary = "Summary generation failed."

    return full_response, summary

# Helper function to process each chunk separately
def process_chunk(chunk, user_message):
    system_message = f"""
    You are given the following context extracted from the SkillsFuture 2023 Report:
    {chunk}
    
    Based on this information, answer the following user query:
    {user_message}
    
    Please provide a comprehensive and user-friendly response.
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{chunk} {user_message}"},
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=512,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Step 5: Main Query Handling
pdf_file = download_pdf(pdf_url)
if pdf_file:
    extracted_text = extract_text_from_pdf(pdf_file)

    if extracted_text:
        user_query = st.text_input("Enter your question about the SkillsFuture 2023/2024 Report:", placeholder="E.g., 'What are the key findings of the report?'")
        submit_button = st.button("Submit")

        if user_query and submit_button:
            
            full_response, summary = generate_response(user_query, extracted_text)
            st.subheader("Guided Summary:") 
            st.write(summary)