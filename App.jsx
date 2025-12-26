import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import SideNav from "./components/SideNav";
import "./app.css";

import Dashboard from "./pages/Dashboard";
import CodeSandbox from "./pages/CodeSandbox";
import AiAnalytics from "./pages/AiAnalytics";
import CpuScheduler from "./pages/CpuScheduler";
import DiskScheduler from "./pages/DiskScheduler";
import MemoryMonitor from "./pages/MemoryMonitor";
import Simulator from "./pages/Simulator";




export default function App() {
  return (
    <Router>
      <div className="app-layout">
        <SideNav />

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/sandbox" element={<CodeSandbox />} />
            <Route path="/ai" element={<AiAnalytics />} />
            <Route path="/cpu" element={<CpuScheduler />} />
            <Route path="/disk" element={<DiskScheduler />} />
            <Route path="/memory" element={<MemoryMonitor />} />
            <Route path="/simulator" element={<Simulator />} />
            

            {/* Requested pages */}
            
            
          </Routes>
        </main>
      </div>
    </Router>
  );
}
