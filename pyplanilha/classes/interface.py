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
		finally:
			#checa em todos os eventos se algum deles tem poste na Whitelist, se sim marca o atributo whitelist como Verdadeiro
			for i in self.evento:
				for p in i.postes:
					if p in self.whitelist:
						i.whitelist = True
						break

	def remove_whitelist(self, poste):
		try:
			if bool(re.match(r'^\d{10}$', str(poste))):
				self.whitelist.remove(poste) 
				salvar_objeto(self.whitelist,'./data/poste_whitelist.pkl')
			else: 
				return
		except Exception as e:
			raise RuntimeError(f"Erro ao remover poste da Whitelist {self}: {str(e)}")
		finally:
			#checa em todos os eventos se algum deles tem poste na Whitelist, se sim marca o atributo whitelist como Verdadeiro
			for i in self.evento:
				i.whitelist = False
				for p in i.postes:
					if p in self.whitelist:
						i.whitelist = True
						break

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
		"""Filtra os eventos com base na blacklist e whitelist.
		Cria uma nova lista com os elementos que não estão na blacklist, ou estão na blacklist E na whitelist; 
		que não estão cancelados e ainda não foram executados (buscando os programados);
		e por fim, eventos que são Uso Mútuo (os postes possuem fibra ótica)
		"""

		#Filtra os elementos por:
		#1. Se não estão na blacklist , ou que estão na blacklist, mas tem postes na whitelist (provavel erro humano)
		#2. Não foram Cancelados nem Executados (queremos os eventos Programados)
		#3. São de Uso Mútuo (os postes tem fibra ótica)
		eventos_filtrados = [evento for evento in self.eventos  if ((evento.bairro not in self.blacklist or evento.whitelist == True) and evento.status not in ["CANCELADO", "EXECUTADO"] and evento.uso_mutuo != "NÃO") ]
		self.eventos = eventos_filtrados
	def visualizar_eventos(self):
		"""Exibe os eventos filtrados"""
		if not self.eventos:
			print("\nNenhum evento para exibir. Execute o filtro primeiro (Opção 1).")
			return
		
		print(f"\n{'='*80}")
		print(f"{'EVENTOS FILTRADOS':^80}")
		print(f"{'='*80}")
		print(f"Total de eventos: {len(self.eventos)}")
		print(f"{'='*80}")
		
		for i, evento in enumerate(self.eventos, 1):
			print(f"\n--- EVENTO {i} ---")
			print(f"Data: {evento.data}")
			print(f"Horário: {evento.horario_inicial} - {evento.horario_final}")
			print(f"Endereço: {evento.endereco}")
			print(f"Bairro: {evento.bairro}")
			print(f"Zona: {evento.zona}")
			print(f"Técnico: {evento.tecnico}")
			print(f"Status: {evento.status}")
			print(f"Uso Mútuo: {evento.uso_mutuo}")
			print(f"Postes: {', '.join(evento.postes) if evento.postes else 'Nenhum'}")
			print(f"Na Whitelist: {'Sim' if evento.whitelist else 'Não'}")
			print("-" * 40)
	
	def gerar_email_evento(self):
		"""Permite gerar e-mail para um evento específico"""
		if not self.eventos:
			print("\nNenhum evento para exibir. Execute o filtro primeiro (Opção 1).")
			return
		
		self.visualizar_eventos()
		
		try:
			num_evento = int(input(f"\nDigite o número do evento (1 a {len(self.eventos)}): "))
			if 1 <= num_evento <= len(self.eventos):
				evento = self.eventos[num_evento - 1]
				
				print("\n" + "="*60)
				print("		   E-MAIL GERADO")
				print("="*60)
				print(f"ASSUNTO: {evento.gerar_assunto_email()}")
				print("\nCORPO DO E-MAIL:")
				print("="*60)
				print(evento.gerar_corpo_email())
				print("="*60)
				
				# Opção para copiar para área de transferência
				copiar = input("\nDeseja copiar o e-mail para a área de transferência? (s/n): ").lower()
				if copiar == 's':
					try:
						import pyperclip
						email_completo = f"Assunto: {evento.gerar_assunto_email()}\n\n{evento.gerar_corpo_email()}"
						pyperclip.copy(email_completo)
						print("E-mail copiado para a área de transferência!")
					except ImportError:
						print("Biblioteca pyperclip não instalada. Instale com: pip install pyperclip")
			else:
				print("Número de evento inválido!")
		except ValueError:
			print("Por favor, digite um número válido.")


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