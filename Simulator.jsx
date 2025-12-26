import React, { useState } from "react";
import "./Simulator.css";

export default function Simulator() {
  const [log, setLog] = useState(["XAI-OS Simulator Initialized..."]);
  const [isRunning, setIsRunning] = useState(false);

  // Adds a log message to the console
  const addLog = (msg) => {
    setLog((prev) => [...prev, `> ${msg}`]);
  };

  // Start simulation
  const startSimulation = () => {
    if (isRunning) return;

    setIsRunning(true);
    addLog("Simulation started...");

    // Example simulation events
    setTimeout(() => addLog("Loading kernel modules..."), 800);
    setTimeout(() => addLog("Initializing CPU scheduler..."), 1500);
    setTimeout(() => addLog("Memory management active..."), 2200);
    setTimeout(() => addLog("Disk I/O processes started."), 3000);
    setTimeout(() => addLog("System running smoothly ✔"), 3800);
  };

  // Stop simulation
  const stopSimulation = () => {
    setIsRunning(false);
    addLog("Simulation stopped.");
  };

  // Reset simulation
  const resetSimulation = () => {
    setLog(["XAI-OS Simulator Reset."]);
    setIsRunning(false);
  };

  return (
    <div className="sim-container">
      <h1 className="sim-title">OS Simulator</h1>

      <div className="sim-controls">
        <button
          className="sim-btn start"
          onClick={startSimulation}
          disabled={isRunning}
        >
          ▶ Start
        </button>

        <button className="sim-btn stop" onClick={stopSimulation}>
          ■ Stop
        </button>

        <button className="sim-btn reset" onClick={resetSimulation}>
          ↻ Reset
        </button>
      </div>

      <div className="sim-console">
        {log.map((line, index) => (
          <div key={index} className="console-line">
            {line}
          </div>
        ))}
      </div>
    </div>
  );
}
