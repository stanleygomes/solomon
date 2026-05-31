from typing import cast
from loguru import logger
from core.usecases.base import UseCase
from core.prompt import Prompt
from core.repositories.study_class import StudyClassRepository
from core.utils.json import JsonUtils
from core.exceptions.InvalidPromptResponseFormatError import (
  InvalidPromptResponseFormatError,
)


class PlanClassesUseCase(UseCase):
  """
  UseCase for generating and persisting the study syllabus/lessons for plans in PLANNING status.
  """

  def execute(self) -> None:
    """
    Executes the planning workflow, generating lessons for pending study plans.
    """
    logger.info("🚀 Executing Plan Classes workflow")

    repo = StudyClassRepository(self.context.db_manager)
    planning_classes = repo.get_planning_classes()
    if not planning_classes:
      logger.warning("💤 No study classes currently in PLANNING status.")
      return

    for plan in planning_classes:
      logger.debug(
        "📝 Planning syllabus for study plan: {} ({} days)",
        plan.subject,
        plan.duration_days,
      )

      prompt_context = {
        "subject": plan.subject,
        "duration_days": cast(int, plan.duration_days),
      }
      prompt_output = Prompt.execute("class-planning.md", context=prompt_context)

      try:
        lessons_data = JsonUtils.parse(prompt_output)
        if not isinstance(lessons_data, list):
          raise InvalidPromptResponseFormatError("Syllabus output is not a JSON list")
      except Exception as e:
        raise InvalidPromptResponseFormatError(
          f"AI generated syllabus for '{plan.subject}' was not valid: {e}"
        ) from e

      repo.create_lessons(cast(str, plan.id), lessons_data)
      repo.update_class_progress(cast(str, plan.id), current_day=1, status="ACTIVE")
      logger.info("✨ Successfully planned and activated study class: {}", plan.subject)
