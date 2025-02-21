import asyncio
import json
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router

bot = Bot(TOKEN)
dp = Dispatcher()
dp.include_router(router)


async def handler(event, context):
    try:
        if event and isinstance(event, dict) and 'messages' in event:
            for message in event['messages']:
                if 'details' in message and 'message' in message['details']:
                    update = json.loads(message['details']['message']['body'])
                    await dp.feed_webhook_update(bot, update)
    finally:
        await bot.session.close()

    return {
        'statusCode': 200,
        'body': 'OK'
    }


# Точка входа для Яндекс Функций
def entrypoint(event, context):
    return asyncio.get_event_loop().run_until_complete(handler(event, context))