class BoardLog {
  constructor(root) {
    this.root = root;
    this.container = root.querySelector('#serialLogContainer');
    this.stateLabel = root.querySelector('#serialState');
    this.reconnectButton = root.querySelector('#serialReconnect');
    this.ws = null;
    this.reconnectTimer = null;
    this.lines = [];
    
    const baseWsUrl = window.CAMERA_WS_URL || "ws://localhost:8765/ws/camera";
    this.wsUrl = baseWsUrl.replace('/ws/camera', '/ws/board-log');

    this.reconnectButton.addEventListener('click', () => this.reconnect());
    this.connect();
  }

  connect() {
    this.cleanupSocket();
    this.setState('CONNECTING');

    const ws = new WebSocket(this.wsUrl);
    this.ws = ws;

    ws.onopen = () => {
      if (this.ws === ws) this.setState('OPEN');
    };

    ws.onmessage = (event) => {
      if (this.ws !== ws) return;
      try {
        const data = JSON.parse(event.data);
        this.appendLine(data.ts, data.line);
      } catch (e) {
        console.error("Failed to parse board log message", e);
      }
    };

    ws.onerror = () => {
      if (this.ws === ws) this.setState('ERROR');
    };

    ws.onclose = () => {
      if (this.ws === ws) this.setState('CLOSED');
    };
  }

  reconnect() {
    this.setState('CONNECTING');
    this.cleanupSocket();
    clearTimeout(this.reconnectTimer);
    this.reconnectTimer = setTimeout(() => this.connect(), 2000);
  }

  setState(state) {
    const isOpen = state === 'OPEN';
    const isConnecting = state === 'CONNECTING';

    if (isOpen) {
      this.stateLabel.textContent = "Serial Connected";
      this.stateLabel.className = "inline-flex rounded-full bg-emerald-100 px-3 py-1 text-sm font-semibold text-emerald-700";
    } else if (isConnecting) {
      this.stateLabel.innerHTML = `<span class="animate-pulse">_</span> Connecting to board...`;
      this.stateLabel.className = "inline-flex rounded-full bg-slate-200 px-3 py-1 text-sm font-semibold text-slate-600";
    } else {
      this.stateLabel.textContent = "Serial disconnected";
      this.stateLabel.className = "inline-flex rounded-full bg-slate-100 px-3 py-1 text-sm font-semibold text-slate-400";
    }

    this.reconnectButton.classList.toggle("hidden", isOpen || isConnecting);
  }

  appendLine(ts, text) {
    const timeStr = new Date(ts * 1000).toLocaleTimeString('en-US', { hour12: false });
    const isError = text.includes("Error") || text.includes("Traceback") || text.includes("Exception");
    
    const lineDiv = document.createElement('div');
    lineDiv.style.whiteSpace = 'pre';
    lineDiv.style.color = isError ? '#ff6b6b' : '#39d353';
    lineDiv.textContent = `[${timeStr}]  ${text}`;
    
    this.container.appendChild(lineDiv);
    this.lines.push(lineDiv);
    
    while (this.lines.length > 500) {
      const oldLine = this.lines.shift();
      if (oldLine.parentNode) {
        oldLine.parentNode.removeChild(oldLine);
      }
    }
    
    this.container.scrollTop = this.container.scrollHeight;
  }

  cleanupSocket() {
    if (this.ws) {
      this.ws.onopen = null;
      this.ws.onmessage = null;
      this.ws.onerror = null;
      this.ws.onclose = null;
      this.ws.close();
      this.ws = null;
    }
  }

  destroy() {
    clearTimeout(this.reconnectTimer);
    this.cleanupSocket();
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const root = document.getElementById("yoloBitLog");
  if (root) {
    window.boardLog = new BoardLog(root);
    window.addEventListener("beforeunload", () => window.boardLog.destroy());
  }
});
