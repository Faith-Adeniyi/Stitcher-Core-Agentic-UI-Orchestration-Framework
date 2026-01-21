# 🛠️ Stitcher-Core: Secure Agentic Web-Assembly Framework

**Stitcher-Core** is a professional-grade, autonomous pipeline designed to transform raw business data into production-ready web interfaces using local LLMs. By decoupling reasoning (Agents) from execution (Core Engine), the framework achieves high-fidelity results on consumer-grade hardware (**8GB RAM**).

---

## 🏗️ System Architecture

The framework follows a modular "Chain of Thought" architecture, ensuring that every piece of AI-generated content is researched, reasoned, debugged, and secured before assembly.

```mermaid
graph TD
    %% Layer 1: Data Ingestion
    A[Brand Data: JSON/CSV] --> B[WebResearcher Agent]
    
    %% Layer 2: Reasoning
    B --> C[UIOrchestrator - The Brain]
    C --> D{Agentic Debugger}
    
    %% Layer 3: Self-Healing & Safety
    D -- "Surgical Patch" --> C
    D -- "Validated Logic" --> E[AgenticGuardian - Security]
    
    %% Layer 4: Deterministic Assembly
    E --> F[Component Editor - The Refiner]
    F --> G[Assembly Engine - The Hands]
    
    %% Layer 5: Output
    G --> H[Production UI: index.html]

    %% Muted Professional Styling
    style C fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000
    style D fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,color:#000
    style E fill:#ffebee,stroke:#c62828,stroke-width:2px,color:#000
    style G fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000

```

---

## 🧩 Framework Modules

### **1. Cognitive Layer (Agents)**

* **WebResearcher:** Extracts structured "Brand Memory" from unstructured sources.
* **UIOrchestrator:** A decision-making agent that leverages **Ollama (Llama 3)** to determine optimal layout structures and component selection.

### **2. Resilience & Safety Layer (Core)**

* **Agentic Debugger (Self-Healing):** An autonomous loop that identifies structural failures (e.g., mismatched tags) and performs surgical patches without full code rewrites.
* **AgenticGuardian (Security):** Implements **Defense-in-Depth**. Features include:
* **XSS Prevention:** Input sanitization for malicious scripts and `<iframe>` injections.
* **DoS Mitigation:** Resource guardrails to prevent memory exhaustion on 8GB systems.
* **Forensic Logging:** Maintains `data/security_audit.log` for system observability.



### **3. Assembly & Refinement Layer**

* **Component Editor:** Performs deterministic data injection (pricing, contact info) to eliminate LLM hallucinations.
* **Assembly Engine:** A robust, path-validated builder that stitches modular HTML/Tailwind components into the final document.

---

## 🚀 Deployment (8GB RAM Optimized)

1. **Environment Setup:**
```bash
pip install -r requirements.txt

```


2. **Local LLM:** Ensure [Ollama](https://ollama.ai/) is running with `llama3`.
3. **Execute Pipeline:**
```bash
python main.py

```



---

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **Inference:** Ollama (Local LLM Orchestration)
* **Security:** Custom Regex-based Sanitization Middleware
* **Styling:** Tailwind CSS (Modular Component Library)

