from core.usecases.daily_bread import DailyBreadUseCase
from core.usecases.execute_class import ExecuteClassUseCase
from core.usecases.plan_classes import PlanClassesUseCase

USE_CASES = {
  "daily-bread": DailyBreadUseCase,
  "execute-class": ExecuteClassUseCase,
  "plan-classes": PlanClassesUseCase,
}
