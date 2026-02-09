from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QGroupBox, QFrame, QProgressBar, QCheckBox
)
from PySide6.QtCore import Qt
from src.widgets.chart_widget import ChartWidget
from src.models.transaction import TransactionType


class StatCard(QFrame):
    def __init__(self, title: str, value: str, color: str, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)

        title_label = QLabel(title.upper())
        title_label.setStyleSheet("font-size: 11px; color: #94A3B8; font-weight: 800; letter-spacing: 0.5px;")
        layout.addWidget(title_label)

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"font-size: 24px; color: {color}; font-weight: 700;")
        layout.addWidget(self.value_label)

        self.setStyleSheet("""
            QFrame { background-color: #1E293B; border: 1px solid #334155; border-radius: 12px; }
            QFrame:hover { border: 1px solid #475569; background-color: #242F42; }
        """)
        self.setFixedHeight(95)

    def set_value(self, value: str):
        self.value_label.setText(value)


class RatioCard(QFrame):
    def __init__(self, title: str, color: str, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 12)
        layout.setSpacing(5)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 11px; color: #94A3B8; font-weight: 600;")

        self.progress = QProgressBar()
        self.progress.setFixedHeight(18)
        self.progress.setTextVisible(True)
        self.progress.setAlignment(Qt.AlignCenter)
        self.progress.setStyleSheet(f"""
            QProgressBar {{ background: #0F172A; border-radius: 9px; text-align: center; color: white; font-weight: 800; font-size: 10px; }}
            QProgressBar::chunk {{ background: {color}; border-radius: 9px; }}
        """)

        layout.addWidget(title_label)
        layout.addWidget(self.progress)
        self.setStyleSheet("background-color: #0F172A; border: 1px solid #1E293B; border-radius: 10px;")
        self.setFixedHeight(75)

    def update_ratio(self, percentage: float):
        self.progress.setValue(int(percentage))
        self.progress.setFormat(f"{percentage:.1f}%")


class StatisticsTab(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.expenses_data = {}
        self.incomes_data = {}
        self.savings_data = {}
        self._setup_ui()
        self.load_data()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title = QLabel("Análisis de tus Finanzas")
        title.setStyleSheet("font-size: 26px; font-weight: 800; color: #F1F5F9;")
        main_layout.addWidget(title)

        top_cards = QHBoxLayout()
        self.income_card = StatCard("Ingresos", "€ 0.00", "#10B981")
        self.expense_card = StatCard("Gastos", "€ 0.00", "#EF4444")
        self.savings_card = StatCard("Ahorrado", "€ 0.00", "#F59E0B")
        self.balance_card = StatCard("Balance", "€ 0.00", "#3B82F6")

        for card in [self.income_card, self.expense_card, self.savings_card, self.balance_card]:
            top_cards.addWidget(card)
        main_layout.addLayout(top_cards)

        body_layout = QHBoxLayout()

        chart_container = QGroupBox("Gráficos")
        chart_container.setStyleSheet(self._group_box_style())
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(15, 30, 15, 15)

        controls = QHBoxLayout()
        self.show_incomes_cb = self._create_cb("Ingresos", "#10B981")
        self.show_expenses_cb = self._create_cb("Gastos", "#EF4444")
        self.show_savings_cb = self._create_cb("Ahorros", "#F59E0B")
        for cb in [self.show_incomes_cb, self.show_expenses_cb, self.show_savings_cb]:
            controls.addWidget(cb)
        controls.addStretch()
        chart_layout.addLayout(controls)

        self.unified_chart = ChartWidget()
        chart_layout.addWidget(self.unified_chart)
        body_layout.addWidget(chart_container, stretch=70)

        side_panel = QVBoxLayout()
        side_panel.setSpacing(15)

        health_group = QGroupBox("Salud Financiera")
        health_group.setStyleSheet(self._group_box_style())
        h_layout = QVBoxLayout(health_group)
        h_layout.setContentsMargins(15, 35, 15, 15)
        h_layout.setSpacing(10)

        self.health_score_label = QLabel("0/100")
        self.health_score_label.setStyleSheet("font-size: 32px; font-weight: 900; color: white;")
        self.health_score_label.setAlignment(Qt.AlignCenter)

        self.health_progress = QProgressBar()
        self.health_progress.setFixedHeight(10)
        self.health_progress.setTextVisible(False)
        self.health_progress.setStyleSheet("""
            QProgressBar { background: #0F172A; border-radius: 5px; }
            QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #EF4444, stop:1 #10B981); border-radius: 5px; }
        """)

        self.health_message = QLabel("Añade movimientos para analizar")
        self.health_message.setStyleSheet("color: #F1F5F9; font-size: 12px; font-style: italic;")
        self.health_message.setWordWrap(True)
        self.health_message.setAlignment(Qt.AlignCenter)

        h_layout.addWidget(self.health_score_label)
        h_layout.addWidget(self.health_progress)
        h_layout.addWidget(self.health_message)
        side_panel.addWidget(health_group)

        ratios_group = QGroupBox("Porcentajes para tener un control")
        ratios_group.setStyleSheet(self._group_box_style())
        r_layout = QVBoxLayout(ratios_group)
        r_layout.setContentsMargins(15, 35, 15, 15)
        r_layout.setSpacing(12)

        self.savings_rate_card = RatioCard("TASA DE AHORRO", "#10B981")
        self.expense_rate_card = RatioCard("TASA DE GASTO", "#EF4444")

        r_layout.addWidget(self.savings_rate_card)
        r_layout.addWidget(self.expense_rate_card)
        side_panel.addWidget(ratios_group)

        body_layout.addLayout(side_panel, stretch=30)
        main_layout.addLayout(body_layout)

    def _create_cb(self, text, color):
        cb = QCheckBox(text)
        cb.setChecked(True)
        cb.stateChanged.connect(self._update_chart)
        cb.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 12px;")
        return cb

    def _update_chart(self):
        combined_data = {}
        combined_colors = {}

        data_map = [
            (self.show_incomes_cb, self.incomes_data, "#10B981"),
            (self.show_expenses_cb, self.expenses_data, "#EF4444"),
            (self.show_savings_cb, self.savings_data, "#F59E0B")
        ]

        for cb, data, color in data_map:
            if cb.isChecked():
                for cat, amount in data.items():
                    combined_data[cat] = combined_data.get(cat, 0) + amount
                    combined_colors[cat] = color

        if not combined_data:
            self.unified_chart.set_data({}, "Sin datos en la aplicación", {})
            return

        self.unified_chart.set_data(combined_data, "Distribución", combined_colors)



    def load_data(self):
        balance = self.controller.get_monthly_balance()
        self.income_card.set_value(f"€ {balance['total_income']:,.2f}")
        self.expense_card.set_value(f"€ {balance['total_expense']:,.2f}")
        self.savings_card.set_value(f"€ {balance['total_savings']:,.2f}")
        self.balance_card.set_value(f"€ {balance['balance']:,.2f}")

        self.expenses_data = self.controller.get_expenses_by_category()
        self.incomes_data = self.controller.get_income_by_category()
        self.savings_data = self.controller.get_savings_by_category()
        self._update_chart()

        health = self.controller.get_financial_health_score()
        self.health_score_label.setText(f"{health['score']}/100")
        self.health_progress.setValue(health['score'])
        self.health_message.setText(health['message'])

        inc = balance['total_income']
        if inc > 0:
            s_rate = (balance['total_savings'] / inc) * 100
            e_rate = (balance['total_expense'] / inc) * 100
            self.savings_rate_card.update_ratio(s_rate)
            self.expense_rate_card.update_ratio(e_rate)

    @staticmethod
    def _group_box_style():
        return """
            QGroupBox { font-size: 13px; font-weight: 800; color: #94A3B8; border: 2px solid #334155; 
                        border-radius: 12px; margin-top: 20px; background-color: #1E293B; }
            QGroupBox::title { subcontrol-origin: margin; left: 15px; padding: 0 8px; }
        """