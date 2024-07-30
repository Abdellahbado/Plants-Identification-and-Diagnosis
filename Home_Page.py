import streamlit as st


st.set_page_config(page_title="Plant Health Assistant", layout="wide", page_icon="🌿")

st.title("Welcome to Plant Health Assistant")

st.write("This app helps you identify plants and diagnose plant diseases.")

col1, col2 = st.columns([1,1])

with col1:
    st.header("Plant Identification")
    st.write("Upload an image to identify your plant.")
    if st.button("Go to Plant Identification"):
        st.switch_page("pages/Plant_Identification.py",)

with col2:
    st.header("Plant Disease Diagnosis")
    st.write("Upload an image to diagnose plant diseases.")
    if st.button("Go to Plant Disease Diagnosis"):
        st.switch_page("pages/Plant_Diagnosis.py")

st.markdown("---")
st.write("© 2024 Plant Health Assistant. All rights reserved.")

