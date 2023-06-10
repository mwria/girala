from src.bot.BotConfig import bot_send_photo
from src.configs.DatabaseConfig import db_config
import telebot
import mysql

bot = telebot.TeleBot("6127981599:AAHBe-NzKCLiE7xAn8iI8Kw2DQHG_SDlu1M")

def armazem_command(message):
    conn = mysql.connector.connect(**db_config())
    cursor = conn.cursor()

    # Obtém o ID do usuário que acionou o comando
    id_usuario = message.from_user.id

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