import React, { useState } from "react";
import "./CpuScheduler.css";

export default function CpuScheduler() {
  const [processes, setProcesses] = useState([]);
  const [pid, setPid] = useState("");
  const [burst, setBurst] = useState("");
  const [priority, setPriority] = useState("");
  const [algorithm, setAlgorithm] = useState("FCFS");
  const [result, setResult] = useState(null);

  const addProcess = () => {
    if (!pid || !burst) return alert("Enter process ID and burst time!");

    setProcesses([
      ...processes,
      { pid, burst: Number(burst), priority: Number(priority) || 0 }
    ]);

    setPid("");
    setBurst("");
    setPriority("");
  };

  const calculateFCFS = () => {
    let time = 0;
    const result = processes.map((p) => {
      const start = time;
      time += p.burst;
      return { pid: p.pid, start, end: time };
    });
    return result;
  };

  const calculateSJF = () => {
    let sorted = [...processes].sort((a, b) => a.burst - b.burst);
    let time = 0;
    return sorted.map((p) => {
      let start = time;
      time += p.burst;
      return { pid: p.pid, start, end: time };
    });
  };

  const calculatePriority = () => {
    let sorted = [...processes].sort((a, b) => a.priority - b.priority);
    let time = 0;
    return sorted.map((p) => {
      let start = time;
      time += p.burst;
      return { pid: p.pid, start, end: time };
    });
  };

  const runScheduler = () => {
    if (processes.length === 0) return alert("Add processes!");

    let output = [];

    if (algorithm === "FCFS") output = calculateFCFS();
    if (algorithm === "SJF") output = calculateSJF();
    if (algorithm === "PRIORITY") output = calculatePriority();

    setResult(output);
  };

  return (
    <div className="cpu-container">
      <h1>CPU Scheduler</h1>

      <div className="cpu-form">
        <input
          type="text"
          placeholder="PID"
          value={pid}
          onChange={(e) => setPid(e.target.value)}
        />
        <input
          type="number"
          placeholder="Burst Time"
          value={burst}
          onChange={(e) => setBurst(e.target.value)}
        />
        <input
          type="number"
          placeholder="Priority (optional)"
          value={priority}
          onChange={(e) => setPriority(e.target.value)}
        />

        <button onClick={addProcess}>Add</button>
      </div>

      <div className="cpu-algo">
        <label>Select Algorithm:</label>
        <select value={algorithm} onChange={(e) => setAlgorithm(e.target.value)}>
          <option value="FCFS">FCFS</option>
          <option value="SJF">SJF (Shortest Job First)</option>
          <option value="PRIORITY">Priority Scheduling</option>
        </select>

        <button className="run-btn" onClick={runScheduler}>
          Run
        </button>
      </div>

      {/* Result Section */}
      {result && (
        <div className="result-section">
          <h2>Gantt Chart</h2>

          <div className="gantt-chart">
            {result.map((r) => (
              <div key={r.pid} className="gantt-block">
                {r.pid}
                <span className="time">
                  {r.start} - {r.end}
                </span>
              </div>
            ))}
          </div>

          <h2>Output Table</h2>
          <table>
            <thead>
              <tr>
                <th>PID</th>
                <th>Start</th>
                <th>End</th>
              </tr>
            </thead>
            <tbody>
              {result.map((r) => (
                <tr key={r.pid}>
                  <td>{r.pid}</td>
                  <td>{r.start}</td>
                  <td>{r.end}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
