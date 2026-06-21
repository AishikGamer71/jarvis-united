import { spawn, ChildProcess } from "child_process";
import { join } from "path";

let pythonProcess: ChildProcess | null = null;

export function startPythonEngine() {
  // apps/desktop/out/main -> ../../../.. -> root
  const engineDir = join(__dirname, "../../../../engine");
  const pythonScript = join(engineDir, "src/jarvis_engine/main.py");

  pythonProcess = spawn("python", [pythonScript], {
    cwd: engineDir,
    env: { ...process.env, PYTHONIOENCODING: "utf-8" },
  });

  pythonProcess.stdout?.on("data", (data) => {
    console.log(`[PYTHON] ${data.toString().trim()}`);
  });

  pythonProcess.on("error", (err) => {
    console.error(
      `[PYTHON LAUNCH ERR] Failed to start Python engine: ${err.message}`,
    );
  });

  pythonProcess.stderr?.on("data", (data) => {
    console.error(`[PYTHON ERR] ${data.toString().trim()}`);
  });

  pythonProcess.on("close", (code) => {
    console.log(`Python engine exited with code ${code}`);
  });
}

export function stopPythonEngine() {
  if (pythonProcess) {
    pythonProcess.kill("SIGKILL");
  }
}
