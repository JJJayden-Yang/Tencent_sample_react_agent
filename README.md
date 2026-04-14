# Tencent_sample_react_agent

A React agent created by tencent:https://mp.weixin.qq.com/s/YAGaXOWh2GBPSNsQt5SlJg

## ⚠️ Security Warning

**IMPORTANT: Please read before using this agent**

This agent has powerful capabilities including:
- Shell command execution (`shell_exec`)
- File read/write operations (`file_read`, `file_write`)
- Python code execution (`python_exec`)

### Risks

⚠️ **DO NOT** use this agent in the following scenarios:
- Production environments without proper sandboxing
- With untrusted LLM models or prompts
- On systems containing sensitive data
- Without understanding the security implications

### Safety Recommendations

1. **Run in an isolated environment**: Use Docker containers or VMs
2. **Restrict permissions**: Modify the code to limit file system access
3. **Monitor execution**: Always supervise the agent's actions
4. **Use trusted models**: Only connect to reputable LLM providers

### Example Security Hardening

To restrict file operations to a specific directory:

```python
import os

ALLOWED_BASE = os.path.abspath('./sandbox')

def is_safe_path(path):
    """Check if path is within allowed directory."""
    abs_path = os.path.abspath(path)
    return abs_path.startswith(ALLOWED_BASE)
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your API key:
```bash
export DEEPSEEK_API_KEY=your_api_key_here
```

3. Run the agent:
```bash
python cli.py
```

## Usage

- Type your message and press Enter
- Type `exit` to quit
- Type `clear` to reset the conversation context

## Architecture

See [archi.md](archi.md) for detailed architecture documentation.

## License

This is a sample implementation for educational purposes.
