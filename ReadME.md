# Google ADK Orchestra Workshop

A hands-on implementation of six AI agent patterns built with Google's Agent Development Kit (ADK), covering single-agent tool use, multi-agent pipelines, parallel execution, feedback loops, and external tool integration via MCP.

##  Repository Overview

This repository contains **six agent patterns**, with each pattern building on the concepts introduced in the previous one.

| # | Agent | Description |
|---|-------|-------------|
| **1** | `single_agent` | One agent with one custom Python tool. The base pattern everything else builds on. |
| **2** | `sequential_pipeline` | Three agents chained in order: write → review → refactor. Each agent's output feeds the next. |
| **3** | `parallel_research` | Three researcher agents run at the same time (fan-out), then a synthesizer agent merges their findings. |
| **4** | `loop_refinement` | A writer agent and a critic agent go back and forth until the output is good enough to publish. |
| **5** | `mcp_travel` | An agent connected to an external MCP server (Airbnb search). Built manually during the workshop's hands-on exercise. |
| **6** | `content_orchestra` | All five patterns combined into one working pipeline. |


##  Setup

### 1. Install dependencies

```bash
./setup.sh
```

### 2. Add your Gemini API key

Get a free API key from:

> https://aistudio.google.com/apikey

Paste your API key into the `.env` file.

### 3. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 4. Launch the ADK Playground

```bash
adk web
```


##  Requirements

- Python **3.10+**
- Node.js / npm *(required for the MCP exercise)*
- A free Google AI Studio API key


##  Key Takeaways

- The single and sequential agents establish the base pattern: an agent is a model with defined instructions, tools, and a role.
- `parallel_research` and `loop_refinement` move beyond prompting into system design — deciding what runs concurrently versus what needs a feedback loop is an architectural choice, not a config setting.
- `mcp_travel` demonstrates connecting an agent to an external MCP server, making the Model Context Protocol concept concrete rather than theoretical.
- `content_orchestra` shows how these primitives compose into a single production-style pipeline.

##  Tech Stack

- **Google ADK** — Agent framework
- **Gemini API** — Underlying LLM
- **Model Context Protocol (MCP)** — External tool and service integration
- **Python 3.10+**
