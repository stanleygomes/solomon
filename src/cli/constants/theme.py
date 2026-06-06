from textual.theme import Theme

RETRO_THEME: Theme = Theme(
  name="retro",
  primary="#ffa500",
  secondary="#b27400",
  warning="#ffa62b",
  error="#ba3c5b",
  success="#4ebf71",
  accent="#ffa500",
  foreground="#ffffff",
  background="#0a0a0a",
  surface="#1e1e1e",
  panel="#1e1e1e",
  boost="#050505",
  dark=True,
  variables={
    "text": "#ffffff",
    "text-muted": "#888888",
    "primary-darken-1": "#e59500",
    "primary-darken-2": "#cc8500",
    "primary-darken-3": "#b27400",
  },
)
