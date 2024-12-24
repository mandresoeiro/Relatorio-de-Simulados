import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
from tkinter import filedialog

class CadastroAlunos:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Alunos")
        
        self.conn = sqlite3.connect('alunos.db')
        self.cursor = self.conn.cursor()

        self.criar_tabela()

        self.criar_widgets()

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY,
                codigo TEXT,
                nome TEXT,
                simulado TEXT,
                periodo TEXT,
                linguagem TEXT,
                acertos INTEGER,
                aproveitamento REAL,
                participantes INTEGER,
                notas TEXT,
                imagem BLOB
            )
        ''')
        self.conn.commit()

    def inserir_aluno(self):
        codigo = self.entry_codigo.get()
        nome = self.entry_nome.get()
        simulado = self.entry_simulado.get()
        periodo = self.entry_periodo.get()
        linguagem = self.entry_linguagem.get()
        acertos = self.entry_acertos.get()
        aproveitamento = self.entry_aproveitamento.get()
        participantes = self.entry_participantes.get()
        notas = self.entry_notas.get()
        imagem = self.imagem_bytes if self.imagem_bytes else None

        self.cursor.execute('''
            INSERT INTO alunos (codigo, nome, simulado, periodo, linguagem, acertos, aproveitamento, participantes, notas, imagem)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (codigo, nome, simulado, periodo, linguagem, acertos, aproveitamento, participantes, notas, imagem))
        self.conn.commit()
        messagebox.showinfo('Sucesso', 'Aluno cadastrado com sucesso.')
        self.limpar_campos()
        self.exibir_alunos()

    def limpar_campos(self):
        self.entry_codigo.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_simulado.delete(0, tk.END)
        self.entry_periodo.delete(0, tk.END)
        self.entry_linguagem.delete(0, tk.END)
        self.entry_acertos.delete(0, tk.END)
        self.entry_aproveitamento.delete(0, tk.END)
        self.entry_participantes.delete(0, tk.END)
        self.entry_notas.delete(0, tk.END)
        self.label_imagem.config(image=None)
        self.imagem_bytes = None

    def buscar_aluno(self):
        codigo = self.entry_codigo.get()
        self.cursor.execute('SELECT * FROM alunos WHERE codigo = ?', (codigo,))
        aluno = self.cursor.fetchone()
        if aluno:
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, aluno[2])
            self.entry_simulado.delete(0, tk.END)
            self.entry_simulado.insert(0, aluno[3])
            self.entry_periodo.delete(0, tk.END)
            self.entry_periodo.insert(0, aluno[4])
            self.entry_linguagem.delete(0, tk.END)
            self.entry_linguagem.insert(0, aluno[5])
            self.entry_acertos.delete(0, tk.END)
            self.entry_acertos.insert(0, aluno[6])
            self.entry_aproveitamento.delete(0, tk.END)
            self.entry_aproveitamento.insert(0, aluno[7])
            self.entry_participantes.delete(0, tk.END)
            self.entry_participantes.insert(0, aluno[8])
            self.entry_notas.delete(0, tk.END)
            self.entry_notas.insert(0, aluno[9])
            if aluno[10]:
                image = Image.open(BytesIO(aluno[10]))
                image = image.resize((100, 100), Image.ANTIALIAS)
                imagem_tk = ImageTk.PhotoImage(image)
                self.label_imagem.config(image=imagem_tk)
                self.label_imagem.image = imagem_tk
            else:
                self.label_imagem.config(image=None)
                self.label_imagem.image = None
        else:
            messagebox.showwarning('Aviso', 'Aluno não encontrado.')

    def exibir_alunos(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        self.cursor.execute('SELECT * FROM alunos')
        alunos = self.cursor.fetchall()

        for aluno in alunos:
            self.treeview.insert('', 'end', values=aluno[1:])

    def abrir_imagem(self):
        filepath = filedialog.askopenfilename(title="Selecionar Imagem", filetypes=(("Arquivos de Imagem", "*.png *.jpg *.jpeg"),))
        if filepath:
            image = Image.open(filepath)
            image = image.resize((100, 100), Image.ANTIALIAS)
            imagem_tk = ImageTk.PhotoImage(image)
            self.label_imagem.config(image=imagem_tk)
            self.label_imagem.image = imagem_tk

            with open(filepath, 'rb') as f:
                self.imagem_bytes = f.read()

    def criar_widgets(self):
        frame_formulario = ttk.Frame(self.root)
        frame_formulario.pack(padx=10, pady=10)

        label_codigo = ttk.Label(frame_formulario, text='Código:')
        label_codigo.grid(row=0, column=0, padx=5, pady=5)
        self.entry_codigo = ttk.Entry(frame_formulario)
        self.entry_codigo.grid(row=0, column=1, padx=5, pady=5)

        label_nome = ttk.Label(frame_formulario, text='Nome:')
        label_nome.grid(row=1, column=0, padx=5, pady=5)
        self.entry_nome = ttk.Entry(frame_formulario)
        self.entry_nome.grid(row=1, column=1, padx=5, pady=5)

        label_simulado = ttk.Label(frame_formulario, text='Simulado:')
        label_simulado.grid(row=2, column=0, padx=5, pady=5)
        self.entry_simulado = ttk.Entry(frame_formulario)
        self.entry_simulado.grid(row=2, column=1, padx=5, pady=5)

        label_periodo = ttk.Label(frame_formulario, text='Período:')
        label_periodo.grid(row=3, column=0, padx=5, pady=5)
        self.entry_periodo = ttk.Entry(frame_formulario)
        self.entry_periodo.grid(row=3, column=1, padx=5, pady=5)

        label_linguagem = ttk.Label(frame_formulario, text='Linguagem:')
        label_linguagem.grid(row=4, column=0, padx=5, pady=5)
        self.entry_linguagem = ttk.Entry(frame_formulario)
        self.entry_linguagem.grid(row=4, column=1, padx=5, pady=5)

        label_acertos = ttk.Label(frame_formulario, text='Acertos:')
        label_acertos.grid(row=5, column=0, padx=5, pady=5)
        self.entry_acertos = ttk.Entry(frame_formulario)
        self.entry_acertos.grid(row=5, column=1, padx=5, pady=5)

        label_aproveitamento = ttk.Label(frame_formulario, text='Aproveitamento:')
        label_aproveitamento.grid(row=6, column=0, padx=5, pady=5)
        self.entry_aproveitamento = ttk.Entry(frame_formulario)
        self.entry_aproveitamento.grid(row=6, column=1, padx=5, pady=5)

        label_participantes = ttk.Label(frame_formulario, text='Participantes:')
        label_participantes.grid(row=7, column=0, padx=5, pady=5)
        self.entry_participantes = ttk.Entry(frame_formulario)
        self.entry_participantes.grid(row=7, column=1, padx=5, pady=5)

        label_notas = ttk.Label(frame_formulario, text='Notas:')
        label_notas.grid(row=8, column=0, padx=5, pady=5)
        self.entry_notas = ttk.Entry(frame_formulario)
        self.entry_notas.grid(row=8, column=1, padx=5, pady=5)

        button_imagem = ttk.Button(frame_formulario, text='Selecionar Imagem', command=self.abrir_imagem)
        button_imagem.grid(row=9, column=0, columnspan=2, pady=10)

        self.label_imagem = ttk.Label(frame_formulario)
        self.label_imagem.grid(row=0, column=2, rowspan=9, padx=10)

        frame_botoes = ttk.Frame(self.root)
        frame_botoes.pack(padx=10, pady=5)

        button_novo = ttk.Button(frame_botoes, text='Novo', command=self.limpar_campos)
        button_novo.grid(row=0, column=0, padx=5)

        button_buscar = ttk.Button(frame_botoes, text='Buscar', command=self.buscar_aluno)
        button_buscar.grid(row=0, column=1, padx=5)

        button_inserir = ttk.Button(frame_botoes, text='Inserir', command=self.inserir_aluno)
        button_inserir.grid(row=0, column=2, padx=5)

        self.treeview = ttk.Treeview(self.root, columns=('Código', 'Nome', 'Simulado', 'Período', 'Linguagem', 'Acertos', 'Aproveitamento', 'Participantes', 'Notas'))
        self.treeview.pack(padx=10, pady=10)

        self.treeview.heading('#0', text='ID')
        self.treeview.column('#0', width=50)
        for col in self.treeview['columns']:
            self.treeview.heading(col, text=col)

        self.exibir_alunos()

root = tk.Tk()
app = CadastroAlunos(root)
root.mainloop()
