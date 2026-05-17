import requests

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from openai import OpenAI

# =====================================
# TOKENS
# =====================================

BOT_TOKEN = "PASTE_BOT_TOKEN"

OPENAI_API_KEY = "PASTE_OPENAI_API_KEY"

CRYPTO_PAY_API_TOKEN = "PASTE_CRYPTOBOT_TOKEN"

# =====================================
# OPENAI
# =====================================

client = OpenAI(
    api_key=OPENAI_API_KEY
)

# =====================================
# TELEGRAM
# =====================================

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher(bot)

# =====================================
# MEMORY
# =====================================

user_memory = {}

# =====================================
# MENU
# =====================================

def menu():

    kb = InlineKeyboardMarkup(row_width=1)

    post_btn = InlineKeyboardButton(
        text="✍️ Создать пост",
        callback_data="post"
    )

    hook_btn = InlineKeyboardButton(
        text="🔥 Viral Hook",
        callback_data="hook"
    )

    ideas_btn = InlineKeyboardButton(
        text="🎬 Reels идеи",
        callback_data="ideas"
    )

    premium_btn = InlineKeyboardButton(
        text="💎 Premium",
        callback_data="premium"
    )

    kb.add(post_btn)
    kb.add(hook_btn)
    kb.add(ideas_btn)
    kb.add(premium_btn)

    return kb

# =====================================
# START
# =====================================

@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    text = """
🚀 CreatorFlow

AI для creators.

Что умеет:
• Telegram посты
• Viral hooks
• Reels идеи
• Контент планы

Выберите функцию 👇
"""

    await message.answer(
        text,
        reply_markup=menu()
    )

# =====================================
# POST
# =====================================

@dp.callback_query_handler(text="post")
async def post(callback: types.CallbackQuery):

    prompt = """
Напиши мощный Telegram пост
про заработок в интернете.

Сделай:
• hook
• эмоции
• CTA
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    await callback.message.answer(answer)

# =====================================
# HOOK
# =====================================

@dp.callback_query_handler(text="hook")
async def hook(callback: types.CallbackQuery):

    prompt = """
Напиши 10 viral hooks
для TikTok про бизнес.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    await callback.message.answer(answer)

# =====================================
# IDEAS
# =====================================

@dp.callback_query_handler(text="ideas")
async def ideas(callback: types.CallbackQuery):

    prompt = """
Придумай 10 viral Reels идей
для Telegram creators.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    await callback.message.answer(answer)

# =====================================
# CRYPTO PAYMENT
# =====================================

def create_invoice():

    url = "https://pay.crypt.bot/api/createInvoice"

    headers = {
        "Crypto-Pay-API-Token": CRYPTO_PAY_API_TOKEN
    }

    data = {
        "asset": "USDT",
        "amount": "9",
        "description": "CreatorFlow Premium"
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    return response.json()

# =====================================
# PREMIUM
# =====================================

@dp.callback_query_handler(text="premium")
async def premium(callback: types.CallbackQuery):

    invoice = create_invoice()

    if invoice.get("ok"):

        pay_url = invoice["result"]["pay_url"]

        text = f"""
💎 CreatorFlow Premium

Что входит:
• Безлимит
• Viral prompts
• Premium AI
• Быстрые ответы

Оплата:
{pay_url}
"""

        await callback.message.answer(text)

    else:

        await callback.message.answer(
            "❌ Ошибка оплаты"
        )

# =====================================
# RUN
# =====================================

if __name__ == "__main__":

    print("CreatorFlow started")

    executor.start_polling(
        dp,
        skip_updates=True
    )