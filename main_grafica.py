import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import pyplanilha
import re

class SistemaEventosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Eventos")
        self.root.geometry("1000x700")
        
        self.interface = pyplanilha.Interface()
        self.criar_interface()
        
    def criar_interface(self):
        # Configurar grid principal
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Aba Principal
        self.aba_principal = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_principal, text="Principal")
        
        # Aba Listas
        self.aba_listas = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_listas, text="Gerenciar Listas")
        
        # Aba Visualização
        self.aba_visualizacao = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_visualizacao, text="Visualizar Eventos")
        
        self.criar_aba_principal()
        self.criar_aba_listas()
        self.criar_aba_visualizacao()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Planilha não carregada")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))
        
    def criar_aba_principal(self):
        # Configurar grid da aba principal
        for i in range(5):
            self.aba_principal.grid_rowconfigure(i, weight=1)
        self.aba_principal.grid_columnconfigure(0, weight=1)
        
        # Título
        titulo = ttk.Label(self.aba_principal, text="SISTEMA DE GERENCIAMENTO DE EVENTOS", 
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, pady=(0, 20))
        
        # Seção de carregamento da planilha
        frame_planilha = ttk.LabelFrame(self.aba_principal, text="Carregar Planilha", padding="10")
        frame_planilha.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        frame_planilha.grid_columnconfigure(0, weight=1)
        
        ttk.Label(frame_planilha, text="Caminho da planilha:").grid(row=0, column=0, sticky=tk.W)
        
        frame_caminho = ttk.Frame(frame_planilha)
        frame_caminho.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        frame_caminho.grid_columnconfigure(0, weight=1)
        
        self.entry_caminho = ttk.Entry(frame_caminho, width=80)
        self.entry_caminho.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.entry_caminho.insert(0, "./planilha/Cronograma_de_Linha_Morta_25-11-07.xlsx")
        
        ttk.Button(frame_caminho, text="Procurar", 
                  command=self.procurar_planilha).grid(row=0, column=1)
        
        frame_botoes_carregar = ttk.Frame(frame_planilha)
        frame_botoes_carregar.grid(row=2, column=0, pady=(10, 0))
        
        ttk.Button(frame_botoes_carregar, text="Carregar Planilha", 
                  command=self.carregar_planilha).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botoes_carregar, text="Aplicar Filtros", 
                  command=self.filtrar_planilha).grid(row=0, column=1, padx=5)
        
        # Frame de informações
        frame_info = ttk.LabelFrame(self.aba_principal, text="Informações", padding="10")
        frame_info.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.info_text = scrolledtext.ScrolledText(frame_info, height=8, width=80)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.info_text.config(state=tk.DISABLED)
        
        # Frame de geração de email
        frame_email = ttk.LabelFrame(self.aba_principal, text="Gerar E-mail", padding="10")
        frame_email.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(frame_email, text="Selecione o evento para gerar e-mail:").grid(row=0, column=0, sticky=tk.W)
        
        frame_selecao_email = ttk.Frame(frame_email)
        frame_selecao_email.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.combo_eventos = ttk.Combobox(frame_selecao_email, state="readonly")
        self.combo_eventos.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(frame_selecao_email, text="Gerar E-mail", 
                  command=self.gerar_email).grid(row=0, column=1)
        
        self.email_text = scrolledtext.ScrolledText(frame_email, height=12, width=80)
        self.email_text.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def criar_aba_listas(self):
        # Configurar grid da aba de listas
        self.aba_listas.grid_columnconfigure(0, weight=1)
        self.aba_listas.grid_columnconfigure(1, weight=1)
        self.aba_listas.grid_rowconfigure(0, weight=1)
        
        # Whitelist
        frame_whitelist = ttk.LabelFrame(self.aba_listas, text="Whitelist (Postes)", padding="10")
        frame_whitelist.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        frame_whitelist.grid_columnconfigure(0, weight=1)
        frame_whitelist.grid_rowconfigure(4, weight=1)  # Ajustado para menos linhas
        
        # Entrada para whitelist
        ttk.Label(frame_whitelist, text="Digite o código do poste (10 dígitos):").grid(row=0, column=0, sticky=tk.W)
        
        frame_whitelist_input = ttk.Frame(frame_whitelist)
        frame_whitelist_input.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        frame_whitelist_input.grid_columnconfigure(0, weight=1)
        
        self.entry_whitelist = ttk.Entry(frame_whitelist_input)
        self.entry_whitelist.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        frame_whitelist_botoes = ttk.Frame(frame_whitelist_input)
        frame_whitelist_botoes.grid(row=0, column=1)
        
        ttk.Button(frame_whitelist_botoes, text="Adicionar", 
                  command=self.adicionar_whitelist, width=12).grid(row=0, column=0, padx=2)
        ttk.Button(frame_whitelist_botoes, text="Remover por Texto", 
                  command=self.remover_whitelist_por_texto, width=15).grid(row=0, column=1, padx=2)
        
        # Botões para carregar listas - MOVIDOS PARA CIMA
        frame_whitelist_carregar = ttk.Frame(frame_whitelist)
        frame_whitelist_carregar.grid(row=2, column=0, pady=10)
        
        ttk.Button(frame_whitelist_carregar, text="Carregar de Arquivo", 
                  command=self.carregar_whitelist_arquivo, width=18).grid(row=0, column=0, padx=2)
        ttk.Button(frame_whitelist_carregar, text="Carregar Lista de Texto", 
                  command=self.carregar_whitelist_texto, width=18).grid(row=0, column=1, padx=2)
        
        # Label explicativo
        ttk.Label(frame_whitelist, text="Itens na whitelist (selecione para remover):", 
                  font=('Arial', 9)).grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        
        # LISTBOX para whitelist
        self.whitelist_listbox = tk.Listbox(frame_whitelist, height=10)
        self.whitelist_listbox.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Botões de ação para a lista
        frame_whitelist_acoes = ttk.Frame(frame_whitelist)
        frame_whitelist_acoes.grid(row=5, column=0, pady=5)
        
        ttk.Button(frame_whitelist_acoes, text="Remover Selecionado", 
                  command=self.remover_whitelist, width=16).grid(row=0, column=0, padx=2)
        ttk.Button(frame_whitelist_acoes, text="Limpar Tudo", 
                  command=self.limpar_whitelist, width=12).grid(row=0, column=1, padx=2)
        
        # Blacklist
        frame_blacklist = ttk.LabelFrame(self.aba_listas, text="Blacklist (Bairros)", padding="10")
        frame_blacklist.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        frame_blacklist.grid_columnconfigure(0, weight=1)
        frame_blacklist.grid_rowconfigure(4, weight=1)  # Ajustado para menos linhas
        
        # Entrada para blacklist
        ttk.Label(frame_blacklist, text="Digite o nome do bairro:").grid(row=0, column=0, sticky=tk.W)
        
        frame_blacklist_input = ttk.Frame(frame_blacklist)
        frame_blacklist_input.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        frame_blacklist_input.grid_columnconfigure(0, weight=1)
        
        self.entry_blacklist = ttk.Entry(frame_blacklist_input)
        self.entry_blacklist.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        frame_blacklist_botoes = ttk.Frame(frame_blacklist_input)
        frame_blacklist_botoes.grid(row=0, column=1)
        
        ttk.Button(frame_blacklist_botoes, text="Adicionar", 
                  command=self.adicionar_blacklist, width=12).grid(row=0, column=0, padx=2)
        ttk.Button(frame_blacklist_botoes, text="Remover por Texto", 
                  command=self.remover_blacklist_por_texto, width=15).grid(row=0, column=1, padx=2)
        
        # Botões para carregar listas - MOVIDOS PARA CIMA
        frame_blacklist_carregar = ttk.Frame(frame_blacklist)
        frame_blacklist_carregar.grid(row=2, column=0, pady=10)
        
        ttk.Button(frame_blacklist_carregar, text="Carregar de Arquivo", 
                  command=self.carregar_blacklist_arquivo, width=18).grid(row=0, column=0, padx=2)
        ttk.Button(frame_blacklist_carregar, text="Carregar Lista de Texto", 
                  command=self.carregar_blacklist_texto, width=18).grid(row=0, column=1, padx=2)
        
        # Label explicativo
        ttk.Label(frame_blacklist, text="Itens na blacklist (selecione para remover):", 
                  font=('Arial', 9)).grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        
        # LISTBOX para blacklist
        self.blacklist_listbox = tk.Listbox(frame_blacklist, height=10)
        self.blacklist_listbox.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Botões de ação para a lista
        frame_blacklist_acoes = ttk.Frame(frame_blacklist)
        frame_blacklist_acoes.grid(row=5, column=0, pady=5)
        
        ttk.Button(frame_blacklist_acoes, text="Remover Selecionado", 
                  command=self.remover_blacklist, width=16).grid(row=0, column=0, padx=2)
        ttk.Button(frame_blacklist_acoes, text="Limpar Tudo", 
                  command=self.limpar_blacklist, width=12).grid(row=0, column=1, padx=2)
        
        # Atualizar listas
        self.atualizar_listas()

    # NOVAS FUNÇÕES PARA REMOÇÃO POR TEXTO
    def remover_whitelist_por_texto(self):
        """Remove poste da whitelist digitando o código"""
        poste = self.entry_whitelist.get().strip()
        if len(poste) == 10 and poste.isdigit():
            if poste in self.interface.whitelist:
                try:
                    self.interface.remove_whitelist(poste)
                    self.atualizar_listas()
                    self.entry_whitelist.delete(0, tk.END)
                    messagebox.showinfo("Sucesso", f"Poste {poste} removido da Whitelist!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao remover poste: {e}")
            else:
                messagebox.showwarning("Aviso", f"Poste {poste} não encontrado na Whitelist!")
        else:
            messagebox.showwarning("Aviso", "Código inválido! Deve conter exatamente 10 dígitos.")

    def remover_blacklist_por_texto(self):
        """Remove bairro da blacklist digitando o nome"""
        bairro = self.entry_blacklist.get().strip().upper()
        if bairro:
            if bairro in self.interface.blacklist:
                try:
                    self.interface.remove_blacklist(bairro)
                    self.atualizar_listas()
                    self.entry_blacklist.delete(0, tk.END)
                    messagebox.showinfo("Sucesso", f"Bairro {bairro} removido da Blacklist!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao remover bairro: {e}")
            else:
                messagebox.showwarning("Aviso", f"Bairro {bairro} não encontrado na Blacklist!")
        else:
            messagebox.showwarning("Aviso", "Digite um nome de bairro!")

    # FUNÇÕES PARA LIMPAR LISTAS COMPLETAS
    def limpar_whitelist(self):
        """Limpa toda a whitelist"""
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja limpar toda a Whitelist?"):
            try:
                # Remove um por um para triggerar o salvamento
                for poste in self.interface.whitelist[:]:  # [:] cria uma cópia da lista
                    self.interface.remove_whitelist(poste)
                self.atualizar_listas()
                messagebox.showinfo("Sucesso", "Whitelist limpa com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao limpar whitelist: {e}")

    def limpar_blacklist(self):
        """Limpa toda a blacklist"""
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja limpar toda a Blacklist?"):
            try:
                # Remove um por um para triggerar o salvamento
                for bairro in self.interface.blacklist[:]:  # [:] cria uma cópia da lista
                    self.interface.remove_blacklist(bairro)
                self.atualizar_listas()
                messagebox.showinfo("Sucesso", "Blacklist limpa com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao limpar blacklist: {e}")

    # MANTER AS FUNÇÕES ORIGINAIS DE REMOÇÃO (por seleção na lista)
    def remover_whitelist(self):
        """Remove poste selecionado na lista"""
        selecionado = self.whitelist_listbox.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um poste na lista para remover!")
            return
        
        poste = self.whitelist_listbox.get(selecionado[0])
        try:
            self.interface.remove_whitelist(poste)
            self.atualizar_listas()
            messagebox.showinfo("Sucesso", f"Poste {poste} removido da Whitelist!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover poste: {e}")

    def remover_blacklist(self):
        """Remove bairro selecionado na lista"""
        selecionado = self.blacklist_listbox.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um bairro na lista para remover!")
            return
        
        bairro = self.blacklist_listbox.get(selecionado[0])
        try:
            self.interface.remove_blacklist(bairro)
            self.atualizar_listas()
            messagebox.showinfo("Sucesso", f"Bairro {bairro} removido da Blacklist!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover bairro: {e}")

    def carregar_whitelist_arquivo(self):
        """Carrega whitelist de um arquivo"""
        caminho = filedialog.askopenfilename(
            title="Selecione arquivo com lista de postes",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            try:
                with open(caminho, 'r', encoding='utf-8') as f:
                    linhas = f.readlines()
                
                postes_adicionados = 0
                for linha in linhas:
                    poste = linha.strip()
                    if len(poste) == 10 and poste.isdigit() and poste not in self.interface.whitelist:
                        self.interface.add_whitelist(poste)
                        postes_adicionados += 1
                
                self.atualizar_listas()
                messagebox.showinfo("Sucesso", f"{postes_adicionados} postes adicionados à Whitelist!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo: {e}")


    def carregar_whitelist_texto(self):
        """Abre janela para colar lista de postes"""
        self._abrir_janela_texto("Whitelist", self._processar_whitelist_texto)

    def carregar_blacklist_arquivo(self):
        """Carrega blacklist de um arquivo"""
        caminho = filedialog.askopenfilename(
            title="Selecione arquivo com lista de bairros",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            try:
                with open(caminho, 'r', encoding='utf-8') as f:
                    linhas = f.readlines()
                
                bairros_adicionados = 0
                for linha in linhas:
                    bairro = linha.strip().upper()
                    if bairro and bairro not in self.interface.blacklist:
                        self.interface.add_blacklist(bairro)
                        bairros_adicionados += 1
                
                self.atualizar_listas()
                messagebox.showinfo("Sucesso", f"{bairros_adicionados} bairros adicionados à Blacklist!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo: {e}")

    def carregar_blacklist_texto(self):
        """Abre janela para colar lista de bairros"""
        self._abrir_janela_texto("Blacklist", self._processar_blacklist_texto)

    def _abrir_janela_texto(self, titulo, funcao_processamento):
        """Abre janela para entrada de texto"""
        janela = tk.Toplevel(self.root)
        janela.title(f"Adicionar {titulo}")
        janela.geometry("500x400")
        janela.transient(self.root)
        janela.grab_set()
        
        ttk.Label(janela, text=f"Cole a lista de {titulo.lower()} (um por linha):").pack(pady=10)
        
        text_area = scrolledtext.ScrolledText(janela, height=15, width=60)
        text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        frame_botoes = ttk.Frame(janela)
        frame_botoes.pack(pady=10)
        
        ttk.Button(frame_botoes, text="Processar", 
                  command=lambda: funcao_processamento(text_area.get(1.0, tk.END), janela)).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Cancelar", 
                  command=janela.destroy).pack(side=tk.LEFT, padx=5)

    def _processar_whitelist_texto(self, texto, janela):
        """Processa texto para whitelist"""
        linhas = texto.split('\n')
        postes_adicionados = 0
        
        for linha in linhas:
            poste = linha.strip()
            if len(poste) == 10 and poste.isdigit() and poste not in self.interface.whitelist:
                self.interface.add_whitelist(poste)
                postes_adicionados += 1
        
        self.atualizar_listas()
        janela.destroy()
        messagebox.showinfo("Sucesso", f"{postes_adicionados} postes adicionados à Whitelist!")

    def _processar_blacklist_texto(self, texto, janela):
        """Processa texto para blacklist"""
        linhas = texto.split('\n')
        bairros_adicionados = 0
        
        for linha in linhas:
            bairro = linha.strip().upper()
            if bairro and bairro not in self.interface.blacklist:
                self.interface.add_blacklist(bairro)
                bairros_adicionados += 1
        
        self.atualizar_listas()
        janela.destroy()
        messagebox.showinfo("Sucesso", f"{bairros_adicionados} bairros adicionados à Blacklist!")

    def criar_aba_visualizacao(self):
        # Configurar grid da aba de visualização
        self.aba_visualizacao.grid_columnconfigure(0, weight=1)
        self.aba_visualizacao.grid_rowconfigure(1, weight=1)
        
        # Controles - REMOVIDO O BOTÃO "ATUALIZAR VISUALIZAÇÃO"
        frame_controles = ttk.Frame(self.aba_visualizacao)
        frame_controles.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.filtro_var = tk.StringVar(value="todos")
        ttk.Radiobutton(frame_controles, text="Todos os eventos", variable=self.filtro_var, 
                       value="todos", command=self.atualizar_visualizacao).grid(row=0, column=0, padx=5)
        ttk.Radiobutton(frame_controles, text="Apenas Whitelist", variable=self.filtro_var, 
                       value="whitelist", command=self.atualizar_visualizacao).grid(row=0, column=1, padx=5)
        
        # Label informativo
        ttk.Label(frame_controles, text="A visualização atualiza automaticamente ao carregar/filtrar a planilha", 
                  font=('Arial', 9), foreground='gray').grid(row=0, column=2, padx=10)
        
        # Frame do treeview
        frame_tree = ttk.Frame(self.aba_visualizacao)
        frame_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame_tree.grid_columnconfigure(0, weight=1)
        frame_tree.grid_rowconfigure(0, weight=1)
        
        # Treeview com colunas ajustáveis
        columns = ('Data', 'Bairro', 'Endereço', 'Status', 'Postes', 'Whitelist')
        self.tree = ttk.Treeview(frame_tree, columns=columns, show='headings', height=20)
        
        # Definir cabeçalhos com larguras mais adequadas
        self.tree.heading('Data', text='Data')
        self.tree.heading('Bairro', text='Bairro')
        self.tree.heading('Endereço', text='Endereço')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Postes', text='Postes')
        self.tree.heading('Whitelist', text='Whitelist')
        
        # Configurar larguras das colunas (Endereço com mais espaço)
        self.tree.column('Data', width=80, minwidth=80)
        self.tree.column('Bairro', width=120, minwidth=120)
        self.tree.column('Endereço', width=300, minwidth=200)  # Mais largura para endereço
        self.tree.column('Status', width=100, minwidth=80)
        self.tree.column('Postes', width=150, minwidth=120)
        self.tree.column('Whitelist', width=80, minwidth=80)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree.yview)
        h_scroll = ttk.Scrollbar(frame_tree, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # Grid do treeview e scrollbars
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scroll.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Permitir redimensionamento de colunas
        for col in columns:
            self.tree.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(_col, False))
        
        # Bind para mostrar tooltip com texto completo
        self.tree.bind("<Motion>", self.mostrar_tooltip)
        self.tree.bind("<Leave>", self.esconder_tooltip)
        
        # Variável para tooltip
        self.tooltip = None

    def treeview_sort_column(self, col, reverse):
        """Ordenar coluna do treeview"""
        if not hasattr(self.interface, 'eventos') or not self.interface.eventos:
            return
            
        # Obter dados atuais
        eventos = self.interface.eventos
        if self.filtro_var.get() == "whitelist":
            eventos = [e for e in eventos if e.whitelist]
        
        # Ordenar
        try:
            if col == 'Data':
                eventos.sort(key=lambda x: x.data, reverse=reverse)
            elif col == 'Bairro':
                eventos.sort(key=lambda x: x.bairro, reverse=reverse)
            elif col == 'Endereço':
                eventos.sort(key=lambda x: x.endereco, reverse=reverse)
            elif col == 'Status':
                eventos.sort(key=lambda x: x.status, reverse=reverse)
            elif col == 'Whitelist':
                eventos.sort(key=lambda x: x.whitelist, reverse=reverse)
        except:
            return
        
        # Atualizar visualização
        self.atualizar_visualizacao()

    def mostrar_tooltip(self, event):
        """Mostrar tooltip com texto completo quando hover"""
        item = self.tree.identify_row(event.y)
        if item:
            col = self.tree.identify_column(event.x)
            if col == '#4':  # Coluna do Endereço (índice 3 = #4)
                endereco_completo = self.tree.item(item, 'values')[2]  # Índice 2 = Endereço
                if len(endereco_completo) > 50:  # Só mostra tooltip se for longo
                    if self.tooltip:
                        self.tooltip.destroy()
                    
                    self.tooltip = tk.Toplevel()
                    self.tooltip.wm_overrideredirect(True)
                    self.tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
                    
                    label = ttk.Label(self.tooltip, text=endereco_completo, 
                                     background="yellow", relief="solid", borderwidth=1,
                                     padding=5, wraplength=400)
                    label.pack()

    def esconder_tooltip(self, event):
        """Esconder tooltip"""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

    def atualizar_visualizacao(self):
        if not hasattr(self.interface, 'eventos') or not self.interface.eventos:
            return
        
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filtrar eventos se necessário
        eventos = self.interface.eventos
        if self.filtro_var.get() == "whitelist":
            eventos = [e for e in eventos if e.whitelist]
        
        # Adicionar eventos ao treeview (ENDEREÇO COMPLETO)
        for evento in eventos:
            postes_str = ', '.join(evento.postes) if evento.postes else 'Nenhum'
            whitelist_str = 'Sim' if evento.whitelist else 'Não'
            
            # MOSTRAR ENDEREÇO COMPLETO (sem truncar)
            endereco_completo = evento.endereco
            
            self.tree.insert('', tk.END, values=(
                evento.data,
                evento.bairro,
                endereco_completo,  # Endereço completo
                evento.status,
                postes_str,
                whitelist_str
            ))
        
        # Ajustar automaticamente a largura das colunas após inserir dados
        self.ajustar_largura_colunas()

    def ajustar_largura_colunas(self):
        """Ajusta automaticamente a largura das colunas baseado no conteúdo"""
        for col in self.tree['columns']:
            # Configurar largura mínima
            if col == 'Endereço':
                self.tree.column(col, width=300)  # Largura padrão maior para endereço
            else:
                self.tree.column(col, width=100)
        
    def procurar_planilha(self):
        caminho = filedialog.askopenfilename(
            title="Selecione a planilha",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            self.entry_caminho.delete(0, tk.END)
            self.entry_caminho.insert(0, caminho)
    
    def carregar_planilha(self):
        caminho = self.entry_caminho.get().strip()
        try:
            self.interface.inicia_planilha(caminho)
            eventos_count = len(self.interface.eventos)
            messagebox.showinfo("Sucesso", f"Planilha carregada! Total de eventos: {eventos_count}")
            self.status_var.set(f"Planilha carregada - {eventos_count} eventos")
            self.atualizar_info(f"Planilha carregada com sucesso!\nTotal de eventos brutos: {eventos_count}")
            self.atualizar_combo_eventos()
            
            # ATUALIZAÇÃO AUTOMÁTICA DA VISUALIZAÇÃO
            self.atualizar_visualizacao()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar planilha: {e}")

    def filtrar_planilha(self):
        if not hasattr(self.interface, 'eventos') or not self.interface.eventos:
            messagebox.showwarning("Aviso", "Carregue uma planilha primeiro!")
            return
        
        try:
            eventos_antes = len(self.interface.eventos)
            self.interface.filtra_evento()
            eventos_depois = len(self.interface.eventos)
            
            self.status_var.set(f"Planilha filtrada - {eventos_depois} eventos")
            self.atualizar_info(
                f"Filtro aplicado com sucesso!\n\n"
                f"Eventos antes do filtro: {eventos_antes}\n"
                f"Eventos depois do filtro: {eventos_depois}\n"
                f"Eventos removidos: {eventos_antes - eventos_depois}"
            )
            self.atualizar_combo_eventos()
            
            # ATUALIZAÇÃO AUTOMÁTICA DA VISUALIZAÇÃO (já estava aqui)
            self.atualizar_visualizacao()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao filtrar: {e}")

    # REMOVER a função treeview_sort_column se não for mais necessária?
    # Ou manter para a funcionalidade de ordenação por clique no cabeçalho

    
    def atualizar_info(self, mensagem):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, mensagem)
        self.info_text.config(state=tk.DISABLED)
    
    def atualizar_combo_eventos(self):
        if hasattr(self.interface, 'eventos') and self.interface.eventos:
            eventos_lista = [f"{i+1}. {evento.data} - {evento.bairro} - {evento.endereco}" 
                           for i, evento in enumerate(self.interface.eventos)]
            self.combo_eventos['values'] = eventos_lista
            if eventos_lista:
                self.combo_eventos.set(eventos_lista[0])
        else:
            self.combo_eventos.set('')
            self.combo_eventos['values'] = []
    
    def gerar_email(self):
        if not hasattr(self.interface, 'eventos') or not self.interface.eventos:
            messagebox.showwarning("Aviso", "Não há eventos para gerar e-mail!")
            return
        
        selecionado = self.combo_eventos.current()
        if selecionado == -1:
            messagebox.showwarning("Aviso", "Selecione um evento!")
            return
        
        evento = self.interface.eventos[selecionado]
        
        assunto = evento.gerar_assunto_email()
        corpo = evento.gerar_corpo_email()
        
        email_completo = f"ASSUNTO: {assunto}\n\n{corpo}"
        
        self.email_text.delete(1.0, tk.END)
        self.email_text.insert(tk.END, email_completo)
        
        # Opção para copiar
        copiar = messagebox.askyesno("Copiar E-mail", "Deseja copiar o e-mail para a área de transferência?")
        if copiar:
            try:
                import pyperclip
                pyperclip.copy(email_completo)
                messagebox.showinfo("Sucesso", "E-mail copiado para a área de transferência!")
            except ImportError:
                messagebox.showwarning("Aviso", "Biblioteca pyperclip não instalada. Instale com: pip install pyperclip")
    
    def adicionar_whitelist(self):
        poste = self.entry_whitelist.get().strip()
        if len(poste) == 10 and poste.isdigit():
            try:
                self.interface.add_whitelist(poste)
                self.atualizar_listas()
                self.entry_whitelist.delete(0, tk.END)
                messagebox.showinfo("Sucesso", f"Poste {poste} adicionado à Whitelist!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar poste: {e}")
        else:
            messagebox.showwarning("Aviso", "Código inválido! Deve conter exatamente 10 dígitos.")
    
    def remover_whitelist(self):
        selecionado = self.whitelist_listbox.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um poste para remover!")
            return
        
        poste = self.whitelist_listbox.get(selecionado[0])
        try:
            self.interface.remove_whitelist(poste)
            self.atualizar_listas()
            messagebox.showinfo("Sucesso", f"Poste {poste} removido da Whitelist!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover poste: {e}")
    
    def adicionar_blacklist(self):
        bairro = self.entry_blacklist.get().strip().upper()
        if bairro:
            try:
                self.interface.add_blacklist(bairro)
                self.atualizar_listas()
                self.entry_blacklist.delete(0, tk.END)
                messagebox.showinfo("Sucesso", f"Bairro {bairro} adicionado à Blacklist!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar bairro: {e}")
        else:
            messagebox.showwarning("Aviso", "Digite um nome de bairro!")
    
    def remover_blacklist(self):
        selecionado = self.blacklist_listbox.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um bairro para remover!")
            return
        
        bairro = self.blacklist_listbox.get(selecionado[0])
        try:
            self.interface.remove_blacklist(bairro)
            self.atualizar_listas()
            messagebox.showinfo("Sucesso", f"Bairro {bairro} removido da Blacklist!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover bairro: {e}")
    
    def atualizar_listas(self):
        # Atualizar whitelist
        self.whitelist_listbox.delete(0, tk.END)
        for poste in self.interface.whitelist:
            self.whitelist_listbox.insert(tk.END, poste)
        
        # Atualizar blacklist
        self.blacklist_listbox.delete(0, tk.END)
        for bairro in self.interface.blacklist:
            self.blacklist_listbox.insert(tk.END, bairro)
    
    

def main():
    root = tk.Tk()
    app = SistemaEventosGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()