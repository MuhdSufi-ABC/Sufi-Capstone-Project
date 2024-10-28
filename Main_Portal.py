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
    if st.button("General Career Guidance & Upskilling"):
        selected_feature = "General Career Guidance & Upskilling"

with col2:
    if st.button("SkillsFuture Upskilling Guidance"):
        selected_feature = "SkillsFuture Upskilling Guidance"

with col3:
    if st.button("Workforce Singapore Career Guidance"):
        selected_feature = "Workforce Singapore Career Guidance"

if selected_feature == "General Career Guidance & Upskilling":
    st.markdown("""
    **General Career Guidance & Upskilling**  
    - Our platform provides personalized career guidance based on your interests and goals, helping you find the right career path and upskilling opportunities. 🚀
    """)

elif selected_feature == "SkillsFuture Upskilling Guidance":
    st.markdown("""
    **SkillsFuture Upskilling Guidance**  
    - We provide tailored suggestions on the best courses and programs to help you use your SkillsFuture credits effectively and achieve your career goals. 🎓
    """)

elif selected_feature == "Workforce Singapore Career Guidance":
    st.markdown("""
    **Workforce Singapore Career Guidance**  
    - Get specific advice related to Workforce Singapore programs, helping you explore available resources for career development. 📊
    """)

# SkillsFuture or Workforce Singapore Career Guidance-Related Question
st.write("""
         Click on the tabs to discover how this portal can help you chart your career path, offering personalized guidance and showing you 
         how to make the most of SkillsFuture for your upskilling journey. 

         If you're ready to explore further, simply select the pages on the left."""
         )

# Disclaimer
with st.expander("❗IMPORTANT NOTICE: Disclaimer"):
    st.write("""
    IMPORTANT NOTICE: This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

    Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

    Always consult with qualified professionals for accurate and personalized advice.
    """)