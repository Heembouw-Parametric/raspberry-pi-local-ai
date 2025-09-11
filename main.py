import tkinter as tk
import sounddevice as sd
import numpy as np
import whisper
import requests
import json
import platform

# ------------------ Microphone index detection ------------------
mic_index = 1  # default for other systems

try:
    with open("/etc/os-release") as f:
        os_info = f.read()
        if "raspbian" in os_info.lower() or "debian" in os_info.lower():
            mic_index = 2  # Raspberry Pi mic index
except FileNotFoundError:
    pass

sd.default.device = (None, mic_index)
print(f"Gebruik microfoon met index {mic_index}")

# ------------------ Load context.json ------------------
with open("context.json", "r", encoding="utf-8") as f:
    context_data = json.load(f)

def build_context_prompt(user_question: str) -> str:
    """
    Match the user question with aliases from context.json
    and build a context-aware system prompt.
    """
    context_text = f"Topic: {context_data['topic']}\n\n"
    matched_entries = []

    q_lower = user_question.lower()
    for entry in context_data["entries"]:
        for alias in entry["aliases"]:
            if alias.lower() in q_lower:
                matched_entries.append(f"{entry['field']}: {entry['value']}")

    if matched_entries:
        context_text += "\n".join(matched_entries)
    else:
        # fallback: full context
        for entry in context_data["entries"]:
            context_text += f"{entry['field']}: {entry['value']}\n"

    return context_text

# ------------------ Audio recording ------------------
def record_audio(seconds=5, samplerate=None):
    if samplerate is None:
        samplerate = int(sd.query_devices(kind="input")["default_samplerate"])
    print(f"Recording {seconds} seconds at {samplerate} Hz...")
    audio = sd.rec(int(seconds * samplerate), samplerate=samplerate,
                   channels=1, dtype='float32')
    sd.wait()
    return np.squeeze(audio)

# ------------------ Speech to text ------------------
def speech_to_text():
    audio = record_audio()
    print("Transcribing...")
    result = stt_model.transcribe(audio, fp16=False, language="nl")
    text = result["text"].strip()
    print("Recognized:", text)
    return text

# ------------------ Ask Ollama with context ------------------
def ask_ollama(prompt, model="gemma3:1b"):
    context_prompt = build_context_prompt(prompt)

    dutch_prompt = (
        "Je bent een assistent die antwoord geeft in het Nederlands.\n"
        "Gebruik de onderstaande context over Heembouw om de vraag te beantwoorden.\n\n"
        f"Context:\n{context_prompt}\n\n"
        f"Vraag: {prompt}\nAntwoord (maximaal 200 woorden):"
    )

    url = "http://localhost:11434/api/generate"
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

# ------------------ Button action ------------------
def on_record():
    vraag = speech_to_text()
    antwoord = ask_ollama(vraag)
    label.config(text=antwoord)

# ------------------ Load Whisper model ------------------
stt_model = whisper.load_model("base")

# ------------------ Tkinter GUI ------------------
root = tk.Tk()
root.title("Heembouw Assistant")

label = tk.Label(root, text="Druk op de knop en spreek je vraag uit.",
                 font=("Arial", 14), wraplength=400, justify="left")
label.pack(padx=20, pady=20)

button = tk.Button(root, text="Start opname", font=("Arial", 12), command=on_record)
button.pack(pady=10)

root.mainloop()
