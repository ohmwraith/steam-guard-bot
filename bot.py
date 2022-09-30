import telebot
from time import sleep
from configLoader import load_config, save_config, is_config_created, make_config, check_loaded_config
from functions import make_sda_screenshot, start_sda, render_error_image, focus_sda, change_user_select,\
    select_account_list, close_sda
import atexit

if not is_config_created():
    make_config()

atexit.register(close_sda)
config = load_config()
check_loaded_config(config)

config['USER_POINTER'] = 0
save_config(config)
API_TOKEN = config['API_TOKEN']
users = config['USER_LIST']
bot = telebot.TeleBot(API_TOKEN)

start_sda(config['SDA_PATH'])
sleep(2)
focus_sda()
select_account_list()


@bot.message_handler(commands=['sda_start'])
def sda_start(command):
    if command.from_user.id == config['TELEGRAM_USER_ID']:
        render_error_image(start_sda(config['SDA_PATH'])).save('test.png')
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
    config = load_config()
    if command.from_user.id == config['TELEGRAM_USER_ID']:
        if len(command.text.split()) > 1:
            focus_sda()
            users_pointer = change_user_select(users, command.text.split()[1], config['USER_POINTER'])
            config['USER_POINTER'] = users_pointer
            save_config(config)
        make_sda_screenshot()
        img = open('output.png', 'rb')
        bot.send_photo(command.from_user.id, img)


@bot.message_handler(commands=['myid'])
def get_user_id_command(command):
    bot.send_message(command.from_user.id, "Ваш user_id: " + str(command.from_user.id))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.from_user.id == config['TELEGRAM_USER_ID']:
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
