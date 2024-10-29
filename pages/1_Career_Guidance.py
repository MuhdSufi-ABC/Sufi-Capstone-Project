import os
import json
import requests
import openai
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI
import re
from helper_functions.utility import check_password 

# Load environment variables (OpenAI API key)
if load_dotenv('.env'):
   # for local development
   OPENAI_KEY = os.getenv('OPENAI_API_KEY')
else:
   OPENAI_KEY = st.secrets['OPENAI_API_KEY']

# Pass the API Key to the OpenAI Client
client = OpenAI(api_key=OPENAI_KEY)
# Some other code here are omitted for brevity

def get_embedding(input, model='text-embedding-3-small'):
    response = client.embeddings.create(
        input=input,
        model=model
    )
    return [x.embedding for x in response.data]

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="🌱General Career Guidance & Upskilling"
)
# endregion <--------- Streamlit App Configuration --------->

# General Career Guidance & Upskilling Questions
st.header("Career Guidance Questions 📈")
st.write(
        "Wondering how to navigate the ever-changing job market? Or maybe you're trying to find the career path that fits you best? We've got you covered!"
        )

# Check if the password is correct.  
if not check_password():  
    st.stop()

# Examples of questions
st.subheader("Example Questions:")
st.markdown(
        "- **What are the best ways to upskill in a changing job market?**\n"
        "- **How to stay relevant in the AI Age?**"
            )

# Step 1: Scrape General Data
def scrape_general_data():
    urls = [
        "https://content.mycareersfuture.gov.sg/stressed-interview-outfits-guide/",
        "https://content.mycareersfuture.gov.sg/25-soft-skills-make-your-resume-stand-out/",
        "https://content.mycareersfuture.gov.sg/fresh-grad-no-experience-how-get-first-job/",
        "https://content.mycareersfuture.gov.sg/mid-career-plateau-30s-check-career-health/",
        "https://content.mycareersfuture.gov.sg/career-guidance-middle-aged-singapore-polaris-wsg/",
        "https://content.mycareersfuture.gov.sg/futureproof-your-career-in-the-age-of-ai-6-expert-career-specialist/",
        "https://content.mycareersfuture.gov.sg/jobs-skills-consider-second-half-career-mature-worker/",
        "https://content.mycareersfuture.gov.sg/career-resilience-skills-mindsets-relevance-industries/",
        "https://www.myskillsfuture.gov.sg/content/portal/en/career-resources/career-resources/education-career-personal-development/skillsfuture-advice.html"
    ]

    scraped_info = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract relevant information: paragraphs, headings, lists, etc.
            paragraphs = [p.get_text().strip() for p in soup.find_all('p')]
            headings = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
            lists = [li.get_text().strip() for li in soup.find_all('li')]

            # Combine all extracted information
            page_data = {
                'url': url,
                'headings': headings,
                'paragraphs': paragraphs,
                'lists': lists
            }
            scraped_info.append(page_data)

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch data from {url}: {e}")

    return scraped_info

# Step 2: Identify Relevant Information Based on User Query
def identify_relevant_information(user_message, scraped_data):
    delimiter = "####"

    # Consolidate all scraped information into a single string for easier LLM processing.
    content = ""
    for page in scraped_data:
        content += f"Headings: {page['headings']}\n"
        content += f"Paragraphs: {page['paragraphs']}\n"
        content += f"Lists: {page['lists']}\n"

    system_message = f"""
    You will be provided with a user query related to career guidance. \
    The user query will be enclosed in the pair of {delimiter}. \
    
    You have the following information available that was scraped from official sources:
    {content}

    Decide which part of the information is most relevant to answer the user's query. \
    The output should include relevant headings, paragraphs, or list items that are relevant to the user's query. \
    
    If no relevant information is found, output an empty JSON array: [].

    Ensure your response is **only** a valid JSON array containing the most relevant points, without any additional text or comments.
    """

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{delimiter}{user_message}{delimiter}"},
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=2048,
        temperature=0.7
    )

    relevant_information_response_str = response.choices[0].message.content
        
    # Attempt to extract valid JSON using regex
    json_match = re.search(r'(\[.*\])', relevant_information_response_str, re.DOTALL)
    if json_match:
        relevant_information_response_str = json_match.group(1)
    else:
        st.error("Failed to find JSON in the response from the LLM. Please try again.")
        return []

    # Try parsing the JSON
    try:
        relevant_information = json.loads(relevant_information_response_str)
    except json.JSONDecodeError:
        st.error("Failed to parse the response from the LLM. Please try again.")
        relevant_information = []

    return relevant_information

# Step 3: Generate a Detailed Response
def generate_response_based_on_scraped_info(user_message, relevant_info):
    delimiter = "####"

    system_message = f"""
    Follow these steps to answer user queries related to career guidance.
    The user query will be delimited with a pair of {delimiter}.

    Step 1:{delimiter} If the user is asking about career guidance, \
    understand the relevant information from the list below.
    Available details are shown in the JSON data below:
    {relevant_info}

    Step 2:{delimiter} Use the information to generate an answer to the user query.
    Your response should be detailed, comprehensive, and help the user understand the career guidance for them.

    Step 3:{delimiter} Answer the user in a friendly and informative tone.
    Make sure the statements are factually accurate. The response should be complete with helpful information \
    that assists the user in thier carrer journey.

    Use the following format:
    Step 1:{delimiter} <step 1 reasoning>
    Step 2:{delimiter} <step 2 reasoning>
    Step 3:{delimiter} <step 3 response to user>

    Make sure to include {delimiter} to separate every step.
    """

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{delimiter}{user_message}{delimiter}"},
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=2048,
        temperature=0.7
    )

    response_to_user = response.choices[0].message.content
    response_to_user = response_to_user.split(delimiter)[-1]
    return response_to_user

# Step 4: Main Query Handling
scraped_data = scrape_general_data()  # Move scraped_data outside the if block to make it accessible globally

user_query = st.text_area("Enter your question:", placeholder="E.g., 'What are the best ways to upskill in a changing job market??'", height=150)
submit_button = st.button("Submit")

if user_query and submit_button:
    # Create a placeholder for status updates
    status_placeholder = st.empty()
    status_placeholder.text("Searching for relevant information...")

    # Fetch the relevant information
    relevant_info = identify_relevant_information(user_query, scraped_data)

    if relevant_info:
        # Generate a short response to use as the subheader
        subheader_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    'role': 'user', 'content': f"""Provide a brief subheader to the following query: '{user_query}'
                    
                    This response should be suitable as a subheader, limited to 1-2 sentences, 
                    to ensure a clear and engaging subheader. No need for quote."""
                    }
            ],
            max_tokens=1024,
            temperature=0.7
        )
        subheader_text = subheader_response.choices[0].message.content.strip()
        
        reply = generate_response_based_on_scraped_info(user_query, relevant_info)
        st.subheader(subheader_text)
        st.write(reply)

        # Remove the "Searching for relevant information..." message
        status_placeholder.empty()
    else:
        st.write(f"No relevant information found for your query.")

# Disclaimer
with st.expander("❗IMPORTANT NOTICE: Disclaimer"):
    st.write("""
    IMPORTANT NOTICE: This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

    Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

    Always consult with qualified professionals for accurate and personalized advice.
    """)
