import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import re
import json
from dotenv import load_dotenv
import os
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


# Streamlit app
st.title("SkillsFuture Chatbot")
st.write(
        "Need help with SkillsFuture Credit? Our chatbot can answer your questions about eligibility, application, and how to use your credit for skill development and training!"
        )

# Check if the password is correct.  
if not check_password():  
    st.stop() 

# Display some common questions
st.write("### Example Questions")
common_questions = [
    "Could you provide a detailed, step-by-step guide on how to utilize my SkillsFuture credits effectively?",
    "Who is eligible for SkillsFuture credits?",
]
for question in common_questions:
    st.write(f"- {question}")

# Function to scrape content from a webpage
def scrape_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = ' '.join([p.get_text() for p in soup.find_all('p')])
        headings = ' '.join([h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])])
        lists = ' '.join([li.get_text() for li in soup.find_all('li')])
        return {'headings': headings, 'paragraphs': paragraphs, 'lists': lists}
    except requests.exceptions.RequestException as e:
        return {'error': f"Error fetching data from {url}: {e}"}

# URLs to scrape information from
urls = [
    "https://www.skillsfuture.gov.sg/initiatives/early-career/credit",
    "https://www.skillsfuture.gov.sg/initiatives/early-career/skills-framework",
    "https://www.skillsfuture.gov.sg/skills-framework/skills-frameworks-faq/",
    "https://www.myskillsfuture.gov.sg/content/portal/en/career-resources/career-resources/education-career-personal-development/SkillsFuture_Credit.html",
    "https://www.myskillsfuture.gov.sg/content/portal/en/career-resources/career-resources/how-to-guides/myskillsfuture-course-search-guide.html",
    "https://www.myskillsfuture.gov.sg/content/portal/en/career-resources/career-resources/how-to-guides/Here_is_How_SkillsFuture_Makes_Upskilling_Easier.html",
    "https://www.myskillsfuture.gov.sg/content/portal/en/career-resources/career-resources/how-to-guides/the-complete-skillsfuture-credit-guide-for-your-next-career-move.html",
    "https://www.myskillsfuture.gov.sg/content/portal/en/career-resources/career-resources/how-to-guides/enjoy-peace-of-mind-as-you-upskill.html",
    "https://www.myskillsfuture.gov.sg/content/portal/en/career-resources/career-resources/education-career-personal-development/use_SFC_for_online_subscriptions_and_courses.html",
    "https://www.skillsfuture.gov.sg/initiatives/early-career/tesa",
    "https://www.myskillsfuture.gov.sg/content/portal/en/career-resources/career-resources/education-career-personal-development/SkillsFuture_Level-Up_Programme.html",
    "https://programmes.myskillsfuture.gov.sg/WorkStudyIndividualProgrammes/Programme_Summary.aspx"
]

# Scrape all URLs and store content
scraped_data = []
for url in urls:
    scraped_data.append(scrape_content(url))

# Function to identify relevant information based on user query
def identify_relevant_information(user_message, scraped_data):
    delimiter = "####"

    # Consolidate all scraped information into a single string for easier LLM processing.
    content = ""
    for page in scraped_data:
        content += f"Headings: {page['headings']}\n"
        content += f"Paragraphs: {page['paragraphs']}\n"
        content += f"Lists: {page['lists']}\n"

    system_message = f"""
    You will be provided with a user query related to SkillsFuture, including topics such as SkillsFuture credits, eligible courses, and career guidance. \
    The user query will be enclosed in the pair of {delimiter}. \
    
    You have the following information available that was scraped from official SkillsFuture sources:
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
    Follow these steps to answer user queries related to SkillsFuture, including topics such as SkillsFuture credits, eligible courses, and career guidance.
    The user query will be delimited with a pair of {delimiter}.

    Step 1:{delimiter} If the user is asking about SkillsFuture, understand the relevant information from the list below.
    Available details are shown in the JSON data below:
    {relevant_info}

    Step 2:{delimiter} Use the information to generate an answer to the user query.
    Your response should be detailed, comprehensive, and help the user understand the options available to them.

    Step 3:{delimiter} Answer the user in a friendly and informative tone.
    Make sure the statements are factually accurate. The response should be complete with helpful information that assists the user in making decisions.

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


# User query input
user_query = st.text_area("Enter your question about SkillsFuture:", placeholder="E.g., 'Could you provide a detailed, step-by-step guide on how to utilize my SkillsFuture credits effectively?")
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
                    'role': 'user', 'content': f"""Provide a brief header to the following query: '{user_query}'
                    
                    This response should be suitable as a header to provide the first impression and 
                    help establish the purpose of the content. Limit to 1 sentence
                    to ensure a clear and engaging header. No need for quote."""
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