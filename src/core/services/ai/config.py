from dataclasses import dataclass


@dataclass(frozen=True)
class AiConfig:
  provider: str
