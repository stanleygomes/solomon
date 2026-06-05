from core.database.setup import DatabaseSetup
from core.database.models.study_class import StudyClassModel
from core.database.models.lesson import LessonModel
from core.utils.date import DateManager


class StudyClassRepository:
  """
  Repository for managing StudyClassModel and LessonModel records in SQLite using Peewee.
  """

  def __init__(self, db_manager: DatabaseSetup) -> None:
    self.db_manager = db_manager
    self.db_manager.db.bind([StudyClassModel, LessonModel])

  def get_active_classes(self) -> list[StudyClassModel]:
    """
    Retrieves all study classes with ACTIVE status.
    """
    return list(StudyClassModel.select().where(StudyClassModel.status == "ACTIVE"))

  def get_planning_classes(self) -> list[StudyClassModel]:
    """
    Retrieves all study classes in PLANNING status.
    """
    return list(StudyClassModel.select().where(StudyClassModel.status == "PLANNING"))

  def get_lesson_for_day(self, class_id: str, day_number: int) -> LessonModel | None:
    """
    Retrieves the lesson for a specific class plan and day number.
    """
    return (
      LessonModel.select()
      .where(
        (LessonModel.class_plan == class_id) & (LessonModel.day_number == day_number)
      )
      .first()
    )

  def update_class_progress(self, class_id: str, current_day: int, status: str) -> None:
    """
    Updates the current day and status of a study class.
    """
    query = StudyClassModel.update(current_day=current_day, status=status).where(
      StudyClassModel.id == class_id
    )
    query.execute()

  def update_lesson_status(self, lesson_id: str, status: str) -> None:
    """
    Updates the completion status of a lesson.
    """
    query = LessonModel.update(status=status).where(LessonModel.id == lesson_id)
    query.execute()

  def create_class(self, subject: str, duration_days: int) -> StudyClassModel:
    """
    Creates and returns a new study class in PLANNING status.
    """
    return StudyClassModel.create(
      subject=subject,
      duration_days=duration_days,
      current_day=1,
      status="PLANNING",
      created_at=DateManager.now_iso(),
    )

  def create_lessons(self, class_id: str, lessons_data: list[dict]) -> None:
    """
    Bulk inserts lessons associated with a class plan.
    """
    with self.db_manager.db.atomic():
      for lesson in lessons_data:
        LessonModel.create(
          class_plan=class_id,
          day_number=lesson["day_number"],
          topic=lesson["topic"],
          summary=lesson.get("summary", ""),
          status="PENDING",
        )
