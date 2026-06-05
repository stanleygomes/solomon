from typing import cast
from loguru import logger
from core.workflow import Workflow
from core.services.ai.prompt import Prompt
from core.database.repositories.study_class import StudyClassRepository


class ExecuteClassUseCase(Workflow):
  """
  UseCase for generating, emailing, and advancing daily study classes.
  """

  def execute(self) -> None:
    """
    Executes the daily study segment delivery and advancement workflow.
    """
    logger.info("🚀 Executing Classes/Study workflow")

    repo = StudyClassRepository(self.context.db_manager)
    active_classes = repo.get_active_classes()
    if not active_classes:
      logger.warning("🚫 No active study classes found to process.")
      return

    from core.utils.date import DateManager
    from core.constants.themes import PREDEFINED_THEMES
    from core.services.render.renderer import TemplateRenderer
    from core.utils.markdown import Markdown
    from core.services.mail.message import MailMessage
    from core.exceptions.PreconditionFailedError import PreconditionFailedError

    today = DateManager.today_str()
    sender = self.context.config.mail.email_from
    to = self.context.config.mail.email_to
    if not to:
      raise PreconditionFailedError("EMAIL_TO is not configured in MailConfig")

    for active_class in active_classes:
      lesson = repo.get_lesson_for_day(
        cast(str, active_class.id), cast(int, active_class.current_day)
      )

      if not lesson:
        logger.warning(
          "⚠️ Lesson for Day {} of study class '{}' not found. Skipping.",
          cast(int, active_class.current_day),
          active_class.subject,
        )
        continue

      logger.info(
        "📚 Processing study lesson: {} - Day {}/{} (Topic: {})",
        active_class.subject,
        active_class.current_day,
        active_class.duration_days,
        lesson.topic,
      )

      prompt_context = {
        "subject": active_class.subject,
        "topic": lesson.topic,
        "summary": lesson.summary,
        "current_day": cast(int, active_class.current_day),
        "duration_days": cast(int, active_class.duration_days),
      }
      prompt_output = Prompt.execute("class-segment.md", context=prompt_context)

      html_content = Markdown.to_html(prompt_output)
      render_context = {
        "date": today,
        "content": html_content,
      }
      theme = PREDEFINED_THEMES["noah"]
      html_body = TemplateRenderer.render_html(theme, render_context)

      logger.debug("✉️ Preparing daily study email to: {}", to)
      message = MailMessage(
        sender=sender,
        to=to,
        subject=f"Daily Study - {active_class.subject} (Day {active_class.current_day}/{active_class.duration_days})",
        body=html_body,
      )
      self.context.mailer.send(message)

      repo.update_lesson_status(cast(str, lesson.id), status="COMPLETED")

      next_day = cast(int, active_class.current_day) + 1
      status = "ACTIVE"
      if cast(int, active_class.current_day) >= cast(int, active_class.duration_days):
        status = "COMPLETED"
        logger.info("🎓 Completed study class plan: {}", active_class.subject)

      repo.update_class_progress(
        cast(str, active_class.id),
        next_day,
        status,
      )
      logger.info(
        "✨ Successfully processed and advanced study class: {}",
        active_class.subject,
      )
