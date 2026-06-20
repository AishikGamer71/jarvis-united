import { contextBridge, ipcRenderer } from "electron";
import { electronAPI } from "@electron-toolkit/preload";
import { IPC_CHANNELS, addMessageSchema } from "@jarvis/ipc-contracts";

// Custom APIs for renderer
const api = {};

const aiAPI = {
  addMessage: (payload: any) => {
    const validated = addMessageSchema.parse(payload);
    return ipcRenderer.invoke(IPC_CHANNELS.ADD_MESSAGE, validated);
  },
  getHistory: () => ipcRenderer.invoke(IPC_CHANNELS.GET_HISTORY),
};

const fsAPI = {
  selectStoragePath: () => ipcRenderer.invoke(IPC_CHANNELS.SELECT_STORAGE_PATH),
};

const systemAPI = {
  getSystemStats: () => ipcRenderer.invoke(IPC_CHANNELS.GET_SYSTEM_STATS),
  getInstalledApps: () => ipcRenderer.invoke(IPC_CHANNELS.GET_INSTALLED_APPS),
};

if (process.contextIsolated) {
  try {
    contextBridge.exposeInMainWorld("electron", electronAPI);
    contextBridge.exposeInMainWorld("api", api);
    contextBridge.exposeInMainWorld("aiAPI", aiAPI);
    contextBridge.exposeInMainWorld("fsAPI", fsAPI);
    contextBridge.exposeInMainWorld("systemAPI", systemAPI);
  } catch (error) {
    console.error(error);
  }
} else {
  // @ts-ignore (define in dts)
  window.electron = electronAPI;
  // @ts-ignore (define in dts)
  window.api = api;
  // @ts-ignore
  window.aiAPI = aiAPI;
  // @ts-ignore
  window.fsAPI = fsAPI;
  // @ts-ignore
  window.systemAPI = systemAPI;
}
