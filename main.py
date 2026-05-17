import os
import requests

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from openai import OpenAI

# =========================
# ENV
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CRYPTO_PAY_API_TOKEN = os.getenv("CRYPTO_PAY_API_TOKEN")

# =========================
# OPENAI
# =========================

client = OpenAI(api_key=OPENAI_API_KEY)

# =========================
# TELEGRAM
# =========================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# =========================
# MEMORY (simple)
# =========================

user_memory = {}

# =========================
# MENU
# =========================

def menu():
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton("✍️ Создать пост", callback_data="post"),
        InlineKeyboardButton("🔥 Viral Hooks", callback_data="hook"),
        InlineKeyboardButton("🎬 Reels идеи", callback_data="ideas"),
        InlineKeyboardButton("💎 Premium", callback_data="premium"),
    )

    return kb

# =========================
# START
# =========================

@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    await message.answer(
        "🚀 CreatorFlow\n\nAI для creators\n\nВыбери функцию 👇",
        reply_markup=menu()
    )

# =========================
# AI FUNCTION
# =========================

def ask_ai(prompt: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# =========================
# CALLBACKS
# =========================

@dp.callback_query_handler(text="post")
async def post(call: types.CallbackQuery):

    prompt = """
Напиши мощный Telegram пост про заработок в интернете.

Добавь:
- hook
- эмоции
- CTA
"""

    await call.message.answer(ask_ai(prompt))


@dp.callback_query_handler(text="hook")
async def hook(call: types.CallbackQuery):

    prompt = """
Сгенерируй 10 viral hooks для TikTok про бизнес и деньги.
"""

    await call.message.answer(ask_ai(prompt))


@dp.callback_query_handler(text="ideas")
async def ideas(call: types.CallbackQuery):

    prompt = """
Придумай 10 идей для Reels/TikTok про контент и бизнес.
"""

    await call.message.answer(ask_ai(prompt))

# =========================
# CRYPTO PAY
# =========================

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

    try:
        r = requests.post(url, headers=headers, json=data, timeout=10)
        return r.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}

# =========================
# PREMIUM
# =========================

@dp.callback_query_handler(text="premium")
async def premium(call: types.CallbackQuery):

    invoice = create_invoice()

    if invoice.get("ok"):
        pay_url = invoice["result"]["pay_url"]

        await call.message.answer(
            f"""💎 CreatorFlow Premium

✔ Безлимит AI
✔ Viral prompts
✔ Быстрые ответы

💳 Оплата:
{pay_url}
"""
        )
    else:
        await call.message.answer("❌ Payment error")

# =========================
# RUN
# =========================

if __name__ == "__main__":
    print("🚀 CreatorFlow started")

    executor.start_polling(
        dp,
        skip_updates=True
    )