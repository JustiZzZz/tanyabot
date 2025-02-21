from aiogram import F, Router
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, CallbackQuery
import keyboards as kb
from aiogram.types import ReplyKeyboardRemove
import random
from config import PHOTO_IDS, HOT_IDS, TEXT_LOADING, TEXT_LOVE, TEXT_TRUE, Y_TOKEN, DATE_LIST, START_DATE, \
    AWS_ACCESS_KEY_ID, AWS_ACCESS_SECRET_KEY, BUCKET_NAME, TODO_FILE, SERVICE_NAME, ENDPOINT_URL
import yandex_music
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from yandex_music import Client
from datetime import datetime, date
import boto3
import json
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio
router = Router()


class TodoStates(StatesGroup):
    waiting_for_task = State()
    waiting_for_delete = State()


# Инициализация S3 клиента
s3 = boto3.client(
    service_name=SERVICE_NAME,
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_ACCESS_SECRET_KEY
)


# Функции для работы с хранилищем
async def load_todos():
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=TODO_FILE)
        return json.loads(response['Body'].read())
    except:
        return []


async def save_todos(todos):
    try:
        for i, task in enumerate(todos, 1):
            task["id"] = i
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=TODO_FILE,
            Body=json.dumps(todos)
        )
        return True
    except Exception as e:
        print(f"Error saving todos: {e}")
        return False


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        'Привет моя любовь!❤️ Я написал этого бота с целью делать тебе приятно, даже когда меня нету(\n'
        'Ты всегда меня заряжаешь, позволяя мне иметь силы для почти любых моих стремлений... '
        'И на самом деле у меня такого не было никогда😮\n'
        'Твоя забота обо мне, твой невероятный ум и твои стремления только подталкивают на то, '
        'чтобы постоянно работать над собой, удивляя в том числе и тебя!!!\n'
        'Давай я попробую провести тебе маленькую экскурсию по функционалу этой бандурины, '
        'а хотя, потыкай и узнаешь)\n'
        'Я тебя люблю!!!❤️',
        reply_markup=kb.main_menu
    )


@router.message(F.text.in_({'Ссылочки🔗', 'Фоточки📷', 'Люблю💞', 'Тыкни📌', 'Я рядом🫂'}))
async def handle_menu(message: Message):
    teext = random.choice(TEXT_LOADING)
    await message.answer(teext, reply_markup=ReplyKeyboardRemove())
    keyboards = {
        'Ссылочки🔗': kb.links_menu,
        'Фоточки📷': kb.photos_menu,
        'Люблю💞': kb.love_menu,
        'Тыкни📌': kb.click_menu,
        'Я рядом🫂': kb.near_menu
    }
    keyboard = keyboards.get(message.text)
    await message.answer('Что ты выберешь, золото?❤️', reply_markup=keyboard)


@router.callback_query(F.data == 'show_random_photo')
async def handle_random_photo(callback: CallbackQuery):
    random_photo_id = random.choice(PHOTO_IDS)
    await callback.message.answer_photo(photo=random_photo_id)
    await callback.message.answer('Что теперь хочешь выбрать😈', reply_markup=kb.photos_menu)
    await callback.answer()


@router.callback_query(F.data == 'show_hot_photo')
async def handle_random_photo(callback: CallbackQuery):
    random_hot_photo_id = random.choice(HOT_IDS)
    await callback.message.answer_photo(
        photo=random_hot_photo_id,
        has_spoiler=True
    )
    await callback.message.answer('Что теперь хочешь выбрать😈', reply_markup=kb.photos_menu)
    await callback.answer()


@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'ID фото: {message.photo[-1].file_id}')


@router.callback_query(F.data == 'love_compliment')
async def handle_love(callback: CallbackQuery):
    lovetext = random.choice(TEXT_LOVE)
    await callback.answer(lovetext, show_alert=True)


@router.callback_query(F.data == 'love_confession')
async def handle_love(callback: CallbackQuery):
    lovetext2 = random.choice(TEXT_TRUE)
    await callback.answer(lovetext2, show_alert=False)


@router.callback_query(F.data == 'yandex_music')
async def handle_random_track(callback: CallbackQuery):
    client = Client(Y_TOKEN).init()
    liked_tracks = client.users_likes_tracks()
    random_track = random.choice(liked_tracks.tracks)
    full_track = client.tracks([random_track.track_id])[0]
    artists = ', '.join(artist.name for artist in full_track.artists)
    track_url = f"https://music.yandex.ru/album/{full_track.albums[0].id}/track/{random_track.track_id}"
    colon_count = track_url.count(':')
    if colon_count >= 2:
        second_colon_index = track_url.find(':', track_url.find(':') + 1)
        track_url = track_url[:second_colon_index]
    track_info = f"Это трек из моих любимых Яндекс Музыки в реальном времени)\n🎵 {full_track.title}\n👤 {artists}\n🔗 {track_url}"
    await callback.message.reply(track_info)
    await callback.message.answer('Что теперь хочешь выбрать?😊', reply_markup=kb.click_menu)
    await callback.answer()


@router.callback_query(F.data == 'dates')
async def handle_click_me(callback: CallbackQuery):
    today = date.today()
    days_together = (today - START_DATE).days
    random_message = random.choice(DATE_LIST)
    await callback.message.answer(
        f"Мы вместе {days_together} дней ❤️\n{random_message}"
    )
    await callback.message.answer(
        'Что теперь хочешь выбрать?😊',
        reply_markup=kb.click_menu
    )
    await callback.answer()


@router.callback_query(F.data == "write_task")
async def handle_new_task(callback: CallbackQuery, state: FSMContext):
    # Сохраняем предыдущее сообщение для последующего удаления
    await state.update_data(last_message=callback.message.message_id)
    # Отправляем новое сообщение и сохраняем его ID
    msg = await callback.message.answer("Напиши задачку, золотце)")
    await state.update_data(prompt_message=msg.message_id)
    await state.set_state(TodoStates.waiting_for_task)


@router.message(TodoStates.waiting_for_task)
async def save_task(message: Message, state: FSMContext):
    try:
        # Загружаем существующие задачи
        todos = await load_todos()

        # Создаем новую задачу
        new_task = {
            "id": len(todos) + 1,
            "text": message.text,
            "author": message.from_user.full_name,
            "date": datetime.now().isoformat()
        }

        # Добавляем задачу в список
        todos.append(new_task)

        # Делаем несколько попыток сохранения с увеличивающимися интервалами
        max_retries = 3
        save_success = False

        for attempt in range(max_retries):
            save_success = await save_todos(todos)
            if save_success:
                break
            # Экспоненциальная задержка между попытками
            await asyncio.sleep(2 ** attempt)

            # Если сохранение не удалось, попробуем сначала очистить список
            if attempt == max_retries - 1 and not save_success:
                todos = await load_todos()  # Перезагружаем актуальный список
                todos.append(new_task)  # Добавляем задачу заново
                save_success = await save_todos(todos)

        if not save_success:
            await message.answer("Произошла ошибка при сохранении задачи. Попробуйте еще раз.")
            return

        # Получаем сохраненные ID сообщений
        data = await state.get_data()

        # Очищаем состояние
        await state.clear()

        # Отправляем подтверждение
        await message.answer("УРА УРА УРА👑")
        await message.answer("Что теперь хочешь выбрать?😊", reply_markup=kb.near_menu)

    except Exception as e:
        print(f"Error in save_task: {e}")
        await message.answer("Произошла ошибка. Попробуйте еще раз.")
        await state.clear()


@router.callback_query(F.data == "list_task")
async def show_tasks(callback: CallbackQuery):
    todos = await load_todos()
    if not todos:
        await callback.message.answer("Список пуст(")
        await callback.message.answer("Что теперь хочешь выбрать?😊", reply_markup=kb.near_menu)
        return
    task_list = "\n".join([
        f"{task['id']}. {task['text']} ({task['author']})"
        for task in todos
    ])
    await callback.message.answer(
        f"Список задач:\n\n{task_list}",
        reply_markup=kb.tasks_menu
    )


@router.callback_query(F.data == "waiting_for_delete")
async def handle_delete_request(callback: CallbackQuery):
    todos = await load_todos()
    if not todos:
        await callback.message.answer("Список пуст(")
        await callback.message.answer("Что теперь хочешь выбрать?😊", reply_markup=kb.near_menu)
        return

    # Создаем inline клавиатуру с номерами задач
    keyboard = InlineKeyboardBuilder()
    for task in todos:
        keyboard.button(
            text=f"{task['id']}",
            callback_data=f"delete_{task['id']}"
        )
    keyboard.button(text="Вернуться назад", callback_data="back")
    keyboard.adjust(3)  # По 3 кнопки в ряд

    task_list = "\n".join([
        f"{task['id']}. {task['text']}"
        for task in todos
    ])
    await callback.message.answer(
        f"Выбери номер задачки для удаления, золотце:\n\n{task_list}",
        reply_markup=keyboard.as_markup()
    )


@router.callback_query(F.data.startswith("delete_"))
async def process_delete_task(callback: CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    todos = await load_todos()

    if not any(task["id"] == task_id for task in todos):
        await callback.message.answer("Не нашли задачку(((")
        return

    todos = [task for task in todos if task["id"] != task_id]
    await save_todos(todos)
    await callback.message.answer("Удалили, солнце💖")
    await callback.message.answer("Что теперь хочешь выбрать?😊", reply_markup=kb.near_menu)


@router.callback_query(F.data == 'back')
async def back_to_start(callback: CallbackQuery):
    await callback.message.answer(
        'Что теперь хочешь выбрать?😊',
        reply_markup=kb.near_menu
    )
    await callback.answer()


@router.callback_query(F.data == 'back_start')
async def back_to_start(callback: CallbackQuery):
    await callback.message.answer(
        'А что сейчас посмотрим, золотце?❤️',
        reply_markup=kb.main_menu
    )
    await callback.answer()