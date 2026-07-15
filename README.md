# AI-First CRM Module Gateway

An intelligent, AI-powered Life Sciences CRM interface designed for field medical representatives. This module uses an **AI Assistant Console** driven by **FastAPI**, **LangGraph**, and **Redux** to parse natural language inputs in real time, automatically populating CRM forms, verifying local product inventories, performing historical HCP lookups, and generating automated follow-up tasks.

---

## 🚀 Key Features

* **Natural Language Interaction Processing:** Evaluates human conversations, extracting crucial metrics like HCP Name, Interaction Type, and Topics Discussed.
* **Automated Sentiment Invoicing:** Infers doctor response behaviors (Positive, Neutral, Negative) directly from chat logs and visually updates radio selections seamlessly.
* **Custom Sales Tool Integration:** Equipped with contextual routing pipelines to trigger simulated tools (`Inventory Assessment`, `HCP Profile Lookup`, `Task Automation`).
* **Resilient Fallback Core:** Designed with a robust frontend mitigation system ensuring operation synchronization even under strict network latency limitations.

---

## 🛠️ Tech Stack Architecture

### Frontend

* **React (v18)** – Component lifecycle orchestration
* **Redux Toolkit** – Centralized application state management (`interactionSlice`)
* **Tailwind CSS** – High-fidelity fluid design system layout
* **Lucide React** – Clean, modern iconography parameters

### Backend

* **FastAPI** – Ultra-low latency asynchronous API gateway router
* **LangGraph & LangChain** – Cyclic state-machine graph engineering for deterministic agent execution routing
* **Uvicorn** – High-performance ASGI server runtime implementation

---

## 📂 Project Structure

```text
├── backend/
│   ├── main.py            # FastAPI Application & Sentiment Pipeline
│   └── agent_graph.py     # Compiled LangGraph State Machine Logic
└── frontend/
    ├── src/
    │   ├── App.js         # Core Layout Console View Matrix
    │   ├── index.js       # React Application Entry Point
    │   └── store/
    │       ├── index.js   # Global Store Setup
    │       └── interactionSlice.js # Redux State Actions & Reducers
    └── package.json

```

---

## ⚙️ Installation & Setup

### 1. Backend Server Setup

Navigate into your backend folder, install dependencies, and run the gateway:

```bash
# Install Python packages
pip install fastapi uvicorn langchain langchain-core pydantic

# Launch the FastAPI application server
python main.py

```

*The service will start running locally at `[http://127.0.0.1:8000](http://127.0.0.1:8000)` with auto-reload activated.*

### 2. Frontend Application Setup

Navigate into your React project directory, install package dependencies, and boot the interface:

```bash
# Install NPM dependencies
npm install

# Run the local webpack server
npm start

```

*The browser portal will open up automatically at `http://localhost:3000`.*

---

## 🧪 Real-World Verification Prompts

You can test the system's core capabilities by entering the following natural language inputs directly into the AI Assistant Sidebar:

| Feature Target | Natural User Input Sample | Expected UI Result |
| --- | --- | --- |
| **Log Interaction** | *"Met Dr. Sharma at 2 PM today for a great meeting on Product X efficacy. Can you log this?"* | Populates HCP Name, selects Interaction Type, updates fields, and marks sentiment. |
| **Edit Fields** | *"Wait, change the follow-up actions field to email him the clinical trial PDF next week."* | Targets and alters the specified text container directly while maintaining form state. |
| **Inventory Tool** | *"Do I have enough sample kits and brochures left in my local inventory for this territory?"* | Triggers `[Inventory Tool Activated]` chat notification and updates sentiment context. |
| **HCP Lookup** | *"Can you pull up Dr. Sharma's profile and check their preferred contact hours real quick?"* | Invokes `[Profile Tool Activated]` without overriding fields currently in progress. |
| **Task Automation** | *"The meeting went great, can you automatically schedule a follow-up call reminder for next Monday?"* | Generates an automated calendar event state update instantly. |
