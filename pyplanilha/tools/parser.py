import pandas as pd
from ..classes import Evento
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl') #Desabilita warns de openpyxl, que ocorrem devido ao cabeçalho da planilha

def parse_planilha(file_path):
    """
    Parses an Excel file and returns a List of Events.

    Parameters:
    file_path (str): The path to the Excel file.

    Returns:
    eventos (list): The parsed data as list of events.
    """
    try:
        colunas = ['Data','Horário Inicial','Horário Final','Descrição de Serviços','Endereço','Bairro','Zona','Técnico','Status','Uso Mútuo']
        colunas2 = ['Data','Horário Inicial','Horário Final','Endereço','Bairro','Zona','Técnico','Descrição de Serviços','Uso Mútuo','Status']

        df = pd.read_excel(file_path, usecols = colunas)
        df  = df[colunas2]
        
        return [Evento(linha) for _, linha in df.iterrows()]
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return None

if __name__ == "__main__":
    file_path = "./planilha/Cronograma_de_Linha_Morta_25-11-07.xlsx"
    df = parse_planilha(file_path)
    if df is not None:
        print(df[:5])