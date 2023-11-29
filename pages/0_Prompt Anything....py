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

defaults = {
  'model': 'models/text-bison-001',
  'temperature': 0.7,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 1024,
  'stop_sequences': [],
  'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":4},{"category":"HARM_CATEGORY_TOXICITY","threshold":4},{"category":"HARM_CATEGORY_VIOLENCE","threshold":4},{"category":"HARM_CATEGORY_SEXUAL","threshold":4},{"category":"HARM_CATEGORY_MEDICAL","threshold":4},{"category":"HARM_CATEGORY_DANGEROUS","threshold":4}],
}

@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()
cookie_manager = get_manager()

Prompt = ""

def clear_prompt():
   Prompt = ""

def chat(prompt):
    global Prompt
    Prompt += (prompt + "\n")
    response = genai.generate_text(
    **defaults,
    prompt=Prompt
    )
    return response.result

with st.sidebar:

    st.write("Please provide your Palm API Key (ignore if already provided):  ")
    API_KEY = st.text_input("Enter your Google PaLM API Key here ")
    if API_KEY:
        cookie_manager.set("api_cookie" , API_KEY)
        genai.configure(api_key=API_KEY)
    st.write("Don't have one.. Get your own [API KEY here](https://makersuite.google.com/app/apikey) (Yes.. it's FREE)")

    if st.button("Clear Chat",key="clear_chat"):
        st.session_state.messages1 = ""
        st.session_state.messages1 = [{"role": "assistant", "content": "Hello there! Ask me anything..."}]
        clear_prompt()
        
        
st.title("💬 Prompt Bot") 
        
api_key = cookie_manager.get(cookie="api_cookie")

if api_key is not None:
    API_KEY = api_key
    show_pages(
    [
        Page("Chat.py", "Chat", "💬"),
        Page("pages/1_Ask PDF.py", "Ask PDF", "📄"),
        Page("pages/2_Ask Article.py", "Ask Article", "🌐"),
        Page("pages/3_Ask Text.py", "Ask Text", "📜"),
    ]
    )
    genai.configure(api_key=API_KEY)
else:
    switch_page("Welcome")
    
# Initialize chat history
if "messages1" not in st.session_state:
    st.session_state.messages1 = [{"role": "assistant", "content": "Hello there! Ask me anything..."}]

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
            response = chat(prompt)
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
if prompt := st.chat_input("What's up?"):
    if not API_KEY:
        st.info("Please add your PaLM API key to continue.")
        st.stop()
    # Add user message to chat history
    st.session_state.messages1.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    get_response(prompt)


