import json
import os


class Config:
    def __init__(self, path='config.json'):
        self.content = {
            "TOKEN": "",
            "TELEGRAM_OWNERS_ID": 0,
            "SDA_PATH": "C:/SDA-1.0.10/Steam Desktop Authenticator.exe",
            "ACCOUNT_LIST": [],
        }
        self.account_pointer = 0
        if not self.is_file_exists():
            self.create_config()
            print("Внесите данные в config.json и запустите приложение повторно")
            exit(0)
        else:
            self.load_from_file(path)
            self.check_content()

    def load_from_file(self, path='config.json'):
        with open(path) as file:
            config = file.read()
            try:
                config_json = json.loads(config)
            except Exception as E:
                print("Ошибка чтения конфига: " + E)
                exit(-1)
            self.content['TOKEN'] = config_json['TOKEN']
            self.content['TELEGRAM_OWNERS_ID'] = config_json['TELEGRAM_OWNERS_ID']
            self.content['SDA_PATH'] = config_json['SDA_PATH']
            self.content['ACCOUNT_LIST'] = config_json['ACCOUNT_LIST']
            return config_json

    def save_to_file(self, conf, path='config.json'):
        with open(path, 'w') as file:
            config = file.write(
                str(conf).replace("'", '"').replace(",", ",\n   ").replace("{", "{\n    ").replace("}", "\n}"))
            return


    def get_accounts(self):
        return self.content['ACCOUNT_LIST']

    def get_sda_path(self):
        return self.content['SDA_PATH']

    def get_owners(self):
        return self.content['TELEGRAM_OWNERS_ID']

    def get_token(self):
        return self.content['TOKEN']

    def get_content(self):
        return self.content

    def is_file_exists(self):
        if 'config.json' not in os.listdir():
            return False
        return True

    def set_account_pointer(self, pointer):
        self.account_pointer = pointer

    def get_account_pointer(self):
        return self.account_pointer

    def check_content(self):
        if self.content['TOKEN'] == "":
            print("TOKEN: Необходимо указать токен бота, выданный при создании @BotFather")
            exit(0)
        if self.content['TELEGRAM_OWNERS_ID'] == 0:
            print("TELEGRAM_OWNER_ID: Необходимо указать user_id пользователя Telegram")
        if len(self.content['ACCOUNT_LIST']) == 0:
            print(
                "ACCOUNT_LIST: Необходимо указать список аккаунтов Steam, в том порядке, в котором они отображаются "
                "SDA. Пример: ['ohmwraith', 'Jessecar96']")
        if not os.path.exists(self.content['SDA_PATH']):
            print("SDA_PATH: Необходимо указать правильный путь до Steam Desktop Authenticator.exe")

    def create_config(self):
        with open('config.json', 'w') as file:
            file.write(json.dumps(self.content))


if __name__ == "__main__":
    conf = Config()
    print(conf.load_config())
