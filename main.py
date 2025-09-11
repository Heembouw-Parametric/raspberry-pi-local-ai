import tkinter as tk
import sounddevice as sd
import numpy as np
import whisper
import requests
import json
import platform

# # Default device
# mic_index = 1  # standaard voor andere systemen
#
# # Check of Raspberry Pi OS
# try:
#     with open("/etc/os-release") as f:
#         os_info = f.read()
#         if "raspbian" in os_info.lower() or "debian" in os_info.lower():
#             mic_index = 2  # Raspberry Pi microfoon index
# except FileNotFoundError:
#     pass  # bestand niet gevonden → niet op Pi
#
# # Zet de default input device
# sd.default.device = (None, mic_index)
#
# print(f"Gebruik microfoon met index {mic_index}")
# def record_audio(seconds=5, samplerate=None):
#     if samplerate is None:
#         samplerate = int(sd.query_devices(kind="input")["default_samplerate"])
#     print(f"Recording {seconds} seconds at {samplerate} Hz...")
#     audio = sd.rec(int(seconds * samplerate), samplerate=samplerate,
#                    channels=1, dtype='float32')
#     sd.wait()
#     return np.squeeze(audio)

def record_audio(seconds=5, samplerate=16000):
    print(f"Recording {seconds} seconds...")
    audio = sd.rec(int(seconds * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    return np.squeeze(audio)


def speech_to_text():
    audio = record_audio()
    print("Transcribing...")
    result = stt_model.transcribe(audio, fp16=False, language="nl")
    text = result["text"].strip()
    print("Recognized:", text)
    return text

def ask_ollama(prompt, model="gemma3:1b"):
    url = "http://localhost:11434/api/generate"
    dutch_prompt = "Beantwoord de vraag in het Nederlands, maximaal 200 woorden.\n" + prompt
    payload = {"model": model, "prompt": dutch_prompt}
    response = requests.post(url, json=payload, stream=True)
    output = ""
    for line in response.iter_lines():
        if line:
            try:
                part = json.loads(line.decode("utf-8"))
                if "response" in part:
                    output += part["response"]
            except Exception:
                pass
    print("LLM Answer:", output.strip())
    return output.strip()

def on_record():
    vraag = speech_to_text()
    antwoord = ask_ollama(vraag)
    label.config(text=antwoord)

# Load Whisper model once
stt_model = whisper.load_model("base")

root = tk.Tk()
root.title("Raspberry Pi Assistant")

label = tk.Label(root, text="Press the button and speak.", font=("Arial", 14), wraplength=400, justify="left")
label.pack(padx=20, pady=20)

button = tk.Button(root, text="Start Recording", font=("Arial", 12), command=on_record)
button.pack(pady=10)

root.mainloop()