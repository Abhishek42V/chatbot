import streamlit as st
import random
import openai
from gtts import gTTS
import os

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
            "What time is it?",
            "Can you speak slowly, please?",
            "I dont understand.",
            "Can you repeat that, please?",
            "Where are you from?",
            "Im from the United States.",
            "Do you speak English?",
            "How do you say this in Spanish?",
            "Can you write that down, please?",
            "What does this word mean?",
            "I am lost.",
            "Where is the nearest hotel?",
            "I need a doctor.",
            "Call the police.",
            "Can I get the bill, please?",
            "Do you accept credit cards?",
            "Where can I exchange money?",
            "I would like to make a reservation.",
            "Can you recommend a good restaurant?",
            "How far is the airport?",
            "What time does the train leave?",
            "I am allergic to peanuts.",
            "I am a vegetarian.",
            "Can I have the menu, please?",
            "I would like to order.",
            "Can you bring me the check?",
            "Is this seat taken?",
            "Can you help me find my seat?",
            "What is the Wi-Fi password?",
            "Can I borrow your pen?",
            "How do I get to the train station?",
            "Is there a hospital nearby?",
            "Can you show me on the map?",
            "Where is the embassy?",
            "How long does it take to get there?",
            "Is it safe to walk at night?",
            "Can I get a taxi, please?",
            "Where can I buy a SIM card?",
            "Do you have vegetarian options?",
            "Is this gluten-free?",
            "I need a charger.",
            "Where can I buy some water?",
            "Can you take a photo of me?",
            "Whats the weather like today?",
            "Do you have any rooms available?",
            "Can I check in early?",
            "When is checkout time?",
            "Is breakfast included?",
            "Can I have an extra towel?",
            "How do I use the air conditioning?",
            "Is there an ATM nearby?",
            "Can I get a map of the city?",
            "I would like a coffee, please.",
            "Can I pay with cash?",
            "Do you have change for a twenty?",
            "Is there a supermarket around here?",
            "How do you say this word?",
            "What time is dinner?",
            "Can I make a phone call?",
            "Do you have free Wi-Fi?",
            "I dont feel well.",
            "I have a reservation under my name.",
            "What time does the museum open?",
            "How much is the entrance fee?",
            "Where is the nearest pharmacy?",
            "Can I get a ticket to the museum?",
            "Does this bus go to the city center?",
            "How long is the tour?",
            "Can I take a picture here?",
            "Is there a fee to enter?",
            "Where can I park my car?",
            "How do I get to the highway?",
            "What is the speed limit here?",
            "How far is the next gas station?",
            "Can I fill up my car, please?",
            "Where is the rental car return?",
            "How do I get to the nearest bank?",
            "Do I need to wear a seatbelt?",
            "Can you help me carry this?",
            "What is the local currency?",
            "Can I drink the tap water?",
            "Is it okay to swim here?",
            "Where is the lifeguard station?",
            "Can I get a beach towel?",
            "How deep is the water here?",
            "Do you have any sunscreen?",
            "Whats the local time?",
            "Whats the emergency number here?",
            "Is there a nearby restaurant?",
            "Can I reserve a table?",
            "How do I get to the city center?",
            "Is the museum within walking distance?",
            "Can you recommend a good tour guide?"
        ]
        return random.choice(sentences)

    # Function to translate text using OpenAI's GPT model
    def translate_text(text, target_language):
        messages = [
            {"role": "system", "content": f"You are a helpful assistant that translates text to {target_language}."},
            {"role": "user", "content": f"Translate the following text: {text}"}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",  # or gpt-4o-mini-2024-07-18 or gpt-4
            messages=messages,
            max_tokens=100
        )
        translation = response['choices'][0]['message']['content'].strip()
        return translation

    # Function to speak text using gTTS
    def speak_text(text):
        tts = gTTS(text=text, lang='hi')  # Specify the language for TTS (default is English)->changed to hindi
        tts_file = "temp_audio.mp3"  # Temporary audio file name
        tts.save(tts_file)  # Save the audio file
        return tts_file

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
        audio_file = speak_text(translated_text)  # Speak the translated text
        st.audio(audio_file, format='audio/mp3')  # Play the audio file
        os.remove(audio_file)  # Remove the audio file after playing
