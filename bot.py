import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import LabeledPrice
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)

PRICE = LabeledPrice(label="Доступ к каналу", amount=500*100)  # 500 RUB в копейках

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "🎟️ Купите доступ к приватному каналу за 500 ₽",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("💰 Оплатить", pay=True)
        )
    )

@dp.pre_checkout_query_handler()
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    await message.answer(
        "✅ Оплата прошла успешно! Вот ссылка: https://t.me/your_channel",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("Перейти в канал", url="https://t.me/your_channel")
        )
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
