
import telebot
import mysql.connector
import random
from telebot import types


bot = telebot.TeleBot("6127981599:AAHBe-NzKCLiE7xAn8iI8Kw2DQHG_SDlu1M")
def db_config():
    return {
        'host': '26.121.107.216',
        'database': 'girala',
        'user': 'maria',
        'password': '13243122'
    }


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
            return f"💌 | Personagem:\n\n{id}. {nome} \nde {subcategoria}", imagem, nome, subcategoria
        else:
            return "Nenhum resultado encontrado para o ID fornecido.", None, None, None

    except mysql.connector.Error as err:
        return f"Erro ao executar a consulta: {err}", None, None, None

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
