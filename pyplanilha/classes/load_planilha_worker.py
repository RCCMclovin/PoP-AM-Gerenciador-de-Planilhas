from PyQt6.QtCore import  pyqtSignal, QObject
from .interface_api import InterfaceAPI

class LoadPlanilhaWorker(QObject):
    finished = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self, api: InterfaceAPI, path: str):
        super().__init__()
        self.api = api
        self.path = path

    def run(self):
        try:
            total = self.api.carregar_planilha(self.path)
            self.finished.emit(total)
        except Exception as e:
            self.error.emit(str(e))