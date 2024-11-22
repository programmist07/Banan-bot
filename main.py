import os
import json
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = "7725512276:AAGsKNGw1xskltcoWfdBnRG3TW-9V_-51Dg"
BOT_USERNAME: Final = '@OOOLLMMAA_bot'

# JSON faylga ma'lumotlarni saqlash
def save_to_json(data: dict, filename: str = "user_data.json"):
    try:
        # Fayl mavjudligini tekshirish
        if os.path.exists(filename):
            with open(filename, "r") as file:
                existing_data = json.load(file)
        else:
            print(f"{filename} fayli topilmadi. Yangi fayl yaratilmoqda.")
            existing_data = []

        # Yangi ma'lumotlarni qo'shish
        existing_data.append(data)

        # JSON faylga yozish
        with open(filename, "w") as file:
            json.dump(existing_data, file, indent=4)
            print(f"Ma'lumot muvaffaqiyatli saqlandi: {data}")
    except Exception as e:
        print(f"JSON faylga yozishda xatolik: {e}")

# Botning buyruqlari
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Thanks for chatting with me! I am a banana!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am a banana! Please type something so I can respond!")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command!")

# Foydalanuvchi xabarlariga javob beruvchi funksiya
def handler_response(text: str):
    processed: str = text.lower()
    if "hello" in processed:
        return "Hey there!"
    if "how are you" in processed:
        return "I'm better!"
    if "i love python" in processed:
        return "Remember to subscribe!"
    else:
        return "Used 🧠"

# Xabarlarni qayta ishlash
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    user_id = update.message.chat_id
    username = update.message.chat.username
    first_name = update.message.chat.first_name

    # Foydalanuvchi ma'lumotlarini yig'ish
    user_data = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "text": text,
        "timestamp": update.message.date.isoformat(),
    }
    print(f"Qabul qilingan ma'lumot: {user_data}")

    # Ma'lumotlarni JSON faylga saqlash
    save_to_json(user_data)

    # Foydalanuvchiga javob yuborish
    response: str = handler_response(text)
    print('Bot:', response)
    await update.message.reply_text(response)

# Xatoliklarni qayd etish
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

# Botni ishga tushirish
if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Buyruqlarni ishlovchilarni ro'yxatdan o'tkazish
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    # Xabarlar uchun ishlovchi
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Xatoliklar uchun ishlovchi
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)
