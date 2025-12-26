// server/server.js  (ESM VERSION)
import express from "express";
import cors from "cors";
import path from "path";
import { fileURLToPath } from "url";

import { runPython } from "./runners/python.js";
import { runC } from "./runners/c.js";
import { runCPP } from "./runners/cpp.js";
import { runJava } from "./runners/java.js";
import { runJS } from "./runners/javascript.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

// Middleware
app.use(cors());
app.use(express.json({ limit: "10mb" }));

// Compiler API
app.post("/run", async (req, res) => {
  const { language, code, input } = req.body;

  if (!language || !code) {
    return res.json({ output: "❌ Missing language or code" });
  }

  try {
    let output = "";

    switch (language.toLowerCase()) {
      case "python":
        output = await runPython(code, input || "");
        break;
      case "c":
        output = await runC(code, input || "");
        break;
      case "cpp":
        output = await runCPP(code, input || "");
        break;
      case "java":
        output = await runJava(code, input || "");
        break;
      case "javascript":
        output = await runJS(code, input || "");
        break;
      default:
        output = `❌ Unknown language: ${language}`;
        break;
    }

    res.json({ output });
  } catch (err) {
    console.error("Server Error:", err);
    res.json({ output: "❌ Server Error:\n" + err.toString() });
  }
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`🔥 Compiler backend running at http://localhost:${PORT}`);
});
