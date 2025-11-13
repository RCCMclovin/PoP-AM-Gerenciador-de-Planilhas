from src.tools.parser import *
from src.tools.saver import *
import re


class interface:
	def __new__(cls):
		if not hasattr(cls, 'instance'):
			cls.instance = super(interface, cls).__new__(cls)
		return cls.instance
	def __init__(self):
		self.blacklist = carregar_objeto('./data/bairro_blacklist.pkl')
		self.whitelist = carregar_objeto('./data/poste_whitelist.pkl')
		self.eventos = [] #Inicializa a lista de enventos vazia

	def add_whitelist(self, poste):
		try:
			if bool(re.match(r'^\d{10}$', str(poste))):
				self.whitelist.append(poste) 
			else: 
				return
		except Exception as e:
			raise RuntimeError(f"Erro ao adicionar poste na Whitelist {self}: {str(e)}")

	def remove_whitelist(self, poste):
		try:
			if bool(re.match(r'^\d{10}$', str(poste))):
				self.whitelist.remove(poste) 
			else: 
				return
		except Exception as e:
			raise RuntimeError(f"Erro ao remover poste da Whitelist {self}: {str(e)}")

	def add_blacklist(self, bairro):
		try:
			if type(bairro) == type(str):
				self.blacklist.append(bairro) 
			else: 
				return
		except Exception as e:
			raise RuntimeError(f"Erro ao adicionar bairro na Blacklist {self}: {str(e)}")

	def remove_blacklist(self, bairro):
		try:
			if type(bairro) == type(str):
				self.blacklist.remove(bairro) 
			else: 
				return
		except Exception as e:
			raise RuntimeError(f"Erro ao remover bairro da Blacklist {self}: {str(e)}")


	def vizualiza_planila(self, file_path):
		self.eventos = parse_planilha(file_path)
		#código aqui pra mostrar a lista de objetos evento

if __name__ == "__main__":

	salvar_objeto(['outro bairro'], './data/bairro_blacklist.pkl')
	salvar_objeto(['0987654321'], './data/poste_whitelist.pkl')
	i = interface()
	i.add_whitelist("1234567890")
	print(i.whitelist)
	i.remove_whitelist("1234567890")
	print(i.whitelist)

	i.add_blacklist("bairro qualquer")
	print(i.blacklist)
	i.remove_blacklist("bairro qualquer")
	print(i.blacklist)
	i2 = interface()
	print(i is i2)
