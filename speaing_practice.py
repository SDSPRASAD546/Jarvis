import speech_recognition as sr
import pyttsx3
import requests

def speech_recognition():
    # Create a recognizer object
    recognizer = sr.Recognizer()
    text = ""
    # Capture audio from the default microphone
    with sr.Microphone() as source:
        print("Listening... Say something!")
        audio = recognizer.listen(source)

    try:
        # Use Google Web Speech API to recognize the speech
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
    except sr.RequestError as e:
        print(f"Error occurred: {e}")
    return text

def chat_with_cohere(prompt):
    cohere_api_key = "Paste your cohere api key"
    cohere_endpoint = "https://api.cohere.ai/v1/generate"

    headers = {
        "Authorization": f"Bearer {cohere_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "max_tokens": 40,
        "temperature": 0.7
    }

    try:
        # Send a POST request to CoHere API
        response = requests.post(cohere_endpoint, json=payload, headers=headers)
        response_json = response.json()
        generations = response_json.get("generations", [])
        if generations:
            return generations[0].get("text")
        else:
            print("No text found in the response.")
            return None
    except Exception as e:
        print(f"Error: {e}")

def text_to_speech(text, language="en"):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set the language (if needed, you can check available voices using engine.getProperty('voices'))
    engine.setProperty('rate', 150)  # You can adjust the speaking rate (words per minute)
    engine.setProperty('volume', 0.9)  # You can adjust the volume (0.0 to 1.0)

    # Set the desired language (if available)
    engine.setProperty('voice', language)

    # Speak the given text
    engine.say(text)

    # Wait for the speech to complete
    engine.runAndWait()

if __name__ == "__main__":
    engine = pyttsx3.init()
    engine.say("Hello, I am ready. Tell me what to do.")
    engine.runAndWait()

    while True:
        user_input = speech_recognition()
        response = chat_with_cohere(user_input)
        if response:
            print("Jarvis:", response)
            text_to_speech(response)
        else:
            print("Jarvis: I didn't catch that. Could you please repeat?")
