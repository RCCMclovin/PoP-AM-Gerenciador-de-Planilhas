# main.py
import sys
import os

# Adiciona o diretório atual ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.classes.interface import Interface

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

def visualizar_eventos(interface):
    """Exibe os eventos filtrados"""
    if not interface.eventos:
        print("\nNenhum evento para exibir. Execute o filtro primeiro (Opção 1).")
        return
    
    print(f"\n{'='*80}")
    print(f"{'EVENTOS FILTRADOS':^80}")
    print(f"{'='*80}")
    print(f"Total de eventos: {len(interface.eventos)}")
    print(f"{'='*80}")
    
    for i, evento in enumerate(interface.eventos, 1):
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

def gerar_email_evento(interface):
    """Permite gerar e-mail para um evento específico"""
    if not interface.eventos:
        print("\nNenhum evento para exibir. Execute o filtro primeiro (Opção 1).")
        return
    
    visualizar_eventos(interface)
    
    try:
        num_evento = int(input(f"\nDigite o número do evento (1 a {len(interface.eventos)}): "))
        if 1 <= num_evento <= len(interface.eventos):
            evento = interface.eventos[num_evento - 1]
            
            print("\n" + "="*60)
            print("           E-MAIL GERADO")
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

def main():
    """Função principal do programa"""
    interface = Interface()
    
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
            visualizar_eventos(interface)
            
        elif opcao == "3":
            gerenciar_listas(interface)
            
        elif opcao == "4":
            gerar_email_evento(interface)
            
        elif opcao == "5":
            print("\nObrigado por usar o sistema! Até mais!")
            break
            
        else:
            print("Opção inválida! Por favor, escolha uma opção de 1 a 5.")

if __name__ == "__main__":
    main()