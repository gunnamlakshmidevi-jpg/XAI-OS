// src/pages/MemoryMonitor.jsx
import React, { useMemo } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function MemoryMonitor({ tick=0 }) {
  const data = useMemo(()=> {
    const arr = [];
    for(let i=0;i<20;i++){
      arr.push({ name: i, used: Math.round(30 + 50*Math.abs(Math.sin((i+tick)/5))+ Math.random()*5) });
    }
    return arr;
  }, [tick]);

  return (
    <div style={{ height: "100%" }}>
      <div style={{ marginBottom: 8 }}>Memory utilization (MB / %)</div>
      <ResponsiveContainer width="100%" height={160}>
        <LineChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="used" stroke="#3fa0ff" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
      <div style={{ marginTop:10 }}>
        <div>Heap used: {Math.round(data[data.length-1].used)}%</div>
        <div>Page faults (sim): {Math.round(Math.random()*5)}</div>
      </div>
    </div>
  );
}
