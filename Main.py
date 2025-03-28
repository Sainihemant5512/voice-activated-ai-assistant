import sys
import speech_recognition as sr
import webbrowser
import pyttsx3
import os
import subprocess  # For opening applications
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont, QMovie
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# Initialize speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

class WakeWordThread(QThread):
    wake_detected = pyqtSignal()

    def run(self):
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            while True:
                print("Listening for wake word...")
                try:
                    audio = recognizer.listen(source, phrase_time_limit=3)
                    result = recognizer.recognize_google(audio).lower()
                    if "jarvis" in result or "hey jarvis" in result:
                        print("Wake word detected!")
                        self.wake_detected.emit()
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    print("Check your internet connection.")

class JarvisUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Jarvis - AI Assistant")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Say 'Hey Jarvis' to activate.")
        self.label.setFont(QFont("Arial", 14))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.setLayout(layout)

        self.wake_thread = WakeWordThread()
        self.wake_thread.wake_detected.connect(self.listen_command)
        self.wake_thread.start()

    def speak(self, text):
        self.label.setText(f"Jarvis: {text}")
        QApplication.processEvents()
        engine.say(text)
        engine.runAndWait()

    def listen_command(self):
        self.label.setText("Listening for command...")
        QApplication.processEvents()

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
                command = recognizer.recognize_google(audio).lower()
                self.label.setText(f"Recognized: {command}")
                self.process_command(command)
            except sr.UnknownValueError:
                self.label.setText("Sorry, could not understand.")
            except sr.RequestError:
                self.label.setText("Check your internet connection.")

    def process_command(self, command):
        if "open" in command:
            app_name = command.replace("open", "").strip()
            self.open_application(app_name)
        elif "play" in command:
            song_name = command.replace("play", "").strip()
            self.speak(f"Sorry, I cannot play music directly. You can ask me to open a music application.")
        elif "stop music" in command:
            self.speak("Sorry, I cannot control music playback directly.")
        elif "pause music" in command:
            self.speak("Sorry, I cannot control music playback directly.")
        elif "resume music" in command:
            self.speak("Sorry, I cannot control music playback directly.")
        elif "search" in command:
            query = command.replace("search", "").strip()
            self.speak(f"Searching Google for {query}...")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        elif "open youtube" in command:
            self.speak("Opening YouTube...")
            webbrowser.open("https://www.youtube.com")
        elif "exit" in command or "quit" in command:
            self.speak("Goodbye!")
            sys.exit()
        else:
            self.speak("I didn't understand that command.")

    def open_application(self, app_name):
        self.speak(f"Attempting to open {app_name}...")
        try:
            if sys.platform.startswith('win'):
                subprocess.Popen(app_name)  # Try running directly on Windows
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(['open', '-a', app_name])  # For macOS
            elif sys.platform.startswith('linux'):
                subprocess.Popen([app_name])  # For Linux (may need exact command)
            else:
                self.speak(f"Sorry, I cannot open applications on this operating system.")
                return
            self.speak(f"Opened {app_name}.")
        except FileNotFoundError:
            self.speak(f"Sorry, I could not find an application named {app_name}.")
        except Exception as e:
            self.speak(f"An error occurred while trying to open {app_name}: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    jarvis_ui = JarvisUI()
    jarvis_ui.show()
    sys.exit(app.exec())