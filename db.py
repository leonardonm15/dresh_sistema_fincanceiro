from supabase import *

db_key = 'tira o olho safado'
db_url = 'https://vmvvijlxqaqnjbnvpxrc.supabase.co'
supabase = create_client(db_url, db_key)


def get_gastos():
    gastos = supabase.table('gastos').select('*').order('id').execute()
    gastos = dict(gastos.dict())['data'][::-1]
    return gastos


gastos_insert = supabase.table('gastos')


def get_gastos_vendedor():
    gastos_vendedor = supabase.table('gastos_vendedor').select('*').order('id').execute()
    gastos_vendedor = dict(gastos_vendedor.dict())['data'][::-1]
    return gastos_vendedor


gastos_vendedor_insert = supabase.table('gastos_vendedor')


def get_ganhos():
    ganhos = supabase.table('ganhos').select('*').order('id').execute()
    ganhos = dict(ganhos.dict())['data'][::-1]
    return ganhos


ganhos_insert = supabase.table('ganhos')

datas = supabase.table('ganhos').select('created_at').order('id').execute()
datas = dict(datas.dict())['data']

def get_all():
    get_ganhos()
    get_gastos()
    get_gastos_vendedor()

# mes das oerações no banco de dados
def mes():
    lista_datas = []
    for dicionario in datas:
        for data in dicionario.values():
            lista_datas.insert(0, data[0:7])
    return lista_datas


# soma dos valores de uma table
def soma_geral(table):
    total_de_gastos = []
    for dicionario in table:
        soma = 0
        for numero in dicionario.values():
            if numero == dicionario['id'] or numero == dicionario['created_at'] or str(numero).replace('.',
                                                                                                       '').isnumeric() == False:
                continue
            soma += int(numero)
        total_de_gastos.append(soma)
    return total_de_gastos


def lucro():
    valores = zip(soma_geral(get_ganhos()), soma_geral(get_gastos()), soma_geral(get_gastos_vendedor()))
    lista_lucros = []
    for tupla in valores:
        lista_lucros.append(round(tupla[0] - (tupla[1] + tupla[2]), 2))
    return lista_lucros


def insert(table, table_insert, data):
    hash_table = {}
    for head in table[0].keys():
        hash_table[head] = data[list(table[0].keys()).index(head)]
    table_insert.insert(hash_table).execute()
    print('''
       ------QUERY EXECUTADA COM SUCESSO INSERÇÃO------
    ''')


def edit(table, table_edit, data):
    hash_table = {} # recebe a row que vai ser trocada
    for head in table[0].keys():
        hash_table[head] = data[list(table[0].keys()).index(head)]
    table_edit.update(hash_table).eq('id', data[0]).execute()
    print(f'''
       ------QUERY EXECUTADA COM SUCESSO EDIÇÃO table = {table[0].keys()}-----
    ''')


def delete(table_edit, data):
    table_edit.delete().eq('id', data[0]).execute()
    print(f'''
        ------QUERY EXECUTADA COM SUCESSO REMOÇÃO {data[0]}-----
    ''')



print(f"""
    mes =>             {mes()}
    gastos =>          {soma_geral(get_gastos())}
    gastos_vendedor => {soma_geral(get_gastos_vendedor())}
    ganhos ->          {soma_geral(get_ganhos())}
    lucro ->           {lucro()}
""")
