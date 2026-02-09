from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QComboBox, QDateEdit, QMessageBox)
from PySide6.QtCore import QDate
from src.models.transaction import TransactionType, Transaction

class AddTransactionDialog(QDialog):
    def __init__(self, parent=None, transaction_type=TransactionType.EXPENSE):
        super().__init__(parent)
        self.parent_widget = parent
        self.setWindowTitle("Nueva Transacción")
        self.setFixedWidth(350)
        self.transaction_data = {}
        self.transaction_type = transaction_type

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Monto (€):"))
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        layout.addWidget(self.amount_input)

        layout.addWidget(QLabel("Categoría:"))
        self.cat_combo = QComboBox()
        cats = Transaction.INCOME_CATEGORIES if transaction_type == TransactionType.INCOME else Transaction.EXPENSE_CATEGORIES
        self.cat_combo.addItems(cats.keys())
        layout.addWidget(self.cat_combo)

        layout.addWidget(QLabel("Fecha:"))
        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        layout.addWidget(self.date_input)

        btns = QHBoxLayout()
        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        btns.addWidget(save_btn)
        btns.addWidget(cancel_btn)
        layout.addLayout(btns)

    def accept(self):
        try:
            amount_text = self.amount_input.text().replace(',', '.')
            amount = float(amount_text)

            self.transaction_data = {
                'type': self.transaction_type,
                'amount': amount,
                'category': self.cat_combo.currentText(),
                'description': "",
                'date': self.date_input.date().toString("yyyy-MM-dd")
            }

            super().accept()
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, introduce un monto válido.")


class AddSavingsGoalDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nueva Meta de Ahorro")
        self.setFixedWidth(300)
        layout = QVBoxLayout(self)

        self.name_in = QLineEdit()
        self.name_in.setPlaceholderText("Nombre (ej: Viaje)")
        self.target_in = QLineEdit()
        self.target_in.setPlaceholderText("Objetivo (€)")

        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.name_in)
        layout.addWidget(QLabel("Objetivo (€):"))
        layout.addWidget(self.target_in)

        btn = QPushButton("Crear Meta")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

    def get_data(self):
        return {
            'name': self.name_in.text(),
            'target_amount': float(self.target_in.text() or 0),
            'current_amount': 0,
            'deadline': QDate.currentDate().addYears(1).toString("yyyy-MM-dd"),
            'description': ""
        }


class AddToSavingsGoalDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aportar a Meta")
        self.setFixedWidth(300)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("¿Cuánto quieres ahorrar hoy? (€):"))
        self.amount_in = QLineEdit()
        self.amount_in.setPlaceholderText("0.00")
        layout.addWidget(self.amount_in)

        layout.addWidget(QLabel("Seleccionar Meta Destino:"))
        self.goal_combo = QComboBox()
        self.goals = controller.get_all_savings_goals()

        if not self.goals:
            self.goal_combo.addItem("No hay metas creadas", None)
        else:
            for g in self.goals:
                self.goal_combo.addItem(f"{g.name} (Saldo: €{g.current_amount:.0f})", g.id)

        layout.addWidget(self.goal_combo)

        btn = QPushButton("Confirmar Ahorro")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

    def get_data(self):
        goal_id = self.goal_combo.currentData()
        if goal_id is None:
            return None

        try:
            amount = float(self.amount_in.text().replace(',', '.'))
            return {
                'amount': amount,
                'goal_id': goal_id
            }
        except ValueError:
            return None