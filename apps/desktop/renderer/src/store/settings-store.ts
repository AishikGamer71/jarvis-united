import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface SettingsState {
  hiddenTabs: string[]
  voice: string
  temperature: number
  maxTokens: number
  alwaysOnTop: boolean
  autoStart: boolean
  storagePath: string
  uiSoundEffects: boolean
  toggleTabVisibility: (tabId: string) => void
  setVoice: (voice: string) => void
  setTemperature: (temperature: number) => void
  setMaxTokens: (maxTokens: number) => void
  setAlwaysOnTop: (alwaysOnTop: boolean) => void
  setAutoStart: (autoStart: boolean) => void
  setStoragePath: (storagePath: string) => void
  setUiSoundEffects: (uiSoundEffects: boolean) => void
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      hiddenTabs: [],
      voice: 'Charon',
      temperature: 0.7,
      maxTokens: 2048,
      alwaysOnTop: false,
      autoStart: false,
      storagePath: '',
      uiSoundEffects: true,
      toggleTabVisibility: (tabId) =>
        set((state) => ({
          hiddenTabs: state.hiddenTabs.includes(tabId)
            ? state.hiddenTabs.filter((id) => id !== tabId)
            : [...state.hiddenTabs, tabId]
        })),
      setVoice: (voice) => set({ voice }),
      setTemperature: (temperature) => set({ temperature }),
      setMaxTokens: (maxTokens) => set({ maxTokens }),
      setAlwaysOnTop: (alwaysOnTop) => set({ alwaysOnTop }),
      setAutoStart: (autoStart) => set({ autoStart }),
      setStoragePath: (storagePath) => set({ storagePath }),
      setUiSoundEffects: (uiSoundEffects) => set({ uiSoundEffects })
    }),
    {
      name: 'jarvis-settings-storage'
    }
  )
)
