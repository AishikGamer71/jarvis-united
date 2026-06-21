import { IPC_CHANNELS } from "@jarvis/ipc-contracts";
import { UserProfile, SystemProfile } from "@jarvis/ipc-contracts";

const ipcRenderer = (window as any).electron?.ipcRenderer;

export const profileApi = {
  // User Profile
  async getUserProfile(): Promise<UserProfile> {
    if (!ipcRenderer) throw new Error("electron.ipcRenderer not found");
    return ipcRenderer.invoke(IPC_CHANNELS.GET_USER_PROFILE);
  },

  async saveUserProfile(data: Partial<UserProfile>): Promise<UserProfile> {
    if (!ipcRenderer) throw new Error("electron.ipcRenderer not found");
    return ipcRenderer.invoke(IPC_CHANNELS.SAVE_USER_PROFILE, data);
  },

  // System Profile
  async getSystemProfile(): Promise<SystemProfile> {
    if (!ipcRenderer) throw new Error("electron.ipcRenderer not found");
    return ipcRenderer.invoke(IPC_CHANNELS.GET_SYSTEM_PROFILE);
  },

  async saveSystemProfile(
    data: Partial<SystemProfile>,
  ): Promise<SystemProfile> {
    if (!ipcRenderer) throw new Error("electron.ipcRenderer not found");
    return ipcRenderer.invoke(IPC_CHANNELS.SAVE_SYSTEM_PROFILE, data);
  },
};
