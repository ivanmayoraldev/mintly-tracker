from enum import Enum
from dataclasses import dataclass
from typing import Optional

class TransactionType(Enum):
    # Trabajar con diccionarios me ha ayudado a desarrollar mejor la aplicacion
    INCOME = "ingreso"
    EXPENSE = "gasto"
    SAVINGS = "ahorro"

@dataclass
class Transaction:
    transaction_type: TransactionType
    amount: float
    category: str
    description: str
    date: str
    transaction_id: Optional[int] = None

    @property
    def id(self):
        return self.transaction_id

    def is_income(self):
        return self.transaction_type == TransactionType.INCOME

    def is_expense(self):
        return self.transaction_type == TransactionType.EXPENSE

    def is_savings(self):
        return self.transaction_type == TransactionType.SAVINGS

    INCOME_CATEGORIES = {
        "💼 Salario": "#10B981",
        "📈 Inversiones": "#3B82F6",
        "🎁 Regalos": "#F59E0B",
        "💰 Otros": "#6B7280"
    }

    EXPENSE_CATEGORIES = {
        "🏠 Vivienda": "#EF4444",
        "🛒 Alimentación": "#F59E0B",
        "🚌 Transporte": "#3B82F6",
        "🎬 Ocio": "#8B5CF6",
        "🏥 Salud": "#10B981",
        "🛍️ Compras": "#EC4899",
        "💰 Ahorro": "#8E44AD",
        "❓ Otros": "#6B7280"
    }

    def get_color(self):
        if self.is_income():
            return self.INCOME_CATEGORIES.get(self.category, "#6B7280")
        return self.EXPENSE_CATEGORIES.get(self.category, "#6B7280")