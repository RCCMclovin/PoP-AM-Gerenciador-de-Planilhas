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
    QProgressDialog,
    QMenu,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator

from pyplanilha.classes.interface_api import InterfaceAPI


# ====================================================
# THREAD PARA CARREGAR PLANILHA
# ====================================================
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


# ====================================================
# DIÁLOGO LISTAS (BLACKLIST/WHITELIST)
# ====================================================
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

        # -------------------
        # W H I T E L I S T
        # -------------------
        label_wl = QLabel("Whitelist (Postes)")
        self.search_wl = QLineEdit()
        self.search_wl.setPlaceholderText("Pesquisar poste...")
        self.lista_wl = QListWidget()

        btn_add_wl = QPushButton("Adicionar Poste")
        btn_add_wl_multi = QPushButton("Adicionar vários postes…")
        btn_rem_wl = QPushButton("Remover Selecionado")

        # -------------------
        # B L A C K L I S T
        # -------------------
        label_bl = QLabel("Blacklist (Bairros)")
        self.search_bl = QLineEdit()
        self.search_bl.setPlaceholderText("Pesquisar bairro...")
        self.lista_bl = QListWidget()

        btn_add_bl = QPushButton("Adicionar Bairro")
        btn_add_bl_multi = QPushButton("Adicionar vários bairros…")
        btn_rem_bl = QPushButton("Remover Selecionado")

        # Layout Whitelist (coluna 0)
        layout.addWidget(label_wl,      0, 0)
        layout.addWidget(self.search_wl, 1, 0)
        layout.addWidget(self.lista_wl,  2, 0)
        layout.addWidget(btn_add_wl,     3, 0)
        layout.addWidget(btn_add_wl_multi, 4, 0)
        layout.addWidget(btn_rem_wl,     5, 0)

        # Layout Blacklist (coluna 1)
        layout.addWidget(label_bl,      0, 1)
        layout.addWidget(self.search_bl, 1, 1)
        layout.addWidget(self.lista_bl,  2, 1)
        layout.addWidget(btn_add_bl,     3, 1)
        layout.addWidget(btn_add_bl_multi, 4, 1)
        layout.addWidget(btn_rem_bl,     5, 1)

        # Botão fechar
        btn_fechar = QPushButton("Fechar")
        layout.addWidget(btn_fechar, 6, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignRight)

        # Conexões
        btn_add_wl.clicked.connect(self.adicionar_poste)
        btn_add_wl_multi.clicked.connect(self.adicionar_postes_lote)
        btn_rem_wl.clicked.connect(self.remover_poste)

        btn_add_bl.clicked.connect(self.adicionar_bairro)
        btn_add_bl_multi.clicked.connect(self.adicionar_bairros_lote)
        btn_rem_bl.clicked.connect(self.remover_bairro)

        btn_fechar.clicked.connect(self.accept)

        # Busca em tempo real
        self.search_wl.textChanged.connect(self.carregar_listas)
        self.search_bl.textChanged.connect(self.carregar_listas)

        self.carregar_listas()

    # -------------------------
    # Carregar listas na GUI (com filtro)
    # -------------------------
    def carregar_listas(self):
        self.lista_wl.clear()
        self.lista_bl.clear()

        filtro_wl = self.search_wl.text().strip()
        filtro_bl = self.search_bl.text().strip().lower()

        # Whitelist (postes)
        for poste in self.api.obter_whitelist():
            s = str(poste)
            if filtro_wl and filtro_wl not in s:
                continue
            self.lista_wl.addItem(QListWidgetItem(s))

        # Blacklist (bairros) – filtro case-insensitive
        for bairro in self.api.obter_blacklist():
            s = str(bairro)
            if filtro_bl and filtro_bl not in s.lower():
                continue
            self.lista_bl.addItem(QListWidgetItem(s))

    # ------------------------------------------------------
    # Adicionar poste individual
    # ------------------------------------------------------
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

    # ------------------------------------------------------
    # Adicionar vários postes (lote)
    # ------------------------------------------------------
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

    # ------------------------------------------------------
    # Remover poste selecionado
    # ------------------------------------------------------
    def remover_poste(self):
        item = self.lista_wl.currentItem()
        if not item:
            return
        poste = item.text()
        self.api.remover_poste_whitelist(poste)
        self.carregar_listas()

    # ------------------------------------------------------
    # Adicionar bairro individual
    # ------------------------------------------------------
    def adicionar_bairro(self):
        texto, ok = QInputDialog.getText(
            self,
            "Adicionar Bairro à Blacklist",
            "Digite o nome do bairro:",
        )
        if ok and texto.strip():
            self.api.adicionar_bairro_blacklist(texto.strip())
            self.carregar_listas()

    # ------------------------------------------------------
    # Adicionar vários bairros (lote)
    # ------------------------------------------------------
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

    # ------------------------------------------------------
    # Remover bairro selecionado
    # ------------------------------------------------------
    def remover_bairro(self):
        item = self.lista_bl.currentItem()
        if not item:
            return
        bairro = item.text()
        self.api.remover_bairro_blacklist(bairro)
        self.carregar_listas()

# ====================================================
# DIÁLOGO E-MAIL
# ====================================================
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


# ====================================================
# JANELA PRINCIPAL
# ====================================================
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

        # ---------------------------
        # Linha de seleção de arquivo
        # ---------------------------
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

        # ---------------------------
        # Botões principais
        # ---------------------------
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

        # ---------------------------
        # Tabela de eventos
        # ---------------------------
        self.tabela_eventos = QTableWidget()
        self.tabela_eventos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Selecionar célula, não linha inteira
        self.tabela_eventos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)

        self.tabela_eventos.setAlternatingRowColors(True)

        header = self.tabela_eventos.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        # Duplo clique para visualizar/copiar o conteúdo da célula
        self.tabela_eventos.itemDoubleClicked.connect(self.mostrar_celula_completa)

        # Clique direito: menu de contexto
        self.tabela_eventos.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tabela_eventos.customContextMenuRequested.connect(
            self.mostrar_menu_contexto_evento
        )

        layout_principal.addWidget(self.tabela_eventos, stretch=1)

        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        self.statusBar().showMessage("Pronto")

        self.setCentralWidget(container)

        # Caminho padrão
        self.input_caminho.setText("./planilha/Cronograma_de_Linha_Morta_25-11-07.xlsx")

    # ========================
    # Funções de UI
    # ========================
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

        # Caixa de "Carregando..."
        self.progress = QProgressDialog(
            "Carregando planilha, por favor aguarde...",
            None,
            0,
            0,
            self,
        )
        self.progress.setWindowTitle("Carregando")
        self.progress.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.progress.setCancelButton(None)
        self.progress.setMinimumDuration(0)
        self.progress.show()

        # Thread + worker
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
        dlg.exec()

    def acao_email(self):
        linha = self.tabela_eventos.currentRow()
        if linha < 0:
            QMessageBox.warning(self, "Seleção necessária", "Selecione um evento na tabela.")
            return

        self._gerar_email_para_linha(linha)

    def _gerar_email_para_linha(self, linha: int):
        try:
            email = self.api.gerar_email(linha)
        except Exception as e:
            QMessageBox.critical(self, "Erro ao gerar e-mail", str(e))
            return

        dlg = EmailDialog(email["assunto"], email["corpo"], self)
        dlg.exec()

    # ========================
    # Menu de contexto (clique direito)
    # ========================
    def mostrar_menu_contexto_evento(self, pos):
        index = self.tabela_eventos.indexAt(pos)
        if not index.isValid():
            return

        linha = index.row()
        if linha < 0 or linha >= len(self.api.eventos):
            return

        menu = QMenu(self)

        act_email = menu.addAction("Gerar e-mail deste evento")
        act_bairro_bl = menu.addAction("Adicionar bairro à blacklist")
        act_postes_wl = menu.addAction("Adicionar poste(s) à whitelist")
        act_copiar_end = menu.addAction("Copiar endereço")

        action = menu.exec(self.tabela_eventos.viewport().mapToGlobal(pos))
        if not action:
            return

        evento = self.api.eventos[linha]

        if action == act_email:
            # Gera e-mail do evento
            self._gerar_email_para_linha(linha)

        elif action == act_bairro_bl:
            bairro = getattr(evento, "bairro", "").strip()
            if not bairro:
                QMessageBox.warning(self, "Sem bairro", "Este evento não possui bairro definido.")
                return
            self.api.adicionar_bairro_blacklist(bairro)
            QMessageBox.information(
                self,
                "Blacklist",
                f"Bairro '{bairro}' adicionado à blacklist.",
            )

        elif action == act_postes_wl:
            postes = getattr(evento, "postes", [])
            if not postes:
                QMessageBox.warning(self, "Sem postes", "Este evento não possui postes associados.")
                return

            # Se tiver um só, adiciona direto (com confirmação simples)
            if len(postes) == 1:
                poste = str(postes[0]).strip()
                try:
                    self.api.adicionar_poste_whitelist(poste)
                    QMessageBox.information(
                        self,
                        "Whitelist",
                        f"Poste {poste} adicionado à whitelist.",
                    )
                except Exception as e:
                    QMessageBox.warning(self, "Erro ao adicionar poste", str(e))
                return

            # Vários postes: diálogo para escolher um ou mais
            dlg = QDialog(self)
            dlg.setWindowTitle("Adicionar poste(s) à Whitelist")
            dlg.resize(400, 300)

            vbox = QVBoxLayout(dlg)
            vbox.addWidget(QLabel("Selecione um ou mais postes para adicionar à whitelist:"))

            lista = QListWidget()
            lista.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
            for p in postes:
                lista.addItem(QListWidgetItem(str(p)))
            vbox.addWidget(lista)

            hbox = QHBoxLayout()
            btn_ok = QPushButton("Adicionar")
            btn_cancel = QPushButton("Cancelar")
            hbox.addStretch()
            hbox.addWidget(btn_ok)
            hbox.addWidget(btn_cancel)
            vbox.addLayout(hbox)

            btn_cancel.clicked.connect(dlg.reject)

            def confirmar():
                itens = lista.selectedItems()
                if not itens:
                    QMessageBox.warning(dlg, "Nenhum selecionado", "Selecione pelo menos um poste.")
                    return

                adicionados = 0
                erros = 0
                for it in itens:
                    poste = it.text().strip()
                    try:
                        self.api.adicionar_poste_whitelist(poste)
                        adicionados += 1
                    except Exception:
                        erros += 1

                msg = f"{adicionados} poste(s) adicionados à whitelist."
                if erros:
                    msg += f"\n{erros} não puderam ser adicionados (duplicados ou inválidos)."

                QMessageBox.information(dlg, "Resultado", msg)
                dlg.accept()

            btn_ok.clicked.connect(confirmar)
            dlg.exec()

        elif action == act_copiar_end:
            endereco = getattr(evento, "endereco", "").strip()
            if not endereco:
                QMessageBox.warning(self, "Sem endereço", "Este evento não possui endereço definido.")
                return
            QApplication.clipboard().setText(endereco)
            self.statusBar().showMessage("Endereço copiado para a área de transferência.", 3000)

    # ========================
    # Visualizar/copiar célula (duplo clique)
    # ========================
    def mostrar_celula_completa(self, item: QTableWidgetItem):
        dlg = QDialog(self)
        nome_coluna = self.tabela_eventos.horizontalHeaderItem(item.column()).text()
        dlg.setWindowTitle(f"{nome_coluna} – Evento {item.row() + 1}")
        dlg.resize(700, 300)

        layout = QVBoxLayout(dlg)

        edit = QPlainTextEdit()
        edit.setPlainText(item.text())
        edit.setReadOnly(True)

        layout.addWidget(edit)

        btns_layout = QHBoxLayout()
        btn_copiar = QPushButton("Copiar")
        btn_fechar = QPushButton("Fechar")
        btns_layout.addWidget(btn_copiar)
        btns_layout.addStretch()
        btns_layout.addWidget(btn_fechar)
        layout.addLayout(btns_layout)

        def copiar():
            QApplication.clipboard().setText(item.text())
            self.statusBar().showMessage(
                "Texto copiado para a área de transferência.", 3000
            )

        btn_copiar.clicked.connect(copiar)
        btn_fechar.clicked.connect(dlg.accept)

        dlg.exec()

    # ========================
    # Atualizar tabela
    # ========================
    def atualizar_tabela_eventos(self):
        eventos = self.api.eventos

        if not eventos:
            self.tabela_eventos.clear()
            self.tabela_eventos.setRowCount(0)
            self.tabela_eventos.setColumnCount(0)
            return

        primeiro = eventos[0]
        if hasattr(primeiro, "to_dict"):
            colunas = list(primeiro.to_dict().keys())
        else:
            colunas = [
                "Data",
                "Horário Inicial",
                "Horário Final",
                "Endereço",
                "Bairro",
                "Zona",
                "Técnico",
                "Status",
                "Uso Mútuo",
                "Postes",
                "Whitelist",
            ]

        self.tabela_eventos.setColumnCount(len(colunas))
        self.tabela_eventos.setHorizontalHeaderLabels(colunas)
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
                item.setToolTip(str(valor))
                self.tabela_eventos.setItem(i, j, item)

        # Ajuste de largura por tipo de coluna
        header = self.tabela_eventos.horizontalHeader()
        for idx, nome_coluna in enumerate(colunas):
            if nome_coluna == "Data":
                header.resizeSection(idx, 90)
            elif nome_coluna in ("Horário Inicial", "Horário Final"):
                header.resizeSection(idx, 110)
            elif nome_coluna in ("Status", "Uso Mútuo", "Whitelist"):
                header.resizeSection(idx, 110)
            elif nome_coluna == "Zona":
                header.resizeSection(idx, 90)
            elif nome_coluna in ("Bairro", "Técnico"):
                header.resizeSection(idx, 150)
            elif nome_coluna in ("Endereço", "Descrição de Serviços"):
                header.resizeSection(idx, 350)

        self.statusBar().showMessage(f"{len(eventos)} eventos exibidos.", 3000)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    janela = MainWindow()
    janela.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
