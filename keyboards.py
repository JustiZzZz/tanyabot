from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ссылочки🔗'),
            KeyboardButton(text='Фоточки📷'),
        ],
        [
            KeyboardButton(text='Люблю💞'),
            KeyboardButton(text='Тыкни📌'),
            KeyboardButton(text='Я рядом🫂'),
        ]
    ],
    resize_keyboard=True,
    persistent=True
)

# Меню для раздела "Ссылки"
links_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Ролик..?', url='https://www.youtube.com/watch?v=xm3YgoEiEDc'),
        InlineKeyboardButton(text='Ты сегодня:', url='https://catsgenerator.ru/')
    ],
    [InlineKeyboardButton(text='Мой канал в детстве)', url='https://www.youtube.com/@tto3utub4uk8/videos')],
    [InlineKeyboardButton(text='Вернуться в начало', callback_data='back_start')]
])

# Меню для раздела "Фоточки"
photos_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Я😉', callback_data='show_random_photo'),
        InlineKeyboardButton(text='🔞', callback_data='show_hot_photo'),
    ],
    [InlineKeyboardButton(text='Вернуться в начало', callback_data='back_start')]
])

# Меню для раздела "Люблю"
love_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Признание', callback_data='love_confession'),
        InlineKeyboardButton(text='Комплимент', callback_data='love_compliment')
    ],
    [InlineKeyboardButton(text='Вернуться в начало', callback_data='back_start')]
])

click_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Хорошие даты📅', callback_data='dates'),
        InlineKeyboardButton(text='Моя Я.Музыка🎧', callback_data='yandex_music')
    ],
    [InlineKeyboardButton(text='Вернуться в начало', callback_data='back_start')]
])

# Меню для раздела "Я рядом"
near_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='+Задачка', callback_data='write_task'),
        InlineKeyboardButton(text='Список тасков', callback_data='list_task')
    ],
    [InlineKeyboardButton(text='Вернуться в начало', callback_data='back_start')]
])


tasks_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Удалить', callback_data='waiting_for_delete'),
        InlineKeyboardButton(text='Вернуться назад', callback_data='back')
    ]
])
