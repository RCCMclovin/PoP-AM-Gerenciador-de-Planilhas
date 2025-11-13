from data import Data
import re #biblioteca de expressões regulares

class Evento:
    def __init__(self, linha_dataframe):
        """
        Inicializa um evento a partir de uma linha do DataFrame
        
        Args:
            linha_dataframe: Series do pandas com os dados da planilha
        """
        # Atributos da planilha
        self.data = Data(str(linha_dataframe['Data']))
        self.horario_inicial = linha_dataframe['Horário Inicial']
        self.horario_final = linha_dataframe['Horário Final']
        self.endereco = linha_dataframe['Endereço']
        self.bairro = linha_dataframe['Bairro']
        self.zona = linha_dataframe['Zona']
        self.tecnico = linha_dataframe['Técnico']
        self.descricao_servicos = linha_dataframe['Descrição de Serviços']
        self.status = linha_dataframe['Status']
        self.uso_mutuo = linha_dataframe['Uso Mútuo']
        
        # Atributos adicionais para controle interno
        self.postes = []  # Lista de postes afetados (inicialmente vazia)
        self._extrair_postes_da_descricao() #Extrai os postes da descrição de serviço
        self.whitelist = False  # Inicialmente não está na whitelist
        self.filtrado = False   # Indica se passou pelos filtros
    
    def __str__(self):
        """Representação em string do evento"""
        return f"Evento: {self.data} - {self.bairro} - {self.endereco} - {self.postes}"
    
    def __repr__(self):
        """Representação para debug"""
        return f"Evento(data='{self.data}', bairro='{self.bairro}', endereco='{self.endereco}, postes='{self.postes}' ')"

    def _extrair_postes_da_descricao(self):
        """
        Extrai todos os códigos de postes (10 dígitos) da descrição de serviços
        e remove duplicatas mantendo a ordem de aparecimento
        """
        try:
            if self.descricao_servicos == "":
                self.postes = []
                print(f"Aviso: Descrição de serviços vazia para evento em {self.bairro}")
                return
	        
	        # Converte para string para garantir que podemos usar regex
            descricao_str = str(self.descricao_servicos)
	        
	        # Expressão regular para encontrar sequências de exatamente 10 dígitos
            padrao_postes = r'\b\d{10}\b'
	        
	        # Encontra todos os códigos de postes
            postes_encontrados = re.findall(padrao_postes, descricao_str)
	        
	        # Remove duplicatas mantendo a ordem
            self.postes = list(dict.fromkeys(postes_encontrados))
	        
	        # Log informativo
            if not self.postes:
                print(f"Aviso: Nenhum poste encontrado na descrição de {self}")
                
        except Exception as e:
            self.postes = []  # Garante que a lista fique vazia em caso de erro
            raise RuntimeError(f"Erro ao extrair postes do evento em {self}: {str(e)}")
            
    
    def marcar_whitelist(self):
        """Marca o evento como estando na whitelist"""
        self.whitelist = True
    
    def to_dict(self):
        """Converte o evento para dicionário (útil para criar DataFrames)"""
        return {
            'Data': self.data,
            'Horário Inicial': self.horario_inicial,
            'Horário Final': self.horario_final,
            'Endereço': self.endereco,
            'Bairro': self.bairro,
            'Zona': self.zona,
            'Técnico': self.tecnico,
            'Descrição de Serviços': self.descricao_servicos,
            'Postes': self.postes,
            'Whitelist': self.whitelist,
            'Status': self.status,
        	'Uso Mútuo': self.uso_mutuo
        }
    
    def gerar_assunto_email(self):
        """Gera o assunto do email baseado no evento"""
        return f"Manobra por poste(s) na rota da MetroMAO - RNP-Manaus ({self.endereco} - {self.data})"
    
    def gerar_corpo_email(self):
        """Gera o corpo completo do email"""
        corpo = f"""Saudações prezados da MEGA;
                A concessionária Amazonas Energia realizará uma manobra por poste(s) onde passa cabo de fibra da MetroMAO(CIRCUITO: IPMNS16401), em {self.endereco} - {self.bairro}.
                Solicitamos que a equipe G8 seja acionada para soltar e depois regularizar a sustentação dos cabos da MetroMAO. Segue abaixo a data e horário da realização da troca.
                
                Data da Operação: {self.data}
                Horário: De {self.horario_inicial} até {self.horario_final}
                Endereço: {self.endereco} - {self.bairro}
                Descrição de Serviço: 
                
                {self.descricao_servicos}
                
                Em anexo, região do mapa com o(s) poste(s) afetados.
                
                Att."""
        return corpo
    
    def esta_na_whitelist(self):
        """Retorna se o evento está na whitelist"""
        return self.whitelist


# Exemplo / Teste
if __name__ == "__main__":
    import pandas as pd
    def criar_eventos_do_dataframe(df):
        """
        Cria uma lista de objetos Evento a partir de um DataFrame
        
        Args:
            df: DataFrame do pandas com os dados da planilha
	    
	    Returns:
	        Lista de objetos Evento
	    """
        eventos = []
        for _, linha in df.iterrows():
            evento = Evento(linha)
            eventos.append(evento)
            
        return eventos

    df = pd.read_excel('./planilha/Cronograma_de_Linha_Morta_25-11-07.xlsx')
    eventos = criar_eventos_do_dataframe(df)
    
    print(eventos)