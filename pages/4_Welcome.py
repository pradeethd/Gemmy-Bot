import streamlit as st
from streamlit_extras.switch_page_button import switch_page 
from st_pages import Page, show_pages
st.set_page_config(
    page_title="PaLM Bot | Welcome",
    page_icon="💬",
)

show_pages(
    [   Page("pages/4_Welcome.py", "Welcome", "👋"),
        Page("Chat.py", "Chat", "💬"),
        Page("pages/0_Text & Code Generator.py", "Generate Texts & Codes", "📜"),
        Page("pages/1_Ask PDF.py", "Ask from PDF", "📄"),
        Page("pages/2_Ask Article.py", "Ask from Article", "🌐"),
        Page("pages/3_Ask Text.py", "Ask from Text", "📃")
    ])

st.title("Welcome to PaLM Bot 💬")
st.write("PalmBot is a conversational AI app that utilizes Google's PaLM 2 LLMs, to engage in comprehensive and informative interactions with users. It goes beyond simple text generation by enabling users to upload and interact with various forms of content, such as PDFs, articles, and text passages.")
st.write("So what are you waiting for? Try it out for yourself!")
st.write("Before trying, please provide your PaLM API Key below to continue..")
API_KEY = st.text_input("Enter your Google PaLM API Key here ")
if API_KEY:
    st.session_state.api_key = API_KEY
    switch_page("Chat")
        
st.write("Don't have one.. Get your own [API KEY here](https://makersuite.google.com/app/apikey) (Yes.. it's FREE)")