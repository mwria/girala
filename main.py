
import telebot
import mysql.connector
import random
from obtercartas import obter_cartas_por_subcategoria
from consultas import consultar_dados, consultar_personagem_por_nome
from telebot import types
from datetime import datetime

bot = telebot.TeleBot("6127981599:AAHBe-NzKCLiE7xAn8iI8Kw2DQHG_SDlu1M")
def db_config():
    return {
        'host': '26.121.107.216',
        'database': 'girala',
        'user': 'maria',
        'password': '13243122'
    }

def conectar_banco_dados():
    conn = mysql.connector.connect(**db_config())
    cursor = conn.cursor()
    return conn, cursor

conn, cursor = conectar_banco_dados()

def fechar_conexao(cursor, conn):
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()

def id_usuario(message):
    return message.from_user.id

def main():
    @bot.callback_query_handler(func=lambda call: call.data.startswith('subcategoria_'))
    def handle_subcategoria_callback(call):
        # Extrair a subcategoria do callback data
        subcategoria = call.data.split('_')[1]

        # Buscar uma carta aleatória da subcategoria
        carta = buscar_carta_aleatoria_por_subcategoria(subcategoria)

        if carta:
            id_carta, nome_carta, imagem_carta = carta
            mensagem = f"ID: {id_carta}\nNome: {nome_carta}"
            bot.send_photo(call.message.chat.id, imagem_carta, caption=mensagem)
        else:
            bot.send_message(call.message.chat.id, "Nenhuma carta encontrada para a subcategoria selecionada.")


def buscar_cartas_usuario(id_usuario):

    global cursor
    try:
        conn, cursor = conectar_banco_dados()
        id_usuario = id_usuario()

            # Consulta SQL para buscar os IDs das cartas relacionadas ao ID do usuário
        query = f"SELECT id_personagem FROM inventario WHERE id_usuario = {id_usuario}"
        cursor.execute(query)

            # Lista para armazenar os IDs das cartas
        cartas_usuario = []

            # Obtém os resultados da consulta e adiciona os IDs das cartas à lista
        for row in cursor.fetchall():
            id_carta = row[0]
            cartas_usuario.append(id_carta)

        return cartas_usuario

    except mysql.connector.Error as err:
        print(f"Erro ao buscar cartas do usuário: {err}")

    finally:
        fechar_conexao(cursor, conn)

    @bot.message_handler(commands=['iduser'])
    def handle_iduser_command(message):
        idusuario = id_usuario()
        bot.reply_to(message, f"Seu ID de usuário é: {idusuario}")

    def execute_query(query):
        conn, cursor = conectar_banco_dados()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result



    def buscar_cartas_usuario(id_usuario):
        global cursor
        try:
            conn = mysql.connector.connect(**db_config())
            cursor = conn.cursor()

            # Consulta SQL para buscar os IDs das cartas relacionadas ao ID do usuário
            query = f"SELECT id_personagem FROM inventario WHERE id_usuario = {id_usuario}"
            cursor.execute(query)

            # Lista para armazenar os IDs das cartas
            cartas_usuario = []

            # Obtém os resultados da consulta e adiciona os IDs das cartas à lista
            for row in cursor.fetchall():
                id_carta = row[0]
                cartas_usuario.append(id_carta)

            return cartas_usuario

        except mysql.connector.Error as err:
            print(f"Erro ao buscar cartas do usuário: {err}")

        finally:
            fechar_conexao(cursor, conn)
def buscar_subcategorias(categoria, user_id=None):
    try:
        conn, cursor = conectar_banco_dados()

        if categoria == 'geral':
            cursor.execute('SELECT DISTINCT subcategoria FROM personagens')
        elif user_id is None:
            cursor.execute('SELECT DISTINCT subcategoria FROM personagens WHERE categoria = %s', (categoria,))
        else:
            cursor.execute('SELECT DISTINCT subcategoria FROM personagens WHERE categoria = %s AND user_id != %s',
                           (categoria, user_id))

        subcategorias = [row[0] for row in cursor.fetchall()]

        return subcategorias

    except mysql.connector.Error as err:
        print(f"Erro ao buscar subcategorias: {err}")
        return []

    finally:
        fechar_conexao(cursor, conn)


# Função para verificar se um valor existe em uma coluna da tabela 'usuarios'
def verificar_valor_existente(coluna, valor):
    try:
        conn, cursor = conectar_banco_dados()

        # Verificar se o valor existe na coluna especificada da tabela 'usuarios'
        query = f"SELECT * FROM usuarios WHERE {coluna} = %s"
        cursor.execute(query, (valor,))
        resultado = cursor.fetchone()

        return resultado is not None

    except mysql.connector.Error as err:
        print(f"Erro ao verificar {coluna}: {err}")

    finally:
        fechar_conexao(cursor, conn)


# Comando /setuser
@bot.message_handler(commands=['setuser'])
def setuser_comando(message):
    # Verificar se o ID do usuário já existe na tabela 'usuarios'
    if verificar_valor_existente("id_usuario", message.from_user.id):
        bot.send_message(message.chat.id, "Seu ID de usuário já está registrado.")
        bot.send_message(message.chat.id, "Por favor, digite um nome de usuário único:")
        bot.register_next_step_handler(message, processar_nome_usuario)
    else:
        bot.send_message(message.chat.id, "Por favor, execute o comando /start primeiro.")


# Função para processar o nome de usuário digitado pelo usuário
def processar_nome_usuario(message):
    nome_usuario = message.text.strip()

    # Verificar se o nome de usuário já existe na tabela 'usuarios'
    if verificar_valor_existente("nome_usuario", nome_usuario):
        bot.send_message(message.chat.id, "O nome de usuário já está em uso.")
        bot.send_message(message.chat.id, "Por favor, escolha um nome de usuário diferente:")
        bot.register_next_step_handler(message, processar_nome_usuario)
    else:
        try:
            conn = mysql.connector.connect(**db_config())
            cursor = conn.cursor()

            # Atualizar a coluna 'nome_usuario' com o nome fornecido
            query = "UPDATE usuarios SET nome_usuario = %s WHERE id_usuario = %s"
            cursor.execute(query, (nome_usuario, message.from_user.id))
            conn.commit()

            bot.send_message(message.chat.id, f"O nome de usuário '{nome_usuario}' foi registrado com sucesso.")

        except mysql.connector.Error as err:
            bot.send_message(message.chat.id, f"Erro ao registrar nome de usuário: {err}")

        finally:
            fechar_conexao(cursor, conn)


# Função para registrar um valor em uma coluna da tabela 'usuarios'
def registrar_valor(coluna, valor, id_usuario):
    try:

        conn, cursor = conectar_banco_dados()
        # Verificar se o valor já está registrado na coluna especificada
        query = f"SELECT * FROM usuarios WHERE {coluna} = %s"
        cursor.execute(query, (valor,))
        resultado = cursor.fetchone()

        if resultado:
            # O valor já está registrado, nada precisa ser feito
            return

        # Registrar o valor na coluna especificada para o ID do usuário
        query = f"UPDATE usuarios SET {coluna} = %s WHERE id_usuario = %s"
        cursor.execute(query, (valor, id_usuario))
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Erro ao registrar {coluna}: {err}")

    finally:
        fechar_conexao(cursor, conn)


# Função para registrar o ID do usuário na tabela 'usuarios'
def registrar_usuario(id_usuario):
    registrar_valor("id_usuario", id_usuario, id_usuario)


def buscar_carta_aleatoria_por_subcategoria(subcategoria):
    try:
        conn, cursor = conectar_banco_dados()

        query = "SELECT id, nome, imagem FROM personagens WHERE subcategoria = %s ORDER BY RAND() LIMIT 1"
        cursor.execute(query, (subcategoria,))
        resultado = cursor.fetchone()

        return resultado

    except mysql.connector.Error as err:
        print(f"Erro ao buscar carta por subcategoria: {err}")

    finally:
        fechar_conexao(cursor, conn)


@bot.message_handler(commands=['start'])
def start_comando(message):
    # Registrar o ID do usuário na tabela 'usuarios'
    registrar_usuario(message.from_user.id)
    keyboard = telebot.types.InlineKeyboardMarkup()
    image_path = "imagens/Normal/halsey.jpeg"  # Defina o caminho correto para a imagem
    with open(image_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption='Seja muito bem vindo ao mabigarden! entre, busque uma sombra e aproveite a estadia.',
                       reply_markup=keyboard)

def add_to_inventory(cursor, conn, id_personagem, id_usuario, nome, subcategoria):
    try:
        # Register the new card in the user's inventory
        cursor.execute(
            "INSERT INTO inventario (id_personagem, id_usuario, nome, subcategoria, quantidade) VALUES (%s, %s, %s, %s, 1)",
            (id_personagem, id_usuario, nome, subcategoria))
        conn.commit()
    except mysql.connector.Error as err:
        bot.send_message(f"Error while adding card to the database: {err}")


@bot.message_handler(commands=['gnome'])
def gnome_command(message):
    nome = message.text.replace('/gnome', '').strip()

    if nome:
        resposta, imagem = consultar_personagem_por_nome(nome)  # Passa o objeto message como parâmetro
        if imagem is not None:
            with open(imagem, 'rb') as photo:
                bot.send_photo(chat_id=message.chat.id, photo=photo, caption=resposta)
        else:
            bot.send_message(chat_id=message.chat.id, text=resposta)
    else:
        bot.send_message(chat_id=message.chat.id, text="O comando /gnome deve ser acompanhado de um nome.")



@bot.callback_query_handler(func=lambda call: call.data.startswith('categoria_'))
def categoria_callback(call):
    categoria = call.data.replace('categoria_', '')

    subcategorias = buscar_subcategorias(categoria)
    subcategorias = [subcategoria for subcategoria in subcategorias if subcategoria]

    if subcategorias:
        keyboard = telebot.types.InlineKeyboardMarkup()

        for subcategoria in subcategorias:
            button = telebot.types.InlineKeyboardButton(subcategoria, callback_data='subcategoria_' + subcategoria)
            keyboard.add(button)

        try:
            bot.edit_message_text('Selecione uma subcategoria:', call.message.chat.id, call.message.message_id,
                                  reply_markup=keyboard)
        except telebot.apihelper.ApiTelegramException:
            pass
    else:
        bot.send_message(call.message.chat.id, "Nenhuma subcategoria encontrada para a categoria selecionada.")


def gerar_carta_sorteada(subcategoria, chat_id):
    try:
        conn, cursor = conectar_banco_dados()

        query = "SELECT id, nome, imagem FROM cartas WHERE subcategoria = %s"
        cursor.execute(query, (subcategoria,))
        cartas = cursor.fetchall()

        if cartas:
            carta_aleatoria = random.choice(cartas)
            id_carta, nome_carta, imagem_carta = carta_aleatoria

            resposta = f"Carta encontrada:\nID: {id_carta}\nNome: {nome_carta}"

            with open(imagem_carta, 'rb') as photo:
                bot.send_photo(chat_id, photo, caption=resposta)

        else:
            bot.send_message(chat_id, f"Nenhuma carta encontrada para a subcategoria '{subcategoria}'.")

    except mysql.connector.Error as err:
        bot.send_message(chat_id, f"Erro ao buscar cartas: {err}")

    finally:
        fechar_conexao(cursor, conn)

@bot.message_handler(commands=['pescar'])
def pescar(message):
    keyboard = telebot.types.InlineKeyboardMarkup()

    # Primeira coluna
    primeira_coluna = [
        telebot.types.InlineKeyboardButton(text="🍃  Música", callback_data='pescar_musica'),
        telebot.types.InlineKeyboardButton(text="🍄  Filmes", callback_data='pescar_filmes'),
        telebot.types.InlineKeyboardButton(text="🍁  Jogos", callback_data='pescar_jogos')
    ]

    # Segunda coluna
    segunda_coluna = [
        telebot.types.InlineKeyboardButton(text="🪹  Animanga", callback_data='pescar_animanga'),
        telebot.types.InlineKeyboardButton(text="🪨  Séries", callback_data='pescar_series'),
        telebot.types.InlineKeyboardButton(text="🌾  Miscelânea", callback_data='pescar_miscelanea')
    ]

    keyboard.add(*primeira_coluna)
    keyboard.add(*segunda_coluna)

    # Botão "Geral"
    keyboard.row(telebot.types.InlineKeyboardButton(text="🫧  Geral", callback_data='pescar_geral'))

    # Imagem
    image_path = "imagens/Normal/halsey.jpeg"  # Defina o caminho correto para a imagem
    with open(image_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption='Selecione uma categoria:', reply_markup=keyboard)

    conn, cursor = conectar_banco_dados()
    cursor.execute("INSERT INTO usuarios (id_telegram) VALUES (%s)", (message.from_user.id,))
    conn.commit()

    fechar_conexao(cursor, conn)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    print("callback", call.data)
    message = call.message
    conn, cursor = conectar_banco_dados()
    idusuario = id_usuario()

    print("callback", call.data)
    if call.message:
        if call.data.startswith('pescar_'):
            categoria = call.data.replace('pescar_', '')
            categoria_handler(call.message, categoria)

        elif call.data.startswith('gmusica'):
            subcategoria = call.data.replace('gmusica_', '')
            id_personagem_query = "SELECT id FROM personagens WHERE subcategoria = %s"
            cursor.execute(id_personagem_query, (subcategoria,))
            results = cursor.fetchall()
            id_personagem = results[0][0]

            subcategoria_handler(message, subcategoria, cursor, conn, id_personagem, idusuario)


@bot.message_handler(commands=['armazem'])
def armazem_command(message):
    conn, cursor = conectar_banco_dados()

    # Obtém o ID do usuário que acionou o comando
    id_usuario = idusuario()

    # Busca as cartas do usuário
    cartas_usuario = buscar_cartas_usuario(id_usuario)

    # Verifica se o usuário possui cartas
    if cartas_usuario:
        resposta = "💌 | Cartas no armazém:\n"
        for id_carta in cartas_usuario:
            # Consulta SQL para obter os dados da carta
            query = f"SELECT nome, subcategoria, quantidade FROM inventario WHERE id_personagem = {id_carta} AND id_usuario = {id_usuario}"
            cursor.execute(query)
            carta = cursor.fetchone()

            nome_carta = carta[0]
            subcategoria_carta = carta[1]
            quantidade_carta = carta[2]

            # Verificação da quantidade
            if quantidade_carta is None:
                quantidade_carta = 0

            # Mapear a quantidade para as letras correspondentes com espaçamento
            if quantidade_carta == 1:
                letra_quantidade = "🍀"
            elif 2 <= quantidade_carta <= 4:
                letra_quantidade = "🍄"
            elif 5 <= quantidade_carta <= 9:
                letra_quantidade = "🕯"
            elif 10 <= quantidade_carta <= 19:
                letra_quantidade = "🫐"
            elif 20 <= quantidade_carta <= 29:
                letra_quantidade = "🧚‍♀️"
            elif 30 <= quantidade_carta <= 39:
                letra_quantidade = "🌙"
            elif 40 <= quantidade_carta <= 49:
                letra_quantidade = "🔮"
            elif 50 <= quantidade_carta <= 99:
                letra_quantidade = "👑"
            else:
                letra_quantidade = "👑"

            resposta += f" {id_carta} - {nome_carta} de {subcategoria_carta} {letra_quantidade} \n"

        bot.send_message(message.chat.id, resposta)
    else:
        bot.send_message(message.chat.id, "Você não possui cartas no armazém.")


def categoria_handler(message, categoria):
    try:
        conn, cursor = conectar_banco_dados()
        subcategorias = buscar_subcategorias(categoria)
        subcategorias = [subcategoria for subcategoria in subcategorias if subcategoria]

        if subcategorias:
            resposta = "E o universo sorteou:\n\n"
            subcategorias_aleatorias = random.sample(subcategorias, min(4, len(subcategorias)))

            keyboard = telebot.types.InlineKeyboardMarkup()

            for i in range(0, 4):
                button = telebot.types.InlineKeyboardButton(text=subcategorias_aleatorias[i], callback_data="gmusica_"+subcategorias_aleatorias[i])
                keyboard.add(button)

            bot.send_message(resposta, reply_markup=keyboard)

        else:
            bot.send_message(message.chat.id, f"Nenhuma subcategoria encontrada para a categoria '{categoria}'.")

    except mysql.connector.Error as err:
        bot.send_message(message.chat.id, f"Erro ao buscar subcategorias: {err}")

    finally:
        fechar_conexao(cursor, conn)

def subcategoria_handler(message, subcategoria, cursor, conn, id_personagem, id_usuario):
    print('subcategoria_handler', subcategoria)

    cartas_disponiveis = obter_cartas_por_subcategoria(subcategoria, conn)

    if cartas_disponiveis:
        carta_aleatoria = random.choice(cartas_disponiveis)
        id, nome, imagem = carta_aleatoria

        add_to_inventory(cursor, conn, id_personagem, id_usuario, nome, subcategoria)  # Pass 'call' as an argument

        query = "SELECT emoji FROM personagens WHERE subcategoria = %s"
        cursor.execute(query, (subcategoria,))
        emoji_categoria = cursor.fetchone()[0]  # Obtém o valor do emoji da consulta

        if imagem is None:
            bot.send_message(message.chat.id, f"🐟 Parabéns! Sua isca era boa e você recebeu:\n{emoji_categoria} {id} - {nome}\nde {subcategoria} - (A carta não tem imagem)")
        else:
            if imagem.endswith(('.jpg', '.jpeg', '.png')):
                bot.send_photo(message.chat.id, imagem,
                               caption=f"🐟 Parabéns! Sua isca era boa e você recebeu:\n\n{emoji_categoria} {id} - {nome}\nde {subcategoria}")
            elif imagem.endswith(('.mp4', '.gif')):
                bot.send_video(message.chat.id, imagem,
                               caption=f"🐟 Parabéns! Sua isca era boa e você recebeu:\n\n{emoji_categoria} {id} - {nome} \nde {subcategoria}")
    else:
        bot.send_message(message.chat.id, "Nenhuma carta disponível nessa subcategoria.")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    numero_selecionado = call.data

    subcategorias = buscar_subcategorias("musica")
    subcategorias = [subcategoria for subcategoria in subcategorias if subcategoria]

    if int(numero_selecionado) in range(1, len(subcategorias) + 1):
        texto_selecionado = subcategorias[int(numero_selecionado) - 1]
        resposta = f"Você selecionou o número {numero_selecionado} - {texto_selecionado}."
    else:
        resposta = "Opção inválida."

    bot.answer_callback_query(call.id, resposta)

    # Comando /troca
    @bot.message_handler(commands=['troca'])
    def troca_handler(message):
        conn, cursor = conectar_banco_dados()
        id_usuario = message.from_user.id

        # Verifica se a mensagem é uma resposta a outra mensagem
        if message.reply_to_message is None:
            bot.send_message(message.chat.id, "Você precisa responder a uma mensagem para realizar a troca.")
            return

        # Obtém o ID da pessoa cuja mensagem foi respondida
        id_outra_pessoa = message.reply_to_message.from_user.id

        # Obtém os IDs das duas cartas fornecidas pelo usuário
        ids_carta = [int(id.strip('()')) for id in message.text.split()[1:]]  # Obtém os argumentos após /troca

        # Verifica se as cartas pertencem aos usuários corretos
        if verificar_cartas(id_usuario, id_outra_pessoa, ids_carta, cursor):
            # Realiza a troca de cartas
            carta_trocada_1, carta_trocada_2 = realizar_troca(id_usuario, id_outra_pessoa, ids_carta, cursor, conn)
            bot.send_message(message.chat.id,
                             f"Troca realizada com sucesso!\nCarta 1 trocada: {carta_trocada_1}\nCarta 2 trocada: {carta_trocada_2}")
        else:
            bot.send_message(message.chat.id, "Algumas das cartas não pertencem aos usuários corretos.")

    # Verifica se as cartas pertencem aos usuários corretos
    def verificar_cartas(id_usuario, id_outra_pessoa, ids_carta, cursor):
        query = "SELECT COUNT(*) FROM inventario WHERE id_usuario = %s AND id_carta = %s"
        cursor.execute(query, (id_usuario, ids_carta[0]))
        count_usuario = cursor.fetchone()[0]
        cursor.execute(query, (id_outra_pessoa, ids_carta[1]))
        count_outra_pessoa = cursor.fetchone()[0]
        return count_usuario == 1 and count_outra_pessoa == 1

    # Realiza a troca de cartas e retorna os IDs das cartas trocadas
    def realizar_troca(id_usuario, id_outra_pessoa, ids_carta, cursor, conn):
        query = "UPDATE inventario SET id_usuario = CASE id_carta " \
                "WHEN %s THEN %s " \
                "WHEN %s THEN %s " \
                "END " \
                "WHERE (id_usuario = %s AND id_carta = %s) OR (id_usuario = %s AND id_carta = %s)"
        params = [ids_carta[0], id_outra_pessoa, ids_carta[1], id_usuario, id_usuario, ids_carta[0], id_outra_pessoa,
                  ids_carta[1]]
        cursor.execute(query, params)
        conn.commit()

        # Retorna os IDs das cartas trocadas
        return ids_carta[0], ids_carta[1]

    fechar_conexao(cursor, conn)


bot.polling()

if __name__ == "__main__":
    main()
