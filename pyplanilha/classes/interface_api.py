# pyplanilha/classes/interface_api.py

import re
from pyplanilha.tools.saver import *
from pyplanilha.tools.parser import parse_planilha


class InterfaceAPI:
    """
    Versão em estilo 'serviço' da sua Interface:
    - Sem input()/print()
    - Sem menus
    - API limpa para a GUI usar.
    """

    def __init__(self):
        try:
            self.blacklist = carregar_objeto('./data/bairro_blacklist.pkl')
        except FileNotFoundError:
            self.blacklist = []

        try:
            self.whitelist = carregar_objeto('./data/poste_whitelist.pkl')
        except FileNotFoundError:
            self.whitelist = []

        # Lista de eventos (objetos Evento)
        self.eventos = []

    # =========================
    # PLANILHA
    # =========================
    def carregar_planilha(self, path: str) -> int:
        """
        Carrega a planilha e popula self.eventos com objetos Evento.
        Retorna a quantidade de eventos brutos.
        """
        self.eventos = parse_planilha(path)
        return len(self.eventos)

    # =========================
    # FILTRO
    # =========================
    def filtrar(self) -> int:
        """
        Aplica a mesma lógica de filtra_evento da Interface antiga:
        - marca eventos com poste na whitelist
        - filtra por blacklist/status/uso_mutuo
        Atualiza self.eventos e retorna o total restante.
        """
        # Marca whitelist em cada evento (se possuir poste whitelisted)
        for evento in self.eventos:
            evento.whitelist = any(p in self.whitelist for p in evento.postes)

        eventos_filtrados = [
            evento for evento in self.eventos
            if (
                (evento.bairro not in self.blacklist or evento.whitelist)
                and evento.status not in ["CANCELADO", "EXECUTADO"]
                and evento.uso_mutuo != "NÃO"
            )
        ]

        self.eventos = eventos_filtrados
        return len(self.eventos)

    # =========================
    # LISTAS
    # =========================
    def obter_whitelist(self):
        return list(self.whitelist)

    def obter_blacklist(self):
        return list(self.blacklist)

    def adicionar_poste_whitelist(self, poste: str):
        """
        Adiciona um poste (10 dígitos) à whitelist.
        Lança ValueError se inválido.
        """
        poste = str(poste).strip()
        if not re.match(r'^\d{10}$', poste):
            raise ValueError("Poste deve ter exatamente 10 dígitos numéricos.")

        if poste not in self.whitelist:
            self.whitelist.append(poste)
            salvar_objeto(self.whitelist, './data/poste_whitelist.pkl')

    def remover_poste_whitelist(self, poste: str):
        poste = str(poste).strip()
        if poste in self.whitelist:
            self.whitelist.remove(poste)
            salvar_objeto(self.whitelist, './data/poste_whitelist.pkl')

    def adicionar_bairro_blacklist(self, bairro: str):
        bairro = str(bairro).strip().upper()
        if bairro and bairro not in self.blacklist:
            self.blacklist.append(bairro)
            salvar_objeto(self.blacklist, './data/bairro_blacklist.pkl')

    def remover_bairro_blacklist(self, bairro: str):
        bairro = str(bairro).strip().upper()
        if bairro in self.blacklist:
            self.blacklist.remove(bairro)
            salvar_objeto(self.blacklist, './data/bairro_blacklist.pkl')

    # =========================
    # E-MAIL
    # =========================
    def gerar_email(self, index: int) -> dict:
        """
        Retorna um dicionário com 'assunto' e 'corpo' do e-mail
        para o evento na posição index de self.eventos.
        """
        if not self.eventos:
            raise RuntimeError("Nenhum evento carregado.")

        if index < 0 or index >= len(self.eventos):
            raise ValueError("Índice de evento inválido.")

        evento = self.eventos[index]

        return {
            "assunto": evento.gerar_assunto_email(),
            "corpo": evento.gerar_corpo_email()
        }
