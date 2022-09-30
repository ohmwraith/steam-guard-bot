import json
import os

def load_config():
    with open('config.json') as file:
        config = file.read()
        config_json = json.loads(config)
        return config_json


def save_config(conf):
    with open('config.json', 'w') as file:
        config = file.write(
            str(conf).replace("'", '"').replace(",", ",\n   ").replace("{", "{\n    ").replace("}", "\n}"))
        return


def is_config_created():
    if 'config.json' not in os.listdir():
        return False
    return True


def check_loaded_config(config):
    if config['API_TOKEN'] == "":
        print("API_TOKEN: Необходимо указать токен бота, выданный при создании @BotFather")
    if config['TELEGRAM_USER_ID'] == 0:
        print("TELEGRAM_USER_ID: Необходимо указать user_id пользователя Telegram")
    if len(config['USER_LIST']) == 0:
        print("USER_LIST: Необходимо указать список аккаунтов Steam, в том порядке, в котором они отображаются SDA. Пример: ['ohmwraith', 'Jessecar96']")
    if not os.path.exists(config['SDA_PATH']):
        print("SDA_PATH: Необходимо указать правильный путь до Steam Desktop Authenticator.exe")


def make_config():
    with open('config.json', 'w') as file:
        text = {
            "API_TOKEN": "",
            "TELEGRAM_USER_ID": 0,
            "SDA_PATH": "C:/SDA-1.0.10/Steam Desktop Authenticator.exe",
            "USER_LIST": [],
            "USER_POINTER": 0
        }
        file.write(json.dumps(text))


if __name__ == "__main__":
    print(load_config())
