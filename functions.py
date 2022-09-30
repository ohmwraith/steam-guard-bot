import win32gui
import win32ui
import os
import keyboard
import win32con
from ctypes import windll
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# Если SDA не запущен запускает его
def start_sda(path):
    hwnd = win32gui.FindWindow(None, 'Steam Desktop Authenticator')
    if hwnd == 0:
        os.startfile('"' + path + '"')
        return ("SDA запущен")
    else:
        return ("SDA уже запущен")


def close_sda():
    hwnd = win32gui.FindWindow(None, 'Steam Desktop Authenticator')
    if hwnd != 0:
        hwndDC = win32gui.GetWindowDC(hwnd)
        try:
            win32gui.PostMessage(hwndDC, win32con.WM_CLOSE, 0, 0)
        except Exception as E:
            print("Ошибка при закрытии SDA. Закройте приложение перед запуском бота.")


# Помещает SDA на передний план
def focus_sda():
    hwnd = win32gui.FindWindow(None, 'Steam Desktop Authenticator')
    try:
        win32gui.SetForegroundWindow(hwnd)
    except Exception:
        err = "SDA не запущен"


# переключает указатель на список аккаунтов после запуска SDA
def select_account_list():
    keyboard.press('tab')
    keyboard.press('tab')
    keyboard.press('tab')
    keyboard.press('down')


def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size

    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)

    return im


# Изменяет текущего пользователя
def change_user_select(users, target_user, users_pointer):
    for target_user_position in range(0, len(users)):
        if users[target_user_position] == target_user:

            steps = target_user_position - users_pointer

            if steps > 0:
                for i in range(steps, 0, -1):
                    keyboard.press('down')
                    users_pointer += 1

            elif steps < 0:
                steps *= -1
                for i in range(steps, 0, -1):
                    keyboard.press('up')
                    users_pointer -= 1

            return users_pointer


# Возвращает картинку с отрисованной ошибкой
def render_error_image(message):
    font = ImageFont.truetype(r'fonts/AvenirNextCyr-Medium.ttf', 45)
    font_small = ImageFont.truetype(r'fonts/AvenirNextCyr-Medium.ttf', 20)

    image = Image.new("RGB", (320, 85), "red")
    draw = ImageDraw.Draw(image)

    draw.text((55, 5), "ОШИБКА", align='center', font=font)
    draw.text((10, 55), message, align='center', font=font_small)
    return image


# Добавляет оформление к выводу
def add_frame_to_image(image):
    frame = Image.open("img/frame.png")
    image.paste(frame, (0, 0), frame)
    return image


# Создает скриншот
def make_sda_screenshot():
    hwnd = win32gui.FindWindow(None, 'Steam Desktop Authenticator')
    if hwnd != 0:
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top

        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)

        result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)

        im_crop = im.crop((15, 95, 335, 180))

        if result == 1:
            width, height = im_crop.size
            black_flag = False
            for i in range(1, width):
                if im_crop.getpixel((i, 1)) == (0, 0, 0):
                    black_flag = True
                    break
            if black_flag == True:
                print("SDA свернут, невозможно сделать скриншот")
                render_error_image("SDA свернут на сервере").save('output.png')
            else:
                add_frame_to_image(im_crop).save('output.png')
    else:
        print("SDA не запущен на сервере")
        render_error_image("SDA не запущен на сервере").save('output.png')


if __name__ == '__main__':
    make_sda_screenshot()
