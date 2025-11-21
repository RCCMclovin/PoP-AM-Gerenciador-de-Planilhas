import pyplanilha
import sys
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    janela = pyplanilha.MainWindow()
    janela.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()