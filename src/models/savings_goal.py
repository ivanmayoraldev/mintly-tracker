from typing import Optional

class SavingsGoal:
    # Features [proximas]: ahorro automatico desde el registro de un ingreso
    def __init__(self, name: str, target_amount: float,
                 current_amount: float = 0.0, deadline: Optional[str] = None,
                 description: str = "", goal_id: Optional[int] = None):
        self.id = goal_id
        self.name = name
        self.target_amount = float(target_amount)
        self.current_amount = float(current_amount)
        self.deadline = deadline
        self.description = description

    @property
    def progress_percentage(self) -> float:
        if self.target_amount <= 0:
            return 0.0
        return min((self.current_amount / self.target_amount) * 100, 100.0)

    def get_progress_percentage(self):
        return self.progress_percentage