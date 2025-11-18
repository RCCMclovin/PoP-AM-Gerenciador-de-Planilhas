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
            interface.gerenciar_listas()
            
        elif opcao == "4":
            interface.gerar_email_evento()
            
        elif opcao == "5":
            print("\nObrigado por usar o sistema! Até mais!")
            break
            
        else:
            print("Opção inválida! Por favor, escolha uma opção de 1 a 5.")

if __name__ == "__main__":
    main()