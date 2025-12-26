// src/components/SideNav.jsx
import React from "react";
import { NavLink } from "react-router-dom";
import "./SideNav.css";

export default function SideNav() {
  const menu = [
    { to: "/dashboard", label: "Dashboard" },
    { to: "/sandbox", label: "Code Sandbox" },
    { to: "/cpu", label: "CPU Scheduler" },
    { to: "/memory", label: "Memory Monitor" },
    
  { to: "/simulator", label: "OS Simulator" }, 
  
    
  ];

  return (
    <div className="sidenav">
      <h2 className="sidenav-title">XAI-OS</h2>

      <div className="sidenav-menu">
        {menu.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              isActive ? "sidenav-link active-link" : "sidenav-link"
            }
            
          >
            {item.label}
          </NavLink>
        ))}
      </div>
    </div>
  );
}
