from pyplanilha.tools.saver import *
from pyplanilha.tools.parser import parse_planilha
import re


class Interface:
	def __new__(cls):
		"""Singleton pattern implementation for securing a single instance of the interface class."""
		if not hasattr(cls, 'instance'):
			cls.instance = super(Interface, cls).__new__(cls)
		return cls.instance
	
	def __init__(self):
		try:
			self.blacklist = carregar_objeto('./data/bairro_blacklist.pkl')
		except FileNotFoundError:
			self.blacklist = []
		try:
			self.whitelist = carregar_objeto('./data/poste_whitelist.pkl')
		except FileNotFoundError:
			self.whitelist = []
		self.eventos = [] #Inicializa a lista de enventos vazia

	def add_whitelist(self, poste):
		try:
			if bool(re.match(r'^\d{10}$', str(poste))):
				self.whitelist.append(poste) 
				salvar_objeto(self.whitelist,'./data/poste_whitelist.pkl')
			else: 
				return
		except Exception as e:
			raise RuntimeError(f"Erro ao adicionar poste na Whitelist {self}: {str(e)}")

	def remove_whitelist(self, poste):
		try:
			if bool(re.match(r'^\d{10}$', str(poste))):
				self.whitelist.remove(poste) 
				salvar_objeto(self.whitelist,'./data/poste_whitelist.pkl')
			else: 
				return
		except Exception as e:
			raise RuntimeError(f"Erro ao remover poste da Whitelist {self}: {str(e)}")

	def add_blacklist(self, bairro):
		try:
			self.blacklist.append(bairro) 
			salvar_objeto(self.blacklist,'./data/bairro_blacklist.pkl')
			
		except Exception as e:
			raise RuntimeError(f"Erro ao adicionar bairro na Blacklist {self}: {str(e)}")

	def remove_blacklist(self, bairro):
		try:
			self.blacklist.remove(bairro) 
			salvar_objeto(self.blacklist,'./data/bairro_blacklist.pkl')
			
		except Exception as e:
			raise RuntimeError(f"Erro ao remover bairro da Blacklist {self}: {str(e)}")

	def inicia_planilha(self, file_path):
		self.eventos = parse_planilha(file_path)

	def filtra_evento(self):
		"""Filtra os eventos em duas etapas;
		Primeiro procura todos os eventos que possuem um ou mais postes na Whitelist, e mudam seu atributo Whitelist para Verdadeiro
		Depois, cria uma nova lista com os elementos que não estão na blacklist, ou estão na blacklist E na whitelist; 
		que não estão cancelados e ainda não foram executados (buscando os programados);
		e por fim, eventos que são Uso Mútuo (os postes possuem fibra ótica)
		"""

		#checa em todos os eventos se algum deles tem poste na Whitelist, se sim marca o atributo whitelist como Verdadeiro
		for i in self.eventos:
			for p in i.postes:
				if p in self.whitelist:
					i.whitelist = True
					break

		#Filtra os elementos por:
		#1. Se não estão na blacklist , ou que estão na blacklist, mas tem postes na whitelist (provavel erro humano)
		#2. Não foram Cancelados nem Executados (queremos os eventos Programados)
		#3. São de Uso Mútuo (os postes tem fibra ótica)
		eventos_filtrados = [evento for evento in self.eventos  if ((evento.bairro not in self.blacklist or evento.whitelist == True) and evento.status not in ["CANCELADO", "EXECUTADO"] and evento.uso_mutuo != "NÃO") ]
		self.eventos = eventos_filtrados
	



if __name__ == "__main__":

	testing = "default" #filtra o que você tá testando, valores:
					   #"filtro","add/remove"
	

	match testing:
		case "default":
			i = Interface()
			print("ok")
		case "add/remove":
			salvar_objeto(["um bairro", "outro bairro"], './data/bairro_blacklist.pkl')
			salvar_objeto(['0987654321'], './data/poste_whitelist.pkl')
			i = Interface()
			i.add_whitelist("1234567890")
			print(i.whitelist)
			i.remove_whitelist("1234567890")
			print(i.whitelist)

			i.add_blacklist("bairro qualquer")
			print(i.blacklist)
			i.remove_blacklist("bairro qualquer")
			print(i.blacklist)
			i2 = Interface()
			print(i is i2)

		case "filtro":
			bl = ['RURAL', 'TARUMÃ', 'CIDADE NOVA', 'TERRA NOVA','ZUMBI DOS PALMARES', 'SANTO ANTÔNIO', 'JORGE TEIXEIRA', 'TARUMÃ-AÇU', 'TANCREDO NEVES', 'COLÔNIA TERRA NOVA', 'NOVA CIDADE', 
					'GILBERTO MESTRINHO', 'PONTA NEGRA', 'NOVO ISRAEL', 'CIDADE DE DEUS', 'SÃO JOSÉ', 'COLÔNIA OLIVEIRA MACHADO', 'ARMANDO MENDES', 'LÍRIO DO VALE', 'SANTA ETELVINA', 'LAGO AZUL', 
					'SANTO AGOSTINHO', 'COLÔNIA ANTÔNIO ALEIXO', 'VILA DA PRATA', 'COLÔNIA SANTO ANTÔNIO', 'DISTRITO INDUSTRIAL 2', 'NOVA ESPERANÇA', 'REDENÇÃO', 'MONTE DAS OLIVEIRAS', 'MAUAZINHO',
					'PURAQUEQUARA', 'PLANALTO', 'NOVO ALEIXO']
			salvar_objeto(bl, './data/bairro_blacklist.pkl')
			salvar_objeto(['1004782702'], './data/poste_whitelist.pkl')
			i = Interface()
			file_path = "./planilha/Cronograma_de_Linha_Morta_25-11-07.xlsx"
			i.inicia_planilha(file_path)
			#print(i.eventos)
			i.filtra_evento()
			for e in i.eventos:
				print(e, e.whitelist)