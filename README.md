# Gerenciador de planilhas para o PoP-AM

Este trabalho foi criado para a disciplina de introdução à Python, do projeto Connor - Pós-Graduação em cibersegurança.

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
<br/>
1. Carregar uma planilha de eventos de manutenção, remoção e adição de postes.<br/><br/>
2. Filtrar os eventos, levando em consideração as seguintes regras:
   <br/>-Remover eventos cujo campo Uso Mútuo sejam "Não" (indica que não há fibra ótica no(s) poste(s));
   <br/>-Remover eventos cujo campo Status sejam "Cancelados" (evento não ocorrerá mais) ou "Realizados" (evento já ocorreu);
   <br/>-Remover eventos cujo campo Bairro esteja na Blacklist, com exceção dos eventos que também possuem um ou mais postes na Whitelist;
   <br/>Obs: Essas políticas utilizam filtragem por exclusão, com o objetivo de combater erros humanos e a falta de padrões e informações.<br/><br/>
3. Gerenciar as listas utilizadas para filtrar os eventos (Blacklist de Bairros e Whitelist de Postes). Isso inclui:
     <br/>-Visualizar as listas;
     <br/>-Adicionaar elementos;
     <br/>-Remover elementos;<br/><br/>
4. Gerar e-mail comunicando o evento para a equipe de manutenção, contendo os campos necessários para a atividade como Data, Horário Inicial, Horário Final, Endereço, Descrição do Evento.<br/><br/>

Todas as funções são realizadas através de uma interface gráfica desenvolvida em PyQt6, com sumporte para algumas funções de qualidade de vida, incluindo, mas não somente:
  <br/>1. Seletor de arquivos, para escolher a planilha a ser carregada;
  <br/>2. Memória persistente da última lista de eventos trabalhada;
  <br/>3. Combobox na visualização de eventos, permitindo agilizar as ações de Gerar e-mail, adicionar elementos a Blacklist e Whitelist, e copiar o endereço do evento;
  <br/>4. Possibilitar a inserção de múltiplos elementos simultâneos na Whitelist e Blacklist;

     
