import React, { useState } from "react";

function CodeSandbox() {
  const [code, setCode] = useState("");
  const [selectedLanguage, setSelectedLanguage] = useState("c");
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");

  const runCode = async () => {
    setOutput("Running...");

    try {
      const response = await fetch("http://localhost:5000/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code,
          language: selectedLanguage,
          input      // <-- textarea input goes to backend
        })
      });

      const data = await response.json();
      setOutput(data.output || data.error || "No output");
    } catch (err) {
      setOutput("Error connecting to server.");
    }
  };

  return (
    <div style={styles.container}>

      {/* Header */}
      <h2 style={styles.title}>XAI-OS Code Sandbox</h2>

      {/* Language Selector */}
      <select
        value={selectedLanguage}
        onChange={(e) => setSelectedLanguage(e.target.value)}
        style={styles.select}
      >
        <option value="c">C</option>
        <option value="cpp">C++</option>
        <option value="python">Python</option>
        <option value="java">Java</option>
        <option value="js">JavaScript</option>
      </select>

      {/* Code Editor */}
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Write your code here..."
        style={styles.codeEditor}
      />

      {/* Run Button */}
      <button onClick={runCode} style={styles.runButton}>
        Run Code
      </button>

      {/* Input Section */}
      <h3 style={styles.label}>Input (down-by-down scanf):</h3>
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter input here...&#10;Each line = one scanf"
        style={styles.inputBox}
      />

      {/* Output Section */}
      <h3 style={styles.label}>Output:</h3>
      <textarea
        value={output}
        readOnly
        style={styles.outputBox}
      />
    </div>
  );
}

const styles = {
  container: {
    width: "90%",
    margin: "20px auto",
    color: "#fff",
    fontFamily: "Arial"
  },
  title: {
    textAlign: "center",
    marginBottom: "20px",
    fontSize: "24px",
    fontWeight: "bold"
  },
  select: {
    width: "150px",
    padding: "10px",
    marginBottom: "10px",
    borderRadius: "6px"
  },
  codeEditor: {
    width: "100%",
    height: "260px",
    padding: "15px",
    borderRadius: "8px",
    background: "#1a1a1a",
    color: "#0f0",
    fontSize: "15px",
    fontFamily: "monospace",
    outline: "none",
    marginBottom: "15px"
  },
  runButton: {
    background: "#007bff",
    padding: "10px 20px",
    borderRadius: "8px",
    border: "none",
    color: "#fff",
    fontSize: "16px",
    cursor: "pointer",
    marginBottom: "20px"
  },
  label: {
    fontSize: "18px",
    marginBottom: "10px",
    marginTop: "10px"
  },
  inputBox: {
    width: "100%",
    height: "120px",
    padding: "10px",
    background: "#111",
    color: "#0f0",
    borderRadius: "8px",
    fontSize: "15px",
    fontFamily: "monospace",
    outline: "none",
    marginBottom: "20px"
  },
  outputBox: {
    width: "100%",
    height: "200px",
    padding: "10px",
    background: "#000",
    color: "#0f0",
    borderRadius: "8px",
    fontSize: "15px",
    fontFamily: "monospace",
    outline: "none"
  }
};

export default CodeSandbox;
