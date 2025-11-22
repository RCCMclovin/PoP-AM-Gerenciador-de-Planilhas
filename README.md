# Gerenciador de planilhas para o PoP-AM

Este trabalho foi criado para a disciplina de introdução à Python, do projeto Connor - Pós-Graduação em cibersegurança.

Membros da Equipe: Gabriel Toledano Feitosa (gtf@icomp.ufam.edu.br), Larissa de Andrade Silva (las@icomp.ufam.edu.br), Rafael Castilho Carvalho (rcc@icomp.ufam.edu.br)

Antes de executar o código:

~~~shell
pip install -r requirements.txt
~~~

Para executar a interface:

~~~shell
python main.py
~~~

O objetivo desta aplicação é auxiliar um analista de redes, responsável por supervisionar uma rede de fibra ótica, identificar eventos (manutenção, remoção e adição) em postes que possuam fibra ótica da qual ele é responsável.

Estes eventos são avisados através de uma planilha, feita por um ser humano sem auxílio de nenhum sistema, e portanto carece de padrões e informações precisas.

Para solucionar este problema a aplicação foi criada com as seguintes funções:

1) Carregar uma planilha de eventos de manutenção, remoção e adição de postes.

2) Filtrar os eventos, levando em consideração as seguintes regras:
   * Remover eventos cujo campo Uso Mútuo sejam "Não" (indica que não há fibra ótica no(s) poste(s));
   * Remover eventos cujo campo Status sejam "Cancelados" (evento não ocorrerá mais) ou "Realizados" (evento já ocorreu);
   * Remover eventos cujo campo Bairro esteja na Blacklist, com exceção dos eventos que também possuem um ou mais postes na Whitelist;
   * Obs: Essas políticas utilizam filtragem por exclusão, com o objetivo de combater erros humanos e a falta de padrões e informações.

3) Gerenciar as listas utilizadas para filtrar os eventos (Blacklist de Bairros e Whitelist de Postes). Isso inclui:
     * Visualizar as listas;
     * Adicionar elementos;
     * Remover elementos;

4) Gerar e-mail comunicando o evento para a equipe de manutenção, contendo os campos necessários para a atividade como Data, Horário Inicial, Horário Final, Endereço, Descrição do Evento.

Todas as funções são realizadas através de uma interface gráfica desenvolvida em PyQt6, com suporte para algumas funções de qualidade de vida, incluindo, mas não somente:

1) Seletor de arquivos, para escolher a planilha a ser carregada;

2) Memória persistente da última lista de eventos trabalhada;

3) Combobox na visualização de eventos, permitindo agilizar as ações de Gerar e-mail, adicionar elementos a Blacklist e Whitelist, e copiar o endereço do evento;

4) Possibilitar a inserção de múltiplos elementos simultâneos na Whitelist e Blacklist;
   
Link para Apresentação da Aplicação: [https://drive.google.com/file/d/1PGE-X6CdqhoIhp7Zixt0EnzJvknZq1JJ/view?usp=sharing](https://drive.google.com/file/d/1PGE-X6CdqhoIhp7Zixt0EnzJvknZq1JJ/view?usp=sharing)

Projeto disponível em: [https://github.com/RCCMclovin/PoP-AM-Gerenciador-de-Planilhas](https://github.com/RCCMclovin/PoP-AM-Gerenciador-de-Planilhas)
