
import mysql.connector

from src.bot.BotConfig import BOT
from src.configs.DatabaseConfig import db_config

def setuser_comando(message):
    # Verificar se o ID do usuário já existe na tabela 'usuarios'
    if verificar_id_usuario(message.from_user.id):
        BOT.send_message(message.chat.id, "Seu ID de usuário já está registrado.")
        BOT.send_message(message.chat.id, "Por favor, digite um nome de usuário único:")
        BOT.register_next_step_handler(message, processar_nome_usuario)
    else:
        BOT.send_message(message.chat.id, "Por favor, execute o comando /start primeiro.")
        
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


        
# Função para processar o nome de usuário digitado pelo usuário
def processar_nome_usuario(message):
    nome_usuario = message.text.strip()

    # Verificar se o nome de usuário já existe na tabela 'usuarios'
    if verificar_nome_usuario(nome_usuario):
        BOT.send_message(message.chat.id, "O nome de usuário já está em uso.")
        BOT.send_message(message.chat.id, "Por favor, escolha um nome de usuário diferente:")
        BOT.register_next_step_handler(message, processar_nome_usuario)
    else:
        try:
            conn = mysql.connector.connect(**db_config())
            cursor = conn.cursor()

            # Atualizar a coluna 'nome_usuario' com o nome fornecido
            query = "UPDATE usuarios SET nome_usuario = %s WHERE id_usuario = %s"
            cursor.execute(query, (nome_usuario, message.from_user.id))
            conn.commit()

            BOT.send_message(message.chat.id, f"O nome de usuário '{nome_usuario}' foi registrado com sucesso.")

        except mysql.connector.Error as err:
            BOT.send_message(message.chat.id, f"Erro ao registrar nome de usuário: {err}")

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