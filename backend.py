from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import cv2
import os
import time
from gradio_client import Client
from pathlib import Path
from openai import OpenAI
import pygame


OPENAI_API_KEY = "**"


openai_client = OpenAI(api_key=OPENAI_API_KEY)

class MyApp(App):
    def build(self):
        self.capture_button = Button(text="Capture Image")
        self.capture_button.bind(on_press=self.capture_and_analyse)
        
        self.image_label = Label(text="Captured Image Will Appear Here")
        
        self.description_label = Label(text="Description Will Appear Here")
        
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.capture_button)
        layout.add_widget(self.image_label)
        layout.add_widget(self.description_label)
        
        return layout
    
    def capture_and_analyse(self, instance):
        path = self.capture_image()
        desc = self.analyse_image(path)
        self.description_label.text = desc
        self.speech_path = self.tts(desc)
        self.play_audio(self.speech_path)
    
    def capture_image(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise IOError("Cannot open camera")
        ret, frame = cap.read()

        cap.release()
        
        if ret:
            path = f"image_{int(time.time())}.jpg"
            filename = os.path.join(".", path)
            cv2.imwrite(filename, frame)
            self.image_label.text = filename
            return filename
        else:
            print("Failed to capture image")
    
    def analyse_image(self, path):
        client = Client("https://ybelkada-llava-1-5-dlai.hf.space/")
        result = client.predict(
            "Describe the image",  
            path,  
            api_name="/predict"
        )
        print(result)
        return result
    
    def tts(self, text):
        speech_file_path = Path(__file__).parent / "speech.mp3"
        response = openai_client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )

        response.stream_to_file(speech_file_path)
        return speech_file_path
    
    def play_audio(self, file_path):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

if __name__ == '__main__':
    MyApp().run()
