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
load_dotenv('.env')

# Streamlit UI Setup
st.title("Career Guidance & Skills Development Portal🚀")
st.subheader("Receive personalized career guidance and learn how to leverage SkillsFuture for your upskilling journey.")

# Check if the password is correct.  
if not check_password():  
    st.stop()

# Add an aesthetic photo from local drive
st.image("mainportal_banner.jpg", use_column_width=True)

# Features Section with Horizontal Slider
st.subheader("🌟Use Cases of Portal🌟")

# Creating columns for feature selection
col1, col2, col3 = st.columns(3)

selected_feature = None

with col1:
    if st.button("Career Guidance Workforce Singapore"):
        selected_feature = "Career Guidance Workforce Singapore"

with col2:
    if st.button("Upskilling with Skillsfuture"):
        selected_feature = "Upskilling with Skillsfuture"

with col3:
    if st.button("Skills Demand for the Future Economy 2023/24 report"):
        selected_feature = "Skills Demand for the Future Economy 2023/24 report"

if selected_feature == "Career Guidance Workforce Singapore":
    st.markdown("""
    **Career Guidance Workforce Singapore**  
    - Our platform provides personalized career guidance based on your interests and goals, helping you find the right career path and upskilling opportunities. 🚀
    """)

elif selected_feature == "Upskilling with Skillsfuture":
    st.markdown("""
    **Upskilling with Skillsfuture**  
    - We provide tailored suggestions on the best courses and programs to help you use your SkillsFuture credits effectively and achieve your career goals. 🎓
    """)

elif selected_feature == "Skills Demand for the Future Economy 2023/24 report":
    st.markdown("""
    **Skills Demand for the Future Economy 2023/24 report**  
    - We provide an interactive way to explore and understand key insights from the Skills Demand for the Future Economy 2023/24 report.
    """)

# SkillsFuture or Workforce Singapore Career Guidance-Related Question
st.write("""
         Click on the tabs to discover how this portal can help you chart your career path, offering personalized guidance, showing you 
         how to make the most of SkillsFuture for your upskilling journey and insights about skills demand for the future economy. 

         If you're ready to explore further, simply select the pages on the left."""
         )

# Disclaimer
with st.expander("❗IMPORTANT NOTICE: Disclaimer"):
    st.write("""
    IMPORTANT NOTICE: This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

    Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

    Always consult with qualified professionals for accurate and personalized advice.
    """)