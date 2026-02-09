from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QMessageBox, QProgressBar, QScrollArea, QTabWidget
)
from PySide6.QtCore import Qt
from src.models.transaction import TransactionType
from src.views.dialogs import (
    AddTransactionDialog, AddSavingsGoalDialog,
    AddToSavingsGoalDialog
)
from src.views.stats_tab import StatisticsTab

COLORS = {
    "bg": "#0F172A",
    "surface": "#1E293B",
    "surface_hover": "#334155",
    "primary": "#3B82F6",
    "success": "#10B981",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "accent": "#8B5CF6",
    "text_main": "#F8FAFC",
    "text_dim": "#94A3B8"
}


class StatCard(QFrame):
    def __init__(self, title: str, amount: float, color: str):
        super().__init__()
        self.setStyleSheet(f"background: {COLORS['surface']}; border-radius: 10px;")

        layout = QVBoxLayout(self)

        title_label = QLabel(title.upper())
        title_label.setStyleSheet(
            f"color: {color}; font-size: 10px; font-weight: bold;"
        )

        self.value_label = QLabel(f"€ {amount:,.0f}")
        self.value_label.setStyleSheet(
            "color: white; font-size: 18px; font-weight: 800;"
        )

        layout.addWidget(title_label)
        layout.addWidget(self.value_label)


class TransactionCard(QFrame):
    def __init__(
            self,
            t_id: int,
            category: str,
            amount: float,
            date: str,
            t_type: TransactionType,
            on_delete
    ):
        super().__init__()
        self.setFixedHeight(75)
        self.setStyleSheet(
            f"QFrame {{ background: {COLORS['surface']}; border-radius: 10px; }} "
            f"QFrame:hover {{ background: {COLORS['surface_hover']}; }}"
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        if t_type == TransactionType.INCOME:
            icon_color, sign = COLORS['success'], "+"
        elif t_type == TransactionType.SAVINGS:
            icon_color, sign = COLORS['warning'], "💰"
        else:
            icon_color, sign = COLORS['danger'], "-"

        indicator = QLabel("●")
        indicator.setStyleSheet(f"color: {icon_color}; font-size: 20px;")

        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        cat_label = QLabel(category)
        cat_label.setStyleSheet("color: white; font-weight: 700; font-size: 14px;")

        date_label = QLabel(date)
        date_label.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 11px;")

        info_layout.addWidget(cat_label)
        info_layout.addWidget(date_label)

        amount_label = QLabel(f"{sign} €{amount:,.2f}")
        amount_label.setStyleSheet(
            f"color: {icon_color}; font-weight: 800; font-size: 15px;"
        )

        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedSize(30, 30)
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.clicked.connect(lambda _: on_delete(t_id))
        delete_btn.setStyleSheet(
            "QPushButton { "
            "background: #EF4444; color: white; border: none; border-radius: 6px; "
            "} "
            "QPushButton:hover { background: #DC2626; }"
        )

        layout.addWidget(indicator)
        layout.addLayout(info_layout, 1)
        layout.addWidget(amount_label)
        layout.addSpacing(10)
        layout.addWidget(delete_btn)


class Dashboard(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.list_layouts = {}
        self.setStyleSheet(f"background-color: {COLORS['bg']};")
        self._setup_ui()
        self.load_data()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 20)
        main_layout.setSpacing(0)

        header = self._create_header()
        main_layout.addWidget(header)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{ border: none; background: transparent; }}
            QTabBar::tab {{ 
                background: #1E293B; color: {COLORS['text_dim']}; 
                padding: 12px 30px; border-top-left-radius: 8px; 
                border-top-right-radius: 8px; margin-right: 2px; font-weight: bold; 
            }}
            QTabBar::tab:selected {{ background: #3B82F6; color: white; }}
        """)

        overview = self._create_overview_tab()

        self.stats_tab = StatisticsTab(self.controller)

        self.tabs.addTab(overview, "Dashboard")
        self.tabs.addTab(self.stats_tab, "Estadísticas")

        self.tabs.currentChanged.connect(self._on_tab_changed)

        main_layout.addWidget(self.tabs)

    def _create_header(self) -> QFrame:
        header = QFrame()
        header.setFixedHeight(110)
        header.setStyleSheet(
            "background: #2563EB; "
            "border-top-left-radius: 16px; border-top-right-radius: 16px;"
        )

        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(25, 15, 25, 15)


        balance_layout = QVBoxLayout()

        balance_title = QLabel("BALANCE DISPONIBLE")
        balance_title.setStyleSheet(
            "color: rgba(255,255,255,0.8); font-weight: bold; "
            "font-size: 11px; letter-spacing: 1px;"
        )

        self.lbl_balance = QLabel("€ 0.00")
        self.lbl_balance.setStyleSheet(
            "color: white; font-size: 34px; font-weight: 900;"
        )

        balance_layout.addWidget(balance_title)
        balance_layout.addWidget(self.lbl_balance)

        h_layout.addLayout(balance_layout)
        h_layout.addStretch()

        self.stat_inc = StatCard("INGRESOS", 0, COLORS['success'])
        self.stat_exp = StatCard("GASTOS", 0, COLORS['danger'])
        self.stat_sav = StatCard("AHORRADO", 0, COLORS['warning'])

        for card in [self.stat_inc, self.stat_exp, self.stat_sav]:
            card.setFixedWidth(140)
            h_layout.addWidget(card)

        return header

    def _create_overview_tab(self) -> QWidget:
        overview = QWidget()
        layout = QHBoxLayout(overview)
        layout.setContentsMargins(0, 20, 0, 0)
        layout.setSpacing(15)

        self.col_inc = self._create_column("INGRESOS", COLORS['success'], "income")
        self.col_exp = self._create_column("GASTOS", COLORS['danger'], "expense")
        self.col_sav = self._create_column("AHORROS", COLORS['warning'], "savings_list")
        self.col_goals = self._create_column("METAS DE AHORRO", COLORS['accent'], "goals")

        for col in [self.col_inc, self.col_exp, self.col_sav, self.col_goals]:
            layout.addWidget(col)

        return overview

    def _create_column(self, title: str, color: str, key: str) -> QFrame:
        container = QFrame()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        header_layout = QHBoxLayout()

        title_label = QLabel(title)
        title_label.setStyleSheet(
            f"color: {color}; font-weight: 900; font-size: 13px;"
        )

        add_btn = QPushButton("+ Añadir")
        add_btn.setFixedSize(90, 28)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(lambda _: self._handle_add(key))
        add_btn.setStyleSheet(
            f"QPushButton {{ "
            f"background: {color}; color: #0F172A; border-radius: 5px; "
            f"font-weight: 800; font-size: 10px; "
            f"}} "
            f"QPushButton:hover {{ background: white; }}"
        )

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(add_btn)

        layout.addLayout(header_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        widget = QWidget()
        self.list_layouts[key] = QVBoxLayout(widget)
        self.list_layouts[key].setContentsMargins(0, 0, 0, 0)
        self.list_layouts[key].addStretch()

        scroll.setWidget(widget)
        layout.addWidget(scroll)

        return container

    def load_data(self):
        try:
            balance = self.controller.get_monthly_balance()

            self.lbl_balance.setText(f"€ {balance['balance']:,.2f}")

            self.stat_inc.value_label.setText(f"€ {balance['total_income']:,.0f}")
            self.stat_exp.value_label.setText(f"€ {balance['total_expense']:,.0f}")
            self.stat_sav.value_label.setText(f"€ {balance['total_savings']:,.0f}")

            incomes = self.controller.get_transactions_by_type(TransactionType.INCOME)
            self._fill_list("income", incomes)

            expenses = self.controller.get_transactions_by_type(TransactionType.EXPENSE)
            self._fill_list("expense", expenses)

            savings = self.controller.get_transactions_by_type(TransactionType.SAVINGS)
            self._fill_list("savings_list", savings)

            goals = self.controller.get_all_savings_goals()
            self._fill_goals(goals)

            if hasattr(self, 'stats_tab') and self.stats_tab:
                self.stats_tab.load_data()

            print("Interfaz Dashboard actualizada al 100%")

        except Exception as e:
            print(f"Error en load_data: {e}")

    def _fill_list(self, key: str, data: list):
        layout = self.list_layouts[key]
        self._clear_layout(layout)

        if key == "income":
            t_type = TransactionType.INCOME
        elif key == "expense":
            t_type = TransactionType.EXPENSE
        else:
            t_type = TransactionType.SAVINGS

        for trans in data[:20]:
            card = TransactionCard(
                trans.id, trans.category, trans.amount,
                trans.date, t_type, self._handle_delete
            )
            layout.insertWidget(0, card)

    def _fill_goals(self, goals: list):
        layout = self.list_layouts['goals']
        self._clear_layout(layout)

        for goal in goals:
            goal_frame = QFrame()
            goal_frame.setStyleSheet(
                f"background: {COLORS['surface']}; border-radius: 10px;"
            )

            goal_layout = QVBoxLayout(goal_frame)
            goal_layout.setContentsMargins(15, 12, 15, 12)

            header_layout = QHBoxLayout()

            name_label = QLabel(f"🎯 {goal.name}")
            name_label.setStyleSheet(
                "color: white; font-weight: bold; font-size: 13px;"
            )
            header_layout.addWidget(name_label)
            header_layout.addStretch()

            add_btn = QPushButton("💰")
            add_btn.setFixedSize(28, 28)
            add_btn.clicked.connect(lambda _, gid=goal.id: self._handle_deposit(gid))
            add_btn.setStyleSheet(f"background: {COLORS['accent']}; border-radius: 5px;")

            del_btn = QPushButton("🗑️")
            del_btn.setFixedSize(28, 28)
            del_btn.clicked.connect(lambda _, gid=goal.id: self._delete_goal(gid))
            del_btn.setStyleSheet("background: #EF4444; border-radius: 5px;")

            header_layout.addWidget(add_btn)
            header_layout.addWidget(del_btn)

            goal_layout.addLayout(header_layout)

            progress = QProgressBar()
            progress.setFixedHeight(5)
            progress.setValue(int(goal.get_progress_percentage()))
            progress.setTextVisible(False)
            progress.setStyleSheet(
                f"QProgressBar {{ background: #0F172A; border-radius: 2px; }} "
                f"QProgressBar::chunk {{ background: {COLORS['accent']}; }}"
            )
            goal_layout.addWidget(progress)

            layout.insertWidget(0, goal_frame)

    @staticmethod
    def _clear_layout(layout):
        while layout.count() > 1:
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _on_tab_changed(self, index: int):
        if index == 1:
            self.stats_tab.load_data()

    def _handle_add(self, key):
        from src.views.dialogs import AddTransactionDialog, AddSavingsGoalDialog, AddToSavingsGoalDialog

        if key == "income":
            dialog = AddTransactionDialog(self, TransactionType.INCOME)
            if dialog.exec():
                self._save_transaction(dialog.transaction_data)

        elif key == "expense":
            dialog = AddTransactionDialog(self, TransactionType.EXPENSE)
            if dialog.exec():
                self._save_transaction(dialog.transaction_data)

        elif key == "savings_list":
            dialog = AddToSavingsGoalDialog(self.controller, self)
            if dialog.exec():
                data = dialog.get_data()
                if data:
                    self.controller.add_to_savings_goal(data['goal_id'], data['amount'])
                    self.load_data()

        elif key == "goals":
            dialog = AddSavingsGoalDialog(self)
            if dialog.exec():
                data = dialog.get_data()
                self.controller.create_savings_goal(
                    data['name'], data['target_amount'],
                    data['current_amount'], data['deadline'], data['description']
                )
                self.load_data()

    def _save_transaction(self, data):
        self.controller.create_transaction(
            t_type=data['type'],
            amount=data['amount'],
            category=data['category'],
            description=data['description'],
            date=data['date']
        )
        self.load_data()

    def _handle_deposit(self, goal_id: int):
        dialog = AddToSavingsGoalDialog(self.controller, self)
        if dialog.exec():
            data = dialog.get_data()
            self.controller.add_to_savings_goal(data['goal_id'], data['amount'])
            self.load_data()

    def _delete_goal(self, goal_id: int):
        reply = QMessageBox.question(
            self,
            "Eliminar Meta",
            "¿Estás seguro de eliminar esta meta?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.controller.delete_savings_goal(goal_id)
            self.load_data()

    def _handle_delete(self, transaction_id: int):
        reply = QMessageBox.question(
            self,
            "Eliminar Registro",
            "¿Deseas eliminar esta transacción?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.controller.delete_transaction(transaction_id)
            self.load_data()