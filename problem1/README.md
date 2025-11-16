# Problem 1 – AI-Powered Airline Call Center (Two-Agent System)

This module simulates two collaborating agents:

1. **Info Agent** – owns the `get_flight_info` function and returns structured
   flight data as JSON.
2. **QA Agent** – receives end-user questions, calls the Info Agent, and
   returns JSON answers.

## Files

- `agent_system.py` – contains the required functions (`get_flight_info`,
  `info_agent_request`, and `qa_agent_respond`). It can also be executed
  directly to see sample output.
- `api_keys.env` – placeholder for any future API keys (not required for the
  mock implementation).
- `requirements.txt` – Python dependencies.

## Setup

```bash
cd problem1
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running

```bash
python agent_system.py
```

The script prints JSON answers for a few example questions.

## Testing the Functions

You can open a Python shell after activating the virtual environment:

```python
from agent_system import get_flight_info, info_agent_request, qa_agent_respond

print(get_flight_info("AI123"))
print(info_agent_request("AI123"))
print(qa_agent_respond("When does Flight AI123 depart?"))
print(qa_agent_respond("What is the status of Flight AI999?"))
```
