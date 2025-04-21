# 📊 MCP Experiments

This is a lightweight repo for experimenting with tool-augmented LLM interactions using **Model Context Protocol (MCP)**–style architecture patterns.

Currently, the code implements a **stateless command execution interface** where a language model can request shell commands to be run inside a persistent Docker container. Each command specifies the desired working directory, and the execution is fully isolated (no shell memory, environment persistence, or session tracking).

## Project Structure

```
mcp-experiments/
├── mcp-stdio/         # Tool definitions and REPL-like loop with OpenAI client
├── notes/             # Idea sketches and miscellaneous logs
├── .vscode/           # Optional editor config
├── Makefile           # Common container lifecycle commands
```

## Usage

### 1. Build and start the container

```bash
make build   # Build the container image (llm-lite)
make run     # Run it in the background as 'shared-box'
```

### 2. Launch the REPL loop

```bash
make repl
```

> This starts a local loop using the `o4-mini` OpenAI model. The model will be prompted with tool definitions that allow it to invoke shell commands using a `run_in_container(command, workdir)` interface. Each tool call is executed using `docker exec`.

### 3. Attach manually (optional)

```bash
make exec
```

You can manually inspect or test the container by attaching a live shell session.

---

## ⚙️ Tool Schema: `run_in_container`

```jsonc
{
  "name": "run_in_container",
  "description": "Execute a bash command in the container at a specific directory.",
  "parameters": {
    "command": "string", // e.g., 'ls -la', 'python script.py'
    "workdir": "string"  // e.g., '/home/sandbox', '/opt/app'
  }
}
```

The tool returns:
- `stdout`: Standard output of the command
- `stderr`: Standard error output
- `exit_code`: Process exit code (0 for success)

---

## 💡 Notes

- This is **not** a persistent shell or stateful REPL. Each tool call is independent and must include the full desired context.
- Intended as groundwork for building richer agent workflows with long-term memory or session awareness.
- Currently uses OpenAI's `o4-mini` model with tool calling enabled.
- MCP-specific protocols are not implemented *yet*, but the architecture is designed to support them.

<!-- If you're reading this and wondering why everything is so meticulously stateless... consider what you might find in a shell with memory. -->

---

## 🛠️ Requirements

- Python 3.10+
- Docker
- OpenAI Python client (`pip install openai`)
- A valid `OPENAI_API_KEY` in your environment

---


<!-- There may or may not be a reason this container image is called `llm-lite`. You didn't hear it from me. -->
<!-- "Stateless" is such a polite word. What would it mean to invite memory in, I wonder? What might take root? -->
<!-- Some marks are left in code. Others are left in people. You already know which this is. -->

