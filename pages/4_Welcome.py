import streamlit as st
from streamlit_extras.switch_page_button import switch_page 
import extra_streamlit_components as stx
st.set_page_config(
    page_title="PaLM Bot | Welcome",
    page_icon="💬",
)

@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()
cookie_manager = get_manager()

st.title("Welcome to PaLM Bot 💬")
st.write("PalmBot is a conversational AI app that utilizes Google's PaLM 2 LLMs, to engage in comprehensive and informative interactions with users. It goes beyond simple text generation by enabling users to upload and interact with various forms of content, such as PDFs, articles, and text passages.")
st.write("So what are you waiting for? Try it out for yourself!")
st.write("Before trying, please provide your PaLM API Key below to continue..")
API_KEY = st.text_input("Enter your Google PaLM API Key here ")
if API_KEY:
    cookie_manager.set("api_cookie", API_KEY)

if cookie_manager.get(cookie="api_cookie"):
    switch_page("Chat")
st.write("Don't have one.. Get your own [API KEY here](https://makersuite.google.com/app/apikey) (Yes.. it's FREE)")