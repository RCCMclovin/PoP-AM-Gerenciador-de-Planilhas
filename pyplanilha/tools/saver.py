import pickle

def salvar_objeto(objeto, nome_arquivo):
    """Salva um objeto em um arquivo usando pickle.

    Args:
        objeto: O objeto a ser salvo.
        nome_arquivo (str): O nome do arquivo onde o objeto será salvo.
    """
    try:
        with open(nome_arquivo, 'wb') as arquivo:
            pickle.dump(objeto, arquivo)
    except Exception as e:
        raise RuntimeError(f"Erro ao salvar o objeto {objeto} em {nome_arquivo}: {str(e)}")
    
    
def carregar_objeto(nome_arquivo):
    """Carrega um objeto de um arquivo usando pickle.

    Args:
        nome_arquivo (str): O nome do arquivo de onde o objeto será carregado.

    Returns:
        O objeto carregado do arquivo.
    """
    try: 
        with open(nome_arquivo, 'rb') as arquivo:
            objeto = pickle.load(arquivo)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Erro ao carregar o objeto de {nome_arquivo}: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar o objeto de {nome_arquivo}: {str(e)}")
    return objeto


if __name__ == "__main__":
    blacklist = ['RURAL', 'TARUMÃ', 'CIDADE NOVA', 'TERRA NOVA','ZUMBI DOS PALMARES', 'SANTO ANTÔNIO', 'JORGE TEIXEIRA', 'TARUMÃ-AÇU', 'TANCREDO NEVES', 'COLÔNIA TERRA NOVA', 'NOVA CIDADE', 
					'GILBERTO MESTRINHO', 'PONTA NEGRA', 'NOVO ISRAEL', 'CIDADE DE DEUS', 'SÃO JOSÉ', 'COLÔNIA OLIVEIRA MACHADO', 'ARMANDO MENDES', 'LÍRIO DO VALE', 'SANTA ETELVINA', 'LAGO AZUL', 
					'SANTO AGOSTINHO', 'COLÔNIA ANTÔNIO ALEIXO', 'VILA DA PRATA', 'COLÔNIA SANTO ANTÔNIO', 'DISTRITO INDUSTRIAL 2', 'NOVA ESPERANÇA', 'REDENÇÃO', 'MONTE DAS OLIVEIRAS', 'MAUAZINHO',
					'PURAQUEQUARA', 'PLANALTO', 'NOVO ALEIXO']
    
    salvar_objeto(blacklist, '../../data/bairro_blacklist.pkl')

    carregada = carregar_objeto('../../data/bairro_blacklist.pkl')
    print(carregada)