import mysql
from src.bot.BotConfig import BOT
from src.configs.DatabaseConfig import db_config


def picnic_command(message):

    conn = mysql.connector.connect(**db_config())
    cursor = conn.cursor()

    # ID da mensagem que está sendo respondida
    replied_message_id = message.reply_to_message.message_id

    # ID do usuário que acionou o comando
    user_id = message.from_user.id

    # ID do usuário que recebeu a mensagem
    partner_id = message.reply_to_message.from_user.id

    # IDs das cartas
    first_card_id, second_card_id = message.text.split()[1:]

    # Verifica se a primeira carta existe no inventário do usuário
    query = f"SELECT COUNT(*) FROM inventario WHERE id_personagem = {first_card_id} AND id_usuario = {user_id}"
    cursor.execute(query)
    first_card_count = cursor.fetchone()[0]

    # Verifica se a segunda carta existe no inventário do parceiro de troca
    query = f"SELECT COUNT(*) FROM inventario WHERE id_personagem = {second_card_id} AND id_usuario = {partner_id}"
    cursor.execute(query)
    second_card_count = cursor.fetchone()[0]

    if first_card_count == 0:
        BOT.reply_to(message, "A carta não foi encontrada no seu inventário.")
    elif second_card_count == 0:
        BOT.reply_to(message, "A carta não foi encontrada no inventário do parceiro de troca.")
    else:
        # Envia uma mensagem para confirmar a troca
        confirmation_message = f"{message.from_user.mention} deseja aceitar essa troca? Responda com 'sim' ou 'não'."
        BOT.reply_to(message.reply_to_message, confirmation_message)

        # Aguarda a resposta da confirmação da troca
        @BOT.message_handler(func=lambda message: message.reply_to_message.message_id == replied_message_id)
        def trade_confirmation(message):
            if message.text.lower() == "sim":
                # Realiza a troca no banco de dados
                query = f"UPDATE inventario SET id_usuario = CASE WHEN id_usuario = {user_id} THEN {partner_id} ELSE {user_id} END WHERE id_personagem IN ({first_card_id}, {second_card_id}) AND id_usuario IN ({user_id}, {partner_id})"
                cursor.execute(query)
                conn.commit()
                BOT.reply_to(message, "Troca realizada com sucesso!")
            else:
                BOT.reply_to(message, "Troca cancelada.")

    cursor.close()
    conn.close()