import { useSettingsStore } from "../store/settings-store";

export class GeminiLiveService {
  public socket: WebSocket | null = null;
  public isConnected: boolean = false;
  private isMicMuted: boolean = false;
  public analyser: any = null; // Mock analyser to prevent crashes
  public apiKey: string = "";

  constructor() {}

  setMute(muted: boolean) {
    this.isMicMuted = muted;
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ type: "set_muted", value: muted }));
    }
  }

  async connect(): Promise<void> {
    if (
      this.socket &&
      (this.socket.readyState === WebSocket.OPEN ||
        this.socket.readyState === WebSocket.CONNECTING)
    ) {
      return Promise.resolve();
    }

    if (window.electron?.ipcRenderer) {
      const secureKeys =
        await window.electron.ipcRenderer.invoke("secure-get-keys");
      this.apiKey =
        secureKeys?.geminiKey ||
        localStorage?.getItem("jarvis_custom_api_key") ||
        "";
    } else {
      this.apiKey = localStorage.getItem("jarvis_custom_api_key") || "";
    }

    this.apiKey = this.apiKey.trim();

    if (!this.apiKey) {
      throw new Error("NO_API_KEY");
    }

    return new Promise((resolve, reject) => {
      this.socket = new WebSocket("ws://localhost:8765");

      this.socket.onopen = () => {
        this.isConnected = true;
        this.socket?.send(
          JSON.stringify({ type: "api_key", value: this.apiKey }),
        );

        const settings = useSettingsStore.getState();
        const voice = settings.voice || "Charon";
        const temperature = settings.temperature ?? 0.7;
        const maxTokens = settings.maxTokens ?? 2048;

        this.socket?.send(JSON.stringify({ type: "set_voice", value: voice }));
        this.socket?.send(
          JSON.stringify({ type: "set_temperature", value: temperature }),
        );
        this.socket?.send(
          JSON.stringify({ type: "set_max_tokens", value: maxTokens }),
        );

        this.setMute(this.isMicMuted);
        resolve();
      };

      this.socket.onerror = (err) => {
        if (!this.isConnected) {
          reject(new Error("Failed to connect to Python backend on port 8765"));
        }
      };

      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === "state") {
            window.dispatchEvent(
              new CustomEvent("jarvis-state", { detail: data.value }),
            );
          } else if (data.type === "log") {
            console.log("[JARVIS PYTHON]", data.value);
            if (typeof data.value === "string") {
              if (data.value.startsWith("Jarvis: ")) {
                const msgText = data.value.substring(8).trim();
                if (msgText) {
                  import("./jarvis-ai-brain").then(({ saveMessage }) =>
                    saveMessage("jarvis", msgText),
                  );
                }
              } else if (data.value.startsWith("You: ")) {
                const msgText = data.value.substring(5).trim();
                if (msgText) {
                  import("./jarvis-ai-brain").then(({ saveMessage }) =>
                    saveMessage("user", msgText),
                  );
                }
              }
            }
          } else if (data.type === "terminal_execute") {
            window.dispatchEvent(
              new CustomEvent("jarvis-terminal-execute", {
                detail: data.value,
              }),
            );
          }
        } catch (err) {}
      };

      this.socket.onclose = () => {
        this.disconnect();
      };
    });
  }

  sendVideoFrame(base64Image: string): void {
    // Forward video frame to python engine if supported later
  }

  sendTextCommand(text: string): void {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ type: "text_command", value: text }));
    }
  }

  setFile(filePath: string): void {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ type: "set_file", value: filePath }));
    }
  }

  disconnect(): void {
    this.isConnected = false;
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}

export const jarvisService = new GeminiLiveService();
