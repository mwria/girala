import telebot
import mysql.connector
import random
from telebot import types
import time

bot = telebot.TeleBot("6127981599:AAHBe-NzKCLiE7xAn8iI8Kw2DQHG_SDlu1M")


def db_config():
    return {
        'host': '26.121.107.216',
        'database': 'girala',
        'user': 'maria',
        'password': '13243122'
    }


def main():
    @bot.callback_query_handler(func=lambda call: call.data.startswith('subcategoria_'))
    def subcategoria_callback(call):
        subcategoria = call.data.replace('subcategoria_', '')
        gerar_carta_sorteada(subcategoria, call.message.chat.id)

    @bot.message_handler(commands=['iduser'])
    def handle_iduser_command(message):
        user_id = message.from_user.id
        bot.reply_to(message, f"Seu ID de usuário é: {user_id}")

    def consultar_personagem_por_nome(nome):
        try:
            con = mysql.connector.connect(**db_config())
            cursor = con.cursor()

            query = "SELECT id, nome, imagem FROM personagens WHERE nome LIKE %s"
            cursor.execute(query, (f"%{nome}%",))
            result = cursor.fetchone()

            # Descartar resultados não lidos
            cursor.fetchall()

            if result:
                id, nome, imagem = result
                return f"ID: {id}\nNome: {nome}\n", imagem

            else:
                return "Nenhum resultado encontrado para o nome fornecido."

        except mysql.connector.Error as err:
            return f"Erro ao executar a consulta: {err}"

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'con' in locals():
                con.close()



def execute_query(query):
    conn = mysql.connector.connect(**db_config())
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def buscar_categorias():
    try:
        conn = mysql.connector.connect(**db_config())
        cursor = conn.cursor()

        cursor.execute('SELECT DISTINCT categoria FROM personagens')

        categorias = [row[0] for row in cursor.fetchall()]

        return categorias

    except mysql.connector.Error as err:
        print(f"Erro ao buscar categorias: {err}")
        return []

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def consultar_dados(id):
    try:
        con = mysql.connector.connect(**db_config())
        cursor = con.cursor()

        query = "SELECT id, nome, imagem, subcategoria FROM personagens WHERE id = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()

        # Descartar resultados não lidos
        cursor.fetchall()

        if result:
            id, nome, imagem, subcategoria = result
            return f"💌 | Personagem:\n\n{id}. {nome} \nde {subcategoria}", imagem
        else:
            return "Nenhum resultado encontrado para o ID fornecido.", None

    except mysql.connector.Error as err:
        return f"Erro ao executar a consulta: {err}", None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()

def consultar_personagens_subcategoria(subcategoria):
    try:
        con = mysql.connector.connect(**db_config())
        cursor = con.cursor()

        query = "SELECT id, nome FROM personagens WHERE subcategoria = %s"
        cursor.execute(query, (subcategoria,))
        results = cursor.fetchall()

        if results:
            lista_personagens = [f"{id}. {nome}" for id, nome in results]
            return lista_personagens

        else:
            return "Nenhum resultado encontrado para a subcategoria fornecida."

    except mysql.connector.Error as err:
        return f"Erro ao executar a consulta: {err}"

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()


def consultar_personagens_por_subcategoria(subcategoria):
    try:
        con = mysql.connector.connect(**db_config())
        cursor = con.cursor()

        query = "SELECT id, nome FROM personagens WHERE subcategoria = %s"
        cursor.execute(query, (subcategoria,))
        results = cursor.fetchall()

        if results:
            lista_personagens = [f"{id}. {nome}" for id, nome in results]
            return lista_personagens

        else:
            return "Nenhum resultado encontrado para a subcategoria fornecida."

    except mysql.connector.Error as err:
        return f"Erro ao executar a consulta: {err}"

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()

def buscar_cartas_usuario(id_usuario):
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
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def consultar_personagem_por_nome(nome: object) -> object:
    try:
        con = mysql.connector.connect(**db_config())
        cursor = con.cursor()

        query = "SELECT id, nome, imagem, subcategoria FROM personagens WHERE nome LIKE %s"
        cursor.execute(query, (f"%{nome}%",))
        result = cursor.fetchone()

        # Descartar resultados não lidos
        cursor.fetchall()

        if result:
            id, nome, imagem, subcategoria = result
            return f"💌 | Personagem:\n\n{id}. {nome} \nde {subcategoria}", imagem

        else:
            return "Nenhum resultado encontrado para o nome fornecido."

    except mysql.connector.Error as err:
        return f"Erro ao executar a consulta: {err}"

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()

def obter_carta_aleatoria(subcategoria, banco_de_dados):
    cartas_disponiveis = [carta for carta in banco_de_dados if carta['subcategoria'] == subcategoria]
    carta_aleatoria = random.choice(cartas_disponiveis)
    return carta_aleatoria

def ler_botao_e_buscar_carta(numero_botao, texto, message):
    try:
        conn = mysql.connector.connect(**db_config())
        cursor = conn.cursor()

        # Extrair a subcategoria do texto
        subcategoria = texto.split('-')[1].strip()

        # Buscar cartas com a subcategoria correspondente
        query = "SELECT id, nome, imagem FROM cartas WHERE subcategoria = %s"
        cursor.execute(query, (subcategoria,))
        cartas = cursor.fetchall()

        if cartas:
            # Selecionar uma carta aleatória
            carta_aleatoria = random.choice(cartas)
            id_carta, nome_carta, imagem_carta = carta_aleatoria

            resposta = f"Carta encontrada:\nID: {id_carta}\nNome: {nome_carta}"

            # Enviar a imagem da carta
            with open(imagem_carta, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption=resposta)

        else:
            bot.send_message(message.chat.id, f"Nenhuma carta encontrada para a subcategoria '{subcategoria}'.")

    except mysql.connector.Error as err:
        bot.send_message(message.chat.id, f"Erro ao buscar cartas: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def buscar_subcategorias(categoria, user_id=None):
    try:
        conn = mysql.connector.connect(**db_config())
        cursor = conn.cursor()

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
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

categorias = buscar_categorias()

# Função para verificar se o ID do usuário já existe na tabela 'usuarios'
def verificar_id_usuario(id_usuario):
    try:
        conn = mysql.connector.connect(**db_config())
        cursor = conn.cursor()

        # Verificar se o ID do usuário existe na tabela 'usuarios'
        query = "SELECT * FROM usuarios WHERE id_usuario = %s"
        cursor.execute(query, (id_usuario,))
        resultado = cursor.fetchone()

        return resultado is not None

    except mysql.connector.Error as err:
        print(f"Erro ao verificar ID do usuário: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# Função para verificar se o nome de usuário já existe na tabela 'usuarios'
def verificar_nome_usuario(nome_usuario):
    try:
        conn = mysql.connector.connect(**db_config())
        cursor = conn.cursor()

        # Verificar se o nome de usuário já existe na tabela 'usuarios'
        query = "SELECT * FROM usuarios WHERE nome_usuario = %s"
        cursor.execute(query, (nome_usuario,))
        resultado = cursor.fetchone()

        return resultado is not None

    except mysql.connector.Error as err:
        print(f"Erro ao verificar nome de usuário: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# Comando /setuser
@bot.message_handler(commands=['setuser'])
def setuser_comando(message):
    # Verificar se o ID do usuário já existe na tabela 'usuarios'
    if verificar_id_usuario(message.from_user.id):
        bot.send_message(message.chat.id, "Seu ID de usuário já está registrado.")
        bot.send_message(message.chat.id, "Por favor, digite um nome de usuário único:")
        bot.register_next_step_handler(message, processar_nome_usuario)
    else:
        bot.send_message(message.chat.id, "Por favor, execute o comando /start primeiro.")

# Função para processar o nome de usuário digitado pelo usuário
def processar_nome_usuario(message):
    nome_usuario = message.text.strip()

    # Verificar se o nome de usuário já existe na tabela 'usuarios'
    if verificar_nome_usuario(nome_usuario):
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
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

# Função para registrar o ID do usuário na tabela 'usuarios'
def registrar_usuario(id_usuario):
    try:
        conn = mysql.connector.connect(**db_config())
        cursor = conn.cursor()

        # Verificar se o ID do usuário já está registrado
        query = "SELECT * FROM usuarios WHERE id_usuario = %s"
        cursor.execute(query, (id_usuario,))
        resultado = cursor.fetchone()

        if resultado:
            # O ID do usuário já está registrado, nada precisa ser feito
            return

        # Registrar o ID do usuário na tabela 'usuarios'
        query = "INSERT INTO usuarios (id_usuario) VALUES (%s)"
        cursor.execute(query, (id_usuario,))
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Erro ao registrar usuário: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def buscar_carta_aleatoria_por_subcategoria(subcategoria):
    try:
        conn = mysql.connector.connect(**db_config())
        cursor = conn.cursor()

        query = "SELECT id, nome, imagem FROM personagens WHERE subcategoria = %s ORDER BY RAND() LIMIT 1"
        cursor.execute(query, (subcategoria,))
        resultado = cursor.fetchone()

        return resultado

    except mysql.connector.Error as err:
        print(f"Erro ao buscar carta por subcategoria: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@bot.message_handler(commands=['start'])
def start_comando(message):
    # Registrar o ID do usuário na tabela 'usuarios'
    registrar_usuario(message.from_user.id)
    keyboard = telebot.types.InlineKeyboardMarkup()
    image_path = "imagens/Normal/halsey.jpeg"  # Defina o caminho correto para a imagem
    with open(image_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption='Seja muito bem vindo ao giralá! entre e fique a vontade',
                       reply_markup=keyboard)



@bot.message_handler(commands=['gid'])
def gid_command(message):
    try:
        conn = mysql.connector.connect(**db_config())
        cursor = conn.cursor()

        # Extrair o ID da carta a partir da mensagem recebida
        id = message.text.replace('/gid', '').strip()

        # Consultar os dados da carta pelo ID
        resposta, imagem = consultar_dados(id)

        if resposta is not None:
            # Enviar a resposta ao usuário
            bot.send_message(chat_id=message.chat.id, text=resposta)

            # Obter o ID do usuário que ativou o comando
            user_id = message.from_user.id

            # Verificar se a carta já está no inventário do usuário
            cursor.execute("SELECT * FROM inventario WHERE id_personagem = %s AND id_usuario = %s", (id, user_id))
            existing_row = cursor.fetchone()

            if not existing_row:
                # Registrar a carta no inventário do usuário
                cursor.execute("INSERT INTO inventario (id_personagem, id_usuario) VALUES (%s, %s)", (id, user_id))
                conn.commit()

                # Confirmar o registro da carta no inventário
                bot.send_message(message.chat.id, "Carta registrada no inventário com sucesso!")
            else:
                # Informar que a carta já está no inventário do usuário
                bot.send_message(message.chat.id, "Esta carta já está no seu inventário!")

            # Enviar a imagem, se disponível
            if imagem is not None:
                with open(imagem, 'rb') as photo:
                    bot.send_photo(chat_id=message.chat.id, photo=photo)
        else:
            bot.send_message(chat_id=message.chat.id, text="Nenhum dado encontrado para o ID informado.")

    except mysql.connector.Error as err:
        bot.send_message(message.chat.id, f"Erro ao buscar dados da carta: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

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
        conn = mysql.connector.connect(**db_config())
        cursor = conn.cursor()

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
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@bot.message_handler(commands=['ggirar'])
def ggirar(message):
    keyboard = telebot.types.InlineKeyboardMarkup()

    # Primeira coluna
    primeira_coluna = [
        telebot.types.InlineKeyboardButton(text="🍃  Música", callback_data='ggirar_musica'),
        telebot.types.InlineKeyboardButton(text="🍄  Filmes", callback_data='ggirar_filmes'),
        telebot.types.InlineKeyboardButton(text="🍁  Jogos", callback_data='ggirar_jogos')
    ]

    # Segunda coluna
    segunda_coluna = [
        telebot.types.InlineKeyboardButton(text="🪹  Animanga", callback_data='ggirar_animanga'),
        telebot.types.InlineKeyboardButton(text="🪨  Séries", callback_data='ggirar_series'),
        telebot.types.InlineKeyboardButton(text="🌾  Miscelânea", callback_data='ggirar_miscelanea')
    ]

    keyboard.add(*primeira_coluna)
    keyboard.add(*segunda_coluna)

    # Botão "Geral"
    keyboard.row(telebot.types.InlineKeyboardButton(text="🫧  Geral", callback_data='ggirar_geral'))

    # Imagem
    image_path = "imagens/Normal/halsey.jpeg"  # Defina o caminho correto para a imagem
    with open(image_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption='Selecione uma categoria:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    print("callback", call.data)
    if call.message:
        if call.data.startswith('ggirar_'):
            categoria = call.data.replace('ggirar_', '')
            categoria_handler(call.message, categoria)

        elif call.data.startswith('gmusica'):
            subcategoria = call.data.replace('gmusica_', '')
            subcategoria_handler(call.message, subcategoria)



@bot.message_handler(commands=['armazem'])
def armazem_command(message):
    # Obtém o ID do usuário que acionou o comando
    id_usuario = message.from_user.id

    # Busca os IDs das cartas do usuário
    cartas_usuario = buscar_cartas_usuario(id_usuario)

    # Verifica se o usuário possui cartas
    if cartas_usuario:
        resposta = "Cartas no armazém:\n"
        for id_carta in cartas_usuario:
            resposta += f"- ID: {id_carta}\n"
        bot.send_message(message.chat.id, resposta)
    else:
        bot.send_message(message.chat.id, "Você não possui cartas no armazém.")

def categoria_handler(message, categoria):
    try:
        conn = mysql.connector.connect(**db_config())
        cursor = conn.cursor()

        subcategorias = buscar_subcategorias(categoria)
        
        subcategorias = [subcategoria for subcategoria in subcategorias if subcategoria]

        if subcategorias:
            resposta = "E o universo sorteou:\n\n"
            subcategorias_aleatorias = random.sample(subcategorias, min(4, len(subcategorias)))

            keyboard = telebot.types.InlineKeyboardMarkup()

            for i in range(0, 4):
                button = telebot.types.InlineKeyboardButton(text=subcategorias_aleatorias[i], callback_data="gmusica_"+subcategorias_aleatorias[i])
                keyboard.add(button)

            bot.send_message(message.chat.id, resposta, reply_markup=keyboard)

        else:
            bot.send_message(message.chat.id, f"Nenhuma subcategoria encontrada para a categoria '{categoria}'.")

    except mysql.connector.Error as err:
        bot.send_message(message.chat.id, f"Erro ao buscar subcategorias: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def subcategoria_handler(message, subcategoria):
    print('subcategoria_handler', subcategoria)

    id, nome, imagem = buscar_carta_aleatoria_por_subcategoria(subcategoria)
    
    print('carta', imagem)

    if imagem == None:
        bot.send_message(message.chat.id, f"{nome} - (A carta não tem imagem)")
    elif imagem.startswith('imagens/'):
        with open(imagem, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=nome)
    else:
        #aqui o imagem é uma url, ele vai ter que retonar a mensagem como link
        #é possivel baixa a imagem e enviar como foto, mas acho isso desnecessario e vai gastar banda da internet
        bot.send_photo(message.chat.id, imagem, caption=nome)
        




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



bot.polling()

if __name__ == "__main__":
    main()
