import pyplanilha

def mostrar_menu():
    """Exibe o menu principal"""
    print("\n" + "="*50)
    print("          SISTEMA DE GERENCIAMENTO DE EVENTOS")
    print("="*50)
    print("1. Filtrar Planilha")
    print("2. Visualizar Planilha Filtrada")
    print("3. Gerenciar Blacklist/Whitelist")
    print("4. Gerar E-mail para Evento")
    print("5. Sair")
    print("="*50)

def gerenciar_listas(interface):
	"""Submenu para gerenciar blacklist e whitelist"""
	while True:
		print("\n" + "-"*40)
		print("   GERENCIAR BLACKLIST/WHITELIST")
		print("-"*40)
		print("1. Adicionar poste à Whitelist")
		print("2. Remover poste da Whitelist")
		print("3. Adicionar bairro à Blacklist")
		print("4. Remover bairro da Blacklist")
		print("5. Visualizar Whitelist")
		print("6. Visualizar Blacklist")
		print("7. Voltar ao menu principal")
			
		opcao = input("\nEscolha uma opção: ").strip()
		
		if opcao == "1":
			poste = input("Digite o código do poste (10 dígitos): ").strip()
			if len(poste) == 10 and poste.isdigit():
				interface.add_whitelist(poste)
				print(f"Poste {poste} adicionado à Whitelist!")
			else:
				print("Código inválido! Deve conter exatamente 10 dígitos.")
					
		elif opcao == "2":
			poste = input("Digite o código do poste a remover: ").strip()
			if poste in interface.whitelist:
				interface.remove_whitelist(poste)
				print(f"Poste {poste} removido da Whitelist!")
			else:
				print("Poste não encontrado na Whitelist.")
				
		elif opcao == "3":
			bairro = input("Digite o nome do bairro: ").strip().upper()
			interface.add_blacklist(bairro)
			print(f"Bairro {bairro} adicionado à Blacklist!")
				
		elif opcao == "4":
			bairro = input("Digite o nome do bairro a remover: ").strip().upper()
			if bairro in interface.blacklist:
				interface.remove_blacklist(bairro)
				print(f"Bairro {bairro} removido da Blacklist!")
			else:
				print("Bairro não encontrado na Blacklist.")
					
		elif opcao == "5":
			print("\nWHITELIST (Postes):")
			print("-" * 20)
			for i, poste in enumerate(interface.whitelist, 1):
				print(f"{i}. {poste}")
			if not interface.whitelist:
				print("Lista vazia")
					
		elif opcao == "6":
			print("\nBLACKLIST (Bairros):")
			print("-" * 20)
			for i, bairro in enumerate(interface.blacklist, 1):
				print(f"{i}. {bairro}")
			if not interface.blacklist:
				print("Lista vazia")
					
		elif opcao == "7":
			break
		else:
			print("Opção inválida!")


def main():
    """Função principal do programa"""
    interface = pyplanilha.Interface()
    
    print("Bem-vindo ao Sistema de Gerenciamento de Eventos!")
    print("Antes de começar, certifique-se de que a planilha está no caminho correto.")
    
    # Solicitar o caminho da planilha
    file_path = input("Digite o caminho para a planilha Excel (ou Enter para usar o padrão): ").strip()
    if not file_path:
        file_path = "./planilha/Cronograma_de_Linha_Morta_25-11-07.xlsx"
    
    try:
        interface.inicia_planilha(file_path)
        print(f"Planilha carregada com sucesso! Total de eventos brutos: {len(interface.eventos)}")
    except Exception as e:
        print(f"Erro ao carregar a planilha: {e}")
        return
    
    while True:
        mostrar_menu()
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            print("\nFiltrando eventos...")
            eventos_antes = len(interface.eventos)
            interface.filtra_evento()
            eventos_depois = len(interface.eventos)
            print(f"Filtro concluído! {eventos_depois} eventos restantes (de {eventos_antes} inicialmente).")
            
        elif opcao == "2":
            interface.visualizar_eventos()
            
        elif opcao == "3":
            gerenciar_listas(interface)
            
        elif opcao == "4":
            interface.gerar_email_evento()
            
        elif opcao == "5":
            print("\nObrigado por usar o sistema! Até mais!")
            break
            
        else:
            print("Opção inválida! Por favor, escolha uma opção de 1 a 5.")

if __name__ == "__main__":
    main()