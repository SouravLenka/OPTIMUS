/**
 * OPTIMUS AI OS - CENTRAL LOGIC AND INTERACTIVE CONTROLLER
 * Includes background particle physics, Canvas-based audio-visualizer,
 * Web Audio sci-fi sound synthesizers, diagnostics fluctuations,
 * high-tech typewriter logs, theme registers, and Python-Eel bindings.
 */

// ==========================================================================
// 1. STATE AND CONSTANT CONFIGURATION
// ==========================================================================
const STATES = {
    IDLE: 'IDLE',
    LISTENING: 'LISTENING',
    THINKING: 'THINKING',
    SPEAKING: 'SPEAKING'
};

let currentAIState = STATES.IDLE;
let appSettings = {
    model: 'optimus-prime',
    continuousLearning: true,
    temperature: 0.4,
    voiceProfile: 'male-deep',
    soundEffects: true,
    micSensitivity: 70,
    theme: 'default-cyber',
    scanlines: true,
    bgParticles: true,
    eelRPC: true,
    startTray: false
};

// State labels and descriptors
const STATE_DESCRIPTORS = {
    [STATES.IDLE]: { label: 'SYSTEM ONLINE', sub: 'CLICK CORE OR MIC TO TRIGGER VOICE' },
    [STATES.LISTENING]: { label: 'LISTENING...', sub: 'AWAITING COMMAND CAPTURE' },
    [STATES.THINKING]: { label: 'THINKING...', sub: 'PROCESSING COGNITIVE PIPELINE' },
    [STATES.SPEAKING]: { label: 'OPTIMUS RESPONDING', sub: 'SYNTHESIZING VOCAL SYNAPSE' }
};

// ==========================================================================
// 2. WEB AUDIO API FUTURISTIC SOUND SYNTHESIS
// ==========================================================================
class CyberSoundEngine {
    constructor() {
        this.ctx = null;
        this.enabled = true;
    }

    init() {
        if (this.ctx) return;
        try {
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.warn("Web Audio API not supported by browser.", e);
        }
    }

    playClick() {
        if (!this.enabled || !appSettings.soundEffects) return;
        this.init();
        if (!this.ctx) return;

        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        
        osc.type = 'sine';
        osc.frequency.setValueAtTime(800, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(1600, this.ctx.currentTime + 0.08);
        
        gain.gain.setValueAtTime(0.06, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.08);
        
        osc.start();
        osc.stop(this.ctx.currentTime + 0.09);
    }

    playHover() {
        if (!this.enabled || !appSettings.soundEffects) return;
        this.init();
        if (!this.ctx) return;

        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        
        osc.type = 'sine';
        osc.frequency.setValueAtTime(1000, this.ctx.currentTime);
        osc.frequency.setValueAtTime(1200, this.ctx.currentTime + 0.02);
        
        gain.gain.setValueAtTime(0.015, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.04);
        
        osc.start();
        osc.stop(this.ctx.currentTime + 0.05);
    }

    playTransition(state) {
        if (!this.enabled || !appSettings.soundEffects) return;
        this.init();
        if (!this.ctx) return;

        const osc1 = this.ctx.createOscillator();
        const osc2 = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc1.connect(gain);
        osc2.connect(gain);
        gain.connect(this.ctx.destination);

        gain.gain.setValueAtTime(0.0, this.ctx.currentTime);
        gain.gain.linearRampToValueAtTime(0.05, this.ctx.currentTime + 0.05);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.4);

        if (state === STATES.LISTENING) {
            // High-pitched listening chime
            osc1.type = 'sine';
            osc1.frequency.setValueAtTime(900, this.ctx.currentTime);
            osc1.frequency.exponentialRampToValueAtTime(1800, this.ctx.currentTime + 0.25);
            osc2.type = 'triangle';
            osc2.frequency.setValueAtTime(450, this.ctx.currentTime);
            osc2.frequency.exponentialRampToValueAtTime(900, this.ctx.currentTime + 0.25);
        } else if (state === STATES.THINKING) {
            // Fast rhythmic processing sound
            osc1.type = 'triangle';
            osc1.frequency.setValueAtTime(300, this.ctx.currentTime);
            osc1.frequency.linearRampToValueAtTime(400, this.ctx.currentTime + 0.15);
            osc1.frequency.linearRampToValueAtTime(350, this.ctx.currentTime + 0.3);
            osc2.type = 'sine';
            osc2.frequency.setValueAtTime(600, this.ctx.currentTime);
            osc2.frequency.exponentialRampToValueAtTime(800, this.ctx.currentTime + 0.3);
        } else if (state === STATES.SPEAKING) {
            // Elegant speech pulse sound
            osc1.type = 'sine';
            osc1.frequency.setValueAtTime(1200, this.ctx.currentTime);
            osc1.frequency.exponentialRampToValueAtTime(600, this.ctx.currentTime + 0.3);
            osc2.type = 'sine';
            osc2.frequency.setValueAtTime(600, this.ctx.currentTime);
            osc2.frequency.exponentialRampToValueAtTime(300, this.ctx.currentTime + 0.3);
        } else {
            // Idle standby chimes
            osc1.type = 'sine';
            osc1.frequency.setValueAtTime(800, this.ctx.currentTime);
            osc1.frequency.exponentialRampToValueAtTime(400, this.ctx.currentTime + 0.3);
            osc2.type = 'sine';
            osc2.frequency.setValueAtTime(400, this.ctx.currentTime);
            osc2.frequency.exponentialRampToValueAtTime(200, this.ctx.currentTime + 0.3);
        }

        osc1.start();
        osc2.start();
        osc1.stop(this.ctx.currentTime + 0.4);
        osc2.stop(this.ctx.currentTime + 0.4);
    }

    playBootSweep() {
        this.init();
        if (!this.ctx) return;

        const osc = this.ctx.createOscillator();
        const filter = this.ctx.createBiquadFilter();
        const gain = this.ctx.createGain();

        osc.connect(filter);
        filter.connect(gain);
        gain.connect(this.ctx.destination);

        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(50, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(800, this.ctx.currentTime + 1.2);

        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(200, this.ctx.currentTime);
        filter.frequency.exponentialRampToValueAtTime(3000, this.ctx.currentTime + 1.2);

        gain.gain.setValueAtTime(0.0, this.ctx.currentTime);
        gain.gain.linearRampToValueAtTime(0.08, this.ctx.currentTime + 0.3);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 1.5);

        osc.start();
        osc.stop(this.ctx.currentTime + 1.5);
    }
}

const AudioSFX = new CyberSoundEngine();

// ==========================================================================
// 3. BACKGROUND CANVAS (GRID SYSTEM & FLOATING NEURAL STARS)
// ==========================================================================
class ParticleGridCanvas {
    constructor() {
        this.canvas = document.getElementById('bg-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.particleCount = 45;
        this.mouseX = 0;
        this.mouseY = 0;
        this.gridColor = 'rgba(0, 243, 255, 0.02)';
        this.starColor = 'rgba(0, 243, 255, 0.15)';
        this.lineColor = 'rgba(0, 243, 255, 0.04)';
        
        this.init();
        window.addEventListener('resize', () => this.resize());
        window.addEventListener('mousemove', (e) => this.trackMouse(e));
        this.animate();
    }

    init() {
        this.resize();
        this.particles = [];
        for (let i = 0; i < this.particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.4,
                vy: (Math.random() - 0.5) * 0.4,
                radius: Math.random() * 2 + 1,
                alpha: Math.random() * 0.5 + 0.2
            });
        }
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    trackMouse(e) {
        this.mouseX = e.clientX;
        this.mouseY = e.clientY;
    }

    drawGrid() {
        const step = 45;
        this.ctx.strokeStyle = this.gridColor;
        this.ctx.lineWidth = 1;

        // Draw horizontal grid lines
        for (let y = 0; y < this.canvas.height; y += step) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.canvas.width, y);
            this.ctx.stroke();
        }

        // Draw vertical grid lines
        for (let x = 0; x < this.canvas.width; x += step) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.canvas.height);
            this.ctx.stroke();
        }
    }

    updateColors() {
        // Adapt grid colors to theme
        if (document.body.classList.contains('theme-neon-fire')) {
            this.gridColor = 'rgba(255, 60, 0, 0.02)';
            this.starColor = 'rgba(255, 60, 0, 0.18)';
            this.lineColor = 'rgba(255, 60, 0, 0.04)';
        } else if (document.body.classList.contains('theme-matrix-code')) {
            this.gridColor = 'rgba(57, 255, 20, 0.015)';
            this.starColor = 'rgba(57, 255, 20, 0.2)';
            this.lineColor = 'rgba(57, 255, 20, 0.04)';
        } else if (document.body.classList.contains('theme-deep-abyss')) {
            this.gridColor = 'rgba(0, 90, 255, 0.03)';
            this.starColor = 'rgba(0, 90, 255, 0.2)';
            this.lineColor = 'rgba(0, 90, 255, 0.05)';
        } else {
            this.gridColor = 'rgba(0, 243, 255, 0.02)';
            this.starColor = 'rgba(0, 243, 255, 0.15)';
            this.lineColor = 'rgba(0, 243, 255, 0.04)';
        }
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.updateColors();
        this.drawGrid();

        if (!appSettings.bgParticles) {
            requestAnimationFrame(() => this.animate());
            return;
        }

        // Draw and update particle nodes
        this.particles.forEach((p, idx) => {
            p.x += p.vx;
            p.y += p.vy;

            // Bounce on boundaries
            if (p.x < 0 || p.x > this.canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > this.canvas.height) p.vy *= -1;

            // Particle glowing nodes
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = this.starColor;
            this.ctx.fill();

            // Connect lines between nearby nodes
            for (let j = idx + 1; j < this.particles.length; j++) {
                const p2 = this.particles[j];
                const dist = Math.hypot(p.x - p2.x, p.y - p2.y);
                if (dist < 130) {
                    const lineAlpha = (1 - (dist / 130)) * 0.45;
                    this.ctx.beginPath();
                    this.ctx.moveTo(p.x, p.y);
                    this.ctx.lineTo(p2.x, p2.y);
                    this.ctx.strokeStyle = this.lineColor;
                    this.ctx.lineWidth = 0.5;
                    this.ctx.stroke();
                }
            }

            // Interactive line pull to mouse
            const distMouse = Math.hypot(p.x - this.mouseX, p.y - this.mouseY);
            if (distMouse < 180) {
                const pullAlpha = (1 - (distMouse / 180)) * 0.35;
                this.ctx.beginPath();
                this.ctx.moveTo(p.x, p.y);
                this.ctx.lineTo(this.mouseX, this.mouseY);
                this.ctx.strokeStyle = this.lineColor;
                this.ctx.lineWidth = 0.5;
                this.ctx.stroke();
            }
        });

        requestAnimationFrame(() => this.animate());
    }
}

// ==========================================================================
// 4. CORE AUDIO WAVEFORM VISUALIZER
// ==========================================================================
class SinesWaveVisualizer {
    constructor() {
        this.canvas = document.getElementById('visualizer-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.phase = 0;
        this.waveSpeed = 0.05;
        this.waveAmplitude = 12;
        this.colorGradient = null;

        this.resize();
        window.addEventListener('resize', () => this.resize());
        this.render();
    }

    resize() {
        this.canvas.width = this.canvas.offsetWidth * window.devicePixelRatio;
        this.canvas.height = this.canvas.offsetHeight * window.devicePixelRatio;
        this.ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    }

    setColors() {
        const width = this.canvas.width / window.devicePixelRatio;
        this.colorGradient = this.ctx.createLinearGradient(0, 0, width, 0);

        if (document.body.classList.contains('theme-neon-fire')) {
            this.colorGradient.addColorStop(0, 'rgba(255, 7, 58, 0.05)');
            this.colorGradient.addColorStop(0.5, 'rgba(255, 60, 0, 0.85)');
            this.colorGradient.addColorStop(1, 'rgba(255, 234, 0, 0.05)');
        } else if (document.body.classList.contains('theme-matrix-code')) {
            this.colorGradient.addColorStop(0, 'rgba(2, 20, 4, 0.05)');
            this.colorGradient.addColorStop(0.5, 'rgba(57, 255, 20, 0.85)');
            this.colorGradient.addColorStop(1, 'rgba(0, 255, 102, 0.05)');
        } else if (document.body.classList.contains('theme-deep-abyss')) {
            this.colorGradient.addColorStop(0, 'rgba(0, 38, 153, 0.05)');
            this.colorGradient.addColorStop(0.5, 'rgba(0, 90, 255, 0.85)');
            this.colorGradient.addColorStop(1, 'rgba(0, 243, 255, 0.05)');
        } else {
            this.colorGradient.addColorStop(0, 'rgba(189, 0, 255, 0.05)');
            this.colorGradient.addColorStop(0.5, 'rgba(0, 243, 255, 0.85)');
            this.colorGradient.addColorStop(1, 'rgba(189, 0, 255, 0.05)');
        }
    }

    render() {
        const width = this.canvas.width / window.devicePixelRatio;
        const height = this.canvas.height / window.devicePixelRatio;
        const centerY = height / 2;

        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.setColors();

        // Adjust sines dynamics based on active state variables
        if (currentAIState === STATES.IDLE) {
            this.waveAmplitude = 4;
            this.waveSpeed = 0.03;
        } else if (currentAIState === STATES.LISTENING) {
            // Loud voice capture simulation
            this.waveAmplitude = 22 + Math.sin(Date.now() * 0.015) * 8;
            this.waveSpeed = 0.16;
        } else if (currentAIState === STATES.THINKING) {
            // Complex processing phase spikes
            this.waveAmplitude = 8 + Math.cos(Date.now() * 0.005) * 4;
            this.waveSpeed = 0.09;
        } else if (currentAIState === STATES.SPEAKING) {
            // Rhythmic speech simulation
            this.waveAmplitude = 16 + Math.abs(Math.sin(Date.now() * 0.008)) * 14;
            this.waveSpeed = 0.07;
        }

        this.phase += this.waveSpeed;

        // Draw multiple stacked waves
        this.drawWave(width, centerY, this.waveAmplitude, this.phase, 1.2, 0.3);
        this.drawWave(width, centerY, this.waveAmplitude * 0.65, -this.phase * 0.8, 1.8, 0.15);
        this.drawWave(width, centerY, this.waveAmplitude * 0.45, this.phase * 1.3, 2.4, 0.1);

        requestAnimationFrame(() => this.render());
    }

    drawWave(width, centerY, maxAmp, phase, frequency, opacity) {
        this.ctx.beginPath();
        this.ctx.moveTo(0, centerY);

        for (let x = 0; x < width; x++) {
            // Fade waves smoothly to 0 on margins (edge-fading sine)
            const edgeFade = Math.sin((x / width) * Math.PI);
            const y = centerY + Math.sin((x * 0.02 * frequency) + phase) * maxAmp * edgeFade;
            this.ctx.lineTo(x, y);
        }

        this.ctx.lineWidth = 2.5;
        this.ctx.strokeStyle = this.colorGradient;
        this.ctx.globalAlpha = opacity;
        this.ctx.stroke();
        this.ctx.globalAlpha = 1.0;
    }
}

// ==========================================================================
// 5. CORE STATE MANAGEMENT ENGINE
// ==========================================================================
function updateAssistantState(state) {
    if (!STATES[state]) {
        console.error(`Invalid state assignment: ${state}`);
        return;
    }

    const prev = currentAIState;
    currentAIState = state;

    // Log update transition
    console.log(`[SYS] Transitioning state: ${prev} -> ${currentAIState}`);
    
    // Play transition sound chime
    AudioSFX.playTransition(currentAIState);

    // Update center Core Stage element styling
    const coreContainer = document.querySelector('.core-stage-container');
    if (coreContainer) {
        coreContainer.className = 'core-stage-container';
        coreContainer.classList.add(`core-state-${state.toLowerCase()}`);
    }

    // Update status labels
    const stateText = document.getElementById('current-state-text');
    const orbLabel = document.getElementById('orb-mode-label');
    const orbSub = document.getElementById('orb-sub-text');

    if (stateText) stateText.textContent = state;
    if (orbLabel) {
        orbLabel.textContent = STATE_DESCRIPTORS[state].label;
        // Swap glow accents
        if (state === STATES.THINKING || state === STATES.SPEAKING) {
            orbLabel.className = 'orb-mode-label purple-glow';
        } else {
            orbLabel.className = 'orb-mode-label cyan-glow';
        }
    }
    if (orbSub) orbSub.textContent = STATE_DESCRIPTORS[state].sub;

    // Mic button active states mapping
    const micBtn = document.getElementById('mic-activation-btn');
    const ripple = document.getElementById('voice-ripple');
    
    if (micBtn && ripple) {
        if (state === STATES.LISTENING) {
            micBtn.classList.add('active');
            ripple.classList.add('active');
        } else {
            micBtn.classList.remove('active');
            ripple.classList.remove('active');
        }
    }
}

// ==========================================================================
// 6. HUD REAL-TIME TELEMETRY DIAGNOSTICS
// ==========================================================================
function startTelemetryLoops() {
    // 1. Time / Date Clock updater
    setInterval(() => {
        const timeVal = document.getElementById('hud-time');
        const dateVal = document.getElementById('hud-date');
        
        const now = new Date();
        let hours12 = now.getHours() % 12;
        hours12 = hours12 ? hours12 : 12; // Convert 0 to 12
        const ampm = now.getHours() >= 12 ? 'PM' : 'AM';
        
        const hours = String(hours12).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        
        if (timeVal) timeVal.textContent = `${hours}:${minutes}:${seconds} ${ampm}`;

        if (dateVal) {
            const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
            const days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
            
            const dayName = days[now.getDay()];
            const monthName = months[now.getMonth()];
            const dayNum = now.getDate();
            
            dateVal.textContent = `${dayName} / ${monthName} ${dayNum}`;
        }
    }, 1000);

    // 2. Mocking fluctuational hardware load
    setInterval(() => {
        if (currentAIState === STATES.THINKING) {
            // Heavy processing CPU spike simulation
            animateCircularGauge('cpu-gauge', 'cpu-value', Math.floor(Math.random() * 20) + 72);
            animateCircularGauge('ram-gauge', 'ram-value', Math.floor(Math.random() * 4) + 64);
            updateLinearProgress('gpu-progress-bar', 'gpu-val-text', Math.floor(Math.random() * 15) + 68, '%');
        } else {
            // Calm fluctuation idling
            animateCircularGauge('cpu-gauge', 'cpu-value', Math.floor(Math.random() * 12) + 26);
            animateCircularGauge('ram-gauge', 'ram-value', Math.floor(Math.random() * 3) + 54);
            updateLinearProgress('gpu-progress-bar', 'gpu-val-text', Math.floor(Math.random() * 8) + 14, '%');
        }

        // Temperature variations
        const activeTemp = Math.floor(Math.random() * 6) + 42;
        updateLinearProgress('temp-progress-bar', 'temp-val-text', activeTemp, '°C');
    }, 3000);
}

function animateCircularGauge(gaugeId, valId, targetVal) {
    const gauge = document.getElementById(gaugeId);
    const valueText = document.getElementById(valId);
    if (!gauge || !valueText) return;

    valueText.textContent = `${targetVal}%`;

    // Formula: dashoffset = circumference - (percent / 100 * circumference)
    // r=40 -> circumference = 2 * PI * 40 ≈ 251.2
    const circumference = 251.2;
    const offset = circumference - (targetVal / 100 * circumference);
    gauge.style.strokeDashoffset = offset;
}

function updateLinearProgress(barId, labelId, val, unit = '') {
    const bar = document.getElementById(barId);
    const label = document.getElementById(labelId);
    if (bar) bar.style.width = `${val}%`;
    if (label) label.textContent = `${val}${unit}`;
}

// ==========================================================================
// 7. HIGH-TECH LOG history WRITER & CHAT ENGINE
// ==========================================================================
function writeTerminalLine(source, tag, message, type = 'system-line') {
    const history = document.getElementById('hud-terminal-history');
    if (!history) return;

    // Get active time stamp
    const now = new Date();
    const ts = `[${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}]`;

    const line = document.createElement('div');
    line.className = `terminal-line ${type}`;

    const tagColor = source === 'USER' ? 'bg-cyan' : source === 'OPTIMUS' ? 'bg-purple' : 'bg-blue';

    line.innerHTML = `
        <span class="term-time">${ts}</span>
        <span class="term-tag ${tagColor}">${tag}</span>
        <span class="term-msg"></span>
    `;

    history.appendChild(line);

    // Apply glowing border flash on creation
    line.style.boxShadow = `0 0 10px rgba(0, 243, 255, 0.15)`;
    setTimeout(() => { line.style.boxShadow = 'none'; }, 500);

    const msgElement = line.querySelector('.term-msg');
    
    // Typewriter effect on bot lines, immediate rendering on standard systems
    if (source === 'OPTIMUS') {
        typewriterEffect(msgElement, message, 35, () => {
            updateAssistantState(STATES.IDLE);
        });
    } else {
        msgElement.textContent = message;
    }

    // Scroll to bottom
    history.scrollTop = history.scrollHeight;

    // Sync to System Master console debug page as well
    writeMasterConsoleLog(ts, tag, message, source);
}

function writeMasterConsoleLog(timestamp, tag, msg, source) {
    const masterLog = document.getElementById('master-console-logs');
    if (!masterLog) return;

    const log = document.createElement('div');
    let logType = 'info';

    if (source === 'SYS') logType = 'sys';
    else if (source === 'OPTIMUS') logType = 'ok';
    else if (tag === 'WARN') logType = 'warn';
    else if (tag === 'ERROR') logType = 'err';

    log.className = `log-entry ${logType}`;
    log.innerHTML = `<span class="log-t">${timestamp}</span> <span class="log-m">[${tag}] ${msg}</span>`;
    
    masterLog.appendChild(log);
    masterLog.scrollTop = masterLog.scrollHeight;
}

function typewriterEffect(element, text, speed = 25, callback = null) {
    let i = 0;
    element.textContent = '';
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        } else if (callback) {
            callback();
        }
    }
    type();
}

// Dialog Bubbles Generator for the interactive Chat tab
function appendChatBubble(sender, text) {
    const container = document.getElementById('chat-messages-container');
    if (!container) return;

    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${sender === 'USER' ? 'user-message' : 'bot-message'}`;

    const now = new Date();
    const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;

    const avatar = sender === 'USER' ? 'U' : 'Ω';

    bubble.innerHTML = `
        <div class="msg-avatar">${avatar}</div>
        <div class="msg-content">
            <p>${text}</p>
            <span class="msg-time">${timeStr}</span>
        </div>
    `;

    container.appendChild(bubble);
    container.scrollTop = container.scrollHeight;
}

// Resolve user terminal input & trigger simulated diagnostics / python fallback
function processUserCommand(cmdText) {
    if (!cmdText.trim()) return;

    // Show input in logs and chats
    writeTerminalLine('USER', 'USER', cmdText, 'command-line');
    appendChatBubble('USER', cmdText);

    // Transition to thinking state
    updateAssistantState(STATES.THINKING);

    // If Eel is loaded and user wants RPC, try targeting Python
    if (typeof eel !== 'undefined' && appSettings.eelRPC) {
        console.log(`Dispatching prompt to Python Eel engine: "${cmdText}"`);
        try {
            // Assume Python exposed function: call_python_nlp(prompt)
            eel.call_python_nlp(cmdText)();
            return;
        } catch (err) {
            console.error("Failed executing Eel Python RPC trigger. Falling back to simulated brains.", err);
        }
    }

    // Local simulated Response Parser
    setTimeout(() => {
        updateAssistantState(STATES.SPEAKING);
        const query = cmdText.toLowerCase().trim();
        let response = '';

        if (query === 'diagnostics' || query === 'run diagnostics' || query.includes('check')) {
            response = "INITIATING HARDWARE INTEGRITY SCRIPTS... Kernels verified. CPU temperatures nominal. Neural memory register allocated. Disk sectors clean. Security parameters at 100%. Optimus operates at maximum calibration.";
        } else if (query === 'load' || query.includes('system load') || query.includes('utilization')) {
            const cpu = document.getElementById('cpu-value').textContent;
            const ram = document.getElementById('ram-value').textContent;
            response = `Diagnostics telemetry fetch: CPU Load is currently throttling at ${cpu}, RAM dynamic footprint sits at ${ram}. Running processes remain index-cached under system tray constraints.`;
        } else if (query.includes('weather')) {
            response = "Optimus telemetry satellites map atmospheric models: Current sector climate registered at 22°C under clear cyber-circuit atmospheric guidelines.";
        } else if (query.includes('clear')) {
            const history = document.getElementById('hud-terminal-history');
            const logs = document.getElementById('master-console-logs');
            if (history) history.innerHTML = `<div class="terminal-line system-line"><span class="term-time">[${Date.now()}]</span> <span class="term-tag bg-blue">SYS</span> <span class="term-msg">LOG FILE BUFFER REFLUSHED.</span></div>`;
            if (logs) logs.innerHTML = '';
            response = "Diagnostic consoles flushed and indices cleared.";
        } else {
            response = `Input directive categorized. Process mapped to neural weight pipeline. Simulated NLP matches criteria for index registers. Under a Python integration layer, this request parses directly into a background sub-script.`;
        }

        writeTerminalLine('OPTIMUS', 'OPTIMUS', response, 'response-line');
        appendChatBubble('OPTIMUS', response);
    }, 1500);
}

// ==========================================================================
// 8. SIDEBAR TABS & HUD SETTINGS TRIGGERS
// ==========================================================================
function setupUIInteractions() {
    // 1. Sidebar tab switcher
    const navButtons = document.querySelectorAll('.nav-btn');
    const tabs = document.querySelectorAll('.hud-tab');

    navButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const tabId = btn.getAttribute('data-tab');
            if (!tabId) return; // Settings or non-tab triggers

            AudioSFX.playClick();

            // Set active buttons
            navButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Swap active dashboard tabs
            tabs.forEach(t => t.classList.remove('active'));
            const activeTab = document.getElementById(`tab-${tabId}`);
            if (activeTab) activeTab.classList.add('active');
        });

        btn.addEventListener('mouseenter', () => AudioSFX.playHover());
    });

    // 2. Quick Command Button triggers
    const quickCmds = document.querySelectorAll('.quick-cmd-btn');
    quickCmds.forEach(btn => {
        btn.addEventListener('click', () => {
            AudioSFX.playClick();
            const cmd = btn.getAttribute('data-cmd');
            const input = document.getElementById('command-input');
            if (input) {
                input.value = cmd;
                document.getElementById('command-form-submit').requestSubmit();
            }
        });
        btn.addEventListener('mouseenter', () => AudioSFX.playHover());
    });

    // 3. Settings Modal switches toggling
    const settingsBtn = document.getElementById('open-settings-btn');
    const settingsModal = document.getElementById('settings-modal');
    const closeSettings = document.getElementById('close-settings-btn');
    const cancelSettings = document.getElementById('settings-cancel-btn');
    const saveSettings = document.getElementById('settings-save-btn');

    const toggleModal = (show) => {
        AudioSFX.playClick();
        if (show) {
            settingsModal.classList.remove('hidden');
            // Sync form states with registry
            document.getElementById('setting-ai-model').value = appSettings.model;
            document.getElementById('setting-learning').checked = appSettings.continuousLearning;
            document.getElementById('setting-temp').value = appSettings.temperature;
            document.getElementById('temp-val').textContent = appSettings.temperature;
            document.getElementById('setting-voice').value = appSettings.voiceProfile;
            document.getElementById('setting-sounds').checked = appSettings.soundEffects;
            document.getElementById('setting-mic-sens').value = appSettings.micSensitivity;
            document.getElementById('setting-color-theme').value = appSettings.theme;
            document.getElementById('setting-scanlines').checked = appSettings.scanlines;
            document.getElementById('setting-bg-particles').checked = appSettings.bgParticles;
            document.getElementById('setting-eel-rpc').checked = appSettings.eelRPC;
            document.getElementById('setting-startup').checked = appSettings.startTray;
        } else {
            settingsModal.classList.add('hidden');
        }
    };

    if (settingsBtn) settingsBtn.addEventListener('click', () => toggleModal(true));
    if (closeSettings) closeSettings.addEventListener('click', () => toggleModal(false));
    if (cancelSettings) cancelSettings.addEventListener('click', () => toggleModal(false));
    
    if (saveSettings) {
        saveSettings.addEventListener('click', () => {
            // Apply updates
            appSettings.model = document.getElementById('setting-ai-model').value;
            appSettings.continuousLearning = document.getElementById('setting-learning').checked;
            appSettings.temperature = parseFloat(document.getElementById('setting-temp').value);
            appSettings.voiceProfile = document.getElementById('setting-voice').value;
            appSettings.soundEffects = document.getElementById('setting-sounds').checked;
            appSettings.micSensitivity = parseInt(document.getElementById('setting-mic-sens').value);
            appSettings.theme = document.getElementById('setting-color-theme').value;
            appSettings.scanlines = document.getElementById('setting-scanlines').checked;
            appSettings.bgParticles = document.getElementById('setting-bg-particles').checked;
            appSettings.eelRPC = document.getElementById('setting-eel-rpc').checked;
            appSettings.startTray = document.getElementById('setting-startup').checked;

            // Apply Theme color modifications on body
            document.body.className = '';
            if (appSettings.theme !== 'default-cyber') {
                document.body.classList.add(`theme-${appSettings.theme.replace('setting-', '')}`);
            }

            // Apply holographic scanlines
            const scanlines = document.querySelector('.scanlines');
            if (scanlines) {
                if (appSettings.scanlines) scanlines.classList.remove('disabled');
                else scanlines.classList.add('disabled');
            }

            // Persist to Python backend registry via Eel RPC
            if (typeof eel !== 'undefined' && appSettings.eelRPC) {
                try {
                    eel.trigger_settings_save(appSettings)();
                } catch (err) {
                    console.error("[EEL] Failed dispatching settings to backend:", err);
                }
            }

            toggleModal(false);
            showSystemNotification("SETTINGS UPDATED", "Optimus registry database recalibrated successfully.");
        });
    }

    // Range dynamic numeric slider
    const tempRange = document.getElementById('setting-temp');
    if (tempRange) {
        tempRange.addEventListener('input', (e) => {
            document.getElementById('temp-val').textContent = e.target.value;
        });
    }

    // Modal Submenus Tab switching inside settings
    const setMenuBtns = document.querySelectorAll('.set-menu-btn');
    const setSections = document.querySelectorAll('.settings-section');
    setMenuBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            AudioSFX.playClick();
            setMenuBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const secId = btn.getAttribute('data-sec');
            setSections.forEach(s => s.classList.remove('active'));
            const targetSec = document.getElementById(secId);
            if (targetSec) targetSec.classList.add('active');
        });
    });

    // 4. Form Submit command input
    const commandForm = document.getElementById('command-form-submit');
    const cmdInput = document.getElementById('command-input');
    if (commandForm && cmdInput) {
        commandForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const text = cmdInput.value;
            if (text.trim()) {
                cmdInput.value = '';
                processUserCommand(text);
            }
        });
    }

    // 5. Interactive Voice Activation (Microphone toggle click)
    const micBtn = document.getElementById('mic-activation-btn');
    const coreTrigger = document.getElementById('core-interactive-trigger');

    const toggleVoiceCapture = () => {
        AudioSFX.playClick();
        if (currentAIState === STATES.IDLE) {
            // Trigger Listening
            updateAssistantState(STATES.LISTENING);
            
            // Simulating audio timeout voice completion
            setTimeout(() => {
                if (currentAIState === STATES.LISTENING) {
                    updateAssistantState(STATES.THINKING);
                    setTimeout(() => {
                        updateAssistantState(STATES.SPEAKING);
                        const voices = [
                            "Optimus audio receptors captured stream. Processing voice synthetics... Dynamic checks confirm thread integrity.",
                            "Directive successfully parsed via voice channel bindings. Execution vectors compiling in background Python threads.",
                            "Vocal query resolved. Optimus brain systems show zero memory leakage during parsing."
                        ];
                        const resp = voices[Math.floor(Math.random() * voices.length)];
                        writeTerminalLine('OPTIMUS', 'OPTIMUS', resp, 'response-line');
                        appendChatBubble('OPTIMUS', resp);
                    }, 1400);
                }
            }, 5000); // 5s recording sweep
        } else {
            // Force return to Idle if clicking again
            updateAssistantState(STATES.IDLE);
        }
    };

    if (micBtn) micBtn.addEventListener('click', toggleVoiceCapture);
    if (coreTrigger) coreTrigger.addEventListener('click', toggleVoiceCapture);

    // 6. Automation Routine Runs Trigger
    const runAutoBtns = document.querySelectorAll('.run-automation-btn');
    runAutoBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            AudioSFX.playClick();
            const task = btn.getAttribute('data-task');
            // Notify user that macro is being dispatched
            showSystemNotification("AUTOMATION TRIGGERED", `Running background macro: ${task}`);
            writeTerminalLine('SYS', 'MACRO', `DISPATCHING THREAD BIND: "${task}"...`, 'system-line');
            // Attempt to invoke backend macro via Eel
            if (typeof eel !== 'undefined' && eel.run_macro_task) {
                try {
                    eel.run_macro_task(task)();
                } catch (err) {
                    console.error('Eel macro execution failed, falling back to simulation.', err);
                    // fallback simulation
                    showSystemNotification("MACRO EXECUTED", `Successfully finalized: ${task}`);
                    writeTerminalLine('SYS', 'OK', `Macro execution finalized: ${task} [EXIT 0]`, 'system-line');
                }
            } else {
                // Fallback simulation when Eel is not available
                showSystemNotification("MACRO EXECUTED", `Successfully finalized: ${task}`);
                writeTerminalLine('SYS', 'OK', `Macro execution finalized: ${task} [EXIT 0]`, 'system-line');
            }
        });
    });
    // 7. Clear chat workspace buttons
    const clearChat = document.getElementById('clear-chat-btn');
    if (clearChat) {
        clearChat.addEventListener('click', () => {
            AudioSFX.playClick();
            const container = document.getElementById('chat-messages-container');
            if (container) {
                container.innerHTML = `
                    <div class="chat-bubble bot-message">
                        <div class="msg-avatar">Ω</div>
                        <div class="msg-content">
                            <p>Dialogue workspaces reinitialized. Optimus is standby.</p>
                            <span class="msg-time">${new Date().toLocaleTimeString()}</span>
                        </div>
                    </div>
                `;
            }
        });
    }

    // 8. General click SFX for normal hover interactive items
    const elementsToSound = document.querySelectorAll('button, select, input[type="checkbox"], input[type="range"]');
    elementsToSound.forEach(el => {
        el.addEventListener('mouseenter', () => AudioSFX.playHover());
    });
}

// System notifications HUD popup drawer
function showSystemNotification(title, message) {
    const notif = document.getElementById('sys-notification');
    const notifTitle = document.getElementById('notif-title');
    const notifMsg = document.getElementById('notif-message');

    if (!notif) return;

    notifTitle.textContent = title.toUpperCase();
    notifMsg.textContent = message;

    notif.classList.add('active');

    // Automatically draw back inside after 4s
    setTimeout(() => {
        notif.classList.remove('active');
    }, 4000);
}

// ==========================================================================
// 9. DIAGNOSTIC INITIAL BOOT TIMELINE SEQUENCE
// ==========================================================================
function orchestrateStartupSequence() {
    const boot = document.getElementById('boot-screen');
    const progress = document.getElementById('boot-progress');
    const statusText = document.getElementById('boot-status-text');
    const percent = document.getElementById('boot-percent');
    const logs = document.getElementById('boot-log');
    
    if (!boot || !progress || !statusText || !percent || !logs) {
        // Fallback if missing
        document.getElementById('app-container').classList.remove('hidden');
        return;
    }

    const bootSteps = [
        { pct: 10, label: 'CHECKING SYSTEM KERNEL CONFIG...', log: 'Kernel parameters detected: V4.9 // CORE.SYS' },
        { pct: 25, label: 'LOADING NEURAL NET WEIGHTS...', log: 'Weights mapping: optimus_brain_v3.bin index loaded.' },
        { pct: 45, label: 'INITIALIZING INTERACTION CHANNELS...', log: 'Voice synthesis voices calibrated. Vocals: male-deep.' },
        { pct: 60, label: 'CONNECTING PYTHON EEL INTEROP SOCKET...', log: 'Eel RPC Server online. Establishing WS hooks on port 8000.' },
        { pct: 85, label: 'COMPILING HOLOGRAM HUD OVERLAYS...', log: 'Dashboard grids and shaders linked successfully.' },
        { pct: 100, label: 'CALIBRATION COMPLETE. STARTING SYSTEM...', log: 'All parameters initialized. Starting OPTIMUS OS.' }
    ];

    let currentStep = 0;

    // Trigger boot sci-fi sweep sound
    setTimeout(() => {
        AudioSFX.playBootSweep();
    }, 200);

    function runNextStep() {
        if (currentStep < bootSteps.length) {
            const step = bootSteps[currentStep];
            
            // Animate labels and progresses
            progress.style.width = `${step.pct}%`;
            percent.textContent = `${step.pct}%`;
            statusText.textContent = step.label;

            // Write logs inside loader terminal
            const p = document.createElement('p');
            p.className = 'log-line text-cyan';
            p.textContent = `> ${step.log}`;
            logs.appendChild(p);
            logs.scrollTop = logs.scrollHeight;

            currentStep++;
            // Randomized realistic delay times
            const delay = Math.random() * 400 + 350;
            setTimeout(runNextStep, delay);
        } else {
            // Finalize sequence
            setTimeout(() => {
                boot.style.opacity = '0';
                
                // Switch display states
                setTimeout(() => {
                    boot.classList.add('hidden');
                    const app = document.getElementById('app-container');
                    app.classList.remove('hidden');
                    
                    // Trigger Lucide icons replacing
                    lucide.createIcons();

                    // Start telemetry clocks and fluctuating metrics loops
                    startTelemetryLoops();

                    // Trigger active chimes
                    AudioSFX.playTransition(STATES.IDLE);

                    // Show boot welcome notification
                    showSystemNotification("OPTIMUS OS ONLINE", "Futuristic cyber assistant is active and listening.");
                }, 800);
            }, 600);
        }
    }

    setTimeout(runNextStep, 500);
}

// ==========================================================================
// 10. EEL INTEROP BRIDGE (FOR PYTHON INTERACTION WORK)
// ==========================================================================
// Check if Python Eel is active and bind functions
window.addEventListener('load', () => {
    // 1. Launch Particle backgrounds and wave canvas
    new ParticleGridCanvas();
    new SinesWaveVisualizer();

    // 2. Bind all custom button clicks and form inputs
    setupUIInteractions();

    // 3. Initiate startup boot timeline sequence
    orchestrateStartupSequence();

    // Eel validation hooks
    if (typeof eel !== 'undefined') {
        const sidebarStatus = document.querySelector('.connection-status');
        if (sidebarStatus) {
            sidebarStatus.className = 'connection-status connected';
            const name = sidebarStatus.querySelector('.status-name');
            if (name) name.textContent = 'EEL: PYTHON';
        }
        console.log("Optimus OS connected successfully to Eel Python backend framework.");
        if (eel._frontend_ready) {
            eel._frontend_ready()();
        }
    }
});

// JavaScript integration functions exposed to Eel Python calls later
if (typeof eel !== 'undefined') {
    // 1. Exposing Assistant response printouts
    eel.expose(displayResponse, 'displayResponse');
    function displayResponse(responseText) {
        updateAssistantState(STATES.SPEAKING);
        writeTerminalLine('OPTIMUS', 'OPTIMUS', responseText, 'response-line');
        appendChatBubble('OPTIMUS', responseText);
    }

    // 2. Exposing state controllers
    eel.expose(updateAssistantState, 'updateAssistantState');
    
    // 3. Exposing system status widgets overrides
    eel.expose(updateTelemetryGauge, 'updateTelemetryGauge');
    function updateTelemetryGauge(gaugeType, value) {
        if (gaugeType === 'cpu') {
            animateCircularGauge('cpu-gauge', 'cpu-value', value);
        } else if (gaugeType === 'ram') {
            animateCircularGauge('ram-gauge', 'ram-value', value);
        } else if (gaugeType === 'gpu') {
            updateLinearProgress('gpu-progress-bar', 'gpu-val-text', value, '%');
        }
    }

    // 4. Trigger system actions via logs printout
    eel.expose(logSystemEvent, 'logSystemEvent');
    function logSystemEvent(eventMsg, severity = 'INFO') {
        let logType = 'system-line';
        if (severity === 'WARN') logType = 'alert-line text-yellow';
        else if (severity === 'ERROR') logType = 'alert-line text-red';
        
        writeTerminalLine('SYS', severity, eventMsg, logType);
    }

    // 5. Exposing top status bar updaters
    eel.expose(updateSystemStatus, 'updateSystemStatus');
    function updateSystemStatus(wifiOnline, batteryPercent) {
        const wifiIcon = document.getElementById('wifi-icon');
        const wifiText = document.getElementById('network-text');
        const battText = document.getElementById('battery-percent');
        
        if (wifiText) wifiText.textContent = wifiOnline ? 'ONLINE' : 'OFFLINE';
        if (wifiIcon) {
            if (wifiOnline) {
                wifiIcon.className = 'lucide lucide-wifi text-cyan';
            } else {
                wifiIcon.className = 'lucide lucide-wifi-off text-red';
            }
        }
        
        if (battText) battText.textContent = `${batteryPercent}%`;
    }
}
