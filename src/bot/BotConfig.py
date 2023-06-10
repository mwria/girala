import telebot

BOT = telebot.TeleBot("6127981599:AAHBe-NzKCLiE7xAn8iI8Kw2DQHG_SDlu1M")

def bot_send_photo(chatId, photo, caption, keyboard):
    BOT.send_photo(chatId, photo, caption, reply_markup=keyboard)