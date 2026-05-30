from abc import ABC, abstractmethod


class AIProvider(ABC):
  """
  Abstract base class representing an AI provider.
  """

  @abstractmethod
  def generate(self, prompt: str) -> str:
    """
    Generate response text based on the provided prompt.
    """
    pass
