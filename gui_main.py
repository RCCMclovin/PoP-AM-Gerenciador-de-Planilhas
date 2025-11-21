# gui_main.py

import sys
import os

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QLineEdit,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QStatusBar,
    QDialog,
    QGridLayout,
    QListWidget,
    QListWidgetItem,
    QInputDialog,
    QPlainTextEdit,
    QProgressDialog    
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator


from pyplanilha.classes.interface_api import InterfaceAPI


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


class ListasDialog(QDialog):
    """
    Diálogo para gerenciar Whitelist (postes) e Blacklist (bairros)
    usando a InterfaceAPI.
    """

    def __init__(self, api: InterfaceAPI, parent=None):
        super().__init__(parent)
        self.api = api
        self.setWindowTitle("Gerenciar Blacklist / Whitelist")
        self.resize(600, 400)

        layout = QGridLayout(self)

        # Whitelist
        label_wl = QLabel("Whitelist (Postes)")
        self.lista_wl = QListWidget()
        btn_add_wl = QPushButton("Adicionar Poste")
        btn_rem_wl = QPushButton("Remover Selecionado")

        # Blacklist
        label_bl = QLabel("Blacklist (Bairros)")
        self.lista_bl = QListWidget()
        btn_add_bl = QPushButton("Adicionar Bairro")
        btn_rem_bl = QPushButton("Remover Selecionado")

        layout.addWidget(label_wl, 0, 0)
        layout.addWidget(self.lista_wl, 1, 0)
        layout.addWidget(btn_add_wl, 2, 0)
        layout.addWidget(btn_rem_wl, 3, 0)

        layout.addWidget(label_bl, 0, 1)
        layout.addWidget(self.lista_bl, 1, 1)
        layout.addWidget(btn_add_bl, 2, 1)
        layout.addWidget(btn_rem_bl, 3, 1)

        btn_fechar = QPushButton("Fechar")
        layout.addWidget(btn_fechar, 4, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignRight)

        btn_add_wl.clicked.connect(self.adicionar_poste)
        btn_rem_wl.clicked.connect(self.remover_poste)
        btn_add_bl.clicked.connect(self.adicionar_bairro)
        btn_rem_bl.clicked.connect(self.remover_bairro)
        btn_fechar.clicked.connect(self.accept)

        self.carregar_listas()

    def carregar_listas(self):
        self.lista_wl.clear()
        self.lista_bl.clear()

        for poste in self.api.obter_whitelist():
            self.lista_wl.addItem(QListWidgetItem(str(poste)))

        for bairro in self.api.obter_blacklist():
            self.lista_bl.addItem(QListWidgetItem(str(bairro)))

    def adicionar_poste(self):
     
        dlg = QDialog(self)
        dlg.setWindowTitle("Adicionar Poste à Whitelist")
        dlg.resize(300, 120)

        layout = QVBoxLayout(dlg)

        label = QLabel("Digite o código do poste (10 dígitos):")
        edit = QLineEdit()
        edit.setMaxLength(10)

        # Aceita apenas dígitos, até 10
        regex = QRegularExpression(r"\d{0,10}")
        validator = QRegularExpressionValidator(regex, edit)
        edit.setValidator(validator)

        layout.addWidget(label)
        layout.addWidget(edit)

        btns_layout = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_cancel = QPushButton("Cancelar")
        btns_layout.addStretch()
        btns_layout.addWidget(btn_ok)
        btns_layout.addWidget(btn_cancel)
        layout.addLayout(btns_layout)

        # Comportamento dos botões
        btn_cancel.clicked.connect(dlg.reject)

        def on_ok():
            texto = edit.text().strip()
            if len(texto) != 10:
                QMessageBox.warning(
                    dlg,
                    "Poste inválido",
                    "O código do poste deve conter exatamente 10 dígitos."
                )
                return
            try:
                self.api.adicionar_poste_whitelist(texto)
                self.carregar_listas()
                dlg.accept()
            except ValueError as e:
                QMessageBox.warning(dlg, "Poste inválido", str(e))

        btn_ok.clicked.connect(on_ok)

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
            "Digite o nome do bairro:"
        )
        if not ok or not texto:
            return

        self.api.adicionar_bairro_blacklist(texto)
        self.carregar_listas()

    def remover_bairro(self):
        item = self.lista_bl.currentItem()
        if not item:
            return
        bairro = item.text()
        self.api.remover_bairro_blacklist(bairro)
        self.carregar_listas()


class EmailDialog(QDialog):
    """
    Diálogo para exibir o e-mail gerado de um evento.
    """

    def __init__(self, assunto: str, corpo: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("E-mail do Evento")
        self.resize(700, 500)

        layout = QVBoxLayout(self)

        label_assunto = QLabel("Assunto:")
        self.edit_assunto = QLineEdit()
        self.edit_assunto.setText(assunto)

        label_corpo = QLabel("Corpo do e-mail:")
        self.edit_corpo = QPlainTextEdit()
        self.edit_corpo.setPlainText(corpo)

        self.edit_assunto.setReadOnly(True)
        self.edit_corpo.setReadOnly(True)

        layout.addWidget(label_assunto)
        layout.addWidget(self.edit_assunto)
        layout.addWidget(label_corpo)
        layout.addWidget(self.edit_corpo)

        btns_layout = QHBoxLayout()
        btn_copiar = QPushButton("Copiar para Área de Transferência")
        btn_fechar = QPushButton("Fechar")
        btns_layout.addWidget(btn_copiar)
        btns_layout.addStretch()
        btns_layout.addWidget(btn_fechar)
        layout.addLayout(btns_layout)

        btn_copiar.clicked.connect(self.copiar_clipboard)
        btn_fechar.clicked.connect(self.accept)

    def copiar_clipboard(self):
        texto = f"Assunto: {self.edit_assunto.text()}\n\n{self.edit_corpo.toPlainText()}"
        QApplication.clipboard().setText(texto)
        QMessageBox.information(self, "Copiado", "E-mail copiado para a área de transferência.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Gerenciamento de Eventos – GUI")
        self.resize(1100, 650)

        self.api = InterfaceAPI()
        self._load_thread = None
        self._load_worker = None
        self.progress = None

        container = QWidget()
        layout_principal = QVBoxLayout(container)
        layout_principal.setContentsMargins(16, 16, 16, 16)
        layout_principal.setSpacing(12)

        layout_arquivo = QHBoxLayout()
        layout_arquivo.setSpacing(8)

        self.input_caminho = QLineEdit()
        self.input_caminho.setPlaceholderText("Caminho para a planilha Excel...")
        self.input_caminho.setClearButtonEnabled(True)

        btn_browse = QPushButton("Escolher Arquivo…")
        btn_browse.clicked.connect(self.escolher_arquivo)

        btn_carregar = QPushButton("Carregar Planilha")
        btn_carregar.clicked.connect(self.carregar_planilha)

        layout_arquivo.addWidget(self.input_caminho)
        layout_arquivo.addWidget(btn_browse)
        layout_arquivo.addWidget(btn_carregar)

        layout_principal.addLayout(layout_arquivo)

        self.label_status = QLabel("Nenhuma planilha carregada.")
        layout_principal.addWidget(self.label_status)

        layout_botoes = QHBoxLayout()
        layout_botoes.setSpacing(10)

        self.btn_filtrar = QPushButton("Filtrar Planilha")
        self.btn_listas = QPushButton("Gerenciar Blacklist / Whitelist")
        self.btn_email = QPushButton("Gerar E-mail do Evento Selecionado")

        for btn in (self.btn_filtrar, self.btn_listas, self.btn_email):
            btn.setEnabled(False)
            btn.setMinimumHeight(40)

        self.btn_filtrar.clicked.connect(self.acao_filtrar)
        self.btn_listas.clicked.connect(self.acao_listas)
        self.btn_email.clicked.connect(self.acao_email)

        layout_botoes.addWidget(self.btn_filtrar)
        layout_botoes.addWidget(self.btn_listas)
        layout_botoes.addWidget(self.btn_email)

        layout_principal.addLayout(layout_botoes)

        self.tabela_eventos = QTableWidget()
        self.tabela_eventos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabela_eventos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela_eventos.setAlternatingRowColors(True)
        self.tabela_eventos.horizontalHeader().setStretchLastSection(True)
        self.tabela_eventos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout_principal.addWidget(self.tabela_eventos, stretch=1)

        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        self.statusBar().showMessage("Pronto")

        self.setCentralWidget(container)

        self.input_caminho.setText("./planilha/Cronograma_de_Linha_Morta_25-11-07.xlsx")

    def escolher_arquivo(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar planilha Excel",
            "",
            "Arquivos Excel (*.xlsx *.xlsm *.xls);;Todos os arquivos (*)",
        )
        if file_path:
            self.input_caminho.setText(file_path)

    def carregar_planilha(self):
        caminho = self.input_caminho.text().strip()
        if not caminho:
            QMessageBox.warning(self, "Aviso", "Informe o caminho da planilha.")
            return

        if not os.path.exists(caminho):
            QMessageBox.critical(self, "Erro", f"Arquivo não encontrado:\n{caminho}")
            return

        self.progress = QProgressDialog(
            "Carregando planilha, por favor aguarde...",
            None,
            0,
            0,
            self
        )
        self.progress.setWindowTitle("Carregando")
        self.progress.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.progress.setCancelButton(None)
        self.progress.setMinimumDuration(0)
        self.progress.show()

        self._load_thread = QThread(self)
        self._load_worker = LoadPlanilhaWorker(self.api, caminho)
        self._load_worker.moveToThread(self._load_thread)

        self._load_thread.started.connect(self._load_worker.run)
        self._load_worker.finished.connect(self._on_load_finished)
        self._load_worker.error.connect(self._on_load_error)

        self._load_worker.finished.connect(self._load_thread.quit)
        self._load_worker.error.connect(self._load_thread.quit)
        self._load_thread.finished.connect(self._load_thread.deleteLater)

        self._load_thread.start()

    def _on_load_finished(self, total: int):
        if self.progress:
            self.progress.close()

        self.label_status.setText(
            f"Planilha carregada com sucesso. Eventos brutos: {total}"
        )
        self.statusBar().showMessage("Planilha carregada.", 5000)

        for btn in (self.btn_filtrar, self.btn_listas, self.btn_email):
            btn.setEnabled(True)

        self.atualizar_tabela_eventos()

    def _on_load_error(self, msg: str):
        if self.progress:
            self.progress.close()

        QMessageBox.critical(self, "Erro ao carregar planilha", msg)
        self.statusBar().showMessage("Erro ao carregar planilha.", 5000)

    def acao_filtrar(self):
        if not self.api.eventos:
            QMessageBox.warning(self, "Aviso", "Nenhum evento carregado para filtrar.")
            return

        self.setCursor(Qt.CursorShape.WaitCursor)
        self.statusBar().showMessage("Aplicando filtro aos eventos...")

        try:
            eventos_antes = len(self.api.eventos)
            eventos_depois = self.api.filtrar()

            self.atualizar_tabela_eventos()

            self.label_status.setText(
                f"Filtro aplicado. {eventos_depois} eventos restantes (de {eventos_antes})."
            )
            self.statusBar().showMessage("Filtro concluído.", 5000)

        except Exception as e:
            QMessageBox.critical(self, "Erro ao filtrar eventos", str(e))
            self.statusBar().showMessage("Erro ao filtrar eventos.", 5000)

        finally:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def acao_listas(self):
        dlg = ListasDialog(self.api, self)
        if dlg.exec():
            pass

    def acao_email(self):
        linha = self.tabela_eventos.currentRow()
        if linha < 0:
            QMessageBox.warning(self, "Seleção necessária", "Selecione um evento na tabela.")
            return

        try:
            email = self.api.gerar_email(linha)
        except Exception as e:
            QMessageBox.critical(self, "Erro ao gerar e-mail", str(e))
            return

        dlg = EmailDialog(email["assunto"], email["corpo"], self)
        dlg.exec()

    def atualizar_tabela_eventos(self):
        eventos = self.api.eventos

        if not eventos:
            self.tabela_eventos.clear()
            self.tabela_eventos.setRowCount(0)
            self.tabela_eventos.setColumnCount(0)
            return

        primeiro = eventos[0]
        if hasattr(primeiro, "to_dict"):
            col_dict = primeiro.to_dict()
            colunas = list(col_dict.keys())
        else:
            colunas = [
                "Data", "Horário Inicial", "Horário Final",
                "Endereço", "Bairro", "Zona", "Técnico",
                "Status", "Uso Mútuo", "Postes", "Whitelist"
            ]

        self.tabela_eventos.setColumnCount(len(colunas))
        self.tabela_eventos.setHorizontalHeaderLabels([str(c) for c in colunas])
        self.tabela_eventos.setRowCount(len(eventos))

        for i, ev in enumerate(eventos):
            if hasattr(ev, "to_dict"):
                dados = ev.to_dict()
            else:
                dados = {
                    "Data": getattr(ev, "data", ""),
                    "Horário Inicial": getattr(ev, "horario_inicial", ""),
                    "Horário Final": getattr(ev, "horario_final", ""),
                    "Endereço": getattr(ev, "endereco", ""),
                    "Bairro": getattr(ev, "bairro", ""),
                    "Zona": getattr(ev, "zona", ""),
                    "Técnico": getattr(ev, "tecnico", ""),
                    "Status": getattr(ev, "status", ""),
                    "Uso Mútuo": getattr(ev, "uso_mutuo", ""),
                    "Postes": getattr(ev, "postes", []),
                    "Whitelist": getattr(ev, "whitelist", False),
                }

            for j, col in enumerate(colunas):
                valor = dados.get(col, "")
                if col == "Postes" and isinstance(valor, (list, tuple)):
                    valor = ", ".join(map(str, valor))
                if col == "Data":
                    valor = str(valor)
                item = QTableWidgetItem(str(valor))
                self.tabela_eventos.setItem(i, j, item)

        self.statusBar().showMessage(f"{len(eventos)} eventos exibidos.", 3000)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    janela = MainWindow()
    janela.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
