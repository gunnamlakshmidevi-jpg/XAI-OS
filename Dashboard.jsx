import React, { useEffect, useState } from "react";

export default function Dashboard() {
  const [cpuLoad, setCpuLoad] = useState(10);
  const [memoryUsage, setMemoryUsage] = useState(20);

  // Simple JS CPU benchmark (browser safe)
  function measureCPULoad() {
    const start = performance.now();

    // perform some heavy operations
    let x = 0;
    for (let i = 0; i < 5000000; i++) {
      x += Math.sqrt(i) % 3;
    }

    const end = performance.now();
    const duration = end - start;

    // Map duration to a 0–100 CPU load scale
    const load = Math.min(100, Math.floor((duration / 50) * 100));
    setCpuLoad(load);
  }

  // Memory usage (browser only)
  function measureMemory() {
    if (performance.memory) {
      const used = performance.memory.usedJSHeapSize;
      const total = performance.memory.totalJSHeapSize;
      const percent = Math.floor((used / total) * 100);
      setMemoryUsage(percent);
    } else {
      // fallback (simulate)
      setMemoryUsage(30 + Math.floor(Math.random() * 40));
    }
  }

  useEffect(() => {
    const interval = setInterval(() => {
      measureCPULoad();
      measureMemory();
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>System Dashboard</h2>

      <div className="card">
        <h3>CPU Usage</h3>
        <div className="bar-bg">
          <div className="bar-fill" style={{ width: cpuLoad + "%" }}></div>
        </div>
        <p>{cpuLoad}%</p>
      </div>

      <div className="card">
        <h3>Memory Usage</h3>
        <div className="bar-bg">
          <div className="bar-fill memory" style={{ width: memoryUsage + "%" }}></div>
        </div>
        <p>{memoryUsage}%</p>
      </div>
    </div>
  );
}


const page = {
  marginLeft: "280px",
  padding: "40px",
  color: "white",
  fontSize: "20px"
};

const title = {
  fontSize: "42px",
  fontWeight: "700",
  marginBottom: "25px"
};

const section = {
  background: "#0d1f33",
  padding: "30px",
  borderRadius: "14px",
  border: "1px solid #1f3b55",
  width: "600px",
  marginBottom: "30px"
};

const heading = {
  fontSize: "28px",
  marginBottom: "10px",
  fontWeight: "600"
};

const value = {
  fontSize: "38px",
  fontWeight: "bold",
  color: "#4da3ff"
};

const subValue = {
  fontSize: "22px",
  marginTop: "8px",
  color: "#7abaff"
};
