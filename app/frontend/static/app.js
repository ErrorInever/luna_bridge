function isJapanese(text) {
    return /[\u3040-\u30ff\u4e00-\u9faf]/.test(text);
}

const ws = new WebSocket("ws://127.0.0.1:8000/ws");
const container = document.getElementById("container");

ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);

    const div = document.createElement("div");
    div.className = "msg";

    div.innerHTML = `
        <div>${msg.text}</div>
    `;

    container.appendChild(div);
};

const fontSelect = document.getElementById("fontSizeSelect");

fontSelect.addEventListener("change", (e) => {
    const size = e.target.value + "px";
    document.documentElement.style.setProperty("--msg-font-size", size);
});

const themeSelect = document.getElementById("themeSelect");

const themes = {
    dark: {
        "--bg": "#232428",
        "--text": "#c8c8c8",
        "--muted": "#8a8f98",
        "--card": "rgba(255,255,255,0.04)",
        "--border": "rgba(255,255,255,0.06)"
    },

    soft: {
        "--bg": "#1f2227",
        "--text": "#d6d6d6",
        "--muted": "#9aa0a6",
        "--card": "rgba(255,255,255,0.05)",
        "--border": "rgba(255,255,255,0.08)"
    },

    sepia: {
        "--bg": "#2a2420",
        "--text": "#e6d3b3",
        "--muted": "#b8a88f",
        "--card": "rgba(255, 240, 220, 0.05)",
        "--border": "rgba(255, 240, 220, 0.1)"
    }
};

themeSelect.addEventListener("change", (e) => {
    const theme = themes[e.target.value];

    for (const key in theme) {
        document.documentElement.style.setProperty(key, theme[key]);
    }
});