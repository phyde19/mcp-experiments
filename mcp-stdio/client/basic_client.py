#!/usr/bin/env python3
"""
repl.py – single‑file demo of correct OpenAI tool‑calling order.
"""

from __future__ import annotations
import json, os, random, sys
from typing import Dict, List, Any
import openai

# ─── mock tool ────────────────────────────────────────────────────────────────
_WEATHER = ("sunny", "rainy", "cloudy")


def get_weather() -> str:
    """Return a random weather condition (demo stub)."""
    return random.choice(_WEATHER)


AVAILABLE_TOOLS = {
    "get_weather": get_weather,
}

TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Returns the current weather (mock).",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    }
]

client = openai.OpenAI()  # uses $OPENAI_API_KEY


def get_openai_response(messages: List[Dict[str, Any]]):
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
system_message = f"""
"""
def main() -> None:
    history: List[Dict[str, Any]] = [
        {"role": "system", "content": system_message}
    ]

    while True:
        # get user message
        user_message = get_user_message()
        history.append({"role": "user", "content": user_message})

        while True:
            # get assistant message
            resp = get_openai_response(history)
            assistant_msg = resp.choices[0].message

            # append assistant message which may contain tool calls
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
