This is a minimal example of using **LangChain MCP (Multi-Component Protocol)** to connect multiple tools (Math and Weather) into a single intelligent agent powered by `langgraph` and `ChatOllama`.
## 🧪 Installation

### 1. Clone this repo (or copy files into a directory)

```bash
git clone <your-repo-url>
cd <your-project-dir>
````

### 2. Install dependencies

Make sure you have Python 3.9+ installed, then:

```bash
pip install -r requirements.txt
```

### 3. Install and run Ollama (if not already)

```bash
ollama serve
ollama pull llama3.2:3b
```

---

## 🚀 Running the Project

### 1. Start the weather server

```bash
python weather_server.py
```

This starts the weather tool on `http://127.0.0.1:8000/mcp`.

### 2. Start the client

In another terminal:

```bash
python client.py
```

This will:

* Launch the `math_server.py` as a subprocess
* Connect to the weather server over HTTP
* Initialize the agent
* Let you chat with the agent about math or weather

---

## 💬 Example Usage

```text
🧑 You: What is the result of 5 * 6?
🤖 Agent: The result of 5 * 6 is 30.

🧑 You: What's the weather in Tokyo?
🤖 Agent: Tokyo: sunny-23 degree
```

---

## 📦 requirements.txt

```txt
langchain
langgraph
langchain-ollama
langchain-mcp-adapters
mcp
```

Install with:

```bash
pip install -r requirements.txt
```

---

## 🧠 Notes

* `math_server.py` runs via `stdio`, which is handled by `MultiServerMCPClient`.
* `weather_server.py` must be running independently before launching the client.
* You can replace the tools or expand them to include more capabilities.
* This setup is designed for experimentation with MCP-based modular agents.

---


