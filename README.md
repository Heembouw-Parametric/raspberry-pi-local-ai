# AI Assistant op Raspberry Pi 5 met Touchscreen

Dit project zet je Raspberry Pi 5 met touchscreen om in een **lokale AI-assistent**.  
De assistant gebruikt **Whisper** voor spraakherkenning en een LLM (via API of lokaal) voor tekstgeneratie.  
De interface draait in **Tkinter** op je Pi-scherm.

---

## 📦 Benodigde software

### 1. Raspberry Pi OS 64-bit
Zorg dat je **Raspberry Pi OS (64-bit)** draait en je systeem up-to-date is:

```bash
sudo apt update && sudo apt upgrade -y
```
### 2. Systeemdependencies
Installeer pakketten die nodig zijn voor audio en Python:

```bash
sudo apt install -y python3 python3-pip python3-venv portaudio19-dev
```

### 3. Project installeren
Clone je project of kopieer het naar de Pi en ga naar de map:

```bash
Code kopiëren
git clone https://github.com/<jouw-repo>.git
cd <jouw-repo>
Maak een virtual environment en installeer dependencies:
```

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install tkinter sounddevice numpy openai-whisper requests
```

ℹ️ Let op:
tkinter zit vaak al in Raspberry Pi OS. Als het ontbreekt:

```bash
sudo apt install -y python3-tk
```

📂 Projectstructuur
Bijvoorbeeld:

arduino
Code kopiëren
mijn_project/
│── main.py
│── run.sh
│── requirements.txt
▶️ Starten van de applicatie
Activeer je venv en run de app handmatig:

```bash
source venv/bin/activate
python main.py
```

⚙️ Automatisch starten bij boot (systemd)
Maak een systemd-service zodat de app automatisch start als de Pi opstart.

Maak een nieuw service-bestand:

```bash
sudo nano /etc/systemd/system/ai-assistant.service
```

Voeg dit toe:

```ini
[Unit]
Description=AI Assistant
After=network.target sound.target

[Service]
ExecStart=/home/pi/mijn_project/venv/bin/python /home/pi/mijn_project/main.py
WorkingDirectory=/home/pi/mijn_project
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Let op: pas /home/pi/mijn_project/ aan naar de locatie van jouw projectmap.
Activeer de service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-assistant
sudo systemctl start ai-assistant
```

Check of het werkt:

```bash
systemctl status ai-assistant
```