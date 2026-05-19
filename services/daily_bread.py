import os
from pathlib import Path
from datetime import datetime
import markdown2
from jinja2 import Template
from dotenv import load_dotenv

from core.logger import Logger
from core.mailer import Mailer, MailMessage
from core.ai import AIProvider


class DailyBreadService:
  def __init__(self, logger: Logger, assets_dir: str):
    self.logger = logger
    self.assets_dir = Path(assets_dir)

  def run(self, ai_provider: AIProvider) -> None:
    load_dotenv()
    self.logger.log("[daily-bread] Starting devotional newsletter generation...")

    date_display = self._get_formatted_date()
    today_iso = datetime.now().strftime("%Y-%m-%d")

    prompt_file = self.assets_dir / "prompts" / "daily-bread.md"
    layout_file = self.assets_dir / "templates" / "daily-bread.html"

    # 1. Generate Content
    markdown_content = self._execute_ai(ai_provider, prompt_file)

    # 2. Compile HTML
    html_content = self._compile_newsletter(markdown_content, layout_file, date_display)

    # 3. Save History
    self._save_history_log(html_content, today_iso)

    # 4. Send Email
    self._send_email(html_content)

    self.logger.log(
      "[daily-bread] Devotional newsletter successfully sent to recipient!"
    )

  def _get_formatted_date(self) -> str:
    months = {
      1: "Janeiro",
      2: "Fevereiro",
      3: "Março",
      4: "Abril",
      5: "Maio",
      6: "Junho",
      7: "Julho",
      8: "Agosto",
      9: "Setembro",
      10: "Outubro",
      11: "Novembro",
      12: "Dezembro",
    }
    now = datetime.now()
    return f"{now.day} de {months[now.month]} de {now.year}"

  def _execute_ai(self, p: AIProvider, prompt_path: Path) -> str:
    if not prompt_path.exists():
      raise FileNotFoundError(f"Prompt file not found at: {prompt_path}")

    self.logger.log("[daily-bread] Reading prompt from: %s", str(prompt_path))
    prompt_content = prompt_path.read_text(encoding="utf-8").strip()

    self.logger.log("[daily-bread] Dispatching prompt content to AI provider...")
    return p.generate(prompt_content)

  def _compile_newsletter(
    self, content_md: str, template_path: Path, date_str: str
  ) -> str:
    if not template_path.exists():
      raise FileNotFoundError(f"Template file not found at: {template_path}")

    self.logger.log("[daily-bread] Converting Markdown to HTML...")
    content_html = markdown2.markdown(
      content_md, extras=["tables", "fenced-code-blocks"]
    )

    self.logger.log("[daily-bread] Loading HTML layout from: %s", str(template_path))
    layout_html = template_path.read_text(encoding="utf-8")

    # Using Jinja2 for safer and more flexible injection
    # But for compatibility with existing templates using {{date}} and {{content}}
    template = Template(layout_html)
    return template.render(date=date_str, content=content_html)

  def _save_history_log(self, html_content: str, date_iso: str) -> Path:
    history_dir = self.assets_dir.parent / "temp" / "history"
    history_dir.mkdir(parents=True, exist_ok=True)

    log_file = history_dir / f"{date_iso}.html"
    log_file.write_text(html_content, encoding="utf-8")

    self.logger.log("[daily-bread] Local HTML history saved at: %s", str(log_file))
    return log_file

  def _send_email(self, html_content: str, template_name: str) -> None:
    self.logger.log(
      "[daily-bread] Preparing to dispatch newsletter via generic mailer..."
    )

    mailer = Mailer.from_env()

    email_from = os.getenv("EMAIL_FROM")
    if not email_from:
      email_from = f"Pão Diário <{os.getenv('SMTP_USER')}>"

    email_subject = os.getenv("EMAIL_SUBJECT")
    if not email_subject:
      display_name = template_name.replace("_", " ").capitalize()
      email_subject = f"Pão Diário - {display_name}"

    msg = MailMessage(
      sender=email_from,
      to=os.getenv("EMAIL_TO", ""),
      subject=email_subject,
      body=html_content,
    )

    mailer.send(msg)
    self.logger.log("[daily-bread] Email successfully delivered!")
