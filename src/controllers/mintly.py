from datetime import datetime
from src.models.database import Database
from src.models.transaction import Transaction, TransactionType
from src.models.savings_goal import SavingsGoal


class Mintly:
    # Debug finished: Solucionado los bugs en la lógica de la aplicación, he tenido problemas a la hora de la actualizacion de datos
    def __init__(self):
        self.db = Database()

    def create_transaction(self, t_type, amount, category, description, date):
        t = Transaction(t_type, amount, category, description, date)
        return self.db.add_transaction(t)

    def add_to_savings_goal(self, goal_id, amount):
        savings_trans = Transaction(
            TransactionType.SAVINGS,
            amount,
            "💰 Ahorro",
            "Traspaso manual a meta",
            datetime.now().strftime("%Y-%m-%d")
        )
        self.db.add_transaction(savings_trans)

        self.db.update_savings_goal_amount(goal_id, amount)
        return True

    def get_monthly_balance(self):
        today = datetime.now()
        start = today.replace(day=1).strftime("%Y-%m-%d")
        end = today.strftime("%Y-%m-%d")

        data = self.db.get_balance_by_period(start, end)

        goals = self.db.get_all_savings_goals()
        total_saved = sum(g.current_amount for g in goals)

        return {
            'total_income': data['total_income'],
            'total_expense': data['total_expense'],
            'total_savings': total_saved,
            'balance': data['total_income'] - data['total_expense'] - total_saved
        }

    def get_financial_health_score(self):
        bal = self.get_monthly_balance()
        income = bal['total_income']

        if income <= 0:
            return {'score': 0, 'level': "Sin datos", 'message': "Registra ingresos para analizar"}

        savings_rate = (bal['total_savings'] / income) * 100
        expense_rate = (bal['total_expense'] / income) * 100

        score = int(savings_rate * 2 + (100 - expense_rate) * 0.8)
        score = max(0, min(100, score))

        if score >= 80:
            return {'score': score, 'level': "Excelente", 'message': "¡Ahorro manual impecable!"}
        elif score >= 50:
            return {'score': score, 'level': "Bueno", 'message': "Buen control de tus aportes."}
        else:
            return {'score': score, 'level': "Mejorable", 'message': "Intenta mover más dinero a tus metas."}

    def get_transactions_by_type(self, t_type, limit=None):
        return self.db.get_transactions_by_type(t_type, limit)

    def get_all_transactions(self, limit=None):
        return self.db.get_all_transactions(limit)

    def get_savings_by_category(self):
        return self.db.get_savings_by_category()

    def get_expenses_by_category(self):
        return self.db.get_expenses_by_category()

    def get_income_by_category(self):
        return self.db.get_income_by_category()

    def get_all_savings_goals(self):
        return self.db.get_all_savings_goals()

    def create_savings_goal(self, name, target_amount, current_amount, deadline, description):
        goal = SavingsGoal(name, target_amount, current_amount, deadline, description)
        return self.db.add_savings_goal(goal)

    def delete_transaction(self, t_id):
        return self.db.delete_transaction(t_id)

    def delete_savings_goal(self, g_id):
        return self.db.delete_savings_goal(g_id)