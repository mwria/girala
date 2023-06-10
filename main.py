from src.bot.BotConfig import BOT
from src.controller.gid import gid_command
import telebot

from src.controller.cenourar import cenourar_command, handle_cenourar
from src.controller.gnome import gnome_command
from src.controller.iscas import iscas_command
from src.controller.picnic import picnic_command
from src.controller.start import start_comando
from src.controller.pescar import categoria_handler, pescar, pescar_selecionar_subcategoria
from src.controller.setuser import setuser_comando
from src.controller.armazen import armazem_command


#Controllers
@BOT.message_handler(commands=['pescar'])
def pescar_handler(message):
    pescar(message)


@BOT.message_handler(commands=['setuser'])
def setuser_handler(message):
    setuser_comando(message)

@BOT.message_handler(commands=['armazem'])
def armazen_handler(message):
    armazem_command(message)

@BOT.message_handler(commands=['start'])
def start_handler(message):
    start_comando(message)


@BOT.message_handler(commands=['gnome'])
def gnome_handler(message):
    gnome_command(message)

@BOT.message_handler(commands=['iscas'])
def iscar_handler(message): 
    iscas_command(message)

@BOT.message_handler(commands=['cenourar'])
def cenourar_handler(message):
    cenourar_command(message)
    
@BOT.message_handler(func=lambda message: message.reply_to_message is not None and message.reply_to_message.from_user.id == BOT.get_me().id)
def picnic_handler(message):
    picnic_command(message)
    
    
@BOT.callback_query_handler(func=lambda call: call.data.startswith('cenourar_'))
def handle_cenourar_callback(call):
    handle_cenourar(call)


@BOT.callback_query_handler(func=lambda call: call.data.startswith('pescar_'))
def callback_handler(call):
    categoria = call.data.replace('pescar_', '')
    categoria_handler(call.message, categoria)


@BOT.callback_query_handler(func=lambda call: call.data.startswith('subcategoria_pescar_'))
def pescar_subcategoria_handler(call):
    categoria = call.data.replace('subcategoria_pescar_', '')
    pescar_selecionar_subcategoria(call.message, categoria)


@BOT.message_handler(commands=['gid'])
def gid_handler(message):
    gid_command(message)

BOT.polling()


if __name__ == "__main__":
    print("Started...")