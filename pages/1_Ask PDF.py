import streamlit as st 
from pypdf import PdfReader
import google.generativeai as palm
import textwrap
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Ask PDF",
    page_icon="📄",
)

def clear_prompt():
        prompt = ""
        answer = ""

def main(text,qn):
    palm.configure(api_key=API_KEY)
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

with st.sidebar:
    st.write("Please provide your Palm API Key:")
    API_KEY = st.text_input("Enter your Google PaLM API Key here ")
    if API_KEY:
        palm.configure(api_key=API_KEY)
    st.write("[Get your own API KEY here for free](https://makersuite.google.com/app/apikey)")
    
    if st.button("Clear Chat",key="clear_chat"):
        st.session_state.qandas = ""
        st.session_state.qandas = [{"role": "assistant", "content": "Hello there! Upload your PDF and ask questions..."}]
        clear_prompt()

def extract_text_from_pdf(pdf): 
    pdf_reader = PdfReader(pdf) 
    return ''.join(page.extract_text() for page in pdf_reader.pages) 

 
st.title("Chat with Your PDF") 
pdf = st.file_uploader("Upload your PDF", type="pdf") 
if pdf: 
    text = extract_text_from_pdf(pdf) 

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
            question,answer = main(text,prompt)
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
        st.info("Please add your PaLM API key to continue.")
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
            