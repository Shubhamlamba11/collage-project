# J.A.R.V.I.S. - Just A Rather Very Intelligent System

An advanced, modern AI assistant inspired by Marvel's J.A.R.V.I.S., powered by Google Gemini 2.5 Flash LLM, FastAPI backend, Web Speech API for real-time voice control, and a futuristic sci-fi HUD web interface.

---

## 🌟 Key Features

- **🤖 Google Gemini LLM Integration**: Uses Google's `gemini-2.5-flash` model for intelligent, context-aware conversational responses.
- **🎙️ Web Speech Voice Control**: Real-time hands-free Speech-to-Text voice recognition and Text-to-Speech audio output using browser-native Web Speech API.
- **🖥️ Futuristic Sci-Fi UI**: Iron Man inspired dark HUD web interface with interactive Arc Reactor visualizer, live system status, and latency metrics.
- **🧠 Conversation Memory**: Keeps track of conversation history with context persistence across chat turns.
- **⚡ Async Architecture & Caching**: Async request handling using FastAPI and thread pool execution, paired with an in-memory query response cache for low latency.
- **🛠️ Built-in Skills & Fallback Engine**:
  - **Live Time & Date**: Accurate datetime telemetry.
  - **Safe Math Evaluation**: Evaluates algebraic, trigonometric, and scientific math functions safely.
  - **System Telemetry**: Displays OS, architecture, and core system status.
  - **Simulated Web & Weather Search**: Instant retrieval of search queries and localized weather updates.
  - **Smart Fallback Engine**: Operates seamlessly even without an API key using internal intent classification.

---

## 📁 Repository Structure

```text
.
├── app/
│   ├── __init__.py
│   ├── ai_engine.py       # Query processing, caching & async execution
│   ├── gemini_client.py   # Google GenAI Gemini integration & fallback engine
│   ├── main.py            # FastAPI web server & endpoints
│   ├── memory.py          # Conversation history state manager
│   └── tools.py           # Math, weather, system info & search skills
├── static/
│   ├── app.js             # Voice recognition, TTS speech synthesis & UI logic
│   ├── index.html         # HUD Web UI layout
│   └── style.css          # Sci-Fi theme styles & Arc Reactor animations
├── tests/
│   ├── test_api.py        # API endpoint tests
│   ├── test_memory.py     # Memory persistence tests
│   └── test_tools.py      # Skill execution unit tests
├── README.md
└── requirements.txt
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10 or higher
- Modern web browser (Chrome / Edge / Safari / Firefox) with Speech API support.

### 2. Installation

Clone the repository and install required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Running the Server

Start the FastAPI application with Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser and navigate to:
```
http://localhost:8000
```

---

## 🔑 Configuring Gemini API Key

You can configure the Gemini API Key in two ways:

1. **Environment Variable**: Set `GEMINI_API_KEY` before starting the server:
   ```bash
   export GEMINI_API_KEY="your-google-gemini-api-key"
   ```
2. **Web UI Interface**: Enter your key directly into the **Gemini API Key** field in the HUD sidebar and click save.

---

## 🧪 Running Unit Tests

Run the full `pytest` test suite to verify system integrity:

```bash
PYTHONPATH=. pytest
```

---

## 📡 API Reference

- `POST /api/chat` - Send a message to JARVIS (`{"message": "string", "api_key": "optional"}`).
- `GET /api/system/status` - Returns current core system metrics and health status.
- `POST /api/math` - Evaluates a mathematical expression (`{"expression": "pow(2, 8)"}`).
- `GET /api/history` - Fetches conversation history.
- `DELETE /api/history` - Resets conversation memory history.
- `POST /api/config` - Dynamically updates Gemini API key configuration.

---

## 🛡️ License

Distributed under the MIT License.
