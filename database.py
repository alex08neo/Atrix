import sys
import psycopg2
import os

# Inicialização de parâmetros
database = os.environ['DATABASE_URL']

# Cria um banco de dados Postgres para armazenar informações, caso não exista.
def carregarBD():
    # Conecta ao banco de dados na URL especificada
    connection = psycopg2.connect(database)
    # Cria um cursor do banco de dados, que é um iterador que permite navegar
    # e manipular os registros do bd, e o atribui a uma variável.
    cursor = connection.cursor()
    # Carrega os comandos a partir do script sql
    script = open('create.sql', 'r').read()
    # Executa os comandos do script SQL diretamente no banco de dados.
    cursor.execute(script)
    # Salva as alterações.
    connection.commit()
    # Encerra a conexão.
    connection.close()

"""-------------------------------------------------------------------------"""

# Confere se o usuário já tem uma ficha criada.
def confereUsuario(id_usuário, id_grupo):
    # Conecta ao banco de dados no arquivo Atrix.
    connection = psycopg2.connect(database)
    # Cria um cursor do banco de dados, que é um iterador que permite navegar
    # e manipular os registros do bd, e o atribui a uma variável.
    cursor = connection.cursor()
    cursor.execute('''  SELECT Id_Grupo, Id_Jogador
                        FROM FICHAS
                        WHERE Id_Grupo = %s AND Id_Jogador = %s;''',
                    id_grupo, id_usuário)
    result = cursor.fetchall()
    if len(result) > 0:
        connection.close()
        return True
    else:
        connection.close()
        return False

"""-------------------------------------------------------------------------"""

# Confere se um grupo já tem uma entrada na base de dados
def confereGrupo(id_grupo):
    connection = psycopg2.connect(database)
    cursor = connection.cursor()
    cursor.execute('''  SELECT Id_Grupo
                        FROM GRUPOS
                        WHERE Id_Grupo = %s;''',
                    id_grupo)
    result = cursor.fetchall()
    if len(result) > 0:
        connection.close()
        return True
    else:
        connection.close()
        return False

"""-------------------------------------------------------------------------"""

# Cria uma entrada para um grupo no banco de dados.
def criaGrupo(id_grupo, id_mestre, edição_livre=True):
    connection = psycopg2.connect(database)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO GRUPOS VALUES(%s, %s, %s);', id_grupo, id_mestre, edição_livre)
    connection.commit()
    connection.close()

"""-------------------------------------------------------------------------"""

# Cria uma entrada para um personagem no banco de dados.
def criaFicha(id_grupo, id_jogador, nome='', identidade_civil='',
              identidade_secreta = True, sexo = '', idade = 0, altura = 0.0,
              peso = 0.0, tamanho = 0, olhos = '', cabelo = '', pele = '',
              base = '', nivel = 0, ataques = 0, defesa = 0):
    pontos = 15*nivel
    connection = psycopg2.connect(database)
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO FICHAS VALUES(%s, %s, %s, %s,
                                                %s, %s, %s, %s, %s, %s,
                                                %s, %s, %s, %s, %s, %s, %s, %s);''',
                    id_grupo, id_jogador, nome, identidade_civil,
                    identidade_secreta, sexo, idade, altura, peso, tamanho,
                    olhos, pele, cabelo, base, nivel, pontos, ataques, defesa)
    # Insere os valores das informações básicas do personagem
    cursor.execute('''INSERT INTO HABILIDADES VALUES(%s, %s,
                                                     %s, %s, %s, %s, %s, %s,
                                                     %s, %s, %s, %s, %s, %s);''',
                   id_grupo, id_jogador,
                   10, 10, 10, 10, 10, 10,
                   0, 0, 0, 0, 0, 0)
    # Insere os valores de habilidades do personagem
    cursor.execute('''INSERT INTO SALVAMENTOS VALUES(%s, %s,
                                                     %s, %s, %s,
                                                     %s, %s, %s, %s);''',
                   id_grupo, id_jogador,
                   0, 0, 0,
                   0, 0, 0, 0)
    # Insere os valores de salvamentos do personagem
    connection.commit()
    connection.close()

"""-------------------------------------------------------------------------"""

# Adiciona um feito a uma ficha
def addFeito(id_grupo, id_jogador, nome, bonus=''):
    connection = psycopg2.connect(database)
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO FEITOS VALUES(%s, %s
                                                %s, %s);''',
                   id_grupo, id_jogador,
                   nome, bonus)
    connection.commit()
    connection.close()

"""-------------------------------------------------------------------------"""

# Adiciona uma perícia a uma ficha
def addPericia(id_grupo, id_jogador, nome, habilidade, grad, bonus):
    connection = psycopg2.connect(database)
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO PERICIAS VALUES(%s, %s,
                                                  %s, %s, %s, %s);''',
                   id_grupo, id_jogador,
                   nome, habilidade, grad, bonus)
    connection.commit()
    connection.close()

"""-------------------------------------------------------------------------"""

# Adiciona uma desvantagem a uma ficha
def addDesvantagem(id_grupo, id_jogador, desc, freq, intensidade):
    connection = psycopg2.connect(database)
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO DESVANTAGENS VALUES(%s, %s,
                                                      %s, %s, %s);''',
                   id_grupo, id_jogador,
                   desc, freq, intensidade)
    connection.commit()
    connection.close()

"""-------------------------------------------------------------------------"""

# Adiciona um poder na ficha do personagem
def addPoder(id_grupo, id_jogador, nome, descrição, ativa, área_efeito,
             tempo_ativação, tempo_recarga, duração, custo_base, grad,
             feitos, extras, falhas):
    connection = psycopg2.connect(database)
    cursor = connection.cursor()
    
    cursor.execute('''INSERT INTO PODERES_E_DISPOSITIVOS VALUES(%s, %s,
                                                                %s, %s, %s, %s,
                                                                %s, %s, %s, %s,
                                                                %s, %s, %s, %s, %s);''',
                   id_grupo, id_jogador,
                   nome, descrição, "PODER", ativa,
                   área_efeito, tempo_ativação, tempo_recarga, duração,
                   custo_base, grad, feitos, extras, falhas)

    connection.commit()
    connection.close()

"""-------------------------------------------------------------------------"""

# Adiciona um dispositivo na ficha do personagem
def addDispositivo(id_grupo, id_jogador, nome, descrição, ativa, área_efeito,
                   tempo_ativação, tempo_recarga, duração, custo_base, grad,
                   feitos, extras, falhas):
    connection = psycopg2.connect(database)
    cursor = connection.cursor()
    
    cursor.execute('''INSERT INTO PODERES_E_DISPOSITIVOS VALUES(%s, %s,
                                                                %s, %s, %s, %s,
                                                                %s, %s, %s, %s,
                                                                %s, %s, %s, %s, %s);''',
                   id_grupo, id_jogador,
                   nome, descrição, "DISPOSITIVO", ativa,
                   área_efeito, tempo_ativação, tempo_recarga, duração,
                   custo_base, grad, feitos, extras, falhas)

    connection.commit()
    connection.close()

"""-------------------------------------------------------------------------"""
