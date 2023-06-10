
from src.bot.BotConfig import BOT
from src.configs.DatabaseConfig import db_config
import telebot
import mysql.connector
import random
from telebot import types


def obter_carta_aleatoria(subcategoria, banco_de_dados):
    # Verificar se o usuário da tabela "usuarios" é diferente do da tabela "inventario"
    if verificar_usuario_diferente():
        # Gerar uma carta aleatória apenas para o usuário da tabela "usuarios"
        query = "SELECT nome FROM usuarios ORDER BY RAND() LIMIT 1"
    else:
        # Gerar uma carta aleatória para qualquer usuário
        query = "SELECT nome FROM usuarios JOIN inventario ON usuarios.id_usuario = inventario.id_usuario ORDER BY RAND() LIMIT 1"

    cartas_disponiveis = [carta for carta in banco_de_dados if carta['subcategoria'] == subcategoria]
    carta_aleatoria = random.choice(cartas_disponiveis)

    # Executar a consulta SQL para obter a carta aleatória
    resultado = executar_consulta_sql(query)
    if resultado:
        carta_aleatoria['nome'] = resultado[0]['nome']

    return carta_aleatoria

def obter_cartas_por_subcategoria(subcategoria, conn):
    cursor = conn.cursor()
    query = "SELECT id, nome, imagem FROM personagens WHERE subcategoria = %s"
    cursor.execute(query, (subcategoria,))
    result = cursor.fetchall()
    cursor.close()
    return result

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
                BOT.send_photo(message.chat.id, photo, caption=resposta)

        else:
            BOT.send_message(message.chat.id, f"Nenhuma carta encontrada para a subcategoria '{subcategoria}'.")

    except mysql.connector.Error as err:
        BOT.send_message(message.chat.id, f"Erro ao buscar cartas: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

