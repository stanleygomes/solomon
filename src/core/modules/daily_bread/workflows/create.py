from typing import override
from core.workflow.base import Workflow
from core.container import Container
from loguru import logger
from core.services.ai.prompt import Prompt
from core.utils.date import DateUtils
from core.constants.themes import PREDEFINED_THEMES
from core.services.render.renderer import TemplateRenderer
from core.utils.markdown import MarkdownUtils
from core.services.mail.message import MailMessage
from core.exceptions.PreconditionFailedError import PreconditionFailedError


class DailyBreadWorkflow(Workflow):
  """
  Workflow for generating and emailing the Daily Bread devotional.
  """

  def __init__(self, container: Container) -> None:
    super().__init__(container)

  @override
  def should_execute(self) -> bool:
    """
    Checks if the Daily Bread devotional has already been successfully sent today.
    """

    today = DateUtils.today_str()
    if self.container.task_execution_repo.has_run_on_date("daily-bread", today):
      return False

    return True

  @override
  def execute(self, input: str | None = None) -> str:
    """
    Executes the Daily Bread email generation and delivery workflow.
    """

    logger.info("🚀 Executing Daily Bread Workflow")

    # 1. Execute the prompt
    logger.debug("📝 Running AI prompt: daily-bread.md")
    prompt_output = Prompt.execute("daily-bread.md")

    # 2. Compile HTML email template with generated text and current date
    today = DateUtils.today_str()
    html_content = MarkdownUtils.to_html(prompt_output)

    render_context = {
      "title": f"The Daily Bread for {today}",
      "date": today,
      "content": html_content,
      "use_case": "daily-bread",
    }

    logger.debug("🎨 Rendering HTML template with theme: noemi")
    theme = PREDEFINED_THEMES["noemi"]
    html_body = TemplateRenderer.render_html(theme, render_context)

    # 3. Use Mailer to send email
    sender = self.container.config.mail.email_from
    to = self.container.config.mail.email_to
    if not to:
      raise PreconditionFailedError("EMAIL_TO is not configured in MailConfig")

    logger.debug("✉️ Preparing email to: {}", to)
    message = MailMessage(
      sender=sender,
      to=to,
      subject=f"The Daily Bread for {today}",
      body=html_body,
    )

    self.container.mailer.send(message)
    logger.info("✨ Daily Bread email sent successfully")

    return prompt_output
