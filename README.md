# 🪞 AI Mirror — Hinglish Roast Edition (v2.0)

> **Real-time webcam emotion detection that delivers savage Hinglish roasts or epic motivational boosts — now with high-fidelity, human-like stand-up comedian voice narration and continuous live tracking!**

![Python](https://img.shields.io/badge/Python-3.9--3.13-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red?style=flat-square&logo=streamlit)
![DeepFace](https://img.shields.io/badge/DeepFace-Emotion%20AI-purple?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🎬 What It Does

Point your webcam at your face → AI detects your emotion → you get either a **savage Hinglish roast** 🔥 or a **fire motivational boost** 💖 — spoken aloud in a highly realistic, human-like voice that sounds exactly like an energetic stand-up comedian.

- **7 emotions detected:** Happy 😄 · Sad 😢 · Angry 😡 · Surprised 😲 · Fear 😱 · Disgust 🤢 · Neutral 😐
- **140+ unique Hinglish responses** (20 per emotion × 2 modes) — meme-grade humor, never repeats too soon.
- **🎙️ Comedian Narrator:** Customize the speech rate and pitch shift to match a fast-talking, sarcastic stand-up comedy delivery.

---

## 🗂️ Project Structure

```
ai-mirror/
├── app.py            ← Upgraded Streamlit app (Python backend, real DeepFace AI, Multi-Engine Voice)
├── index.html        ← Standalone browser demo (no install needed, native Web Speech API)
├── requirements.txt  ← Python dependencies (updated with edge-tts)
├── config.toml       ← Streamlit custom theme configuration
└── README.md         ← This file
```

---

## ⚡ Two Ways to Run

### Option A — Browser Demo (Zero Install)
> Works instantly in any modern browser. No Python, no server.

1. Download or clone this repo.
2. Open `index.html` by double-clicking it.
3. Allow camera access when prompted.
4. Hit **📸 Capture & Analyse** and face the mirror!
*Note: The HTML demo uses client-side brightness heuristics for emotion simulation. For real AI emotion detection, use Option B.*

---

### Option B — Full Python App (Real AI & Advanced Comedian Voice)

#### 🍎 Note for Apple Silicon (M1/M2/M3) Mac Users
To avoid the common TensorFlow AVX instruction crash under Intel (x86_64) emulation, you **must** run the app using a native Apple Silicon (`arm64`) Python environment (e.g., Python 3.11 or 3.12). 

#### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-mirror.git
cd ai-mirror
```

#### 2. Install dependencies using `uv` (Recommended)
We recommend using [**`uv`**](https://github.com/astral-sh/uv), a blazing-fast Python package installer that handles large machine learning wheels natively and securely on Apple Silicon:
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Install all requirements natively into your active environment
uv pip install --system -r requirements.txt
```
*Alternatively, using standard pip:*
```bash
pip install -r requirements.txt
```

> ⏳ **First run:** DeepFace auto-downloads the FER2013 facial expression model weights (~6 MB). This happens once and is cached in `~/.deepface/`.

#### 3. Launch the app
```bash
python3 -m streamlit run app.py --browser.gatherUsageStats=false
```

Open your browser at **http://localhost:8501** 🎉

---

## 🛠️ Tech Stack

| Layer              | Technology                         |
|--------------------|------------------------------------|
| **UI**             | Streamlit (Python web app)         |
| **Emotion AI**     | DeepFace + FER2013 model           |
| **Face Detection** | OpenCV Haar Cascade (Fast CPU-only)|
| **Voice (Python)** | **Multi-Engine Speech Narrator**:<br>• *Microsoft Edge Neural* (Free, human-like neural voices)<br>• *ElevenLabs* (Premium, custom comedian voices)<br>• *OpenAI TTS* (Premium, expressive models)<br>• *gTTS* (Legacy computer fallback) |
| **Voice (HTML)**   | Web Speech API (browser built-in)  |
| **Image**          | Pillow + NumPy                     |
| **Fonts**          | Space Grotesk + JetBrains Mono     |

---

## 🎭 Feature List

### Core Features
- ✅ **Real DeepFace AI** — `enforce_detection=False` + `opencv` backend (CPU-only, no GPU needed).
- ✅ **7 emotion classes** — happy, sad, angry, surprise, fear, disgust, neutral.
- ✅ **140+ Hinglish responses** — 20 roasts + 20 boosts per emotion.
- ✅ **🎙️ Multi-Engine Comedian Voice** — High-fidelity human-like voice narration. Supports Microsoft Edge Neural TTS (Free, no API key), ElevenLabs (Premium, custom cloned comedian voices), OpenAI TTS (Premium, expressive models), or gTTS (Legacy).
- ✅ **🏎️ Stand-up Comedian Tuning** — Sliders to adjust **Speech Speed (Rate)** and **Voice Pitch Shift** dynamically to match a fast-talking, energetic stand-up comedy delivery.
- ✅ **🤖 Continuous Live Roast Mode** — The AI continuously tracks your face using fast Haar Cascades, displaying a smooth video stream. Every X seconds (configurable via slider), it triggers deep emotion detection, generates a Hinglish response, and reads it out loud without ever freezing or stuttering the camera feed (powered by background threading)!
- ✅ **Animated face bounding box** — colour-coded corner brackets per emotion.
- ✅ **Confidence bar** — animated progress bar showing model certainty.
- ✅ **Reaction history** — last 6 captures shown inline.
- ✅ **Score tracker** — total captures, roasts, and boosts counted.

---

## 🔥 Sample Roasts & Boosts

### Roasts
| Emotion  | Roast |
|----------|-------|
| 😄 Happy  | "Bhai, itna khush mat ho. Tax notice abhi tak nahi aayi — aa jaayegi." |
| 😢 Sad    | "Yeh sad face dekh ke lagta hai kisi ne tujhe 'seen' kiya aur reply nahi kiya." |
| 😡 Angry  | "Shant ho ja bhai. Gusse mein kiye gaye decisions, EMI mein convert ho jaate hain." |
| 😲 Surprise| "Teri eyebrows itni upar gayi hain — last train miss ho gayi kya?" |

### Boosts
| Emotion  | Boost |
|----------|-------|
| 😄 Happy  | "Bhai, teri smile ka ROI bohot zyada hai. Invest kar isme aur duniya jeet le." |
| 😢 Sad    | "Sadness matlab teri story ka interval — climax abhi baaki hai bhai!" |
| 😡 Angry  | "Is gusse se ek page likh, ek project shuru kar, ek idea execute kar. NOW!" |
| 😐 Neutral| "Tu stoic hai — aur stoics hi duniya ko change karte hain. History check kar." |

---

## 🚀 Viral Features Roadmap

| Feature                   | Status      | Description                                                   |
|---------------------------|-------------|---------------------------------------------------------------|
| 🤖 Continuous Live Roast Mode | ✅ **Live** | Real-time face tracking and continuous, non-blocking voice roasts. |
| 🏆 Emotion Leaderboard      | ✅ **Live** | Your emotion breakdown with ASCII bar chart (HTML version).    |
| 🃏 Shareable Roast Card     | ✅ **Live** | PNG meme card download — emotion + roast text + branding.      |
| 🎮 Multiplayer Roast Battle | Coming Soon | Two webcams, one screen — AI judges who gets roasted harder.  |
| 🎙️ 30-sec Roast Reel        | Coming Soon | Video clip with frame-by-frame emotion + AI voice narration.   |
| 📊 Emotion Timeline Chart   | Coming Soon | Line chart of your emotional journey across captures.          |

---

## 🐛 Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `The TensorFlow library was compiled to use AVX instructions...` | Running Python in Intel (x86_64) mode under Rosetta on Apple Silicon. | Run the app under a native Apple Silicon (`arm64`) Python environment (e.g., Python 3.11 or 3.12). Avoid Python 3.14 as TensorFlow wheels are not yet available. |
| `ModuleNotFoundError: edge-tts` | Package missing. | Run `pip install edge-tts` or `uv pip install edge-tts`. |
| Streamlit page is completely blank | Startup runtime crash. | Check the terminal console for exceptions. The most common cause is the AVX crash above, resolved by using a native Python interpreter. |
| Camera stream freezes during voice narration | Network latency or blocking calls. | Fully resolved in v2.0 using non-blocking background threads and an asynchronous audio playback queue. |
| Webcam not found | System index mismatch. | Try changing `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` in `app.py`. |
| macOS camera permission denied | Security restriction. | Go to System Settings → Privacy & Security → Camera → allow Terminal / VS Code / Cursor. |

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

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙏 Credits

- **[DeepFace](https://github.com/serengil/deepface)** — emotion detection engine
- **[edge-tts](https://github.com/rany2/edge-tts)** — Microsoft Edge Neural TTS wrapper
- **[Streamlit](https://streamlit.io)** — Python web app framework  
- **[OpenCV](https://opencv.org)** — computer vision & camera capture
- **[Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk)** — UI font
- Inspired by every stand-up comedian roasting front rows 🎤

---

<div align="center">

**Built with 🔥 (and mild sarcasm) for the Indian internet**

*Agar pasand aaya toh ⭐ star dena bhai — AI bhi khush hoga!*

</div>
