import asyncio
import aiohttp

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "ВСТАВЬ_ТЕЛЕГРАМ_ТОКЕН"
GEMINI_KEY = "ВСТАВЬ_GEMINI_KEY"

bot = Bot(token=TOKEN)
dp = Dispatcher()

keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🤖 ИИ")]],
    resize_keyboard=True
)

users = set()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Бот работает 🤖", reply_markup=keyboard)

@dp.message(F.text == "🤖 ИИ")
async def on(message: Message):
    users.add(message.from_user.id)
    await message.answer("ИИ включён")

async def ask_ai(text: str):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"

    payload = {
        "contents": [{"parts": [{"text": text}]}]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as r:
            data = await r.json()
            try:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except:
                return "Ошибка"

@dp.message()
async def chat(message: Message):
    if message.from_user.id not in users:
        await message.answer("Нажми 🤖 ИИ")
        return

    reply = await ask_ai(message.text)
    await message.answer(reply)

async def main():
    print("BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    print("TOKEN =", repr(TOKEN))
