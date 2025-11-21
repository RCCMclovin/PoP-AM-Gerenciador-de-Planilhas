from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QMessageBox,
    QDialog,
    QPlainTextEdit,
)

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