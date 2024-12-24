from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
from tkinter import filedialog 

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser
from PIL import ImageTk , Image
import base64

# importando pillow
from PIL import ImageTk, Image


root = Tk()

class Relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf")
    def geraRelatCliente(self):
        self.c = canvas.Canvas("cliente.pdf")

        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.turmaRel = self.turma_entry.get()
        self.simuladoRel = self.simulado_entry.get()
        self.periodoRel = self.periodo_entry.get()
        self.leRel = self.le_entry.get()
        self.acertosRel = self.acertos_entry.get()
        self.aproveitamentoRel = self.aproveitamento_entry.get()
        self.participantesRel = self.participantes_entry.get()
        self.notaRel = self.nota_entry.get()

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(200, 690, 'Ficha do Cliente')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'Codigo: ')
        self.c.drawString(50, 630, 'Nome: ')
        self.c.drawString(50, 630, 'Turma: ')
        self.c.drawString(50, 630, 'Simulado: ')
        # self.c.drawString(50, 200, 'Periodo: ')
        # self.c.drawString(50, 200, 'Linguagem: ')
        # self.c.drawString(50, 200, 'Acertos: ')
        # self.c.drawString(50, 200, 'Aproveitamento: ')
        # self.c.drawString(50, 200, 'Participantes: ')
        # self.c.drawString(50, 200, 'Notas: ')

        self.c.setFont("Helvetica", 18)
        self.c.drawString(150, 700, self.codigoRel)
        self.c.drawString(150, 670, self.nomeRel)
        self.c.drawString(150, 630, self.turmaRel)
        self.c.drawString(150, 600, self.simuladoRel)
        # self.c.drawString(150, 600, self.periodoRel)
        # self.c.drawString(150, 600, self.leRel)
        # self.c.drawString(150, 600, self.acertosRel)
        # self.c.drawString(150, 600, self.aproveitamentoRel)
        # self.c.drawString(150, 600, self.participantesRel)
        # self.c.drawString(150, 600, self.notaRel)
        

        # self.c.rect(20, 720, 550, 200, fill= False, stroke=True)

        self.c.showPage()
        self.c.save()
        self.printCliente()

class Funcs():      #FUNÇÕES DO BACKEND
    def limpa_cliente(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.turma_entry.delete(0, END)
        self.simulado_entry.delete(0, END)
        self.periodo_entry.delete(0, END)
        self.le_entry.delete(0, END)
        self.acertos_entry.delete(0, END)
        self.aproveitamento_entry.delete(0, END)
        self.participantes_entry.delete(0, END)
        self.nota_entry.delete(0, END)
    def conecta_bd(self):  #Conectar o banco
        self.conn = sqlite3.connect("clientes.db")
        self.cursor = self.conn.cursor();print("Conectando ao banco de dados")
    def desconecta_bd(self):
        self.conn.close(); print("Desconectando ao banco de dados")
    def montaTabelas(self):
        self.conecta_bd()
        ### Criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                turma INTEGER(20)NOT NULL,
                simulado TEXTO(40)NOT NULL,
                periodo CHAR(20) NOT NULL,               
                le CHAR(40) NOT NULL,              
                acertos CHAR(20) NOT NULL,              
                aproveitamento CHAR(20) NOT NULL,               
                participantes CHAR(20)  NOT NULL,              
                nota CHAR(20),
                imagem BLOB           
            );
        """)
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd()
        
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome =  self.nome_entry.get()
        self.turma = self.turma_entry.get()
        self.simulado = self.simulado_entry.get()
        self.periodo = self.periodo_entry.get()
        self.le = self.le_entry.get()
        self.acertos = self.acertos_entry.get()
        self.aproveitamento = self.aproveitamento_entry.get()
        self.participantes = self.participantes_entry.get()
        self.nota = self.nota_entry.get()
        # self.label_imagem.config(image=None)
        # self.imagem_bytes = None
    def OnDoubleClick(self, event):  # Duplo Click
        self.limpa_cliente()

        for n in self.listaCli.selection():
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, = self.listaCli.item(n, 'values')
            
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.turma_entry.insert(END, col3)
            self.simulado_entry.insert(END, col4) 
            self.periodo_entry.insert(END, col5) 
            self.le_entry.insert(END, col6) 
            self.acertos_entry.insert(END, col7) 
            self.aproveitamento_entry.insert(END, col8) 
            self.participantes_entry.insert(END, col9) 
            self.nota_entry.insert(END, col10) 
        
    def add_cliente(self):
        self.variaveis()
        self.conecta_bd()
        
        self.cursor.execute(""" INSERT INTO clientes (nome_cliente, turma, simulado, periodo, le, acertos, aproveitamento, participantes, nota)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (self.nome, self.turma, self.simulado, self.periodo, self.le, self.acertos, self.aproveitamento, self.participantes, self.nota))
        messagebox.showinfo('Sucesso', 'Aluno cadastrado com sucesso.')
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_cliente()
    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, turma = ?, simulado = ?, periodo = ?, le = ?, acertos = ?, aproveitamento = ?, participantes = ?, nota = ?
            WHERE cod = ? """,
                            (self.nome, self.turma, self.simulado, self.periodo, self.le, self.acertos, self.aproveitamento, self.participantes, self.nota, self.codigo))
        self.conn.commit()
        self.desconecta_bd()            
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_cliente()
        self.select_lista()
    
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, turma, simulado, periodo, le, acertos, aproveitamento, participantes, nota FROM clientes
            ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()
    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(
            """ SELECT cod, nome_cliente, turma, simulado, periodo, le, acertos, aproveitamento, participantes, nota  FROM clientes
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % nome)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("", END, values=i)
        self.limpa_cliente()
        self.desconecta_bd()
    
       
class Application(Funcs, Relatorios):   #FUNÇÕES DO FRONTEND
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.Menus()
        root.mainloop()
    def tela(self):
        self.root.title("Cadastro de Alunos")
        self.root.configure(background= '#164074')
        self.root.geometry("1250x650")
        self.root.resizable(True, True) # Tela responsiva
        self.root.maxsize(width=1300, height=700)
        self.root.minsize(width=1100, height=600)
    def frames_da_tela(self):
        
    
     
    # FRAME DE CABEÇALHO
               
        # self.frame_logo = Frame(self.root, bd=4, bg= '#dfe3ee'
        #                      , highlightbackground= '#759fe6', highlightthickness=2)
        # self.frame_logo.place(relx=0.01, rely=0.1, relwidth=0.20, relheight=0.25)
        
        self.frame_imagem = Frame(self.root, bd=4, bg= '#dfe3ee'
                             , highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_imagem.place(relx=0.01, rely=0.45, relwidth=0.22, relheight=0.35)
        
        
        self.frame_1 = Frame(self.root, bd=4, bg= '#dfe3ee'
                             , highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_1.place(relx=0.25, rely=0.02, relwidth=0.74, relheight=0.55)
        
        self.frame_2 = Frame(self.root, bd=4, bg= '#dfe3ee'
                             , highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_2.place(relx=0.25, rely=0.60, relwidth=0.74, relheight=0.38)
                   
        self.frame_3 = Frame(self.root, bd=4, bg= '#dfe3ee'
                             , highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_3.place(relx=0.01, rely=0.80, relwidth=0.22, relheight=0.15)
    
        # self.frame_5 = Frame(self.root)   
           
        # self.cabecalho = Label(self.frame_5, text ='cadastro', bg='orange')
        # self.cabecalho.pack(fill=X)
        # self.frame_5.pack(anchor=W, pady=20, padx=20)
        # self.frame_5.pack_propagate(False)
        # self.frame_5.configure(width=280, height=50, bg='red')

        self.frame_4 = Frame(self.root)

        self.img_frame = Frame(self.frame_4)
        self.img_padrao = PhotoImage(file='logo2.png')
        self.img_label = Label(self.img_frame, image=self.img_padrao, bd=2, relief=SOLID)
        self.img_label.pack(side=LEFT)
        self.img_frame.pack(anchor=W, pady=50, padx=50)
        
        
        
        self.frame_4.pack(anchor=W, pady=50, padx=50)
        self.frame_4.pack_propagate(False)
        self.frame_4.configure(width=250, height=250, bg='green')
          
         
    def quadro_aluno(self):
       
        imagem  = Image.open('logo.png')
        imagem = imagem.resize((130, 130))
        imagem = ImageTk.PhotoImage(imagem)

        l_imagem = Label(self.frame_4, image=imagem,bg=co1, fg=co4)
        # l_imagem.place(x=50, y=10)
        l_imagem.grid(column=0, row=1, padx=0, pady=0, ipadx=0, ipady=0, sticky='nsew', command=self.quadro_aluno)
            
        
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
                
       
        
    def widgets_frame1(self):
        ###Criação do botao limpar
        self.bt_limpar = Button(self.frame_1, text= "Limpar", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command=self.limpa_cliente)
        self.bt_limpar.place(relx= 0.3, rely=0.03, relwidth=0.1, relheight= 0.10)
        
        ### Criação do botao buscar
        self.bt_buscar = Button(self.frame_1, text="Buscar", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command=self.busca_cliente)
        self.bt_buscar.place(relx=0.4, rely=0.03, relwidth=0.1, relheight=0.10)
        
        ### Criação do botao novo    
        self.bt_novo = Button(self.frame_1, text="Novo", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'),command= self.add_cliente)
        self.bt_novo.place(relx=0.6, rely=0.03, relwidth=0.1, relheight=0.10)
        
        ### Criação do botao alterar
        self.bt_alterar = Button(self.frame_1,  text="Alterar", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command=self.altera_cliente)
        self.bt_alterar.place(relx=0.7, rely=0.03, relwidth=0.1, relheight=0.10)
        
        ### Criação do botao apagar       
        self.bt_apagar = Button(self.frame_1, text="Apagar", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'),command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.8, rely=0.03, relwidth=0.1, relheight=0.10)
        
        ### BOTÃO IMAGEM
        self.bt_imagem = Button(self.frame_imagem,text='Selecionar Imagem', command=self.abrir_imagem)
        self.bt_imagem.place(relx=0.2, rely=0.70, relwidth=0.50, relheight=0.10)

         
## Criação da label e entrada do codigo
        
        self.lb_codigo = Label(self.frame_1, text="Código", font=('Arial', '10', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_codigo.place(relx=0.04, rely=0.02)
        
        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.04, rely=0.09, relwidth=0.10, relheight=0.08)
    
    ## Criação da label e entrada do Nome
        self.lb_nome = Label(self.frame_1, text='Nome Completo', font=('Arial', '10', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_nome.place(relx=0.01, rely=0.20, relwidth=0.2, relheight=0.10)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.04, rely=0.28, relwidth=0.64, relheight=0.10)   
        
        ### Criação da label e entry TURMA
        self.lb_turma = Label(self.frame_1, text='Turma', font=('Arial', '10', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_turma.place(relx=0.7, rely=0.20, relwidth=0.1, relheight=0.10)
        
        self.turma_entry = Entry(self.frame_1)
        self.turma_entry.place(relx=0.7, rely=0.28, relwidth=0.25, relheight=0.10)     
        
        ### Criação da label e entry Simulado
        self.lb_simulado = Label(self.frame_1, text='Simulado', font=('Arial', '10', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_simulado.place(relx=0.03, rely=0.40, relwidth=0.1, relheight=0.10)
     
        self.simulado_entry = Entry(self.frame_1)
        self.simulado_entry.place(relx=0.04, rely=0.48, relwidth=0.45, relheight=0.10)
        
        ### Criação da label e entry Período
        self.lb_periodo = Label(self.frame_1, text='Período', font=('Arial', '10', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_periodo.place(relx=0.5, rely=0.40, relwidth=0.1, relheight=0.10)

        self.periodo_entry = Entry(self.frame_1)
        self.periodo_entry.place(relx=0.5, rely=0.48, relwidth=0.18, relheight=0.10)
        
    ### Criação da label e entry Linguagem          
        self.lb_le = Label(self.frame_1, text='Linguagem', font=('Arial', '10', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_le.place(relx=0.7, rely=0.40, relwidth=0.1, relheight=0.10)

        self.le_entry = Entry(self.frame_1)
        self.le_entry.place(relx=0.7, rely=0.48, relwidth=0.25, relheight=0.10)
        
        ### Criação da label e entry Acertos
        self.lb_acertos = Label(self.frame_1, text='Acertos', font=('Arial', '10', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_acertos.place(relx=0.01, rely=0.60, relwidth=0.12, relheight=0.10)
        
        self.acertos_entry = Entry(self.frame_1)
        self.acertos_entry.place(relx=0.04, rely=0.70, relwidth=0.10, relheight=0.10)
    
        ### Criação da label e entry Aproveitamento
        self.lb_aproveitamento = Label(self.frame_1, text='Aproveitamento', font=('Arial', '10', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_aproveitamento.place(relx=0.10, rely=0.60, relwidth=0.25, relheight=0.10)
        
        self.aproveitamento_entry = Entry(self.frame_1)
        self.aproveitamento_entry.place(relx=0.15, rely=0.70, relwidth=0.16, relheight=0.10)
    
        ### Criação da label e entry Participantes
        self.lb_participantes = Label(self.frame_1, text='Participantes', font=('Arial', '10', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_participantes.place(relx=0.29, rely=0.60, relwidth=0.2, relheight=0.10)
        
        self.participantes_entry = Entry(self.frame_1)
        self.participantes_entry.place(relx=0.33, rely=0.70, relwidth=0.17, relheight=0.10)
     
        ### Criação da label e entry Notas
        self.lb_nota = Label(self.frame_1, text='Notas', font=('Arial', '10', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_nota.place(relx=0.44, rely=0.60, relwidth=0.2, relheight=0.10)
        
        self.nota_entry = Entry(self.frame_1)
        self.nota_entry.place(relx=0.52, rely=0.70, relwidth=0.17, relheight=0.10)
        
               
        
    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3,
                                     column=("col1", "col2", "col3", "col4", 'col5','col6','col7', 'col8','col9', 'col10'))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Codigo")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="Turma")
        self.listaCli.heading("#4", text="Simulado")
        self.listaCli.heading("#5", text="Periodo")
        self.listaCli.heading("#6", text="LE")
        self.listaCli.heading("#7", text="Acertos")
        self.listaCli.heading("#8", text="Aproveitamento")
        self.listaCli.heading("#9", text="Participantes")
        self.listaCli.heading("#10", text="Nota")
        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=3)
        self.listaCli.column("#2", width=140)
        self.listaCli.column("#3", width=30)
        self.listaCli.column("#4", width=30)
        self.listaCli.column("#5", width=30)
        self.listaCli.column("#6", width=20)
        self.listaCli.column("#7", width=20)
        self.listaCli.column("#8", width=20)
        self.listaCli.column("#9", width=30)
        self.listaCli.column("#10", width=30)
        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)
        
        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.95, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)
    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label= "Opções", menu=filemenu)
        menubar.add_cascade(label="Relatorios", menu=filemenu2)

        filemenu.add_command(label="Sair", command=Quit)
        filemenu.add_command(label="Limpa cliente", command= self.limpa_cliente)

        filemenu2.add_command(label="Ficha do cliente", command=self.geraRelatCliente)

Application()