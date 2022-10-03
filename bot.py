import telebot
from time import sleep
from configHandler import Config
from functions import make_sda_screenshot, start_sda, render_error_image, focus_sda, change_user_select,\
    select_account_list, close_sda
import atexit

atexit.register(close_sda)
config = Config()

API_TOKEN = config.get_token()
accounts = config.get_accounts()
bot = telebot.TeleBot(API_TOKEN)

start_sda(config.get_sda_path())
sleep(2)
focus_sda()
select_account_list()


@bot.message_handler(commands=['sda_start'])
def sda_start(command):
    if command.from_user.id in config.get_owners():
        render_error_image(start_sda(config.get_sda_path())).save('test.png')
        img = open('test.png', 'rb')
        bot.send_photo(command.from_user.id, img)


@bot.message_handler(commands=['start'])
def get_start_command(command):
    img = open('img/banner.png', 'rb')
    bot.send_photo(command.from_user.id, photo=img,
                   caption="Этот бот выводит коды STEAM GUARD из приложения Steam Desktop Authenticator (Jessecar96). SDA должен иметь настроенный генератор кодов. Чтобы настроить безопасность используйте config.json.\n\nВаш user_id: " + str(
                       command.from_user.id) + ' \n\nby @ohmwraith')


@bot.message_handler(commands=['sda'])
def get_sda_command(command):
    if command.from_user.id in config.get_owners():
        if len(command.text.split()) > 1:
            focus_sda()
            users_pointer = change_user_select(config.get_accounts(), command.text.split()[1], config.get_account_pointer())
            config.set_account_pointer(users_pointer)
        make_sda_screenshot()
        img = open('output.png', 'rb')
        bot.send_photo(command.from_user.id, img)


@bot.message_handler(commands=['myid'])
def get_user_id_command(command):
    bot.send_message(command.from_user.id, "Ваш user_id: " + str(command.from_user.id))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.from_user.id in config.get_owners():
        if message.text == "Привет":
            bot.send_message(message.from_user.id, "Привет, хозяин")
        elif message.text == "/help":
            bot.send_message(message.from_user.id,
                             "Доступные команды:\n/myid - узнать свой user_id\n/sda - получить код Steam Guard")
        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
    else:
        bot.send_message(message.from_user.id, "Только для авторизованных пользователей")

try:
    bot.polling(none_stop=True, interval=0)
except Exception as E:
    print("Ошибка: " + str(E))
