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

### RAG Architecture Overview
The Retrieval-Augmented Generation (RAG) system serves as the foundation of our project, enabling efficient and effective information retrieval and response generation. The following steps outline the key components of our methodology:

1. **Data Collection**: We begin by gathering relevant information from various sources, including the SkillsFuture website and other reputable resources, ensuring a comprehensive knowledge base.

2. **Creating Embeddings**: The collected data is processed and transformed into numerical representations known as embeddings, which uniquely represent each piece of information.

3. **Knowledge Storage**: These embeddings are stored in a vector database, enabling efficient retrieval of relevant information when needed.

4. **Query Processing**: When a user submits a question, it is transformed into a "query vector"—a numerical representation that the system can understand and use for searching.

5. **Information Retrieval**: Using the query vector, the system searches the vector database to identify the most relevant information for the given query.

6. **Context Integration**: The retrieved information is then combined with the original user query to ensure a coherent and contextually accurate response.

7. **Generating the Response**: Finally, the LLM utilizes the combined information to generate a complete and well-formed response, providing the user with accurate and helpful insights.

This structured approach ensures that users receive precise, contextually relevant answers, enhancing the overall learning experience by effectively combining data collection, efficient retrieval, and advanced AI capabilities.

""")