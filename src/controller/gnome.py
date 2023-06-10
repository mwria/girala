import mysql
from src.bot.BotConfig import BOT
from src.configs.DatabaseConfig import db_config
from telebot import types


def gnome_command(message):
    try:
        conn = mysql.connector.connect(**db_config())
        cursor = conn.cursor()

        # Extrai o nome do personagem da mensagem recebida
        name = message.text.replace('/gnome', '').strip()

        # Consulta os dados dos personagens que contenham a palavra buscada
        cursor.execute("SELECT * FROM personagens WHERE nome LIKE %s", ('%' + name + '%',))
        character_data = cursor.fetchall()

        if character_data:
            # Armazena os resultados da pesquisa em uma variável global do BOT
            BOT.character_results = character_data
            BOT.current_page = 0  # Define a página inicial como 0 (primeiro resultado)

            # Mostra o primeiro resultado
            index = BOT.current_page
            character = character_data[index]
            id = character[0]
            resposta, imagem, nome, subcategoria = consultar_dados(id)

            if resposta is not None:
                response_message = f"{resposta}\n\n{nome}\n\n"

                keyboard = types.InlineKeyboardMarkup()

                # Botão ">" para próxima página
                next_button = types.InlineKeyboardButton(">", callback_data=f"next")
                keyboard.add(next_button)

                # Envia a mensagem com o resultado e o botão de próxima página
                BOT.send_photo(chat_id=message.chat.id, photo=imagem, caption=response_message, reply_markup=keyboard)

            else:
                BOT.send_message(message.chat.id, f"Não foi possível obter os dados do personagem.")

        else:
            # Informa que nenhum personagem foi encontrado
            BOT.send_message(message.chat.id, f"Nenhum personagem encontrado com a palavra '{name}'.")

    except mysql.connector.Error as err:
        BOT.send_message(message.chat.id, f"Erro ao obter os dados dos personagens: {err}")

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
