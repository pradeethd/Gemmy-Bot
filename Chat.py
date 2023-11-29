import streamlit as st
from st_pages import Page, show_pages
from streamlit_extras.switch_page_button import switch_page 
import extra_streamlit_components as stx
import google.generativeai as palm
import time
import web_scrapers

st.set_page_config(
    page_title="PaLM Bot",
    page_icon="💬",
)

defaults = {
  'model': 'models/chat-bison-001',
  'temperature': 0.25,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
}
context = ""
examples = []
messages = [
]

@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()
cookie_manager = get_manager()

def clear_prompt():
    context = ""
    examples = []
    messages = []
    
def chat(request):
      messages.append(request)
      response = palm.chat(
      **defaults,
      context=context,
      examples=examples,
      messages=messages
      )
      return response.last # Response of the AI to your most recent request

with st.sidebar:
    st.write("Please provide your Palm API Key (ignore if already provided): ")
    API_KEY = st.text_input("Enter your Google PaLM API Key here ")
    if API_KEY:
        cookie_manager.set("api_cookie" , API_KEY)
        palm.configure(api_key=API_KEY)
    st.write("Don't have one.. Get your own [API KEY here](https://makersuite.google.com/app/apikey) (Yes.. it's FREE)")

    if st.button("Clear Chat",key="clear_chat"):
        st.session_state.messages = ""
        st.session_state.messages = [{"role": "assistant", "content": "Hello there! I am a simple chatbot. How can I assist you today?"}]
        clear_prompt()

st.title("💬 PaLM Bot")

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
    palm.configure(api_key=API_KEY)
else:
    switch_page("Welcome")
        
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello there! I am a simple chatbot. How can I assist you today?"}]


# Display chat messages from history on app rerun
for message in st.session_state.messages:
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
        for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    except:
        pass
        
# Accept user input
if prompt := st.chat_input("What's up?"):
    if not API_KEY:
        st.info("Please add your PaLM API key to continue.")
        st.stop()
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    get_response(prompt)

