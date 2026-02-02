```markdown
# Stitcher-Core: Autonomous Web Assembly Framework
**Author:** Faith Adeniyi  
**Status:** v1.0.0-Production (Refactored for Scalability)

## 🚀 Overview
Stitcher-Core is a deterministic, agentic framework designed to orchestrate local LLMs (Ollama/Llama 3.2) for the automated assembly of high-fidelity web interfaces. By decoupling cognitive reasoning from physical file I/O, Stitcher-Core ensures secure, scalable, and self-healing UI deployment.

## 🏗️ System Architecture
The framework operates via a multi-agent pipeline governed by a central project manifest:

* **Cognitive Layer (Orchestrator):** Reasons through brand intelligence to derive structural UI blueprints.
* **Ingestion Layer (Researcher):** Sources and sanitizes entity-specific data.
* **Assembly Layer (Engine):** Deterministically stitches HTML components into a master layout.
* **Self-Healing Layer (Debugger/Guardian):** Intercepts structural hallucinations and enforces security protocols.

graph TD
    A[Project Manifest] -->|Configures| B(Orchestrator)
    B -->|Task Routing| C{Dual-Model Logic}
    C -->|Narrative| D[Llama 3.2:1b]
    C -->|Code/Structure| E[Qwen2.5-Coder:7b]
    D & E -->|JSON Plan| F[Agentic Guardian]
    F -->|Sanitization| G[Assembly Engine]
    G -->|Stitching| H[Component Library]
    H -->|Raw HTML| I[Debugger/Editor]
    I -->|Polished Artifact| J[Production index.html]

## 🛠️ Tech Stack
* **Core:** Python 3.x
* **AI Inference:** Ollama (Llama 3.2:1b)
* **Frontend Logic:** Tailwind CSS, HTML5, Jinja-style templating
* **Security:** Regex-based XSS mitigation & Payload Auditing

## 🧠 Model Orchestration Strategy
To maximize output quality while maintaining local performance, Stitcher-Core utilizes a bifurcated inference strategy:

* **Logic & Syntax (Qwen2.5-Coder:7b):** Specialized for deterministic code generation, CSS architecture, and structural integrity.
* **Narrative & Reasoning (Llama3.2:1b):** Optimized for brand analysis, copywriting, and "vibe" orchestration.

## 📦 Installation & Usage
1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/Faith-Adeniyi/Stitcher-Core-Agentic-UI-Orchestration-Framework](https://github.com/Faith-Adeniyi/Stitcher-Core-Agentic-UI-Orchestration-Framework)

```

2. **Initialize Local LLM:**
```bash
ollama pull llama3.2:1b
ollama pull qwen2.5-coder:7b

```


3. **Configure the Manifest:**
Edit `project_manifest.json` to define your target UI components and design specs.
4. **Execute Pipeline:**
```bash
python main.py

```



## 🛡️ Professional Standards

This project adheres to **Enterprise-Grade** standards:

* **Zero Hard-Coding:** All logic is manifest-driven for portability.
* **Deterministic Safety:** Critical data injection bypasses stochastic AI processes.
* **Self-Healing:** Autonomous patching of malformed HTML structures.

---

## 🛡️ Security-First Protocols
To counter the risks associated with stochastic AI code generation, Stitcher-Core implements a **Defensive Ingestion Layer**:

* **Deterministic Scrubbing:** AI-generated plans are cross-referenced against a whitelist of approved components.
* **Surgical Sanitization:** The `AgenticGuardian` module intercepts common web vulnerabilities (XSS, Script Injections) using regex-based forensic scans.
* **Payload Auditing:** Strict size and type enforcement to prevent Denial of Service (DoS) vectors through malformed LLM outputs.

*Built with precision. Optimized for the future of Agentic Web Development.*

```

---
