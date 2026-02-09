from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class BalanceCard(QWidget):
    clicked = Signal()

    def __init__(self, title: str, amount: float = 0.0, subtitle: str = "", color: str = "#3498DB", parent=None):
        super().__init__(parent)

        self.title_text = title
        self.amount_value = amount
        self.subtitle_text = subtitle
        self.accent_color = color

        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(8)

        self.title_label = QLabel(self.title_text)
        self.title_label.setAlignment(Qt.AlignLeft)
        self.title_label.setObjectName("cardTitle")

        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setWeight(QFont.Medium)
        self.title_label.setFont(title_font)

        self.amount_label = QLabel(self._format_amount(self.amount_value))
        self.amount_label.setAlignment(Qt.AlignLeft)
        self.amount_label.setObjectName("cardAmount")

        amount_font = QFont()
        amount_font.setPointSize(28)
        amount_font.setWeight(QFont.Bold)
        self.amount_label.setFont(amount_font)

        self.subtitle_label = QLabel(self.subtitle_text)
        self.subtitle_label.setAlignment(Qt.AlignLeft)
        self.subtitle_label.setObjectName("cardSubtitle")

        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        self.subtitle_label.setFont(subtitle_font)

        layout.addWidget(self.title_label)
        layout.addWidget(self.amount_label)
        if self.subtitle_text:
            layout.addWidget(self.subtitle_label)
        layout.addStretch()

        self.setCursor(Qt.PointingHandCursor)

    def _apply_styles(self):
        self.setStyleSheet(f"""
            BalanceCard {{
                background-color: palette(base);
                border-left: 5px solid {self.accent_color};
                border-radius: 12px;
                min-height: 140px;
            }}
            
            BalanceCard:hover {{
                background-color: palette(alternate-base);
            }}
            
            QLabel#cardTitle {{
                color: palette(text);
                opacity: 0.7;
            }}
            
            QLabel#cardAmount {{
                color: {self.accent_color};
            }}
            
            QLabel#cardSubtitle {{
                color: palette(text);
                opacity: 0.6;
            }}
        """)
    @staticmethod
    def _format_amount(amount: float) -> str:
        if amount >= 0:
            return f"€ {amount:,.2f}"
        else:
            return f"-€ {abs(amount):,.2f}"

    def set_amount(self, amount: float):
        self.amount_value = amount
        self.amount_label.setText(self._format_amount(amount))

    def set_subtitle(self, subtitle: str):
        self.subtitle_text = subtitle
        self.subtitle_label.setText(subtitle)

    def set_color(self, color: str):
        self.accent_color = color
        self._apply_styles()
    
    def mouse_press_event(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mouse_press_event(event)