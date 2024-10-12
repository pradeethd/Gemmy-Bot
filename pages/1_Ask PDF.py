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
    page_title="Ask PDF",
    page_icon="📄",
)

@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()
cookie_manager = get_manager()

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
messages1 = [
]

chat = model.start_chat(
    history=[
        {"role": "model", "parts": "Hey, user! What's up?"}
    ]
)

def clear_prompt():
    context = ""
    examples = []
    messages = []
    
# def chat_prompt(request):
#       messages1.append(request)
#       response = chat.send_message(request)
#       return response.text 

def prompt_pdf(text,qn):
    messages1.append(qn)
    response = model.generate_content([qn, text])
    return qn,response.text

with st.sidebar:

    st.write("Please provide your Gemini API Key (ignore if already provided):  ")
    API_KEY = st.text_input("Enter your Google Gemini API Key here ")
    if API_KEY:
        cookie_manager.set("api_cookie" , API_KEY)
        genai.configure(api_key=API_KEY)
    st.write("Don't have one.. Get your own [API KEY here](https://aistudio.google.com/app/apikey) (Yes.. it's FREE)")

    if st.button("Clear Chat",key="clear_chat"):
        st.session_state.messages1 = ""
        st.session_state.messages1 = [{"role": "assistant", "content": "Hello there! Ask me anything..."}]
        clear_prompt()

def extract_text_from_pdf(pdf): 
    pdf_reader = PdfReader(pdf) 
    return ''.join(page.extract_text() for page in pdf_reader.pages) 

 
st.title("Chat with Your PDF") 
pdf = st.file_uploader("Upload your PDF", type="pdf") 
if pdf: 
    text = extract_text_from_pdf(pdf) 

if "api_key" not in st.session_state:
    switch_page("Welcome")

if "api_key" in st.session_state:
    API_KEY = st.session_state.api_key
    genai.configure(api_key=API_KEY)
    
if "qandas" not in st.session_state:
    st.session_state.qandas = [{"role": "assistant", "content": "Hi there! Upload your PDF and ask questions..."}]

# Display chat messages from history on app rerun
for message in st.session_state.qandas:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
def get_response(prompt):
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Placeholder for answer fetching 
        try:
            question,answer = prompt_pdf(text,prompt)
            assistant_response = question + "\n" + answer
        except NameError:
            assistant_response = "Please upload your PDF file above."
            
    
    try:    
        # Add a blinking cursor to simulate typing
        message_placeholder.write(assistant_response + "▌")
        message_placeholder.write(assistant_response)
        # Add assistant response to chat history
        st.session_state.qandas.append({"role": "assistant", "content": assistant_response})
    except:
        pass
            

if prompt := st.chat_input("Ask any question..."):
    if not API_KEY:
        st.info("Please add your Gemini API key to continue.")
        st.stop()
    # Add user message to chat history
    st.session_state.qandas.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    get_response(prompt)

try:
    st.download_button("Open PDF", pdf.getvalue(), "document.pdf", mime="application/pdf")
except AttributeError:
    pass 
            