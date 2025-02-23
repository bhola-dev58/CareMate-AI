import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory

# Load the pdf files from the path
loader = DirectoryLoader('data/', glob="*.pdf", loader_cls=PyPDFLoader)
documents = loader.load()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
text_chunks = text_splitter.split_documents(documents)

# Create embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                   model_kwargs={'device': "cpu"})

# Vectorstore
vector_store = FAISS.from_documents(text_chunks, embeddings)

# Create LLM
llm = CTransformers(model="llama-2-7b-chat.ggmlv3.q4_0.bin", model_type="llama",
                    config={'max_new_tokens': 128, 'temperature': 0.01})

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff',
                                              retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
                                              memory=memory)

# Define healthcare-related keywords
HEALTHCARE_KEYWORDS = [
    "public health", "medical research", "healthcare professionals", "primary care", "preventive care",
    "chronic conditions", "acute conditions", "telemedicine", "rehabilitation centers", "palliative care",
    "mental well-being", "therapies", "counseling", "health insurance", "nutrition",
    "exercise", "emergency response", "medical technology", "AI-driven diagnostics", "robotic surgeries",
    "physical therapy", "screenings", "vaccinations", "diabetes", "hypertension",
    "terminal illnesses", "routine check-ups", "disease prevention", "patient outcomes", "financial support",
    "influenza", "fever", "cough", "fatigue", "muscle pain", "common cold", "sore throat", "runny nose",
    "asthma", "shortness of breath", "wheezing", "chest tightness", "pneumonia", "chills", "rapid breathing",
    "bronchitis", "persistent cough", "mucus production", "tuberculosis", "weight loss", "night sweats",
    "hepatitis", "jaundice", "abdominal pain", "nausea", "dengue", "rash", "joint pain", "malaria",
    "shivering", "headache", "tuberculosis", "persistent fever", "HIV/AIDS", "weakened immunity",
    "measles", "red spots", "conjunctivitis", "chickenpox", "itchy blisters", "varicella",
    "stroke", "paralysis", "speech difficulty", "Alzheimer's", "memory loss", "confusion",
    "depression", "hopelessness", "loss of interest", "anxiety", "nervousness", "panic attacks"
]

# Function to check if the query is healthcare-related
def is_healthcare_related(query):
    query = query.lower()
    for keyword in HEALTHCARE_KEYWORDS:
        if keyword in query:
            return True
    return False

# Sidebar Section
with st.sidebar:
    st.title("User Profile")
    
    # Profile Picture
    st.image("https://png.pngtree.com/png-clipart/20200224/original/pngtree-avatar-icon-profile-icon-member-login-vector-isolated-png-image_5247852.jpg", caption="Profile Picture", width=150)
    
    # Login Section
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:
            st.success(f"Logged in as {username}")
        else:
            st.error("Please enter username and password")
    
    # About Section
    st.header("About")
    st.write("This is a healthcare chatbot designed to provide information and support for healthcare-related queries.")
    st.write("Feel free to ask questions about mental health, physical health, diseases, treatments, and more.")

# Main Chatbot Section
st.title("HealthCare ChatBot 🧑🏽‍⚕️")


def conversation_chat(query):
    if is_healthcare_related(query):
        result = chain({"question": query, "chat_history": st.session_state['history']})
        st.session_state['history'].append((query, result["answer"]))
        return result["answer"]
    else:
        return "⚠️ Warning: This query is not related to healthcare. Please ask healthcare-related questions."

def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about healthcare 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey! 👋"]

def display_chat_history():
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            # Wrap the text input in a custom div with the "text_input_3" class
            st.markdown('<div class="text_input_3">', unsafe_allow_html=True)
            user_input = st.text_input("Question:", placeholder="Enter your Problem Here...", key='input')
            st.markdown('</div>', unsafe_allow_html=True)
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            output = conversation_chat(user_input)

            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
                message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")

# Initialize session state
initialize_session_state()

# Display chat history
display_chat_history()
