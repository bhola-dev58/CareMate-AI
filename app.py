import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import CTransformers
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from huggingface_hub import login

# Authenticate with Hugging Face
login(token="HUGGINGFACEHUB_API_TOKEN")

# Load the PDF files from the path
def load_documents():
    try:
        loader = DirectoryLoader("data/", glob="*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        return documents
    except Exception as e:
        st.error(f"Error loading documents: {e}")
        return None

# Split text into chunks
def split_text(documents):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        text_chunks = text_splitter.split_documents(documents)
        return text_chunks
    except Exception as e:
        st.error(f"Error splitting text: {e}")
        return None

# Create embeddings
def create_embeddings():
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}
        )
        return embeddings
    except Exception as e:
        st.error(f"Error creating embeddings: {e}")
        return None

# Create vector store
def create_vector_store(text_chunks, embeddings):
    try:
        vector_store = FAISS.from_documents(text_chunks, embeddings)
        return vector_store
    except Exception as e:
        st.error(f"Error creating vector store: {e}")
        return None

# Create LLM
def create_llm():
    try:
        llm = CTransformers(
            model="llama-2-7b-chat.ggmlv3.q4_0.bin",
            model_type="llama",
            config={"max_new_tokens": 128, "temperature": 0.01}
        )
        return llm
    except Exception as e:
        st.error(f"Error creating LLM: {e}")
        return None

# Initialize session state
def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state["history"] = []

    if "generated" not in st.session_state:
        st.session_state["generated"] = ["Hello! Ask me anything about healthcare 🤗"]

    if "past" not in st.session_state:
        st.session_state["past"] = ["Hey! 👋"]

# Main chatbot function
def conversation_chat(query):
    if is_healthcare_related(query):
        try:
            result = chain({"question": query, "chat_history": st.session_state["history"]})
            st.session_state["history"].append((query, result["answer"]))
            return result["answer"]
        except Exception as e:
            return f"Error generating response: {e}"
    else:
        return "⚠️ Warning: This query is not related to healthcare. Please ask healthcare-related questions."

# Check if the query is healthcare-related
def is_healthcare_related(query):
    query = query.lower()
    healthcare_keywords = [
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
    for keyword in healthcare_keywords:
        if keyword in query:
            return True
    return False

# Display chat history
def display_chat_history():
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key="my_form", clear_on_submit=True):
            user_input = st.text_input(
                "Question:", placeholder="Ask anything about healthcare", key="input"
            )
            submit_button = st.form_submit_button(label="Send")

        if submit_button and user_input:
            output = conversation_chat(user_input)
            st.session_state["past"].append(user_input)
            st.session_state["generated"].append(output)

    if st.session_state["generated"]:
        with reply_container:
            for i in range(len(st.session_state["generated"])):
                message(
                    st.session_state["past"][i],
                    is_user=True,
                    key=str(i) + "_user",
                    avatar_style="thumbs",
                )
                message(
                    st.session_state["generated"][i],
                    key=str(i),
                    avatar_style="fun-emoji",
                )

# Sidebar Section
def sidebar():
    with st.sidebar:
        st.title("User Profile")
        st.image(
            "https://png.pngtree.com/png-clipart/20200224/original/pngtree-avatar-icon-profile-icon-member-login-vector-isolated-png-image_5247852.jpg",
            caption="Profile Picture",
            width=150,
        )
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username and password:
                st.success(f"Logged in as {username}")
            else:
                st.error("Please enter username and password")
        st.header("About")
        st.write("This is a healthcare chatbot designed to provide information and support for healthcare-related queries.")
        st.write("Feel free to ask questions about mental health, physical health, diseases, treatments, and more.")

# Main function
def main():
    st.title("HealthCare ChatBot 🧑🏽‍⚕️")
    sidebar()

    # Load documents and initialize components
    documents = load_documents()
    if documents:
        text_chunks = split_text(documents)
        embeddings = create_embeddings()
        if embeddings:
            vector_store = create_vector_store(text_chunks, embeddings)
            if vector_store:
                llm = create_llm()
                if llm:
                    global chain
                    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
                    chain = ConversationalRetrievalChain.from_llm(
                        llm=llm,
                        chain_type="stuff",
                        retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
                        memory=memory,
                    )
                    initialize_session_state()
                    display_chat_history()

# Run the app
if __name__ == "__main__":
    main()
