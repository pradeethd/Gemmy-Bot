import streamlit as st 
from streamlit_extras.switch_page_button import switch_page 
from st_pages import Page, show_pages
import extra_streamlit_components as stx
from pypdf import PdfReader
import google.generativeai as genai
import textwrap
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Ask Text",
    page_icon="📄",
)

@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()
cookie_manager = get_manager()

show_pages(
    [
        Page("pages/4_Welcome.py", "Welcome", "👋"),
        Page("Chat.py", "Chat", "💬"),
        Page("pages/0_Text & Code Generator.py", "Generate Texts & Codes", "📜"),
        Page("pages/1_Ask PDF.py", "Ask from PDF", "📄"),
        Page("pages/2_Ask Article.py", "Ask from Article", "🌐"),
        Page("pages/3_Ask Text.py", "Ask from Text", "📃")
    ]
)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}


model = genai.GenerativeModel(model_name="gemini-1.5-flash",generation_config=generation_config)
context = ""
examples = []
messages3 = [
]

chat = model.start_chat(
    history=[
        {"role": "model", "parts": "Hey, user! What's up?"}
    ]
)

def clear_prompt():
    context = ""
    examples = []
    messages3 = []

def prompt_text(text,qn):
    messages3.append(qn)
    response = model.generate_content([qn, text])
    return qn,response.text


def get_response(prompt):
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Placeholder for answer fetching 
        try:
            question,answer = prompt_text(text,prompt)
            assistant_response = question + "\n" + answer
        except NameError:
            assistant_response = "Please enter your text above."
    
    try:    
        # Add a blinking cursor to simulate typing
        message_placeholder.write(assistant_response + "▌")
        message_placeholder.write(assistant_response)
        # Add assistant response to chat history
        st.session_state.messages3.append({"role": "assistant", "content": assistant_response})
    except:
        pass
    
with st.sidebar:
    st.write("Please provide your genai API Key (ignore if already provided):  ")
    API_KEY = st.text_input("Enter your Google genai API Key here ")
    if API_KEY:
        st.session_state.api_key = API_KEY
        genai.configure(api_key=API_KEY)
    st.write("Don't have one.. Get your own [API KEY here](https://aistudio.google.com/app/apikey) (Yes.. it's FREE)")
    
    if st.button("Clear Chat",key="clear_chat"):
        st.session_state.messages3 = ""
        st.session_state.messages3 = [{"role": "assistant", "content": "Hello there! I am ready to answer your questions..."}]
        clear_prompt()
    

st.title("Chat with any Text:") 
text = st.text_area(label="Enter your text here: (max: 1000 words)", max_chars=10000, height = 250, placeholder="Write and ask your questions...")

if "api_key" not in st.session_state:
    switch_page("Welcome")

if "api_key" in st.session_state:
    API_KEY = st.session_state.api_key
    genai.configure(api_key=API_KEY)
    show_pages(
    [
        Page("Chat.py", "Chat", "💬"),
        Page("pages/0_Text & Code Generator.py", "Generate Texts & Codes", "📜"),
        Page("pages/1_Ask PDF.py", "Ask from PDF", "📄"),
        Page("pages/2_Ask Article.py", "Ask from Article", "🌐"),
        Page("pages/3_Ask Text.py", "Ask from Text", "📃")
    ]
)


if text:
    if "messages3" not in st.session_state:
        st.session_state.messages3 = [{"role": "assistant", "content": "Hi there! I am ready to answer your questions..."}]
    # Display chat messages3 from history on app rerun
    for message in st.session_state.messages3:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask any question..."):
        if not API_KEY:
            st.info("Please add your genai API key to continue.")
            st.stop()
        # Add user message to chat history
        st.session_state.messages3.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        get_response(prompt)
