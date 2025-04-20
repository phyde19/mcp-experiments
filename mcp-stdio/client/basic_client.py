#!/usr/bin/env python3
"""
repl.py – ultra‑lean CLI chat loop with one mock tool.
-----------------------------------------------------
$ pip install --upgrade openai
$ export OPENAI_API_KEY=sk‑...
$ python repl.py
"""

from __future__ import annotations

import os
import random
import sys
from typing import List, Dict, Any

import openai

# ---- mock tool ---------------------------------------------------------------

_WEATHER = ("sunny", "rainy", "cloudy")


def get_weather() -> str:
    """Return a random weather condition."""
    return random.choice(_WEATHER)


# ---- OpenAI plumbing ---------------------------------------------------------

TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Returns the current weather (mock).",
            "parameters": {
                "type": "object",
                "properties": {},  # no args
                "required": [],
            },
        },
    }
]

client = openai.OpenAI()  # picks up OPENAI_API_KEY


def chat_completion(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Ship a single request to OpenAI and return the raw response object."""
    return client.chat.completions.create(
        model="gpt-4o",          # swap for the exact 4.1 model name when available
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )


# ---- REPL driver -------------------------------------------------------------

def main() -> None:
    history: List[Dict[str, Any]] = [
        {"role": "system", "content": "You are a concise, capable assistant."}
    ]

    while True:
        try:
            user_text = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye.")
            break

        if not user_text:
            continue

        history.append({"role": "user", "content": user_text})

        # loop because a single turn may include tool‑call → tool‑result → follow‑up
        while True:
            resp = chat_completion(history)
            msg = resp.choices[0].message

            # Did the model request a tool?
            if msg.tool_calls:
                call = msg.tool_calls[0]  # we only defined one tool
                if call.function.name == "get_weather":
                    tool_result = get_weather()
                    history.append(
                        {
                            "role": "tool",
                            "tool_call_id": call.id,
                            "name": "get_weather",
                            "content": tool_result,
                        }
                    )
                    # Let the model integrate the tool result
                    continue
                else:  # unknown tool – shouldn't happen
                    print("?? requested unknown tool:", call.function.name, file=sys.stderr)
                    break

            # Normal assistant reply
            history.append(msg)
            print(msg.content, "\n")
            break


if __name__ == "__main__":
    if "OPENAI_API_KEY" not in os.environ:
        sys.exit("Set OPENAI_API_KEY first.")
    main()
