import { Link } from "react-router-dom";
import "./NavBar.css";

export default function NavBar() {
  return (
    <nav className="navbar">
      <div className="logo">⚡ XAI-OS</div>

      <div className="nav-links">
        <Link to="/">Dashboard</Link>
        <Link to="/cpu">CPU Scheduling</Link>
        <Link to="/memory">Memory</Link>
        <Link to="/disk">Disk</Link>
        <Link to="/ai">AI Analytics</Link>
           {/* ← THIS ONE */}
        <Link to="/simulator">Simulator</Link>
        <Link to="/sandbox">Code Sandbox</Link>
        <Link to="/ml">ML Prediction</Link>

      </div>
    </nav>
  );
}
