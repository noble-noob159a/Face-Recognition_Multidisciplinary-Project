class CameraStream {
  constructor(root) {
    this.root = root;
    this.img = root.querySelector("[data-camera-img]");
    this.stateLabel = root.querySelector("[data-camera-state]");
    this.placeholder = root.querySelector("[data-camera-placeholder]");
    this.reconnectButton = root.querySelector("[data-camera-reconnect]");
    this.prevUrl = null;
    this.ws = null;
    this.reconnectTimer = null;
    this.wsUrl = window.CAMERA_WS_URL || "ws://localhost:8765/ws/camera";

    this.reconnectButton.addEventListener("click", () => this.reconnect());
    this.connect();
  }

  connect() {
    this.cleanupSocket();
    this.setState("connecting");

    const ws = new WebSocket(this.wsUrl);
    this.ws = ws;
    ws.binaryType = "blob";

    ws.onopen = () => {
      if (this.ws === ws) {
        this.setState("open");
      }
    };

    ws.onmessage = (event) => {
      if (this.ws !== ws) {
        return;
      }

      const url = URL.createObjectURL(event.data);
      this.img.src = url;
      this.img.classList.remove("hidden");
      if (this.prevUrl) {
        URL.revokeObjectURL(this.prevUrl);
      }
      this.prevUrl = url;
    };

    ws.onerror = () => {
      if (this.ws === ws) {
        this.setState("error");
      }
    };

    ws.onclose = () => {
      if (this.ws === ws) {
        this.setState("closed");
      }
    };
  }

  reconnect() {
    this.setState("connecting");
    this.cleanupSocket();
    clearTimeout(this.reconnectTimer);
    this.reconnectTimer = setTimeout(() => this.connect(), 2000);
  }

  setState(state) {
    const isOpen = state === "open";
    const isConnecting = state === "connecting";

    this.stateLabel.textContent = isOpen ? "Live" : isConnecting ? "Connecting" : "Disconnected";
    this.stateLabel.className = "inline-flex rounded-full px-3 py-1 text-sm font-semibold " +
      (isOpen ? "bg-emerald-100 text-emerald-700" : "bg-slate-200 text-slate-600");

    this.placeholder.classList.toggle("hidden", isOpen);
    this.reconnectButton.classList.toggle("hidden", isOpen || isConnecting);

    if (isConnecting) {
      this.placeholder.innerHTML = `
        <div class="h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-slate-600"></div>
        <p class="mt-3 font-medium text-slate-600">Connecting to camera...</p>
      `;
    } else if (!isOpen) {
      this.clearFrame();
      this.placeholder.innerHTML = `
        <div class="text-center">
          <p class="font-medium text-slate-600">Stream disconnected</p>
        </div>
      `;
      this.img.classList.add("hidden");
    }
  }

  clearFrame() {
    if (this.prevUrl) {
      URL.revokeObjectURL(this.prevUrl);
      this.prevUrl = null;
    }
    this.img.removeAttribute("src");
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

    this.clearFrame();
  }

  destroy() {
    clearTimeout(this.reconnectTimer);
    this.cleanupSocket();
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const root = document.getElementById("cameraStream");
  if (root) {
    window.cameraStream = new CameraStream(root);
    window.addEventListener("beforeunload", () => window.cameraStream.destroy());
  }
});
