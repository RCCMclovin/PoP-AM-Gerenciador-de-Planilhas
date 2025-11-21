# pyplanilha/classes/interface_api.py

import re
from pyplanilha.tools.saver import *
from pyplanilha.tools.parser import parse_planilha


class InterfaceAPI:
    whitelist_path = './data/poste_whitelist.pkl'
    blacklist_path = './data/bairro_blacklist.pkl'

    def __new__(cls):
        """Implementação do padrão Singleton para garantir apensas uma intância da interface."""
        if not hasattr(cls, 'instance'):
            cls.instance = super(InterfaceAPI, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        try:
            self.blacklist = carregar_objeto(InterfaceAPI.blacklist_path)
        except FileNotFoundError:
            self.blacklist = []

        try:
            self.whitelist = carregar_objeto(InterfaceAPI.whitelist_path)
        except FileNotFoundError:
            self.whitelist = []

        # Lista de eventos (objetos Evento)
        self.eventos = []


    def carregar_planilha(self, path: str) -> int:
        """
        Carrega a planilha e popula self.eventos com objetos Evento.
        Retorna a quantidade de eventos brutos.
        """
        self.eventos = parse_planilha(path)
        for evento in self.eventos:
            evento.whitelist = any(p in self.whitelist for p in evento.postes)
        return len(self.eventos)


    def filtrar(self) -> int:
        """
        Filtra a lista, removendo todos os elementos que:
        1) Estão em bairros na Blacklist e não têm postes na Whitelist
        2) Estão com o status "CANCELADO" ou "EXECUTADO"
        3) Têm conflito de uso (uso_mutuo == "SIM")
        """
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


# Controle da Blacklist e Whitelist
    def obter_whitelist(self):
        return list(self.whitelist)

    def obter_blacklist(self):
        return list(self.blacklist)

    def adicionar_poste_whitelist(self, poste: str):
        poste = str(poste).strip()
        if not re.match(r'^\d{10}$', poste):
            raise ValueError("Poste deve ter exatamente 10 dígitos numéricos.")

        if poste not in self.whitelist:
            self.whitelist.append(poste)
            salvar_objeto(self.whitelist, InterfaceAPI.whitelist_path)
            for i in self.eventos:
                for p in i.postes:
                    if p in self.whitelist:
                        i.whitelist = True
                        break

    def remover_poste_whitelist(self, poste: str):
        poste = str(poste).strip()
        if poste in self.whitelist:
            self.whitelist.remove(poste)
            salvar_objeto(self.whitelist, InterfaceAPI.whitelist_path)
            for i in self.eventos:
                i.whitelist = False
                for p in i.postes:
                    if p in self.whitelist:
                        i.whitelist = True
                        break

    def adicionar_bairro_blacklist(self, bairro: str):
        bairro = str(bairro).strip().upper()
        if bairro and bairro not in self.blacklist:
            self.blacklist.append(bairro)
            salvar_objeto(self.blacklist, InterfaceAPI.blacklist_path)

    def remover_bairro_blacklist(self, bairro: str):
        bairro = str(bairro).strip().upper()
        if bairro in self.blacklist:
            self.blacklist.remove(bairro)
            salvar_objeto(self.blacklist, InterfaceAPI.blacklist_path)

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
