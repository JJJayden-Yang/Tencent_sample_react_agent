import os
import sys

from openai import OpenAI

from agent_loop import agent_loop
from tools import SYSTEM_PROMPT


def main() -> None:
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("Error: please set DEEPSEEK_API_KEY environment variable.")
        sys.exit(1)

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    messages: list = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Agent ready. Type your message (or 'exit' to quit, 'clear' to reset).\n")

    while True:
        try:
            user_input = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not user_input:
            continue
        if user_input.lower() == "exit":
            print("Bye.")
            break
        if user_input.lower() == "clear":
            messages.clear()
            messages.append({"role": "system", "content": SYSTEM_PROMPT})
            print("(context cleared)\n")
            continue

        reply = agent_loop(user_input, messages, client)
        print(f"\nAgent> {reply}\n")


if __name__ == "__main__":
    main()
