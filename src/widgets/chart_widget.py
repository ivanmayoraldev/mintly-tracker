import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget, QVBoxLayout
import re
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")


class ChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        plt.rcParams.update({
            'text.color': '#F8FAFC',
            'axes.labelcolor': '#94A3B8',
            'font.size': 9,
            'legend.edgecolor': '#334155',
            'legend.facecolor': '#1E293B'
        })

        self.figure = Figure(figsize=(5, 4), dpi=100, facecolor='#1E293B')
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)

    @staticmethod
    def _clean_text(text):
        return re.sub(r'[^\w\s,.€%]', '', str(text)).strip()

    def set_data(self, data, title, colors_map=None, chart_type="barras"):
        self.ax.clear()
        self.ax.set_facecolor('#1E293B')

        if not data:
            self.ax.text(0.5, 0.5, 'Sin datos', ha='center', va='center', color='#94A3B8')
            self.ax.set_axis_off()
            self.canvas.draw()
            return

        self.ax.set_axis_on()

        labels = [self._clean_text(k) for k in data.keys()]
        values = list(data.values())

        colors = []
        for original_key in data.keys():
            colors.append(colors_map.get(original_key, '#3B82F6') if colors_map else '#3B82F6')

        if chart_type == "sectores":
            self.ax.pie(
                values, labels=labels, autopct='%1.1f%%',
                startangle=140, colors=colors,
                textprops={'color': "#F8FAFC", 'weight': 'bold'},
                pctdistance=0.85
            )
            centre_circle = plt.Circle((0, 0), 0.70, fc='#1E293B')
            self.figure.gca().add_artist(centre_circle)

            self.ax.legend(labels, loc="upper right", bbox_to_anchor=(1.1, 1),
                           fontsize=8, labelcolor='#F8FAFC', frameon=False)
        else:
            bars = self.ax.bar(labels, values, color=colors, edgecolor='#334155')
            for bar in bars:
                height = bar.get_height()
                self.ax.text(bar.get_x() + bar.get_width() / 2., height,
                             f'€{height:,.0f}', ha='center', va='bottom', color='#F8FAFC')

            for spine in self.ax.spines.values():
                spine.set_color('#334155')

        self.ax.set_title(self._clean_text(title), pad=20, color='#F8FAFC', fontweight='bold')
        self.figure.tight_layout()
        self.canvas.draw()