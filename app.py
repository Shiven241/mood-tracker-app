# -*- coding: utf-8 -*-
import streamlit as st

# --- App Title ---
st.set_page_config(page_title="My AI App", layout="wide")
st.title("🚀 My Streamlit Test App")

# --- Instructions ---
st.info("Paste your code inside the section below. Even if it's incomplete, this template makes sure the app runs.")

# --- Your Code Section ---
try:
    # 🔽 Paste your code here 🔽
    
    st.write("This is where your incomplete code will go.")
    
    # Example (remove later):
    # x = 10
    # st.write("x is:", x)
    
    # 🔼 End of your code 🔼

except Exception as e:
    st.error(f"⚠️ Your code raised an error: {e}")
