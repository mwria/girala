import types
from src.bot.BotConfig import BOT
from src.configs.DatabaseConfig import db_config
import mysql.connector

def cenourar_command(message):
    # Pergunta o ID da carta ao usuário
    BOT.send_message(message.chat.id, "Digite o ID da carta que deseja cenourar:")

    # Define um novo estado de conversa para aguardar a resposta do ID da carta
    BOT.register_next_step_handler(message, process_card_id)
    
    
    
def process_card_id(message):
    try:
        # Obtém o ID da carta fornecido pelo usuário
        card_id = int(message.text)

        # Consulta o inventário para verificar se o usuário possui a carta com o ID informado
        conn = mysql.connector.connect(**db_config())
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventario WHERE usuario_id = %s AND carta_id = %s", (message.from_user.id, card_id))
        inventory_data = cursor.fetchone()

        if inventory_data:
            card_id, user_id, quantity = inventory_data

            # Obtém os detalhes da carta para exibir na mensagem
            cursor.execute("SELECT id, nome, subcategoria FROM cartas WHERE id = %s", (card_id,))
            card_details = cursor.fetchone()
            card_id, card_name, card_subcategory = card_details

            # Cria os botões de confirmação (sim e não) com os respectivos dados da carta
            keyboard = types.InlineKeyboardMarkup([
                [types.InlineKeyboardButton("Sim", callback_data=f"cenourar_{card_id}")],
                [types.InlineKeyboardButton("Não", callback_data="cancelar")]
            ])

            # Monta a mensagem de confirmação com os dados da carta
            message_text = f"Deseja cenourar essa carta?\n\nID: {card_id}\nNome: {card_name}\nSubcategoria: {card_subcategory}"

            # Envia a mensagem de confirmação com os botões de ação
            BOT.send_message(message.chat.id, message_text, reply_markup=keyboard)

        else:
            # Informa ao usuário que ele não possui a carta
            BOT.send_message(message.chat.id, "Você não possui essa carta no inventário.")

    except ValueError:
        # Informa ao usuário que o ID da carta fornecido é inválido
        BOT.send_message(message.chat.id, "ID da carta inválido.")

    except mysql.connector.Error as err:
        # Informa ao usuário caso ocorra um erro na consulta ao banco de dados
        BOT.send_message(message.chat.id, f"Erro ao consultar o inventário: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()




## função executada ao clicar na categoria do /cenourar



def handle_cenourar(call):
    try:
        # Extrai o ID da carta do callback data
        card_id = int(call.data.split('_')[1])

        # Obtém os detalhes da carta para verificação adicional
        conn = mysql.connector.connect(**db_config())
        cursor = conn.cursor()
        cursor.execute("SELECT id, usuario_id, quantidade FROM inventario WHERE usuario_id = %s AND carta_id = %s", (call.from_user.id, card_id))
        inventory_data = cursor.fetchone()

        if inventory_data:
            card_id, user_id, quantity = inventory_data

            if quantity == 1:
                # Remove a carta do inventário, já que a quantidade é 1
                cursor.execute("DELETE FROM inventario WHERE usuario_id = %s AND carta_id = %s", (user_id, card_id))

            else:
                # Decrementa a quantidade da carta em 1
                cursor.execute("UPDATE inventario SET quantidade = quantidade - 1 WHERE usuario_id = %s AND carta_id = %s", (user_id, card_id))

            # Incrementa a quantidade de cenouras na tabela de usuários
            cursor.execute("UPDATE usuarios SET cenouras = cenouras + 1 WHERE id = %s", (user_id,))

            # Confirma as alterações no banco de dados
            conn.commit()

            # Informa ao usuário que a carta foi cenourada com sucesso
            BOT.send_message(call.message.chat.id, "Carta cenourada com sucesso!")

        else:
            # Informa ao usuário que ele não possui mais a carta no inventário
            BOT.send_message(call.message.chat.id, "Você não possui mais essa carta no inventário.")

    except mysql.connector.Error as err:
        # Informa ao usuário caso ocorra um erro na consulta ao banco de dados
        BOT.send_message(call.message.chat.id, f"Erro ao cenourar a carta: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()