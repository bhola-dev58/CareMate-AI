import streamlit as st
from streamlit_chat import message
import google.generativeai as genai
import re
import os
from dotenv import load_dotenv


# Loading the gemini API key in the this code
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


# Configure Gemini API
if not api_key:
    st.error("API key not found. Please check your .env file.")
genai.configure(api_key=api_key) 
model = genai.GenerativeModel(model_name="gemini-1.5-flash")#gemini-2.5-pro


# Health-related keywords
HEALTH_KEYWORDS = [
    "health", "medicine", "mental", "therapy", "disease", "covid", "pain", "cancer",
    "fever", "flu", "injury", "illness", "diet", "exercise", "anxiety", "depression",
    "nutrition", "blood", "doctor", "treatment", "symptoms", "cure", "remedy",
    "vaccine", "infection", "cholesterol", "diabetes", "asthma", "wellness", "stress"
]


def is_health_related(text):
    return any(keyword in text.lower() for keyword in HEALTH_KEYWORDS)

# Format response text
def format_response(text):
    text = re.sub(r"(?<=\n)- ", "\n• ", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"🔹 **\1**", text)
    return text.strip()

# Get structured response from Gemini
def get_gemini_response(prompt, history):
    if not history:
        chat = model.start_chat(history=[])
        system_message = (
            "You are a professional healthcare assistant AI. "
            "Provide well-structured, clear, and helpful responses only for health-related questions. "
            "Structure the answer using bullet points, headings, or numbered lists if necessary."
        )
        chat.send_message(system_message)
    else:
        chat = model.start_chat(history=history)

    response = chat.send_message(prompt)
    return format_response(response.text), chat.history

# Initialize session state
def initialize_session_state():
    st.session_state.setdefault('history', [])
    st.session_state.setdefault('generated', ["Hello! Ask me any health-related question 🩺"])
    st.session_state.setdefault('past', ["Hi! 👋"])

# Sidebar (Login Removed)
with st.sidebar:
    st.title("User Profile")
    st.image(
        "https://png.pngtree.com/png-clipart/20200224/original/pngtree-avatar-icon-profile-icon-member-login-vector-isolated-png-image_5247852.jpg",
        caption="Profile Picture", width=150
    )
    st.header("About")
    st.write("This chatbot is powered by Gemini 1.5 Flash and designed to answer only health-related queries in a clear, structured way.")

# App title
st.title("🩺 AI-Powered Healthcare Assistant")

# Initialize session
initialize_session_state()

# Chat Interface
reply_container = st.container()
container = st.container()

with container:
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input("Ask a health-related question...", key='input')
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        if is_health_related(user_input):
            output, updated_history = get_gemini_response(user_input, st.session_state['history'])
        else:
            output = "⚠️ I'm here to help only with health-related questions."
            updated_history = st.session_state['history']

        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['history'] = updated_history

if st.session_state['generated']:
    with reply_container:
        for i in range(len(st.session_state['generated'])):
            if i < len(st.session_state['past']):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
            message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")
