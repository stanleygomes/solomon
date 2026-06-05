from core.workflow import Workflow
from core.context import WorkflowContext
from loguru import logger
from core.services.ai.prompt import Prompt


class DailyBreadWorkflow(Workflow):
  """
  Workflow for generating and emailing the Daily Bread devotional.
  """

  def __init__(self, context: WorkflowContext) -> None:
    super().__init__(context)

  def should_execute(self) -> bool:
    """
    Checks if the Daily Bread devotional has already been successfully sent today.
    """
    from core.utils.date import DateManager

    today = DateManager.today_str()
    if self.context.task_execution_repo.has_run_on_date("daily-bread", today):
      return False

    return True

  def execute(self) -> None:
    """
    Executes the Daily Bread email generation and delivery workflow.
    """
    logger.info("🚀 Executing Daily Bread Workflow")

    # 1. Execute the prompt
    logger.debug("📝 Running AI prompt: daily-bread.md")
    prompt_output = Prompt.execute("daily-bread.md")

    # 2. Compile HTML email template with generated text and current date
    from core.utils.date import DateManager
    from core.constants.themes import PREDEFINED_THEMES
    from core.services.render.renderer import TemplateRenderer
    from core.utils.markdown import Markdown

    today = DateManager.today_str()
    html_content = Markdown.to_html(prompt_output)

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
    from core.services.mail.message import MailMessage
    from core.exceptions.PreconditionFailedError import PreconditionFailedError

    sender = self.context.config.mail.email_from
    to = self.context.config.mail.email_to
    if not to:
      raise PreconditionFailedError("EMAIL_TO is not configured in MailConfig")

    logger.debug("✉️ Preparing email to: {}", to)
    message = MailMessage(
      sender=sender,
      to=to,
      subject=f"The Daily Bread for {today}",
      body=html_body,
    )

    self.context.mailer.send(message)
    logger.info("✨ Daily Bread email sent successfully")
