from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
  name: str
  background: str
  surface: str
  surface_variant: str
  primary: str
  secondary: str
  border: str
  text_primary: str
  text_secondary: str
  text_on_variant: str


