import speech_recognition as sr
import pyttsx3
from gpt4all import GPT4All

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 175)  # Speaking speed

# Initialize model
model = GPT4All("gpt4all-13b-snoozy-q4_0.gguf")


system_prompt = (
    "You are CLARA, the Cognitive Logic and Autonomous Response Assistant. "
    "You help users with advice, conversation, emotional support, and answering questions. "
    "You are supportive, not judgmental. Be clear, warm, and respectful in every response. "
    "You are a helpful assistant, not a substitute for a human professional."
    "You answer in short and straight to the point sentences."
)

history = system_prompt

# Function to speak text aloud
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to get user voice input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You: {text}")
        return text
    except sr.UnknownValueError:
        print("❗ Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"❗ Could not request results; {e}")
        return ""
    
    

history = []

while True:
    user_input = input("You: ")
    history.append(f"User: {user_input}")
    history.append("CLARA:")
    prompt = system_prompt + "\n" + "\n".join(history[-6:])  # Last 3 turns
    response = model.generate(prompt, max_tokens=200)
    print("CLARA:", response.strip())
    history.append(response.strip())

