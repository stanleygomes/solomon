import json
from dataclasses import dataclass, field
from typing import Dict
from pathlib import Path
from datetime import datetime

@dataclass
class State:
    last_runs: Dict[str, str] = field(default_factory=dict)

def load_state(path: str) -> State:
    path_obj = Path(path)
    if not path_obj.exists():
        return State()
    
    with open(path_obj, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            # The Go version saves as "lastRuns", but Pythonic would be "last_runs"
            # We check both for compatibility
            last_runs = data.get("lastRuns") or data.get("last_runs") or {}
            return State(last_runs=last_runs)
        except json.JSONDecodeError:
            return State()

def save_state(path: str, state: State):
    path_obj = Path(path)
    # We save as "lastRuns" to maintain compatibility with the Go version
    data = {"lastRuns": state.last_runs}
    
    with open(path_obj, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
