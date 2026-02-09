import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from src.views.main_window import MainWindow


def main():
    """
    Aplicación de finanzas para llevar un seguimiento sobre los Ingresos, Gastos y Ahorros.
    Con expectativas de seguir creciendo la aplicación ya sea con Python o migrandola a Java con Spring (que lo estoy aprendiendo)
    Donde podremos conseguir features como Login de perfiles, compartir cuenta entre perfiles, lectura de recibos para registrar gastos más facilmente,
    importar csv de nuestro gestor o poder hacer la declaración de la renta, entre otros...
    """
    app = QApplication(sys.argv)

    font = QFont("Segoe UI", 10)
    app.setFont(font)

    app.setStyle("Fusion")

    app.setApplicationName("Mintly Tracker")
    app.setOrganizationName("Iván Mayoral Capel")
    app.setApplicationVersion("1.0.0")

    try:
        window = MainWindow()
        window.show()
    except Exception as e:
        print(f"Error al crear la ventana: {e}")
        import traceback
        traceback.print_exc()
        return 1

    sys.exit(app.exec())

if __name__ == "__main__":
    main()