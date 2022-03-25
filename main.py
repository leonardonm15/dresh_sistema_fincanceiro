import tkinter
from tkinter import *
from tkinter import ttk
import db
import matplotlib.pyplot as plt
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()

        # configurando a janela inicial
        self.title('Dresh')
        self.geometry('1200x700')
        self.configure(bg='#383333')
        self.resizable(False, False)

        self.state = True  # controla o estado do switch
        self.current_page = None  # controla em que table da db o usuario esta
        self.page_insert = None  # controla a table.insert

        # imagens do switch
        self.left_switch = PhotoImage(file=f'switch_left.png')
        self.right_switch = PhotoImage(file=f'switch_right.png')

        # declaraçãodo canvas principal do app
        self.canvas = Canvas(
            bg="#383333",
            height=700,
            width=1200,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        # coloca o ackgroud no canvas
        self.background_img = PhotoImage(file=f"background.png")
        self.background = self.canvas.create_image(
            163.0, 519.5,
            image=self.background_img)

        # cria um frame, cria scrollbars para os eixos x e y, cria uma planilha e acopla os scrolls
        self.frame = Frame()
        self.game_scroll = Scrollbar(self.frame)

        self.game_scroll.pack(side=RIGHT, fill=Y)
        self.game_scroll = Scrollbar(self.frame, orient='horizontal')

        self.game_scroll.pack(side=BOTTOM, fill=X)

        self.planilha = ttk.Treeview(self.frame, yscrollcommand=self.game_scroll.set,
                                     xscrollcommand=self.game_scroll.set)

        self.game_scroll.config(command=self.planilha.yview)

        self.game_scroll.config(command=self.planilha.xview)

        # cria a box das entrys e o scroll dela
        self.label_frame = LabelFrame()
        self.canvas_label = Canvas(self.label_frame)
        self.xscrollbar = Scrollbar(self.label_frame, orient='horizontal', command=self.canvas_label.xview)
        self.xscrollbar.pack(side=BOTTOM, fill=X)

        self.canvas_label.configure(xscrollcommand=self.xscrollbar.set)

        self.canvas_label.bind('<Configure>',
                               lambda e: self.canvas_label.configure(scrollregion=self.canvas_label.bbox('all')))
        self.frame_canvas = Frame(self.canvas_label, padx=350)

        self.canvas_label.create_window((0, 0), window=self.frame_canvas)

        # dados para o grafico dos lucros da empresa
        self.data_frame = {
            'Mês': db.mes(),
            'Lucro': db.lucro()
        }

        self.data_frame2 = {'gastos': db.soma_geral(db.get_gastos()),
                            'vendedor': db.soma_geral(db.get_gastos_vendedor()),
                            'ganhos': db.soma_geral(db.get_ganhos())
        }

        # configuração do grafico
        self.frame_graph = Frame()
        self.df = DataFrame(self.data_frame, columns=['Mês', 'Lucro'])

        figure = plt.Figure(figsize=(7, 4), dpi=100)
        ax = figure.add_subplot(111)
        ax.margins(y=.1, x=.1)
        self.graph = FigureCanvasTkAgg(figure, self.frame_graph)
        self.graph = self.graph.get_tk_widget()
        self.df = self.df[['Mês', 'Lucro']].groupby('Mês').sum()
        self.df.plot(kind='line', legend=True, ax=ax, color='r', marker='o', fontsize=10)
        ax.set_title('Meses X Lucro')

        # planilha dos lucros da empresa
        self.frame_resumo = Frame(height=100, width=100)
        self.game_scroll_resumo = Scrollbar(self.frame_resumo, orient='vertical')
        self.game_scroll_resumo.pack(side=RIGHT, fill=Y)

        self.planilha_resumo = ttk.Treeview(self.frame_resumo, yscrollcommand=self.game_scroll_resumo.set)

        self.planilha_resumo['columns'] = ['mês', 'lucro', 'taxa']

        self.planilha_resumo.column('#0', width=0, stretch=NO)
        self.planilha_resumo.column('mês', anchor=CENTER, width=50)
        self.planilha_resumo.column('lucro', anchor=CENTER, width=50)
        self.planilha_resumo.column('taxa', anchor=CENTER, width=50)

        self.planilha_resumo.heading('#0', text='', anchor=CENTER)
        self.planilha_resumo.heading('mês', text='mês', anchor=CENTER)
        self.planilha_resumo.heading('lucro', text='lucro', anchor=CENTER)
        self.planilha_resumo.heading('taxa', text='taxa', anchor=CENTER)

        #planilha somas
        self.frame_resumo_somas = Frame()
        self.game_scroll_resumo_somas = Scrollbar(self.frame_resumo_somas, orient='vertical')
        self.game_scroll_resumo.pack(side=RIGHT, fill=Y)

        self.planilha_resumo_somas = ttk.Treeview(self.frame_resumo_somas, yscrollcommand=self.game_scroll_resumo_somas.set)

        self.planilha_resumo_somas['columns'] = ['gastos', 'gastos_vendedor', 'ganhos']

        self.planilha_resumo_somas.column('#0', width=0, stretch=NO)
        self.planilha_resumo_somas.column('gastos', anchor=CENTER, width=60)
        self.planilha_resumo_somas.column('gastos_vendedor', anchor=CENTER, width=60)
        self.planilha_resumo_somas.column('ganhos', anchor=CENTER, width=60)

        self.planilha_resumo_somas.heading('#0', text='', anchor=CENTER)
        self.planilha_resumo_somas.heading('gastos', text='gastos', anchor=CENTER)
        self.planilha_resumo_somas.heading('gastos_vendedor', text='vendedor', anchor=CENTER)
        self.planilha_resumo_somas.heading('ganhos', text='ganhos', anchor=CENTER)

        # declara os botoes que vao ser controlados pelo switch
        self.editar = Button(self.canvas,
                             text='EDITAR',
                             font=('VollKorn', 15),
                             background="#717171",
                             fg='black',
                             command=lambda: self.edit_db(self.current_page, self.page_insert,
                                                          self.get_entrys_values_list()))

        self.inserir = Button(self.canvas,
                              text='INSERIR',
                              font=('VollKorn', 15),
                              background="#717171",
                              fg='black',
                              state=DISABLED,
                              command=lambda: self.insert_db(self.current_page, self.page_insert,
                                                             self.get_entrys_values_list()))

        # declara o switch
        self.switch = Button(image=self.left_switch,
                             bd=0,
                             command=self.change_state,
                             background="#383333",
                             highlightcolor="#383333",
                             activebackground="#383333")

        self.delete = Button(
            self.canvas,
            text='DELETE',
            font=('Vollkorn', 10),
            background='#717171',
            fg='black',
            command=lambda: self.row_delete()

        )

        # declara o double click como um evento da planilha
        self.planilha.bind('<Double-1>', self.doubleclick)

        # coonfgura os botoes principais do menu
        self.img_ganhos = PhotoImage(file=f"ganhos.png")  # GANHOS
        self.b0 = Button(
            image=self.img_ganhos,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.config_scr(db.get_ganhos(), db.ganhos_insert),
            relief="flat")

        self.b0.place(
            x=15, y=255,
            width=296,
            height=119)

        self.img_gastos = PhotoImage(file=f"gastos.png")  # GASTOS
        self.b1 = Button(
            image=self.img_gastos,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.config_scr(db.get_gastos(), db.gastos_insert),
            relief="flat")

        self.b1.place(
            x=15, y=109,
            width=296,
            height=119)

        self.img_vendedor = PhotoImage(file=f"vendedor.png")  # VENDEDOR
        self.b2 = Button(
            image=self.img_vendedor,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.config_scr(db.get_gastos_vendedor(), db.gastos_vendedor_insert),
            relief="flat")

        self.b2.place(
            x=15, y=406,
            width=296,
            height=124)

        self.img_resumo = PhotoImage(file=f"resumo.png")  # RESUMO
        self.b3 = Button(
            image=self.img_resumo,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.resumo_scr(),
            bd=0,
            relief="flat")

        self.b3.place(
            x=15, y=557,
            width=296,
            height=119)

    # muda o estado do botao para Frue ou False
    def change_state(self):
        if self.state:
            self.state = False
            self.switch.config(image=self.right_switch)
            self.editar.config(state=DISABLED)
            self.inserir.config(state=NORMAL)
            self.change_entrys([value.replace('_', ' ') for value in self.planilha['columns']])
        else:
            self.state = True
            self.switch.config(image=self.left_switch)
            self.editar.config(state=NORMAL)
            self.inserir.config(state=DISABLED)
        return self.state

    # passa a row seleconada para as entrys
    def doubleclick(self, event):
        if self.state == True:
            self.selecionado = self.planilha.selection()
            self.selecionado = self.planilha.item(self.selecionado, 'values')
            self.change_entrys(self.selecionado)
        else:
            pass

    # muda o texto das entrys com base no parametro passado
    def change_entrys(self, data):
        if len(data) > 1:
            c = 0
            for _ in self.frame_canvas.winfo_children():
                v = StringVar(value=str(data[c]))
                _.configure(textvariable=v)
                c += 1

    # limpa o texto das entrys
    def clean_entrys(self):
        for _ in self.frame_canvas.winfo_children():
            v = StringVar(value='')
            _.configure(textvariable=v)

    # destroi as entrys para a criação de novas
    def destroy_entrys(self):
        for _ in self.frame_canvas.winfo_children():
            _.destroy()

    def clean_planilhas_resumos(self):
        for _ in self.planilha_resumo.get_children():
            self.planilha_resumo.delete(_)

        for _ in self.planilha_resumo_somas.get_children():
            self.planilha_resumo_somas.delete(_)

    # limpa a planilha
    def clean_planilha(self):
        for _ in self.planilha.get_children():
            self.planilha.delete(_)

    # pega o cabeçalho para colocar na planilha
    def get_headings_from_db(self, table):
        self.planilha['columns'] = [coluna for coluna in table[0].keys()]
        return self.planilha['columns']

    # insere o cabeçalho da planilha e passa para a entry
    def insert_headings(self, table):
        heads = self.get_headings_from_db(table)
        for name in heads:
            if name == heads[0].replace('_', ' '):
                self.planilha.column('#0', width=0, stretch=NO)
                self.planilha.heading('#0', text='', anchor=CENTER)
                pass
            v = StringVar(value=str(name).replace('_', ' '))
            self.planilha.column(name, anchor=CENTER, width=80, stretch=NO)
            self.planilha.heading(name, text=name, anchor=CENTER)
            Entry(self.frame_canvas, textvariable=v).grid(row=0, column=int(heads.index(name)))

    # coloca os titulos das colunas da planilha e da entry com base na db
    def get_entrys_values_list(self):
        entrys_list = []
        for value in self.frame_canvas.winfo_children():
            entrys_list.append(value.get())
        return entrys_list

    # coloca os valores na planilha
    def insert_values(self, table):
        for dicionario in table:
            self.planilha.insert(parent='', index='end', text='', values=([values for values in dicionario.values()]))

    # manda para o banco de dados a var data e atualiza a planilha
    def insert_db(self, table, table_insert, data):
        db.insert(table, table_insert, data)
        self.planilha.insert(parent='', index='end', text='', values=([values for values in data]))
        db.lucro()

    # edita o banco de dados com os novos valores da row
    def edit_db(self, table, table_insert, data):
        if self.planilha.focus():
            db.edit(table, table_insert, data)
            row = self.planilha.focus()
            self.planilha.item(row, text='', values=[values for values in self.get_entrys_values_list()])
            db.lucro()

    # deleta a row escolhida
    def row_delete(self):
        if self.planilha.selection():
            if len(self.planilha.get_children()) > 1:
                row = self.planilha.selection()
                row_values = self.planilha.item(row, 'values')
                db.delete(self.page_insert, row_values)
                self.planilha.delete(row)
            else:
                pass

    # função que configura a tela de resumo
    def resumo_scr(self):
        if self.current_page != 'resumo':
            self.widget_forget()
            self.current_page = 'resumo'
            self.frame_graph.pack(padx=(380, 20), pady=20)
            self.graph.pack()
            self.config_planilhas_resumo().pack()
            self.frame_resumo.pack(padx=0, pady=10)
            self.config_planilha_resumo_somas().pack()
            self.frame_resumo_somas.place(x=900, y=450)

    def config_planilha_resumo_somas(self):
        lista_ganhos = self.data_frame2['ganhos']
        lista_gastos = self.data_frame2['gastos']
        lista_gastos_vendedor = self.data_frame2['vendedor']
        for num in range(len(db.lucro())):
            self.planilha_resumo_somas.insert(parent='',
                                              index='end',
                                              text='',
                                              values=(lista_gastos[num],
                                                      lista_gastos_vendedor[num],
                                                      lista_ganhos[num]))
        return self.planilha_resumo_somas


    #configura as 2 planilhas da aba de resumo
    def config_planilhas_resumo(self):
        self.data_frame['Lucro'] = db.lucro()
        self.data_frame['Mês'] = db.mes()

        if len(self.data_frame['Mês']) > len(self.data_frame['Lucro']):
            self.data_frame['Lucro'].append(0)
        if len(self.data_frame['Mês']) < len(self.data_frame['Lucro']):
            if self.data_frame['Lucro'][::-1] == 0:
                self.data_frame['Lucro'].pop()

        lista_lucro = self.data_frame['Lucro']
        lista_mes = self.data_frame['Mês']
        for number in range(len(db.lucro())):
            if lista_lucro[number] > 0:
                taxa_lucro = lista_lucro[number] / 100 * 5
            else:
                taxa_lucro = 0
            self.planilha_resumo.insert(parent='',
                                        index='end',
                                        text='',
                                        values=(lista_mes[number],
                                                round(lista_lucro[number] - taxa_lucro, 2),
                                                round(taxa_lucro, 2)))
        return self.planilha_resumo

    # coloca os valores na planilha
    def config_scr(self, table, table_insert):
        if self.current_page == 'resumo':
            self.clean_planilhas_resumos()
            self.frame_graph.pack_forget()
            self.graph.pack_forget()
            self.planilha_resumo.pack_forget()
            self.frame_resumo.pack_forget()
            self.planilha_resumo_somas.pack_forget()
            self.frame_resumo_somas.place_forget()
        self.current_page = table
        self.page_insert = table_insert
        self.destroy_entrys()
        self.clean_planilha()
        self.insert_headings(table)
        self.insert_values(table)

        self.frame.pack(pady=20, padx=(380, 20), anchor=CENTER)
        self.planilha.pack()
        self.switch.place(y=275, x=725)
        self.inserir.place(y=310, x=835)
        self.editar.place(y=310.5, x=630)
        self.delete.place(y=270, x=1120)
        self.canvas_label.pack(fill='both', expand=True, side=LEFT)
        self.label_frame.pack(fill='both', expand=True, padx=(380, 20), pady=(100, 270))
        return self.current_page

    # tira da tela os widgets
    def widget_forget(self):
        self.frame.pack_forget()
        self.planilha.pack_forget()
        self.switch.place_forget()
        self.inserir.place_forget()
        self.editar.place_forget()
        self.delete.place_forget()
        self.canvas_label.pack_forget()
        self.label_frame.pack_forget()


if __name__ == '__main__':
    a = App()
    a.mainloop()
