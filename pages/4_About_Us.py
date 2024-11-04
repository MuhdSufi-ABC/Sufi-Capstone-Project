import streamlit as st
from helper_functions.utility import check_password 

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="🌱About Us"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About Career Guidance & Skills Development Portal🚀")

st.write("""
    🌟 ***Welcome to the Career Guidance & Skills Development Portal! Our mission is to empower individuals by providing easy access to information about upskilling opportunities and career guidance.*** 🌟
    """)


st.write("""
         Please remember that this portal is a prototype developed for educational purposes, and we encourage you to consult qualified professionals for personalized career advice.

         Read more about us below!

         Created by Sufi Abd Samat for AI Bootcamp 2024.
         
         """)

# Check if the password is correct.  
if not check_password():  
    st.stop() 

with st.expander("**🌱Project Scope Statement**"):
    st.markdown("""
    The Career Guidance & Skills Development Portal is here to help you grow in your career and improve your skills. Our mission is to make it easy for you to make use upskilling opportunities, and receive personalized career advice so you can confidently move forward in your professional journey. 
    
    **Use Cases:**
    1. Career Guidance Workforce Singapore  
    2. Upskilling with SkillsFuture
    3. Skills Demand for the Future Economy 2023/24 insights
    """)

with st.expander("**🤖Career Guidance & Skills Development**"):
    st.markdown("""
    This platform uses knowledge from the AI Champions Bootcamp 2024 to give you personalized guidance on using SkillsFuture credits, along with career coaching tips based on your interests and goals. 🤖 The portal makes it easy to improve your skills and advance your career by providing helpful resources through a simple Streamlit interface.

    We believe that with the right guidance and resources, anyone can reach their potential and achieve their career goals. 🌟 By giving you clear information, we want to make learning new skills and advancing your career easy and engaging for everyone.
    """)

with st.expander("**💡Objectives**"):
    st.markdown("""
    Our main goal is to create a platform that helps you take control of your career growth and upskilling journey. With so many opportunities out there, it can be hard to know where to start. This portal aims to clear up confusion by giving you simple, clear information about career guidance and upskilling options so you can make informed decisions about your future. 💡

    We provide accurate recommendations that match your goals. By giving detailed advice on how to use SkillsFuture credits and offering personalized coaching tips, we help make your upskilling journey easier and less time-consuming. ⏱️
    """)

# Data Sources
with st.expander("**📚 Data Sources**"):
    st.markdown("""
    The data used in this portal comes from trusted sources, including SkillsFuture Singapore and Workforce Singapore. The information is collected to provide accurate and up-to-date recommendations for career development and upskilling. 📚
    
    - [SkillsFuture Singapore](https://www.skillsfuture.gov.sg/)
    - [Workforce Singapore (WSG)](https://www.wsg.gov.sg/)
    - [MyCareersFuture](https://content.mycareersfuture.gov.sg/)
    - [Skills Demand for the Future Economy 2023/24 report](https://www.skillsfuture.gov.sg/skillsreport)
    """)

# How to Use This App
with st.expander("**How to use this App**"):
    st.write("""
    1. Enter your prompt in the text area below.
    2. Click the 'Submit' button to send your query.
    3. The app will generate a personalized response based on your input. 
    
    It's simple, intuitive, and designed to help you make informed decisions about your career and skills journey! 😊
    """)
