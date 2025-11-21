from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QMessageBox,
    QDialog,
    QGridLayout,
    QListWidget,
    QListWidgetItem,
    QInputDialog,
    QPlainTextEdit,
)
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator

from .interface_api import InterfaceAPI

class ListasDialog(QDialog):
    """
    Diálogo para gerenciar Whitelist (postes) e Blacklist (bairros)
    usando a InterfaceAPI, com busca para facilitar remoção.
    """

    def __init__(self, api: InterfaceAPI, parent=None):
        super().__init__(parent)
        self.api = api
        self.setWindowTitle("Gerenciar Blacklist / Whitelist")
        self.resize(800, 450)

        layout = QGridLayout(self)

        label_wl = QLabel("Whitelist (Postes)")
        self.search_wl = QLineEdit()
        self.search_wl.setPlaceholderText("Pesquisar poste...")
        self.lista_wl = QListWidget()

        btn_add_wl = QPushButton("Adicionar Poste")
        btn_add_wl_multi = QPushButton("Adicionar vários postes…")
        btn_rem_wl = QPushButton("Remover Selecionado")

        label_bl = QLabel("Blacklist (Bairros)")
        self.search_bl = QLineEdit()
        self.search_bl.setPlaceholderText("Pesquisar bairro...")
        self.lista_bl = QListWidget()

        btn_add_bl = QPushButton("Adicionar Bairro")
        btn_add_bl_multi = QPushButton("Adicionar vários bairros…")
        btn_rem_bl = QPushButton("Remover Selecionado")

        layout.addWidget(label_wl,      0, 0)
        layout.addWidget(self.search_wl, 1, 0)
        layout.addWidget(self.lista_wl,  2, 0)
        layout.addWidget(btn_add_wl,     3, 0)
        layout.addWidget(btn_add_wl_multi, 4, 0)
        layout.addWidget(btn_rem_wl,     5, 0)

        layout.addWidget(label_bl,      0, 1)
        layout.addWidget(self.search_bl, 1, 1)
        layout.addWidget(self.lista_bl,  2, 1)
        layout.addWidget(btn_add_bl,     3, 1)
        layout.addWidget(btn_add_bl_multi, 4, 1)
        layout.addWidget(btn_rem_bl,     5, 1)

        btn_fechar = QPushButton("Fechar")
        layout.addWidget(btn_fechar, 6, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignRight)

        btn_add_wl.clicked.connect(self.adicionar_poste)
        btn_add_wl_multi.clicked.connect(self.adicionar_postes_lote)
        btn_rem_wl.clicked.connect(self.remover_poste)

        btn_add_bl.clicked.connect(self.adicionar_bairro)
        btn_add_bl_multi.clicked.connect(self.adicionar_bairros_lote)
        btn_rem_bl.clicked.connect(self.remover_bairro)

        btn_fechar.clicked.connect(self.accept)

        self.search_wl.textChanged.connect(self.carregar_listas)
        self.search_bl.textChanged.connect(self.carregar_listas)

        self.carregar_listas()

    def carregar_listas(self):
        self.lista_wl.clear()
        self.lista_bl.clear()

        filtro_wl = self.search_wl.text().strip()
        filtro_bl = self.search_bl.text().strip().lower()

        for poste in self.api.obter_whitelist():
            s = str(poste)
            if filtro_wl and filtro_wl not in s:
                continue
            self.lista_wl.addItem(QListWidgetItem(s))

        for bairro in self.api.obter_blacklist():
            s = str(bairro)
            if filtro_bl and filtro_bl not in s.lower():
                continue
            self.lista_bl.addItem(QListWidgetItem(s))

    def adicionar_poste(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Adicionar Poste à Whitelist")
        dlg.resize(300, 120)

        layout = QVBoxLayout(dlg)
        label = QLabel("Digite o código do poste (10 dígitos):")
        edit = QLineEdit()
        edit.setMaxLength(10)

        regex = QRegularExpression(r"\d{0,10}")
        validator = QRegularExpressionValidator(regex, edit)
        edit.setValidator(validator)

        layout.addWidget(label)
        layout.addWidget(edit)

        btns = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_cancel = QPushButton("Cancelar")
        btns.addStretch()
        btns.addWidget(btn_ok)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

        btn_cancel.clicked.connect(dlg.reject)

        def on_ok():
            texto = edit.text().strip()
            if len(texto) != 10 or not texto.isdigit():
                QMessageBox.warning(dlg, "Poste inválido", "Deve conter exatamente 10 dígitos.")
                return
            try:
                self.api.adicionar_poste_whitelist(texto)
                self.carregar_listas()
                dlg.accept()
            except Exception as e:
                QMessageBox.warning(dlg, "Erro", str(e))

        btn_ok.clicked.connect(on_ok)
        dlg.exec()

    def adicionar_postes_lote(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Adicionar vários postes à Whitelist")
        dlg.resize(420, 300)

        layout = QVBoxLayout(dlg)
        layout.addWidget(QLabel("Digite vários postes (um por linha):"))

        edit = QPlainTextEdit()
        layout.addWidget(edit)

        btns = QHBoxLayout()
        btn_ok = QPushButton("Adicionar")
        btn_cancel = QPushButton("Cancelar")
        btns.addStretch()
        btns.addWidget(btn_ok)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

        btn_cancel.clicked.connect(dlg.reject)

        def confirmar():
            texto = edit.toPlainText().strip()
            linhas = texto.split("\n")

            validos = []
            erros = []

            for linha in linhas:
                codigo = linha.strip()
                if not codigo:
                    continue
                if not codigo.isdigit() or len(codigo) != 10:
                    erros.append(codigo)
                else:
                    validos.append(codigo)

            adicionados = 0
            for poste in validos:
                try:
                    self.api.adicionar_poste_whitelist(poste)
                    adicionados += 1
                except Exception:
                    pass

            self.carregar_listas()

            msg = f"{adicionados} postes adicionados."
            if erros:
                msg += f"\nIgnorados (inválidos): {', '.join(erros)}"

            QMessageBox.information(self, "Resultado", msg)
            dlg.accept()

        btn_ok.clicked.connect(confirmar)
        dlg.exec()

    def remover_poste(self):
        item = self.lista_wl.currentItem()
        if not item:
            return
        poste = item.text()
        self.api.remover_poste_whitelist(poste)
        self.carregar_listas()

    def adicionar_bairro(self):
        texto, ok = QInputDialog.getText(
            self,
            "Adicionar Bairro à Blacklist",
            "Digite o nome do bairro:",
        )
        if ok and texto.strip():
            self.api.adicionar_bairro_blacklist(texto.strip())
            self.carregar_listas()

    def adicionar_bairros_lote(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Adicionar vários bairros à Blacklist")
        dlg.resize(420, 300)

        layout = QVBoxLayout(dlg)
        layout.addWidget(QLabel("Digite vários bairros (um por linha):"))

        edit = QPlainTextEdit()
        layout.addWidget(edit)

        btns = QHBoxLayout()
        btn_ok = QPushButton("Adicionar")
        btn_cancel = QPushButton("Cancelar")
        btns.addStretch()
        btns.addWidget(btn_ok)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

        btn_cancel.clicked.connect(dlg.reject)

        def confirmar():
            linhas = edit.toPlainText().split("\n")
            bairros = {linha.strip() for linha in linhas if linha.strip()}

            adicionados = 0
            for bairro in bairros:
                self.api.adicionar_bairro_blacklist(bairro)
                adicionados += 1

            self.carregar_listas()
            QMessageBox.information(self, "Resultado", f"{adicionados} bairros adicionados.")
            dlg.accept()

        btn_ok.clicked.connect(confirmar)
        dlg.exec()

    def remover_bairro(self):
        item = self.lista_bl.currentItem()
        if not item:
            return
        bairro = item.text()
        self.api.remover_bairro_blacklist(bairro)
        self.carregar_listas()