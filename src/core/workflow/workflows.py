from core.modules.daily_bread.workflows.create import DailyBreadWorkflow
from core.modules.classes.usecases.execute_class import ExecuteClassUseCase
from core.modules.classes.usecases.plan_classes import PlanClassesUseCase

WORKFLOWS = {
  "/daily-bread": DailyBreadWorkflow,
  "/execute-class": ExecuteClassUseCase,
  "/plan-classes": PlanClassesUseCase,
}
