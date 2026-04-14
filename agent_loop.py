import json
import textwrap
from typing import Any

from openai import OpenAI

from tools import TOOLS


MAX_TURNS = 20


def _truncate(value: str, max_len: int = 1200) -> str:
    if len(value) <= max_len:
        return value
    return value[:max_len] + "\n... (truncated)"


def _format_tool_call(name: str, raw_args: str, args: dict[str, Any]) -> str:
    lines = [f"  [tool] {name}"]

    if not args:
        raw_preview = _truncate(raw_args.strip() or "(empty)")
        lines.append(f"    raw_args: {raw_preview}")
        return "\n".join(lines)

    for key, value in args.items():
        if isinstance(value, str):
            if "\n" in value:
                lines.append(f"    {key}:")
                body = _truncate(value)
                lines.append(textwrap.indent(body, "      "))
            else:
                lines.append(f"    {key}: {_truncate(value)}")
        else:
            compact = json.dumps(value, ensure_ascii=False)
            lines.append(f"    {key}: {_truncate(compact)}")

    return "\n".join(lines)


def agent_loop(user_message: str, messages: list, client: OpenAI) -> str:
    """
    Agent Loop：while 循环驱动 LLM 推理与工具调用。
    流程：
      1. 将用户消息追加到 messages
      2. 调用 LLM
      3. 若 LLM 返回 tool_calls → 逐个执行 → 结果追加到 messages → 继续循环
      4. 若 LLM 直接返回文本（无 tool_calls）→ 退出循环，返回文本
      5. 安全上限 MAX_TURNS 轮
    """
    messages.append({"role": "user", "content": user_message})
    tool_schemas = [t["schema"] for t in TOOLS.values()]
    for _turn in range(1, MAX_TURNS + 1):
        # --- LLM Call ---
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tool_schemas,
        )
        choice = response.choices[0]
        assistant_msg = choice.message
        # 将 assistant 消息追加到上下文
        messages.append(assistant_msg.model_dump())
        # --- 终止条件：无 tool_calls ---
        if not assistant_msg.tool_calls:
            return assistant_msg.content or ""
        # --- 执行每个 tool_call ---
        for tool_call in assistant_msg.tool_calls:
            name = tool_call.function.name
            raw_args = tool_call.function.arguments
            # 解析参数并调用工具
            try:
                args = json.loads(raw_args)
            except json.JSONDecodeError:
                args = {}
            print(_format_tool_call(name, raw_args, args))
            tool_entry = TOOLS.get(name)
            if tool_entry is None:
                result = f"[error] unknown tool: {name}"
            else:
                result = tool_entry["function"](**args)
            # 将工具结果追加到上下文
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )
    return "[agent] reached maximum turns, stopping."
