import streamlit as st
from streamlit_extras.switch_page_button import switch_page 
from st_pages import Page, show_pages
import extra_streamlit_components as stx
import google.generativeai as genai
import time
import web_scrapers

st.set_page_config(
    page_title="Prompt Bot",
    page_icon="💬",
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
    
def chat_prompt(request):
      messages1.append(request)
      response = chat.send_message(request)
      return response.text 

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
        
        
st.title("💬 Prompt Bot") 
        
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

    
# Initialize chat history
if "messages1" not in st.session_state:
    st.session_state.messages1 = [{"role": "assistant", "content": "Hi there! I am Gemmy Bot. How can I assist you today?"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages1:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
def get_response(prompt):
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        if prompt.lower().startswith("google "):
            prompt = prompt.replace("google ", "")
            response = "Search: " + web_scrapers.google_search(prompt)
        elif prompt.lower().startswith("stack "):
             prompt = prompt.replace("stack ", "")
             web_scrapers.sendreq(prompt)
             response = "Stackoverflow pages are opened in new tabs."
        elif prompt.lower()=="ask pdf":
            url = "Ask_PDF"
            response = "Go here matey! [Ask PDF](%s)" % url
        elif prompt.lower()=="ask article":
            url = "Ask_Article"
            response = "Go here matey! [Ask Article](%s)" % url
        elif prompt.lower()=="ask text":
            url = "Ask_Text"
            response = "Go here matey! [Ask Text](%s)" % url
        else:
            response = chat_prompt(prompt)
        try:
            assistant_response = response
        except NameError:
            pass
    
    try:    
        # Add a blinking cursor to simulate typing
        message_placeholder.write(assistant_response + "▌")
        message_placeholder.write(assistant_response)
        # Add assistant response to chat history
        st.session_state.messages1.append({"role": "assistant", "content": assistant_response})
    except:
        pass
    
# Accept user input
if prompt := st.chat_input("What's on your mind?"):
    if not API_KEY:
        st.info("Please add your genai API key to continue.")
        st.stop()
    # Add user message to chat history
    st.session_state.messages1.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    get_response(prompt)


