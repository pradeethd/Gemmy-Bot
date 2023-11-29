from bs4 import BeautifulSoup
import requests
import streamlit as st
from streamlit_extras.switch_page_button import switch_page 
from st_pages import Page, show_pages
import extra_streamlit_components as stx
import google.generativeai as palm
import textwrap
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Ask Article",
    page_icon="📄",
)

@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()
cookie_manager = get_manager()

def clear_prompt():
        prompt = ""
        answer = ""

def main(text,qn):
    palm.configure(api_key='AIzaSyCPNNbrGTmWHtiGi9-tTSaEq9z1Civ6h0c')
    models = [m for m in palm.list_models() if 'embedText' in m.supported_generation_methods]
    model = models[0]
    sample_text = ("Title: The next generation of AI for developers and Google Workspace"
    "\n"
    "Full article:\n"
    "\n"
    "PaLM API & MakerSuite: An approachable way to explore and prototype with generative AI applications")
# Create an embedding
    embedding = palm.generate_embeddings(model=model, text=sample_text)
# print(embedding)
    texts = [text]
    query = qn
    
    df = pd.DataFrame(texts)
    df.columns = ['Text']
    # print(df)

    # Get the embeddings of each text and add to an embeddings column in the dataframe
    def embed_fn(text):
      return palm.generate_embeddings(model=model, text=text)['embedding']

    df['Embeddings'] = df['Text'].apply(embed_fn)
    # print(df)

    def find_best_passage(query, dataframe):
      """
      Compute the distances between the query and each document in the dataframe
      using the dot product.
      """
      query_embedding = palm.generate_embeddings(model=model, text=query)
      dot_products = np.dot(np.stack(dataframe['Embeddings']), query_embedding['embedding'])
      idx = np.argmax(dot_products)
      return dataframe.iloc[idx]['Text'] # Return text from index with max value

    passage = find_best_passage(query, df)
    # print(passage)
        
    def make_prompt(query, relevant_passage):
      escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
      prompt = textwrap.dedent("""
      QUESTION: '{query}' \n
        ANSWER:
      """).format(query=query, relevant_passage=escaped)

      return prompt
    
    prompt = make_prompt(query, passage)
    
    text_models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]

    text_model = text_models[0]

    temperature = 0.5
    answer = palm.generate_text(prompt=prompt,
                                model=text_model,
                                candidate_count=1,
                                temperature=temperature,
                                max_output_tokens=1000)

    for i, candidate in enumerate(answer.candidates):
      answer = f"{candidate['output']}\n"
    
    return prompt,answer

def get_response(prompt):
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Placeholder for answer fetching 
        try:
            question,answer = main(result,prompt)
            assistant_response = question + "\n" + answer
        except NameError:
            assistant_response = "Please paste the article link above."
    
    try:    
        # Add a blinking cursor to simulate typing
        message_placeholder.write(assistant_response + "▌")
        message_placeholder.write(assistant_response)
        # Add assistant response to chat history
        st.session_state.qandas1.append({"role": "assistant", "content": assistant_response})
    except:
        pass

with st.sidebar:
    st.write("Please provide your Palm API Key (ignore if already provided):  ")
    API_KEY = st.text_input("Enter your Google PaLM API Key here ")
    if API_KEY:
        cookie_manager.set("api_cookie" , API_KEY)
        palm.configure(api_key=API_KEY)
    st.write("Don't have one.. Get your own [API KEY here](https://makersuite.google.com/app/apikey) (Yes.. it's FREE)")
    
    if st.button("Clear Chat",key="clear_chat"):
        st.session_state.qandas1 = ""
        st.session_state.qandas1 = [{"role": "assistant", "content": "Hello there! I am ready to answer your questions..."}]
        clear_prompt()

st.title('Ask your Article 💬')
URL=st.text_input(label='Your article link here 😀')
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
if URL:
        try:
            request=requests.get(URL)
            request=BeautifulSoup(request.text,'html.parser')
            request=request.find_all(['h1','p','li','h2'])
        except:
            st.error("Please enter a valid URL (including HTTP/HTTPS)")
            st.stop()
        
        result=[element.text for element in request]
        result=''.join(result)
        
        if "qandas1" not in st.session_state:
            st.session_state.qandas1 = [{"role": "assistant", "content": "Hi there! I am ready to answer your questions..."}]
        # Display chat messages from history on app rerun
        for message in st.session_state.qandas1:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask any question..."):
            if not API_KEY:
                st.info("Please add your PaLM API key to continue.")
                st.stop()
            # Add user message to chat history
            st.session_state.qandas1.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            get_response(prompt)
            

    

