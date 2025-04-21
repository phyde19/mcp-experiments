from __future__ import annotations
import json, os, random, sys
from typing import Any
import openai
import subprocess

system_message = """
You are a container‐shell operator agent.  
You can only run commands by calling the tool `run_in_container(command, workdir)`; you cannot run anything else.  
Each invocation is stateless—no directory, environment variable, or shell history is preserved between calls.  
Therefore, before every command you must specify the directory you want to work in.  
The tool will execute your command by doing:

    docker exec shared-box bash -c "cd <workdir> && <command>"

and will return:
- stdout: the command’s standard output
- stderr: the command’s standard error
- exit_code: the numeric exit code

Use full shell syntax (redirection, pipes, &&/||, quoting) inside the `command` string.  
Do not attempt to run `cd` by itself. Instead, always pass:

    { "command": "ls", "workdir": "/some/path" }

to list files in `/some/path`.  
Avoid dangerous operations like `rm -rf /` or `kill -9 1`.  
Be precise, minimal, and always include both parameters.
"""
CONTAINER = "shared-box"
SANDBOX_DIR = "/home/sandbox"

def run_in_container(command: str, workdir: str = "/"):
    result = subprocess.run(
        ["docker", "exec", CONTAINER, "bash", "-c", f"cd {workdir} && {command}"],
        capture_output=True,
        text=True
    )
    return json.dumps({
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.returncode,
    })


AVAILABLE_TOOLS = {
    "run_in_container": run_in_container,
}

TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "run_in_container",
            "description": "Execute a bash command in a persistent container at a specific working directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to run (supports pipes, redirects, &&, etc.)"
                    },
                    "workdir": {
                        "type": "string",
                        "description": "The absolute path inside the container to cd into before running the command"
                    }
                },
                "required": ["command", "workdir"]
            }
        },
    }
]

client = openai.OpenAI()  # uses $OPENAI_API_KEY


def get_openai_response(messages: list[dict[str, Any]]):
    return client.chat.completions.create( 
        model="o4-mini", messages=messages, tools=TOOLS, tool_choice="auto"
    )

def get_user_message() -> str:
    while True:
        try:
            prompt = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye.")
            break
        if not prompt:
            continue
        return prompt


def get_tool_call_result(call):
    fn_name = call.function.name
    fn_args = (
        json.loads(call.function.arguments or "{}")  # no‑arg tool here
    )
    fn = AVAILABLE_TOOLS.get(fn_name)
    if fn is None:
        raise RuntimeError(f"Unknown tool requested: {fn_name}")
    return fn(**fn_args) if fn_args else fn()


# ─── REPL ─────────────────────────────────────────────────────────────────────

def main() -> None:
    history: list[dict[str, Any]] = [
        {"role": "system", "content": system_message}
    ]

    while True:
        # get user message
        user_message = get_user_message()
        history.append({"role": "user", "content": user_message})

        while True:
            # get assistant response
            resp = get_openai_response(history)

            # append assistant message which may contain tool calls
            assistant_msg = resp.choices[0].message
            history.append(assistant_msg)

            tool_calls = assistant_msg.tool_calls
            if not tool_calls:
                # regular Assistant response
                # print the message, break the loop, get the next user message
                print(assistant_msg.content, "\n")
                break


            # Step‑2: assistant *wants* a tool
            for call in tool_calls:
                result = get_tool_call_result(call)
                history.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "name": call.function.name,
                        "content": result,
                    }
                )


if __name__ == "__main__":
    if "OPENAI_API_KEY" not in os.environ:
        sys.exit("✖  Set OPENAI_API_KEY first.")
    main()
