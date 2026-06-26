# 🪞 AI Mirror — Hinglish Roast Edition

> **Real-time webcam emotion detection that delivers savage Hinglish roasts or epic motivational boosts — with voice output!**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red?style=flat-square&logo=streamlit)
![DeepFace](https://img.shields.io/badge/DeepFace-Emotion%20AI-purple?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🎬 What It Does

Point your webcam at your face → AI detects your emotion → you get either a **savage Hinglish roast** 🔥 or a **fire motivational boost** 💖 — spoken aloud in Hindi voice.

**7 emotions detected:** Happy 😄 · Sad 😢 · Angry 😡 · Surprised 😲 · Fear 😱 · Disgust 🤢 · Neutral 😐

**140+ unique Hinglish responses** (20 per emotion × 2 modes) — meme-grade humor, never repeats too soon.

---

## 🗂️ Project Structure

```
ai-mirror/
├── app.py            ← Streamlit app (Python backend, real DeepFace AI)
├── index.html        ← Standalone browser demo (no install needed)
├── requirements.txt  ← Python dependencies
├── .gitignore        ← Git ignore rules
└── README.md         ← This file
```

---

## ⚡ Two Ways to Run

### Option A — Browser Demo (Zero Install)
> Works instantly in any modern browser. No Python, no server.

1. Download or clone this repo
2. Open `index.html` by double-clicking it
3. Allow camera access when prompted
4. Hit **📸 Capture & Analyse** and face the mirror!

> **Note:** The HTML demo uses client-side brightness heuristics for emotion simulation.  
> For **real AI emotion detection**, use Option B.

---

### Option B — Full Python App (Real AI)

#### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-mirror.git
cd ai-mirror
```

#### 2. Create a virtual environment
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

> ⏳ **First run:** DeepFace auto-downloads the FER2013 model weights (~50 MB).  
> This happens once and is cached in `~/.deepface/`.

#### 4. Launch the app
```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501** 🎉

---

## 🛠️ Tech Stack

| Layer              | Technology                         |
|--------------------|------------------------------------|
| **UI**             | Streamlit (Python web app)         |
| **Emotion AI**     | DeepFace + FER2013 model           |
| **Face Detection** | OpenCV Haar Cascade                |
| **Voice (Python)** | edge-tts (Neural), ElevenLabs / OpenAI (Premium), gTTS (Legacy) |
| **Voice (HTML)**   | Web Speech API (browser built-in)  |
| **Image**          | Pillow + NumPy                     |
| **Fonts**          | Space Grotesk + JetBrains Mono     |

---

## 🎭 Feature List

### Core Features
- ✅ **Real DeepFace AI** — `enforce_detection=False` + `opencv` backend (CPU-only, no GPU needed)
- ✅ **7 emotion classes** — happy, sad, angry, surprise, fear, disgust, neutral
- ✅ **140+ Hinglish responses** — 20 roasts + 20 boosts per emotion
- ✅ **Multi-Engine Comedian Voice** — High-fidelity human-like narration via **Microsoft Edge Neural TTS** (Free, no API key), **ElevenLabs** (Premium, custom comedian voices), **OpenAI TTS** (Premium, expressive models), or **gTTS** (Legacy).
- ✅ **Stand-up Comedian Tuning** — Dynamic speech speed (Rate) and pitch-shifting controls to achieve a fast-talking, energetic, or sarcastic stand-up comedy delivery.
- ✅ **Animated face bounding box** — colour-coded corner brackets per emotion
- ✅ **Confidence bar** — animated progress bar showing model certainty
- ✅ **Reaction history** — last 6 captures shown inline
- ✅ **Score tracker** — total captures, roasts, and boosts counted
- ✅ **Live preview toggle** — 5-second continuous camera loop

### HTML-Only Bonus Features
- ✅ **Emotion Leaderboard** — ASCII bar chart of your most-detected emotions
- ✅ **Shareable Roast Card** — downloads a PNG meme card (face emoji + emotion + roast text)
- ✅ **Toast notifications** — popup on each capture
- ✅ **Animated scan line** — visual effect on face box during detection
- ✅ **Hindi/English TTS toggle** — switch voice language on the fly
- ✅ **Random voice pitch** — lower/grittier for roasts, higher/brighter for boosts

---

## 🔥 Sample Roasts

| Emotion  | Roast                                                                          |
|----------|--------------------------------------------------------------------------------|
| 😄 Happy  | "Bhai, itna khush mat ho. Tax notice abhi tak nahi aayi — aa jaayegi."         |
| 😢 Sad    | "Yeh sad face dekh ke lagta hai kisi ne tujhe 'seen' kiya aur reply nahi kiya."  |
| 😡 Angry  | "Shant ho ja bhai. Gusse mein kiye gaye decisions, EMI mein convert ho jaate hain." |
| 😲 Surprise| "Teri eyebrows itni upar gayi hain — last train miss ho gayi kya?"            |
| 😐 Neutral| "Bhai, teri personality toh hai, lekin aaj chhuti pe gayi hai."               |

---

## 💖 Sample Boosts

| Emotion  | Boost                                                                           |
|----------|---------------------------------------------------------------------------------|
| 😄 Happy  | "Bhai, teri smile ka ROI bohot zyada hai. Invest kar isme aur duniya jeet le." |
| 😢 Sad    | "Sadness matlab teri story ka interval — climax abhi baaki hai bhai!"          |
| 😡 Angry  | "Is gusse se ek page likh, ek project shuru kar, ek idea execute kar. NOW!"    |
| 😐 Neutral| "Tu stoic hai — aur stoics hi duniya ko change karte hain. History check kar." |

---

## 🚀 Viral Features Roadmap

| Feature                   | Status      | Description                                                   |
|---------------------------|-------------|---------------------------------------------------------------|
| 🎮 Multiplayer Roast Battle | Coming Soon | Two webcams, one screen — AI judges who gets roasted harder  |
| 🏆 Emotion Leaderboard      | ✅ Live      | Your emotion breakdown with ASCII bar chart                   |
| 🃏 Shareable Roast Card     | ✅ Live      | PNG meme card download — emotion + roast text + branding      |
| 🎙️ 30-sec Roast Reel        | Coming Soon | Video clip with frame-by-frame emotion + AI voice narration   |
| 📊 Emotion Timeline Chart   | Coming Soon | Line chart of your emotional journey across captures          |
| 🤖 Live Roast Mode          | Coming Soon | Continuous detection every 3s with automatic voice output     |

---

## 🐛 Troubleshooting

| Problem                          | Solution                                                                      |
|----------------------------------|-------------------------------------------------------------------------------|
| `ModuleNotFoundError: deepface`  | `pip install deepface tf-keras`                                               |
| `ModuleNotFoundError: gtts`      | `pip install gtts`                                                            |
| Webcam not found                 | Try `cv2.VideoCapture(1)` in `app.py` instead of `(0)`                       |
| DeepFace slow on first run       | Normal — downloading model weights (~50 MB). Cached after first run.          |
| macOS camera permission denied   | System Settings → Privacy & Security → Camera → allow Terminal / VS Code     |
| Windows camera in use            | Close other apps (Zoom, Teams, OBS) using the webcam                         |
| HTML voice not speaking          | Click anywhere on the page first (browsers require user gesture for audio)    |
| Hindi voice not available        | Browser falls back to English voice automatically                              |

---

## 📦 Dependencies

```
streamlit>=1.32.0       # Web UI framework
opencv-python>=4.9.0    # Camera capture + face detection
deepface>=0.0.93        # Emotion AI (FER2013 model)
tf-keras>=2.16.0        # DeepFace backend
Pillow>=10.2.0          # Image processing
numpy>=1.24.0           # Array operations
gtts>=2.5.1             # Google Text-to-Speech (Hindi voice)
```

---

## 🖥️ System Requirements

| Requirement     | Minimum                    |
|-----------------|----------------------------|
| Python          | 3.9+                       |
| RAM             | 4 GB                       |
| Webcam          | Any USB or built-in camera |
| GPU             | ❌ Not required (CPU only)  |
| Internet        | Only for first-run model download + gTTS |
| OS              | Windows 10+ / macOS 11+ / Ubuntu 20.04+ |

---

## 🌐 Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select `app.py` as the main file
5. Click **Deploy** — done!

> **Note:** Streamlit Cloud doesn't have webcam access by default.  
> For live demos, run locally or use a tunnelling service like ngrok.

---

## 🤝 Contributing

Pull requests are welcome! To contribute:

```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
# Open a Pull Request
```

Ideas for contributions:
- Add more Hinglish roast lines
- Add regional language support (Tamil, Telugu, Bengali)
- Build the multiplayer mode
- Add emotion timeline chart with Plotly

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙏 Credits

- **[DeepFace](https://github.com/serengil/deepface)** — emotion detection engine
- **[Streamlit](https://streamlit.io)** — Python web app framework  
- **[gTTS](https://gtts.readthedocs.io)** — Hindi text-to-speech
- **[OpenCV](https://opencv.org)** — computer vision & camera capture
- **[Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk)** — UI font
- Inspired by every meme page on Indian Twitter/Instagram 🇮🇳

---

<div align="center">

**Built with 🔥 (and mild sarcasm) for the Indian internet**

*Agar pasand aaya toh ⭐ star dena bhai — AI bhi khush hoga!*

</div>
