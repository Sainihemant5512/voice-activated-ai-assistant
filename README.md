# Jarvis - Basic Voice-Activated AI Assistant

This project implements a simple voice-activated AI assistant named "Jarvis" with a graphical user interface (GUI) built using PyQt6. It listens for a wake word ("Hey Jarvis" or "Jarvis") and allows users to perform basic tasks using voice commands.

## Features

* **Wake Word Detection:** Continuously listens for "Hey Jarvis" or "Jarvis" to activate.
* **Open Applications:** Open installed applications by name (platform-dependent).
* **Web Search:** Perform Google searches using voice queries.
* **Open YouTube:** Quickly open the YouTube website.
* **Textual and Verbal Feedback:** Provides status updates and responses through the GUI and text-to-speech.

## Prerequisites

Before running the code, ensure you have the following Python libraries installed:

```bash
pip install PyQt6 speechrecognition pyttsx3
