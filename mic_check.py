import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import whisper
import torch

# --- Kies input en output device ---
mic_index = 1   # jouw microfoon (Intel Smart Sound)
speaker_index = 6  # bv. Luidsprekers (Realtek) → kies juiste index uit lijst

sd.default.device = (speaker_index, mic_index)

print("Beschikbare audio devices:")
print(sd.query_devices())
print(f"\nGebruik microfoon index {mic_index}, speaker index {speaker_index}\n")

def record_audio(seconds=5, samplerate=None):
    if samplerate is None:
        samplerate = int(sd.query_devices(mic_index)["default_samplerate"])
    print(f"🎙️ Opnemen {seconds} seconden op {samplerate} Hz...")
    audio = sd.rec(int(seconds * samplerate), samplerate=samplerate,
                   channels=1, dtype='float32', device=mic_index)
    sd.wait()
    print("✅ Opname klaar.")
    return np.squeeze(audio), samplerate

def test_microphone_with_stt(seconds=5):
    audio, samplerate = record_audio(seconds=seconds)

    # Playback
    print("🔊 Afspelen...")
    sd.play(audio, samplerate, device=speaker_index)
    sd.wait()

    # Plot waveform
    plt.figure(figsize=(8, 3))
    plt.plot(audio, linewidth=0.8)
    plt.title("Opgenomen geluid")
    plt.xlabel("Samples")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()

    # Zet om naar tensor (direct, zonder wav)
    audio_tensor = torch.tensor(audio).float()

    print("📄 Transcriberen met Whisper...")
    model = whisper.load_model("small")
    result = model.transcribe(audio_tensor, language="nl")

    print("\n📝 Herkende tekst:")
    print(result["text"])

if __name__ == "__main__":
    test_microphone_with_stt(seconds=5)
