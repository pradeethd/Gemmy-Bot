import streamlit as st
from streamlit_extras.switch_page_button import switch_page 
import extra_streamlit_components as stx
from st_pages import Page, show_pages
st.set_page_config(
    page_title="Gemmy Bot | Welcome",
    page_icon="💬",
)

@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()
cookie_manager = get_manager()

show_pages(
    [   Page("pages/4_Welcome.py", "Welcome", "👋"),
        Page("Chat.py", "Chat", "💬"),
        Page("pages/0_Text & Code Generator.py", "Generate Texts & Codes", "📜"),
        Page("pages/1_Ask PDF.py", "Ask from PDF", "📄"),
        Page("pages/2_Ask Article.py", "Ask from Article", "🌐"),
        Page("pages/3_Ask Text.py", "Ask from Text", "📃")
    ])

st.title("Welcome to Gemmy Bot 💬")
st.write("Gemmy Bot is a conversational AI app that utilizes Google's Gemini LLMs, to engage in comprehensive and informative interactions with users. It goes beyond simple text generation by enabling users to upload and interact with various forms of content, such as PDFs, articles, and text passages.")
st.write("So what are you waiting for? Try it out for yourself!")
st.write("Before trying, please provide your Gemini API Key below to continue..")
API_KEY = st.text_input("Enter your Google Gemini API Key here ")
st.write("Don't have one? Don't worry, click the below button to try instantly")
try_now = st.button("Try Now",key="try_now")
if try_now:
    API_KEY = "AIzaSyApN-j-ROLb7ZhCYlyh5D_R3ltXN0rMI2A"
st.write("Been here already?.. You can get your own [API KEY here](https://aistudio.google.com/app/apikey) (Yes.. it's FREE)")
if API_KEY:
    st.session_state.api_key = API_KEY
    switch_page("Chat")
        
