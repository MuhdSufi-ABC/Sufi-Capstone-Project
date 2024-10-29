import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Methodology"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("Methodology")

st.write("""
This project leverages Large Language Model (LLM) techniques in combination with Retrieval-Augmented Generation (RAG) learnt during AI Bootcamp 2024 to provide accurate and efficient responses. Below, we detail the methodology employed in our approach.      
""")
# Create two columns for displaying the images side by side
col1, col2 = st.columns(2)

with col1:
    st.image("Career_Guidance_Flow.drawio.png", caption='Career Guidance Flow Diagram')

with col2:
    st.image("Skillsfuture_Flow.drawio.png", caption='Skillfuture Flow Diagram')

st.write("""
### RAG Architecture Overview
The Retrieval-Augmented Generation (RAG) system serves as the foundation of our project, enabling efficient and effective information retrieval and response generation. The following steps outline the key components of our methodology:
""")

st.write("**1. Start:** User initiates a query through the portal, which starts the process of retrieving relevant information.")

st.write("**2. Input User Query:** User enters query through the interface. This interface is designed to be user-friendly and intuitive, allowing users to express their questions or information needs clearly.")

st.write("**3. Scrape Relevant Websites:** Scrape relevant websites for information. For example, scrape data from websites like SkillsFuture and Workforce Singapore (WSG). This ensures that the most current and accurate information is collected to address the user's query.")

st.write("**4. Process Query and Data:** Process the user query along with the scraped data to understand the context and extract relevant information. This involves analyzing the query and matching it with the data gathered.")

st.write("**5. LLM Generates Response:** Generate response using LLM. The processed information is passed to the LLM to generate a comprehensive and relevant response to the user's query.")

st.write("**6. Display Response:** Display the generated response to the user in an easily understandable format. This may include formatting the response in a way that highlights key points or provides additional insights.")

st.write("**7. End:** Flow completes, ready for the next query. The system waits for the next user input to restart the process.")

st.write("""
This structured approach ensures that users receive precise, contextually relevant answers, enhancing the overall learning experience by effectively combining data collection, efficient retrieval, and advanced AI capabilities.
""")