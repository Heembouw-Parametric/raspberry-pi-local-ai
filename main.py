import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sounddevice as sd
import numpy as np
import whisper
import requests
import json
from scipy.signal import resample
from test_web import request_llm


# # ------------------ Load context.json ------------------
# with open("context.json", "r", encoding="utf-8") as f:
#     context_data = json.load(f)
#
# def build_context_prompt(user_question: str) -> str:
#     """
#     Match the user question with aliases from context.json
#     and build a context-aware system prompt.
#     """
#     context_text = f"Topic: {context_data['topic']}\n\n"
#     matched_entries = []
#
#     q_lower = user_question.lower()
#     for entry in context_data["entries"]:
#         for alias in entry["aliases"]:
#             if alias.lower() in q_lower:
#                 matched_entries.append(f"{entry['field']}: {entry['value']}")
#
#     if matched_entries:
#         context_text += "\n".join(matched_entries)
#     else:
#         # fallback: full context
#         for entry in context_data["entries"]:
#             context_text += f"{entry['field']}: {entry['value']}\n"
#
#     return context_text

# ------------------ AUDIO ------------------

def record_audio(seconds=5, samplerate=44100):
    print(f"Recording {seconds} seconds at {samplerate} Hz...")
    audio = sd.rec(int(seconds * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    audio = np.squeeze(audio)

    # Resample naar 16kHz
    target_sr = 16000
    num_samples = int(len(audio) * target_sr / samplerate)
    audio_resampled = resample(audio, num_samples)

    return audio_resampled

def speech_to_text():
    audio = record_audio()
    print("Transcribing...")
    result = stt_model.transcribe(audio, fp16=False, language="nl")
    text = result["text"].strip()
    print("Recognized:", text)
    return text

# ------------------ OLLAMA ------------------

def ask_ollama(prompt, model="gemma3:1b"):
    url = "http://localhost:11434/api/generate"
    payload = {"model": model, "prompt": prompt}
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

# ------------------ TKINTER UI ------------------

def on_record():
    # Stap 1: Opnemen
    label.config(text="🎙 Opnemen... even wachten.")
    root.update()
    vraag = speech_to_text()

    # Stap 2: Denken
    label.config(text="⚙️ Ik denk even na over je vraag...")
    root.update()
    # antwoord = ask_ollama(vraag, model="heembouw")
    antwoord = request_llm(vraag)

    # Stap 3: Resultaat tonen
    label.config(text=antwoord)

# Load Whisper model once
stt_model = whisper.load_model("base")

root = tk.Tk()
root.title("Steampunk Assistant")

# Fullscreen
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

# Achtergrond
try:
    bg_image = Image.open("steampunk_background.jpg")
    bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
except FileNotFoundError:
    root.configure(bg="#2B2B28")

# Steampunk kleuren
fg_color = "#E1C16E"
bg_color = "#2B2B28"

style = ttk.Style()
style.theme_use("clam")

style.configure("Steampunk.TButton",
                font=("Courier New", 20, "bold"),
                foreground=fg_color,
                background=bg_color,
                padding=15,
                borderwidth=5,
                relief="raised")
style.map("Steampunk.TButton",
          foreground=[("active", bg_color)],
          background=[("active", fg_color)])

style.configure("Steampunk.TLabel",
                font=("Courier New", 22, "bold"),
                foreground=fg_color,
                background=bg_color)

frame = tk.Frame(root, bg=bg_color, bd=10, relief="ridge")
frame.place(relx=0.5, rely=0.5, anchor="center")

label = ttk.Label(frame, text="🎩 Welkom bij de Steampunk Assistant", style="Steampunk.TLabel", wraplength=800, justify="center")
label.pack(pady=20, padx=20)

button = ttk.Button(frame, text="Start Opname", style="Steampunk.TButton", command=on_record)
button.pack(pady=20)

root.mainloop()
