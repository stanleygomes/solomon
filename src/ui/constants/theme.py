from textual.theme import Theme

RETRO_THEME: Theme = Theme(
  name="retro",
  primary="#00ff00",
  secondary="#006400",
  warning="#ffa62b",
  error="#ba3c5b",
  success="#4ebf71",
  accent="#39ff14",
  foreground="#00ff00",
  background="#000000",
  surface="#0a0a0a",
  panel="#101010",
  boost="#081008",
  dark=True,
  variables={
    "text": "#00ff00",
    "text-muted": "#008000",
    "primary-darken-1": "#00d900",
    "primary-darken-2": "#00b300",
    "primary-darken-3": "#008d00",
  },
)
