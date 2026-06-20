import { contextBridge, ipcRenderer } from 'electron';
import { IPC_CHANNELS } from '@jarvis/ipc-contracts';

contextBridge.exposeInMainWorld('fsAPI', {
  selectStoragePath: () => ipcRenderer.invoke(IPC_CHANNELS.SELECT_STORAGE_PATH)
});
