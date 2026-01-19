"""
Simple test app to verify Streamlit works
"""

import streamlit as st

st.title("🎬 Text-to-Animation AI - Test")
st.write("If you can see this, Streamlit is working!")

if st.button("Test Button"):
    st.success("✅ Everything is working!")
    
st.sidebar.write("Sidebar test")
