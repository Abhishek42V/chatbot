import streamlit as st
import random
import openai
import os

# Show title and description.
st.title("💬 Multilingual Chatbot with Translation")
st.write(
    "This chatbot generates and translates sentences to various languages using OpenAI's GPT model. "
    "You can also have the translations spoken out loud using OpenAI's Text-to-Speech (TTS). "
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

    # Function to translate text using OpenAI's model
    def translate_text(text, target_language):
        prompt = f"Translate the following text to {target_language}: {text}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        translation = response.choices[0].text.strip()
        return translation

    # Function to speak text using OpenAI's TTS
    def speak_text(text):
        response = openai.Audio.create(
            model="whisper-1",
            prompt=text
        )
        return response['data']['audio']

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
        audio_response = speak_text(translated_text)
        st.audio(audio_response)  # Streamlit audio player to play the speech output

