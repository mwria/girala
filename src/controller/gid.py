from funções import consultar_dados
from src.bot.BotConfig import BOT
from src.configs.DatabaseConfig import db_config
import mysql

def gid_command(message):
    try:
        conn = mysql.connector.connect(**db_config())
        cursor = conn.cursor()

        # Extract the ID of the card from the received message
        id = message.text.replace('/gid', '').strip()

        # Query the card data by ID
        resposta, imagem, nome, subcategoria = consultar_dados(id)

        if resposta is not None:
            # Send the response to the user
            BOT.send_message(chat_id=message.chat.id, text=resposta)

            # Get the ID of the user who triggered the command
            user_id = message.from_user.id

            # Check if the card already exists in the user's inventory
            cursor.execute("SELECT * FROM inventario WHERE id_personagem = %s AND id_usuario = %s", (id, user_id))
            existing_row = cursor.fetchone()

            if existing_row is not None:
                # Increment the quantity of the existing card
                add_to_inventory(cursor, conn, id, user_id, nome, subcategoria, message.chat.id)
                BOT.send_message(message.chat.id, "Quantidade atualizada no inventário: {}".format(existing_row[4] + 1))
            else:
                # Register the new card in the user's inventory
                add_to_inventory(cursor, conn, id, user_id, nome, subcategoria, message.chat.id)
                BOT.send_message(message.chat.id, "Carta registrada no inventário com sucesso!")
        else:
            # Informar que a carta já está no inventário do usuário
            BOT.send_message(message.chat.id, "Esta carta já está no seu inventário!")

        # Send the image if available
        if imagem is not None:
            BOT.send_photo(message.chat.id, imagem, caption=nome)
    except mysql.connector.Error as err:
        BOT.send_message(message.chat.id, f"Erro ao buscar dados da carta: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            
            
def add_to_inventory(cursor, conn, id_personagem, id_usuario, nome, subcategoria, chatId):
    try:
        # Register the new card in the user's inventory
        cursor.execute(
            "INSERT INTO inventario (id_personagem, id_usuario, nome, subcategoria, quantidade) VALUES (%s, %s, %s, %s, 1)",
            (id_personagem, id_usuario, nome, subcategoria))
        conn.commit()
    except mysql.connector.Error as err:
        BOT.send_message(chatId, f"Error while adding card to the database: {err}")
