import { app, BrowserWindow, ipcMain, dialog } from 'electron'
import { join } from 'path'

// Handlers Imports
import registerWormhole from './ai/wormhole'
import registerOracle from './ai/rag-oracle'
import registerJarvisCoder from './ai/jarvis-coder'
import registerDeepResearch from './ai/deep-research'

import registerSecurityVault from './security/security-vault'
import registerLockSystem from './security/lock-system'

import registerWebAgent from './ai/web-agent'
import registerSystemControl from './system/terminal-control'
// import registerTelekinesis from './ai/telekinesis'
import registerRealityHacker from './ai/reality-hacker'
import registerPermanentMemory from './ai/permanent-memory'
import registerNotesHandlers from './features/notes-manager'
import registerLocationHandlers from './features/live-location'
import registerIpcHandlers from './ai/jarvis-memory'
import registerGmailHandlers from './features/gmail-manager'
import registerGhostControl from './ai/ghost-control'
import registerSystemHandlers from './system/system-info'
import registerGalleryHandlers from './features/gallery-manager'
import registerFileWrite from './fs/file-write'
import registerFileSearch from './fs/file-search'
import registerFileRead from './fs/file-read'
import registerFileOps from './fs/file-ops'
import registerFileOpen from './fs/file-open'
import registerFileScanner from './fs/file-launcher'
import registerDirLoader from './fs/dir-load'
import registerAppLauncher from './system/app-launcher'
import registerAdbHandlers from './system/adb-manager'

import registerDropZoneControl from './system/smart-drop-zone'
import registerScreenPeeler from './system/screen-peeler'
import registerPhantomKeyboard from './system/phantom-control'

import registerWidgetMaker from './features/widget-manager'
import registerWebsiteBuilder from './ai/website-builder'

import { registerUserProfileHandlers } from './profiles/user-profile'
import { registerSystemProfileHandlers } from './profiles/system-profile'

import { startPythonEngine, stopPythonEngine } from './python-launcher'
import registerTaskManager from './features/task-manager'
import { setupTerminal } from './system/terminal'
function registerAllHandlers() {
  registerTaskManager()
  registerWormhole({ ipcMain })
  registerOracle({ ipcMain })
  registerJarvisCoder({ ipcMain, app })
  registerDeepResearch({ ipcMain })

  registerSecurityVault()
  registerLockSystem()

  registerWebAgent(ipcMain)
  registerSystemControl(ipcMain)
  // registerTelekinesis({ ipcMain })
  registerRealityHacker(ipcMain)
  registerPermanentMemory({ ipcMain, app })
  registerNotesHandlers(ipcMain)
  registerLocationHandlers(ipcMain)
  registerIpcHandlers({ ipcMain, app })
  registerGmailHandlers(ipcMain)
  registerGhostControl(ipcMain)
  registerSystemHandlers(ipcMain)
  registerGalleryHandlers(ipcMain)
  registerFileWrite(ipcMain)
  registerFileSearch(ipcMain)
  registerFileRead(ipcMain)
  registerFileOps(ipcMain)
  registerFileOpen(ipcMain)
  registerFileScanner(ipcMain)
  registerDirLoader(ipcMain)
  registerAppLauncher(ipcMain)
  registerAdbHandlers(ipcMain)

  registerDropZoneControl(ipcMain)
  registerScreenPeeler()
  registerPhantomKeyboard()

  registerWidgetMaker()
  registerWebsiteBuilder()
  
  registerUserProfileHandlers()
  registerSystemProfileHandlers()
}

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 900,
    height: 670,
    show: false,
    autoHideMenuBar: true,
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      sandbox: false,
      contextIsolation: true
    }
  })

  mainWindow.on('ready-to-show', () => {
    mainWindow.show()
  })
  
  setupTerminal(mainWindow)

  if (process.env['ELECTRON_RENDERER_URL']) {
    mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'])
  } else {
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
  }
}

app.whenReady().then(() => {
  startPythonEngine()
  registerAllHandlers()
  createWindow()

  ipcMain.on('set-always-on-top', (_, value: boolean) => {
    const win = BrowserWindow.getAllWindows()[0]
    if (win) win.setAlwaysOnTop(value)
  })

  ipcMain.on('set-auto-start', (_, value: boolean) => {
    app.setLoginItemSettings({ openAtLogin: value })
  })

  ipcMain.handle('select-storage-path', async () => {
    const win = BrowserWindow.getAllWindows()[0]
    const result = await dialog.showOpenDialog(win, {
      properties: ['openDirectory']
    })
    if (!result.canceled && result.filePaths.length > 0) {
      return result.filePaths[0]
    }
    return null
  })

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('will-quit', () => {
  stopPythonEngine()
})
