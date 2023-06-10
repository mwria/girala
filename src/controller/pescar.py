import random
from obtercartas import obter_cartas_por_subcategoria
from src.bot.BotConfig import BOT, bot_send_photo
from src.configs.DatabaseConfig import db_config
import telebot
import mysql.connector

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
        bot_send_photo(message.chat.id, photo, 'Selecione uma categoria:', keyboard)
        
        
        
## função executada ao clicar na categoria do /pescar




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
                button = telebot.types.InlineKeyboardButton(text=subcategorias_aleatorias[i], callback_data="subcategoria_pescar_"+subcategorias_aleatorias[i])
                keyboard.add(button)

            BOT.send_message(message.chat.id, resposta, reply_markup=keyboard)

        else:
            BOT.send_message(message.chat.id, f"Nenhuma subcategoria encontrada para a categoria '{categoria}'.")

    except mysql.connector.Error as err:
        BOT.send_message(message.chat.id, f"Erro ao buscar subcategorias: {err}")

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
            
            
            
def pescar_selecionar_subcategoria(message, subcategoria):
    try:
        conn = mysql.connector.connect(**db_config())
        cursor = conn.cursor()
        
        id_personagem_query = "SELECT id FROM personagens WHERE subcategoria = %s"
        cursor.execute(id_personagem_query, (subcategoria,))
        results = cursor.fetchall()
        id_personagem = results[0][0]
        
        subcategoria_handler(message, subcategoria, cursor, conn, id_personagem, message.from_user.id)
        
    except mysql.connector.Error as err:
        print(f"Erro ao buscar subcategorias: {err}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        
        
def subcategoria_handler(message, subcategoria, cursor, conn, id_personagem, id_usuario):
    print('subcategoria_handler', subcategoria)

    cartas_disponiveis = obter_cartas_por_subcategoria(subcategoria, conn)

    if cartas_disponiveis:
        carta_aleatoria = random.choice(cartas_disponiveis)
        id, nome, imagem = carta_aleatoria

        add_to_inventory(cursor, conn, id_personagem, id_usuario, nome, subcategoria, message.chat.id)  # Pass 'call' as an argument


        if imagem is None:
            BOT.send_message(message.chat.id, f"{nome} - (A carta não tem imagem)")
        else:
            BOT.send_photo(message.chat.id, imagem, caption=nome)
    else:
        BOT.send_message(message.chat.id, "Nenhuma carta disponível nessa subcategoria.")
        
        
def add_to_inventory(cursor, conn, id_personagem, id_usuario, nome, subcategoria, chatId):
    try:
        # Register the new card in the user's inventory
        cursor.execute(
            "INSERT INTO inventario (id_personagem, id_usuario, nome, subcategoria, quantidade) VALUES (%s, %s, %s, %s, 1)",
            (id_personagem, id_usuario, nome, subcategoria))
        conn.commit()
    except mysql.connector.Error as err:
        BOT.send_message(chatId, f"Error while adding card to the database: {err}")
