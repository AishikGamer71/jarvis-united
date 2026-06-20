import { contextBridge, ipcRenderer } from 'electron';
import { IPC_CHANNELS } from '@jarvis/ipc-contracts';

contextBridge.exposeInMainWorld('systemAPI', {
  getSystemStats: () => ipcRenderer.invoke(IPC_CHANNELS.GET_SYSTEM_STATS),
  getInstalledApps: () => ipcRenderer.invoke(IPC_CHANNELS.GET_INSTALLED_APPS)
});
