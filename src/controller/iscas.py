import datetime
import mysql
from src.bot.BotConfig import BOT
from src.configs.DatabaseConfig import db_config


def iscas_command(message):
    message_id = message.message_id
    quantidadegiros(message_id, message)  # Pass the 'message' object as an argument
    
    
    
    
    
def quantidadegiros(message_id, message):  # Add 'message' as a parameter
    try:
        conn = mysql.connector.connect(**db_config())
        cursor = conn.cursor()
        # Consultar o valor de "ultimogiro" e "qntdgiros" com base no "id_mensagem"
        cursor.execute("SELECT ultimogiro, qntdgiros FROM giros WHERE id_mensagem = %s", (message_id,))
        result = cursor.fetchone()

        if result:
            ultimogiro, qntdgiros = result

            # Calcular a diferença de tempo em relação ao horário atual
            horario_atual = datetime.now()
            diff = horario_atual - ultimogiro

            # Calcular a quantidade de giros a adicionar
            if qntdgiros == 0:
                qntdgiros = diff.total_seconds() // 2
            else:
                qntdgiros += diff.total_seconds() // 2

            # Atualizar o valor de "ultimogiro" e "qntdgiros" no banco de dados
            cursor.execute("UPDATE giros SET ultimogiro = %s, qntdgiros = %s WHERE id_mensagem = %s",
                           (horario_atual, qntdgiros, message_id))
            conn.commit()

            # Exibir a mensagem com o número de giros
            BOT.send_message(message.chat.id, f"Você tem {qntdgiros} giros.")
        else:
            # A mensagem não foi encontrada na tabela giros
            BOT.send_message(message.chat.id, "Mensagem não encontrada.")


    except mysql.connector.Error as err:

        BOT.send_message(message.chat.id, f"Erro ao consultar os giros: {err}")


    finally:

        if 'cursor' in locals():
            cursor.close()

        if 'conn' in locals():
            conn.close()