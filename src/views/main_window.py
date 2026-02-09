from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QMessageBox,
    QFileDialog, QTextEdit, QDialog
)
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtCore import Qt
import os
from datetime import datetime

from src.controllers.mintly import Mintly
from src.views.dashboard import Dashboard
from src.utils.export_manager import ExportManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = Mintly()
        self.setWindowTitle("Mintly Tracker")

        self._setup_ui()
        self._create_menu()
        self.showMaximized()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        self.dashboard = Dashboard(self.controller, self)
        layout.addWidget(self.dashboard)

    def _create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("Archivo")

        export_menu = file_menu.addMenu("Exportar")

        export_csv = QAction("CSV", self)
        export_csv.triggered.connect(self._export_csv)
        export_menu.addAction(export_csv)

        export_pdf = QAction("PDF", self)
        export_pdf.triggered.connect(self._export_pdf)
        export_menu.addAction(export_pdf)

        file_menu.addSeparator()

        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        view_menu = menubar.addMenu("Ver")

        refresh_action = QAction("Actualizar Datos", self)
        refresh_action.setShortcut(QKeySequence("F5"))
        refresh_action.triggered.connect(self.refresh_all)
        view_menu.addAction(refresh_action)

        fullscreen_action = QAction("Pantalla Completa", self)
        fullscreen_action.setShortcut(QKeySequence("F11"))
        fullscreen_action.triggered.connect(self._toggle_fullscreen)
        view_menu.addAction(fullscreen_action)

        help_menu = menubar.addMenu("Ayuda")

        doc_action = QAction("Documentación", self)
        doc_action.setShortcut(QKeySequence("F1"))
        doc_action.triggered.connect(self._show_documentation)
        help_menu.addAction(doc_action)

        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _show_documentation(self):
        doc_dialog = QDialog(self)
        doc_dialog.setWindowTitle("Documentación - Mintly")
        doc_dialog.setMinimumSize(800, 600)
        layout = QVBoxLayout(doc_dialog)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #0F172A;
                color: #E2E8F0;
                padding: 20px;
                border: 1px solid #334155;
                line-height: 1.6;
            }
        """)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(os.path.dirname(current_dir))
        readme_path = os.path.join(root_dir, "docs", "README.md")

        if os.path.exists(readme_path):
            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    text_edit.setMarkdown(content)
            except Exception as e:
                text_edit.setText(f"Error al leer el archivo: {str(e)}")
        else:
            text_edit.setText(
                f"Archivo no encontrado.\n\n"
            )

        layout.addWidget(text_edit)
        doc_dialog.exec()

    def _export_csv(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar CSV",
            f"mintly_export_{datetime.now().strftime('%Y%m%d')}.csv",
            "CSV Files (*.csv)"
        )

        if filename:
            transactions = self.controller.get_all_transactions()
            goals = self.controller.get_all_savings_goals()

            if ExportManager.export_to_csv(transactions, filename, goals):
                QMessageBox.information(
                    self,
                    "Éxito",
                    f"CSV exportado correctamente\n\n"
                )
            else:
                QMessageBox.critical(self, "Error", "No se pudo exportar el CSV")

    def _export_pdf(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar PDF",
            f"mintly_report_{datetime.now().strftime('%Y%m%d')}.pdf",
            "PDF Files (*.pdf)"
        )

        if filename:
            transactions = self.controller.get_all_transactions()
            balance = self.controller.get_monthly_balance()
            goals = self.controller.get_all_savings_goals()

            if ExportManager.export_to_pdf(transactions, balance, filename, goals):
                QMessageBox.information(
                    self,
                    "Éxito",
                    f"PDF exportado correctamente\n\nArchivo: {filename}"
                )
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "No se pudo exportar el PDF.\n\n"
                    "Asegúrate de tener instalado reportlab:\n"
                    "pip install reportlab"
                )

    def _toggle_fullscreen(self):
        if self.isFullScreen():
            self.showMaximized()
        else:
            self.showFullScreen()

    def refresh_all(self):
        self.dashboard.load_data()
        QMessageBox.information(self, "Actualizado", "Datos actualizados correctamente")

    def _show_about(self):
        QMessageBox.about(
            self,
            "Acerca de Mintly",
            "<h2 style='color: #3B82F6;'>Mintly Tracker</h2>"
            "<p><b>Versión:</b> 1.0.0</p>"
            "<p><b>Proyecto para Desarrollo de Interfaces</b></p>"
            "<br>"
            "<p>Aplicación de finanzas personales desarrollada con:</p>"
            "<ul>"
            "<li>Python</li>"
            "<li>PySide6</li>"
            "<li>SQLite</li>"
            "<li>Matplotlib</li>"
            "</ul>"
            "<br>"
            "<p>Mintly te ayuda a llevar un control completo de tus "
            "ingresos, gastos y metas de ahorro de manera simple y visual.</p>"
        )

    def key_press_event(self, event):
        if event.key() == Qt.Key_Escape and self.isFullScreen():
            self.showMaximized()
        elif event.key() == Qt.Key_F5:
            self.refresh_all()
        else:
            super().key_press_event(event)