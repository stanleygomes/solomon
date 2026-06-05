from core.module.daily_bread.worfkflows.create import DailyBreadWorkflow
from core.module.classes.usecases.execute_class import ExecuteClassUseCase
from core.module.classes.usecases.plan_classes import PlanClassesUseCase

USE_CASES = {
  "daily-bread": DailyBreadWorkflow,
  "execute-class": ExecuteClassUseCase,
  "plan-classes": PlanClassesUseCase,
}
