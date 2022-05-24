import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import json
import time


class ChatBot():
    text = ''

    def __init__(self, name):
        print("----- starting up", name, "-----")
        self.name = name
        with open("fixes.json", 'r') as f:
            self.fixes = json.load(f)

    def fix(self):
        for word in self.text.split(' '):
            if word in self.fixes:
                self.text = self.text.replace(word, self.fixes[word])

    def unfixed(self, text: str):
        for word in text.split(' '):
            for key, val in self.fixes.items():
                if word == val:
                    text = text.replace(word, key)
        return text

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            print("listening...")
            audio = recognizer.listen(mic)
        try:
            self.text = recognizer.recognize_google(audio)
            self.fix()
            print("me --> ", self.text)
        except:
            print("me -->  ERROR")

    def wake_up(self, text):
        self.text = ''
        return self.name.lower() in text.lower()

    def text_to_speech(self, text):
        print("AI --> ", text)
        text = self.unfixed(text)
        print(text)
        speaker = gTTS(text=text, lang="en", slow=False)
        speaker.save("res.mp3")
        playsound('res.mp3')
        os.remove("res.mp3")


# Execute the AI
if __name__ == "__main__":
    ai = ChatBot(name="Huncho")
    while True:
        ai.speech_to_text()
        res = None
        if ai.wake_up(ai.text):
            res = "Hello I am Huncho the AI, what can I do for you?"
        if res:
            ai.text_to_speech(res)
        ai.text = ''
