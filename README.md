# Ω OPTIMUS: Futuristic Cybernetic Desktop Assistant

OPTIMUS is a premium, cinematic, and highly interactive desktop AI assistant interface. Engineered for daily productivity and system monitoring, it is powered by **HTML5, CSS3, Vanilla JavaScript**, and **Python + Eel Integration**. 

The application replicates next-generation cyberpunk operating systems (such as J.A.R.V.I.S.), combining a gorgeous high-contrast glassmorphism HUD dashboard with sound synthesis, hardware monitoring, and interactive AI states.

---

## 🚀 Key Features

*   **Cinematic Boot Diagnostic**: A high-tech startup scanning routine checks hardware nodes, establishes Python RPC channels, logs calibrating modules, and fades cleanly into the application.
*   **Web Audio API Sound Synthesis**: Native browser oscillators synthesize futuristic sweep sounds, hover blips, and state-change chirps entirely in JavaScript (requiring zero external audio file assets).
*   **Interactive Multi-State AI Core**: An SVG-driven holographic core surrounded by three concentric rings spinning in opposite directions. The core morphs visually through four states:
    *   `Idle`: Slow pulsing cyan sphere, calm background particles, slow visualizer wave.
    *   `Listening`: Glowing electric cyan sphere with accelerated rings, reactive canvas waveforms.
    *   `Thinking`: Pulsing electric purple color-cycle core with vertical holographic scanner sweeps.
    *   `Speaking`: Radiating outer waves, sound visualizer peaks, and typewriter response logs.
*   **Audio-Reactive Waveform Visualizer**: A multi-layered Canvas rendering engine drawing edge-faded Bézier curve sine waves that dynamically alter speed, color palettes, and amplitudes based on AI state.
*   **Particle Field Background**: A canvas particle system that tracks mouse coordinates, generating soft floating stardust links responsive to user spatial cursor movements.
*   **Real-time PC Telemetry Gauges**: Circular SVG gauges and progress bars update dynamically. When linked to the Python backend, it queries actual PC **CPU load, RAM memory usage, and thread processes** in real-time.
*   **System Event Logs & Chat Workspace**:
    *   *Core HUD Terminal*: Typewriter logging for prompt histories and backend outputs.
    *   *Interactive AI Chat*: Continuous bubble thread view for dialogue workspaces.
    *   *Automation Panel*: Quick buttons to trigger Python macros (System Resource Clean, news feeds, code indexing).
    *   *Master Event Console*: Live UTF-8 developer debug logs.
*   **Registry Customizer Modal**: Fully custom glassmorphic modal configuring voice synthesis speed, AI models, sound triggers, toggleable scanlines, background particle fields, and color theme profiles:
    *   `Electric Cyan & Purple` (Default Cyberpunk)
    *   `Solar Flare` (Cyber Hot Gold & Hot Red)
    *   `Matrix Code` (Classic Retro Green Terminal)
    *   `Deep Abyss` (Electric Blue & Dark Navy)

---

## 📁 File Structure

```text
d:/PROJECT/OPTIMUS/
├── index.html       # Structural layout, HUD modules, SVG rings & settings modals
├── style.css        # Glassmorphic layout grid, theme variable overrides & keyframes
├── script.js        # Web Audio engine, Particle Canvas, visualizer sines & Eel adapters
├── app.py           # Python Eel server, hardware psutil loop & NLP query resolver
└── README.md        # Technical specifications and setup documentation
```

---

## 🛠️ Setup and Installation

### Prerequisites
Make sure Python 3.7+ is installed on your computer.

1.  **Clone or navigate** to the project workspace:
    ```bash
    cd d:/PROJECT/OPTIMUS
    ```

2.  **Install requirements**:
    Install **Eel** for Python-to-JS communication, and optionally **psutil** to fetch your actual PC hardware stats (CPU/RAM) instead of random simulations.
    ```bash
    pip install eel psutil
    ```

3.  **Launch OPTIMUS**:
    Execute the Python server:
    ```bash
    python app.py
    ```

*Note: If Google Chrome is installed, Eel will open OPTIMUS in a dedicated chromeless app window. Otherwise, it will launch inside your default desktop browser.*

---

## 🔗 Eel Two-Way RPC Bindings

The application is pre-bound and ready for full two-way communication between Python and JavaScript:

### JavaScript Calling Python (Front-to-Back)
*   `eel.call_python_nlp(prompt)`: Routes console prompt box strings directly to Python NLP processors.

### Python Calling JavaScript (Back-to-Front)
*   `eel.displayResponse(responseText)`: Commands the frontend to show the AI response with typewriter effects and enter `SPEAKING` state.
*   `eel.updateTelemetryGauge(gaugeType, value)`: Feeds live CPU, RAM, or GPU sensor load values directly into the circular gauges.
*   `eel.logSystemEvent(eventMsg, severity)`: Appends warning, error, or standard runtime actions to the dashboard consoles.
