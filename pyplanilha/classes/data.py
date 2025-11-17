class Data:
    """Classe para maniipulação de datas"""
    meses_com_30_dias = [4, 6, 9, 11]

    def __init__(self, data_str):
        """Inicializa a data a partir de uma string no formato 'DD-MM-AAAA' ou 'AAAA-MM-DD'"""

        try: 
            self.dia = int(data_str[0:2])
            self.mes = int(data_str[3:5])
            self.ano = int(data_str[6:10])
        except:
            try:
                self.dia = int(data_str[8:10])
                self.mes = int(data_str[5:7])
                self.ano = int(data_str[0:4])
            except:
                raise ValueError("Data deve estar no formato 'DD-MM-AAAA' ou 'AAAA-MM-DD'")

    def _is_bissexto(self):
        """Verifica se o ano é bissexto"""
        return (self.ano % 4 == 0 and self.ano % 100 != 0) or (self.ano % 400 == 0)
    
    def __add__(self, other):
        """Adiciona dias à data"""
        if isinstance(other, int):
            self.dia += other
        if isinstance(other, Data):
            self.dia += other.dia
            self.mes += other.mes
            self.ano += other.ano
        if isinstance(other, str):
            try:
                self += Data(other)
            except:
                raise ValueError("String deve estar no formato 'DD-MM-AAAA' ou 'AAAA-MM-DD'")
        if self.mes == 2:
            if self._is_bissexto():
                if self.dia > 29:
                    self.dia -= 29
                    self.mes += 1
            else:
                if self.dia > 28:
                    self.dia -= 28
                    self.mes += 1
        elif self.mes in Data.meses_com_30_dias:
            if self.dia > 30:
                self.dia -= 30
                self.mes += 1
        else:
            if self.dia > 31:
                self.dia -= 31
                self.mes += 1
        if self.mes > 12:
            self.mes -= 12
            self.ano += 1
        return self
    
    def __str__(self):
        """Retorna a data no formato 'DD-MM-AAAA'"""
        return f"{self.dia:02d}-{self.mes:02d}-{self.ano}"
    
if __name__ == "__main__":
    data1 = Data("28-02-2020") #testando em um ano bissexto
    print(f"Data inicial: {data1}")
    data1 += 3
    print(f"Data após adicionar 3 dias: {data1}")
    
    data2 = Data("30-10-2025")
    print(f"Data inicial: {data2}")
    data2 += 5
    print(f"Data após adicionar 5 dias: {data2}")

    print("Testando adição de duas datas:")
    print(data1+'01-01-0001')  # Adiciona 1 dia, 1 mês e 1 ano a data1
    