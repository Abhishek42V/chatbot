import streamlit as st
import random
import openai
import pyttsx3  # Importing the pyttsx3 library.ensure that espeak is installed and espeak/command-line is in system path variables

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init(driverName='sapi5') # Specify sapi5 for Windows

# Show title and description.
st.title("💬 Multilingual Chatbot with Translation")
st.write(
    "This chatbot generates and translates sentences to various languages using OpenAI's GPT model. "
    "You can also have the translations spoken out loud using Text-to-Speech (TTS). "
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    openai.api_key = openai_api_key

    # Define available languages for translation
    languages = {
        'English': 'en',
        'Hindi': 'hi',
        'French': 'fr',
        'German': 'de',
        'Spanish': 'es',
        'Sanskrit': 'sa'
    }

    # Create a session state variable to store the chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Function to generate random sentences for learning a new language
    def generate_skill_sentence():
        sentences = [
            "Hello, how are you?",
            "What is your name?",
            "I need help.",
            "Where is the nearest bus stop?",
            "Can you show me the way?",
            "How much does this cost?",
            "Thank you for your help.",
            "I would like some water.",
            "Excuse me, where is the restroom?",
            "What time is it?"
        ]
        return random.choice(sentences)

    # Function to translate text using OpenAI's GPT model
    def translate_text(text, target_language):
        messages = [
            {"role": "system", "content": f"You are a helpful assistant that translates text to {target_language}."},
            {"role": "user", "content": f"Translate the following text: {text}"}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or gpt-4 based on your needs
            messages=messages,
            max_tokens=100
        )
        translation = response['choices'][0]['message']['content'].strip()
        return translation

    # Function to speak text using pyttsx3
    def speak_text(text):
        tts_engine.say(text)  # Convert text to speech
        tts_engine.runAndWait()  # Block while processing all currently queued commands

    # Text input for user prompt
    user_input = st.text_input("Enter a sentence to translate:")

    # Dropdown to select target language
    target_language = st.selectbox("Choose a language to translate to:", list(languages.keys()))

    # Button to generate random sentence
    if st.button("Generate"):
        random_sentence = generate_skill_sentence()
        st.write(f"Generated Sentence: {random_sentence}")

    # Button to translate user input
    if st.button("Translate") and user_input:
        selected_language = languages[target_language]
        translated_text = translate_text(user_input, target_language)
        st.write(f"Translated to {target_language}: {translated_text}")

    # Button to speak the translation
    if st.button("Speak") and user_input:
        selected_language = languages[target_language]
        translated_text = translate_text(user_input, target_language)
        speak_text(translated_text)  # Speak the translated text
