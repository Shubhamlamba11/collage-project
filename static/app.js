document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const voiceBtn = document.getElementById('voice-btn');
    const clearBtn = document.getElementById('clear-btn');
    const clockDisplay = document.getElementById('clock-display');
    const arcReactor = document.getElementById('arc-reactor');
    const arcStatus = document.getElementById('arc-status');
    const metricLatency = document.getElementById('metric-latency');
    const apiKeyInput = document.getElementById('api-key-input');
    const saveKeyBtn = document.getElementById('save-key-btn');
    const keyStatusMsg = document.getElementById('key-status-msg');

    // Speech Recognition Setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;
    let isListening = false;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            isListening = true;
            voiceBtn.classList.add('listening');
            arcReactor.classList.add('active');
            arcStatus.innerText = 'LISTENING...';
        };

        recognition.onend = () => {
            isListening = false;
            voiceBtn.classList.remove('listening');
            arcReactor.classList.remove('active');
            arcStatus.innerText = 'STATIONARY';
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            sendMessage(transcript);
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            isListening = false;
            voiceBtn.classList.remove('listening');
            arcReactor.classList.remove('active');
            arcStatus.innerText = 'ERROR';
        };
    } else {
        voiceBtn.style.display = 'none';
        console.warn('Web Speech API not supported in this browser.');
    }

    // Text-to-Speech Synthesis
    function speakText(text) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel(); // Stop any ongoing speech
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 1.0;
            utterance.pitch = 0.9;

            // Try to find a good robotic/clear voice
            const voices = window.speechSynthesis.getVoices();
            const preferredVoice = voices.find(v => v.name.includes('Google UK English Male') || v.name.includes('Daniel') || v.name.includes('David') || v.lang.startsWith('en'));
            if (preferredVoice) utterance.voice = preferredVoice;

            utterance.onstart = () => {
                arcReactor.classList.add('active');
                arcStatus.innerText = 'SPEAKING...';
            };
            utterance.onend = () => {
                arcReactor.classList.remove('active');
                arcStatus.innerText = 'STATIONARY';
            };

            window.speechSynthesis.speak(utterance);
        }
    }

    // Live Clock Display
    function updateClock() {
        const now = new Date();
        clockDisplay.innerText = now.toLocaleTimeString();
    }
    setInterval(updateClock, 1000);
    updateClock();

    // Append Message to Chat UI
    function appendMessage(sender, text, isUser = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-message ${isUser ? 'user-msg' : 'assistant-msg'}`;

        const iconClass = isUser ? 'fa-user' : 'fa-robot';
        const senderName = isUser ? 'YOU' : 'J.A.R.V.I.S.';

        msgDiv.innerHTML = `
            <div class="msg-avatar"><i class="fas ${iconClass}"></i></div>
            <div class="msg-content">
                <div class="msg-sender">${senderName}</div>
                <div class="msg-text">${escapeHtml(text)}</div>
            </div>
        `;

        chatWindow.appendChild(msgDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function escapeHtml(text) {
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;")
            .replace(/\n/g, "<br>");
    }

    // Send Message Handler
    async function sendMessage(text) {
        const message = text || userInput.value.trim();
        if (!message) return;

        appendMessage('User', message, true);
        userInput.value = '';

        arcReactor.classList.add('active');
        arcStatus.innerText = 'PROCESSING...';

        try {
            const apiKey = localStorage.getItem('gemini_api_key') || '';
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message, api_key: apiKey })
            });

            const data = await res.json();
            if (data.status === 'success') {
                appendMessage('JARVIS', data.response, false);
                metricLatency.innerText = `${data.latency_ms} ms`;
                speakText(data.response);
            } else {
                appendMessage('JARVIS', 'An error occurred processing your request.', false);
            }
        } catch (err) {
            console.error('Chat API Error:', err);
            appendMessage('JARVIS', 'Unable to reach backend telemetry core.', false);
        } finally {
            arcReactor.classList.remove('active');
            arcStatus.innerText = 'STATIONARY';
        }
    }

    // Event Listeners
    sendBtn.addEventListener('click', () => sendMessage());
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    voiceBtn.addEventListener('click', () => {
        if (!recognition) return;
        if (isListening) {
            recognition.stop();
        } else {
            recognition.start();
        }
    });

    clearBtn.addEventListener('click', async () => {
        try {
            await fetch('/api/history', { method: 'DELETE' });
            chatWindow.innerHTML = '';
            appendMessage('JARVIS', 'Memory cleared and reset, sir.', false);
        } catch (e) {
            console.error('Failed to clear memory', e);
        }
    });

    // Quick Skill Buttons
    document.querySelectorAll('.skill-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const query = btn.getAttribute('data-query');
            sendMessage(query);
        });
    });

    // Save API Key locally and notify backend
    saveKeyBtn.addEventListener('click', async () => {
        const key = apiKeyInput.value.trim();
        if (key) {
            localStorage.setItem('gemini_api_key', key);
            try {
                const res = await fetch('/api/config', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ gemini_api_key: key })
                });
                const data = await res.json();
                keyStatusMsg.innerText = data.message || 'Key saved successfully.';
                keyStatusMsg.style.color = 'var(--success)';
            } catch (e) {
                keyStatusMsg.innerText = 'Failed to update key on server.';
                keyStatusMsg.style.color = 'var(--danger)';
            }
        }
    });

    // Load saved API key on startup
    const savedKey = localStorage.getItem('gemini_api_key');
    if (savedKey) {
        apiKeyInput.value = savedKey;
        keyStatusMsg.innerText = 'Loaded key from local storage.';
        keyStatusMsg.style.color = 'var(--cyan-glow)';
    }
});
