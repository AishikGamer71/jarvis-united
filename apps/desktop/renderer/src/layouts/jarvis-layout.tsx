import { useState, useEffect, Suspense, lazy } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  RiWifiLine,
  RiShieldFlashLine,
  RiLayoutGridLine,
  RiBrainLine,
  RiFolderOpenLine,
  RiPhoneLine,
  RiSettings4Line,
  RiBatteryChargeLine,
  RiCameraLine,
  RiComputerLine,
  RiCloseLine,
  RiImageLine,
  RiDashboard2Line,
  RiTerminalBoxLine
} from 'react-icons/ri'
import { getSystemStatus } from '@renderer/services/system-info'
import { getHistory } from '@renderer/services/jarvis-ai-brain'
import ViewSkeleton from '@renderer/components/common/view-skeleton'

import DashboardView from '../pages/dashboard'
import PhoneView from '../pages/phone'
import { VisionMode } from '@renderer/IndexRoot'
import { useSettingsStore } from '../store/settings-store'
import { useProfileStore } from '../store/profile-store'
import { NAVIGATION_MODULES } from '../config/navigation'

const AppsView = lazy(() => import('../pages/app-store'))
const TaskManagerView = lazy(() => import('../pages/task-manager'))
const NotesView = lazy(() => import('../pages/notes'))
const SettingsView = lazy(() => import('../pages/settings'))
const GalleryView = lazy(() => import('../pages/gallery'))
const TerminalView = lazy(() => import('@renderer/components/terminal/terminal'))

interface JarvisProps {
  isSystemActive: boolean
  toggleSystem: () => void
  isMicMuted: boolean
  toggleMic: () => void
  isVideoOn: boolean
  visionMode: VisionMode
  startVision: (mode: 'camera' | 'screen') => void
  stopVision: () => void
  activeStream: MediaStream | null
}

const glassPanel = 'bg-zinc-950/40 backdrop-blur-sm border border-white/5 rounded-2xl shadow-xl'

const JARVIS = (props: JarvisProps) => {
  const hiddenTabs = useSettingsStore((state) => state.hiddenTabs)
  const loadProfiles = useProfileStore((state) => state.loadProfiles)
  const [activeTab, setActiveTab] = useState('DASHBOARD')
  const [stats, setStats] = useState<any>(null)
  const [time, setTime] = useState<Date>(new Date())
  const [chatHistory, setChatHistory] = useState<any[]>([])
  const [showSourceModal, setShowSourceModal] = useState(false)

  useEffect(() => {
    loadProfiles()
  }, [])

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date())
      getSystemStatus().then(setStats)
    }, 500)
    return () => clearInterval(timer)
  }, [])

  useEffect(() => {
    const fetchHistory = async () => {
      const history = await getHistory()
      if (Array.isArray(history)) setChatHistory(history.slice(-15))
    }
    fetchHistory()
    const interval = setInterval(fetchHistory, 500)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    const handleJarvisExecute = () => {
      // Just switch to the TERMINAL tab — Terminal.tsx's own handler sends the command
      // with the correct tabId via its own 'jarvis-terminal-execute' listener
      setActiveTab('TERMINAL')
    }
    window.addEventListener('jarvis-terminal-execute', handleJarvisExecute)
    return () => window.removeEventListener('jarvis-terminal-execute', handleJarvisExecute)
  }, [])

  const handleVisionClick = () => {
    if (props.isVideoOn) {
      props.stopVision()
    } else {
      setShowSourceModal(true)
    }
  }

  return (
    <div className="h-screen w-full bg-black text-zinc-100 font-sans overflow-hidden select-none flex flex-col relative pb-5">
      <div className="h-14 w-full flex items-center justify-between px-6 bg-zinc-950/80 border-b border-white/5 z-50 backdrop-blur-md">
        <div className="hidden lg:flex items-center gap-3">
          <RiShieldFlashLine className="text-emerald-500 text-xl animate-pulse" />
          <div className="flex flex-col leading-none">
            <span className="font-black tracking-[0.2em] text-sm text-zinc-100">JARVIS AI</span>
            <span className="text-[11px] font-mono text-emerald-500/60 tracking-widest">
              NEURAL INTERFACE
            </span>
          </div>
        </div>

        <div className="hidden md:flex gap-2 bg-black/40 p-1 rounded-lg border border-white/5">
          {NAVIGATION_MODULES
            .filter((tab) => !hiddenTabs.includes(tab.id) || tab.isCore)
            .map((tab) => {
              const isActive = activeTab === tab.id;
              return (
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.95 }}
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`relative cursor-pointer px-5 py-1.5 text-[10px] font-bold tracking-widest rounded-md transition-colors duration-300 flex items-center gap-2 overflow-hidden z-20 ${
                    isActive
                      ? 'text-emerald-400'
                      : 'text-zinc-500 hover:text-zinc-300 hover:bg-white/5'
                  }`}
                >
                  {isActive && (
                    <motion.div
                      layoutId="activeNavTab"
                      className="absolute inset-0 bg-emerald-500/20 border border-emerald-500/40 rounded-md shadow-[0_0_15px_rgba(16,185,129,0.2)]"
                      initial={false}
                      transition={{ type: 'spring', stiffness: 500, damping: 35 }}
                      style={{ zIndex: -1 }}
                    />
                  )}
                  <span className="relative z-10 flex items-center gap-2">
                    {tab.icon} {tab.id}
                  </span>
                </motion.button>
              )
            })}
        </div>

        <div className="flex items-center gap-6 text-[11px] font-mono font-bold opacity-60">
          <div className="flex items-center gap-2 text-emerald-500">
            <RiWifiLine /> <span>LINKED</span>
          </div>
          <div className="hidden sm:flex items-center gap-2">
            <RiBatteryChargeLine /> <span>100%</span>
          </div>
          <div className="bg-zinc-800 px-2 py-1 rounded text-zinc-300">
            {time.toLocaleTimeString()}
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-hidden relative bg-[radial-gradient(circle_at_center,var(--tw-gradient-stops))] from-zinc-900/50 via-black to-black">
        <AnimatePresence mode="wait">
          {activeTab === 'DASHBOARD' && (
            <motion.div
              key="DASHBOARD"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3, type: 'spring', stiffness: 300, damping: 30 }}
              className="absolute inset-0"
            >
              <DashboardView
                props={props}
                stats={stats}
                chatHistory={chatHistory}
                onVisionClick={handleVisionClick}
              />
            </motion.div>
          )}

          {activeTab === 'PHONE' && (
            <motion.div
              key="PHONE"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3, type: 'spring', stiffness: 300, damping: 30 }}
              className="absolute inset-0"
            >
              <PhoneView glassPanel={glassPanel} />
            </motion.div>
          )}

          {activeTab === 'TASK MANAGER' && (
            <motion.div
              key="TASK MANAGER"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3, type: 'spring', stiffness: 300, damping: 30 }}
              className="absolute inset-0"
            >
              <Suspense fallback={<ViewSkeleton />}>
                <TaskManagerView />
              </Suspense>
            </motion.div>
          )}

          {activeTab === 'Apps' && (
            <motion.div
              key="Apps"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3, type: 'spring', stiffness: 300, damping: 30 }}
              className="absolute inset-0"
            >
              <Suspense fallback={<ViewSkeleton />}>
                <AppsView />
              </Suspense>
            </motion.div>
          )}

          {activeTab === 'NOTES' && (
            <motion.div
              key="NOTES"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3, type: 'spring', stiffness: 300, damping: 30 }}
              className="absolute inset-0"
            >
              <Suspense fallback={<ViewSkeleton />}>
                <NotesView glassPanel={glassPanel} />
              </Suspense>
            </motion.div>
          )}

          {activeTab === 'SETTINGS' && (
            <motion.div
              key="SETTINGS"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3, type: 'spring', stiffness: 300, damping: 30 }}
              className="absolute inset-0"
            >
              <Suspense fallback={<ViewSkeleton />}>
                <SettingsView isSystemActive={props.isSystemActive} />
              </Suspense>
            </motion.div>
          )}

          {activeTab === 'GALLERY' && (
            <motion.div
              key="GALLERY"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3, type: 'spring', stiffness: 300, damping: 30 }}
              className="absolute inset-0"
            >
              <Suspense fallback={<ViewSkeleton />}>
                <GalleryView />
              </Suspense>
            </motion.div>
          )}

          {activeTab === 'TERMINAL' && (
            <motion.div
              key="TERMINAL"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3, type: 'spring', stiffness: 300, damping: 30 }}
              className="absolute inset-0"
            >
              <div className="w-full h-full p-4">
                <Suspense fallback={<ViewSkeleton />}>
                  <TerminalView />
                </Suspense>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {showSourceModal && (
        <div className="absolute inset-0 z-100 flex items-center justify-center bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
          <div className={`${glassPanel} w-96 p-1 border-emerald-500/30 flex flex-col shadow-2xl`}>
            <div className="flex items-center justify-between p-4 border-b border-white/5 bg-white/5">
              <span className="text-xs font-bold tracking-widest text-emerald-400">
                ESTABLISH UPLINK
              </span>
              <button
                onClick={() => setShowSourceModal(false)}
                className="cursor-pointer text-zinc-500 hover:text-white"
              >
                <RiCloseLine size={18} />
              </button>
            </div>

            <div className="p-4 grid grid-cols-2 gap-4">
              <button
                onClick={() => {
                  props.startVision('camera')
                  setShowSourceModal(false)
                }}
                className="cursor-pointer group flex flex-col items-center justify-center gap-3 p-6 rounded-xl bg-black/40 border border-white/10 hover:border-emerald-500/50 hover:bg-emerald-500/10 transition-all"
              >
                <div className="p-3 rounded-full bg-zinc-900 group-hover:bg-emerald-500 text-zinc-400 group-hover:text-black transition-colors">
                  <RiCameraLine size={28} />
                </div>
                <span className="text-[10px] font-bold tracking-widest text-zinc-300 group-hover:text-emerald-400">
                  CAMERA FEED
                </span>
              </button>

              <button
                onClick={() => {
                  props.startVision('screen')
                  setShowSourceModal(false)
                }}
                className="cursor-pointer group flex flex-col items-center justify-center gap-3 p-6 rounded-xl bg-black/40 border border-white/10 hover:border-emerald-500/50 hover:bg-emerald-500/10 transition-all"
              >
                <div className="p-3 rounded-full bg-zinc-900 group-hover:bg-emerald-500 text-zinc-400 group-hover:text-black transition-colors">
                  <RiComputerLine size={28} />
                </div>
                <span className="text-[10px] font-bold tracking-widest text-zinc-300 group-hover:text-emerald-400">
                  SCREEN SHARE
                </span>
              </button>
            </div>

            <div className="p-3 bg-black/20 text-center">
              <p className="text-[9px] text-zinc-600 font-mono">
                SELECT INPUT SOURCE FOR NEURAL PROCESSING
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default JARVIS
