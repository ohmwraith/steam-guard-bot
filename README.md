<h1 align="center">
  <img  src="https://user-images.githubusercontent.com/44874495/193207668-c9b5cec7-0e8c-43b5-af50-37a117d77d8f.png" height="64" width="64" />
  <br/>
  Telegram Steam Guard Bot
</h1>
<p align="center">
  Telegram бот для использования 2FA Steam Guard.<br/>
  <sup>Это мой личный проект, он <b>никак не связан со Steam и Scrap.</b>
</p>
<img align="center" src="https://user-images.githubusercontent.com/44874495/193208264-d2dc46c2-2f2c-443a-ad0c-030ae97d1abf.png" width="1920">
Спасибо <a href="https://github.com/Jessecar96/">Jessecar96</a> за <a href="https://github.com/Jessecar96/SteamDesktopAuthenticator/">пк-версию</a> Steam Guard
<h3 align="left">
  Установка
</h3>
<hr>
<ul>
  <li>Скачайте и настройте 2FA в <a href="https://github.com/Jessecar96/SteamDesktopAuthenticator/releases/latest">SDA</a></li>
  <li>Загрузите <a href="https://github.com/ohmwraith/steam-guard-bot/releases/latest">последнюю версию</a></li>
  <li>Установите <a href="https://pypi.org/project/pywin32/">pywin32</a></li>
  <li>Создайте бота через @BotFather в Telegram</a></li>
  <li>Запустите bot.py, чтобы создать конфиг и узнать свой user_id</li>
  <li>Укажите токен, путь до SDA и user_id в config.json</li>
  <li>Перезапустите бота</li>
</ul>
<h3 align="left">
Конфиг
</h3>
<hr>
Пример настройки `config.json`:

```python
{
    "TOKEN": "3213123:klnjifawNFDOnjfJGIRkfnmvdc", # Токен бота
    "TELEGRAM_OWNERS_ID": [56530123, 3123154], # ID аккаунта, с которого вы будете получать коды
    "SDA_PATH": "C:/SDA-1.0.10/Steam Desktop Authenticator.exe",
    "ACCOUNT_LIST": [
      "ohmwraith",
      "Jessecar96"
      ], # Список аккаунтов в SDA
}
```
