from src.bot.BotConfig import BOT
from src.configs.DatabaseConfig import db_config
import telebot
import mysql

def start_comando(message):
    # Registrar o ID do usuário na tabela 'usuarios'
    registrar_usuario(message.from_user.id)
    keyboard = telebot.types.InlineKeyboardMarkup()
    image_path = "imagens/Normal/halsey.jpeg"  # Defina o caminho correto para a imagem
    with open(image_path, 'rb') as photo:
        BOT.send_photo(message.chat.id, photo, caption='Seja muito bem vindo ao giralá! entre e fique a vontade',
                       reply_markup=keyboard)
        
        
        

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
