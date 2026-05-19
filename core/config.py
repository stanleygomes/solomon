import json
from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path

@dataclass
class TaskConfig:
    id: str
    name: str
    command: str
    args: List[str] = field(default_factory=list)
    dir: str = ""
    schedule: str = "daily"

@dataclass
class Config:
    tasks: List[TaskConfig]

def load_config(path: str) -> Config:
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    
    with open(path_obj, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    tasks = [TaskConfig(**task) for task in data.get("tasks", [])]
    return Config(tasks=tasks)
