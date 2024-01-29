#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
"""2024-01-25 Fil - Future code Yandex.Practicum
Фрактал Пифагорово дерево по параметрам пользователя
Описание в README.md

Fil FC Fractal Фрактал
@fil_fc_fractal_bot
https://t.me/fil_fc_fractal_bot
6833176309:AAHElIZfrCUOoXDCTPAcPmLMrIuzn_RPs5Q
"""
__version__ = '0.2'
__author__ = 'Firip Yamagusi'

from math import sin, cos, radians
from time import time, strftime
from random import choice
import io

from PIL import Image, ImageDraw, ImageFont

import telebot
from telebot import types

# Замените 'YOUR_BOT_TOKEN' на фактический токен вашего бота
TOKEN = '6833176309:AAHElIZfrCUOoXDCTPAcPmLMrIuzn_RPs5Q'
bot_name = "Fil FC Fractal Фрактал | @fil_fc_fractal_bot"
# Для понимания в консоли
print(strftime("%F %T"))
print(bot_name)
print(TOKEN, "\n")

bot = telebot.TeleBot(TOKEN)

funny_numbers = [
    "120, 20, 0, 90",
    "120, 20, 90, 90 (Н-антенна)",
    "70, 10, 45, 45",
    "115, 30, 45, 45",
    "100, 10, 72, 72",
    "100, 1, 15, 15",
    "80, 1, 0, 15",
    "100, 1, 10, 20",
    "90, 30, 45, 45",
    "115, 1, 10, 20",
    "120, 30, 10, 10",
    "120, 1, 60, 60 (соты)",

    "70, 25, 36, 36",
    "120, 25, 10, 10",
    "120, 30, 45, 45",
    "100, 30, 80, 45",
    "111, 25, 80, 80",
    "111, 11, 80, 80",
    "120, 1, 45, 45",
    "120, 14, 45, 45",
    "100, 9, 30, 45",
    "120, 30, 90, 90",
    "120, 20, 45, 45",
    "120, 1, 45, 90",
]


def draw_pythagoras_tree(
        draw: ImageDraw.Draw,
        x_start: int, y_start: int,
        length: int, length_delta: int,
        angle: int, angle_left: int, angle_right: int,
        depth: int):
    """Рекурсивная прорисовка дерева Пифагора на глубину depth"""
    if depth == 0:
        return

    colors = ["blue", "red", "green", "black", "brown"]
    x_end = x_start + int(length * cos(radians(angle)))
    y_end = y_start - int(length * sin(radians(angle)))

    draw.line(
        [(x_start, y_start), (x_end, y_end)],
        fill=colors[depth % len(colors)], width=depth)

    draw_pythagoras_tree(
        draw, x_end, y_end,
        length - length_delta, length_delta,
        angle + angle_right, angle_left, angle_right,
        depth - 1)
    draw_pythagoras_tree(
        draw, x_end, y_end,
        length - length_delta, length_delta,
        angle - angle_left, angle_left, angle_right,
        depth - 1)


user_data = {}

# Стартовые значения параметров
DEFAULT_VALUES = {
    'Длина': 120, 'Уменьшение': 12, 'Угол влево': 30, 'Угол вправо': 45
}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    user_data[user_id] = {'numbers': DEFAULT_VALUES.copy()}
    bot.send_message(
        message.chat.id,
        '<b>Бот рисует варианты фрактала "Дерево Пифагора".</b>\n\n'
        'Меняйте четыре параметра и получите свой фрактал!\n\n'
        '<b>Длина</b> - начальный размер линии-"веточки":\n'
        'Целое число от 70 до 120\n\n'
        '<b>Уменьшение</b> - насколько следующий уровень короче:\n'
        'Целое число от 1 до 30\n\n'
        '<b>Угол влево</b> - отклонение влево на каждом уровне:\n'
        'Целое число от 0 до 90 (градусы)\n\n'
        '<b>Угол вправо</b> - отклонение вправо на каждом уровне:\n'
        'Целое число от 0 до 90 (градусы)\n\n'
        'В ответ вы получите изображение вашего Дерева Пифагора!\n\n'
        '<i>Кстати, код телеграм-бота и код прорисовки фрактала на спор '
        'полностью написан нейросетью по текстовому описанию задачи. '
        'Меньше, чем за 20 уточняющих запросов! <b>Нейросети - сила!</b></i>',
        parse_mode="HTML")
    send_number_buttons(message)

# Отправка кнопок для ввода числа
def send_number_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # решил всё-таки убрать Нарисовать
    buttons = [
        'Длина', 'Уменьшение', 'Угол влево', 'Угол вправо'
    ]
    # for btn in buttons:
    #     markup.add(types.KeyboardButton(btn))
    markup.add(* buttons)
    bot.send_message(
        message.chat.id,
        'Выберите параметр и введите значение:',
        reply_markup=markup)

# Обработчик ввода числа
@bot.message_handler(func=lambda message: message.text in [
    'Длина', 'Уменьшение', 'Угол влево', 'Угол вправо'])
def handle_number_input(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {'numbers': DEFAULT_VALUES.copy()}
    selected_parameter = message.text

    # Пользователь выбрал параметр
    user_data[user_id]['selected_parameter'] = selected_parameter
    bot.send_message(user_id, f'Введите число для {selected_parameter}:')

# Обработчик ввода числа
@bot.message_handler(func=lambda message: message.text.replace('-',
                                                               '').isdigit())
def handle_number_value(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {'numbers': DEFAULT_VALUES.copy()}
        user_data[user_id]['selected_parameter'] = 'Уменьшение'
    selected_parameter = user_data[user_id].get('selected_parameter')

    if selected_parameter is not None:
        entered_number = int(message.text)

        # Проверяем, что введенное число соответствует разрешенному диапазону
        allowed_ranges = {
            'Длина': (70, 120), 'Уменьшение': (1, 30),
            'Угол влево': (0, 90), 'Угол вправо': (0, 90)}

        if (allowed_ranges[selected_parameter][0] <= entered_number
                <= allowed_ranges[selected_parameter][1]):
            # Сохраняем введенное число под выбранным параметром
            user_data[user_id]['numbers'][selected_parameter] = entered_number
            bot.send_message(
                user_id,
                f'Число {entered_number} для '
                f'{selected_parameter} сохранено.')

            # Если введены все 4 числа, отправляем кнопку "Нарисовать"
            if len(user_data[user_id]['numbers']) == 4:
                send_draw_button(message)
            else:
                send_number_buttons(message)
        else:
            bot.send_message(
                user_id,
                f'Пожалуйста, введите число в диапазоне от '
                f'{allowed_ranges[selected_parameter][0]} до '
                f'{allowed_ranges[selected_parameter][1]}.')
    else:
        bot.send_message(user_id, 'Выберите параметр и введите значение.')

# Обработчик кнопки "Нарисовать"
@bot.message_handler(func=lambda message: message.text == 'Нарисовать')
def send_draw_button(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {'numbers': DEFAULT_VALUES.copy()}
    if len(user_data[user_id]['numbers']) == 4:
        image = create_image(user_data[user_id]['numbers'])
        bot.send_photo(user_id, image)
        bot.send_message(
            user_id,
            'Попробуйте ещё прикольное сочетание:\n'
            f'{choice(funny_numbers)}')
        # После отправки изображения отправляем кнопки снова
        send_number_buttons(message)
    else:
        bot.send_message(
            user_id,
            'Введите все 4 числа перед тем, как нарисовать.')

# Обработчик нечислового ввода
@bot.message_handler(
    func=lambda message: not message.text.replace('-', '').isdigit())
def handle_non_number_input(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {'numbers': DEFAULT_VALUES.copy()}
    bot.send_message(user_id, 'Пожалуйста, введите число.')

# Создание изображения с числами
def create_image(numbers):
    # Создаем изображение
    print(strftime("%F %T"), numbers)
    image_size = 800
    background_color = "#FAEBD7"

    image = Image.new(
        "RGB", (image_size, image_size), background_color)
    draw = ImageDraw.Draw(image)

    x_initial, y_initial = image_size // 2, 4 * image_size // 5
    length_initial = numbers['Длина']
    length_delta_initial = numbers['Уменьшение']
    angle_initial = 90
    angle_initial_left = numbers['Угол влево']
    angle_initial_right = numbers['Угол вправо']
    depth_initial = 8

    draw_pythagoras_tree(
        draw,
        x_initial, y_initial,
        length_initial, length_delta_initial,
        angle_initial, angle_initial_left, angle_initial_right,
        depth_initial)

    # Сохраняем изображение в формате PNG
    # font = ImageFont.load_default(size=40)
    # font_small = ImageFont.load_default(size=20)
    # font = ImageFont.truetype(font="vga866.fon", size=40.0)
    # font_small = ImageFont.truetype(font="vga866.fon", size=20.0)
    font = ImageFont.truetype(font="verdana.ttf", size=40)
    font_small = ImageFont.truetype(font="verdana.ttf", size=20)
    # font = ImageFont.truetype()
    # font_small = ImageFont.truetype()
    # Формируем строку с числами
    numbers_str = \
        (f"Length = {length_initial}; "
         f"Delta = {length_delta_initial};  "
         f"Angle_Left = {angle_initial_left}; "
         f"Angle_Right = {angle_initial_right}")

    # Рисуем текст на изображении
    draw.text(
        (10, image_size - 90),
        "Pythagoras tree | @fil_fc_fractal_bot", font=font, fill='black')
    draw.text(
        (10, image_size - 35),
        numbers_str, font=font_small, fill='black')

    # image.save("pythagoras_tree.png", "PNG")

    # Сохраняем изображение в байтовом потоке
    image_stream = io.BytesIO()
    image.save(image_stream, format='PNG')
    image_stream.seek(0)

    return image_stream

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
