import { contextBridge, ipcRenderer } from 'electron';
import { IPC_CHANNELS, addMessageSchema } from '@jarvis/ipc-contracts';

contextBridge.exposeInMainWorld('aiAPI', {
  addMessage: (payload: any) => {
    // Validate payload against Zod schema before sending over IPC
    const validated = addMessageSchema.parse(payload);
    return ipcRenderer.invoke(IPC_CHANNELS.ADD_MESSAGE, validated);
  },
  getHistory: () => ipcRenderer.invoke(IPC_CHANNELS.GET_HISTORY)
});
