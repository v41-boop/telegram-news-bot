import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import img2pdf
from pdf2docx import Converter

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

user_mode = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("📄 PDF ➜ Word", callback_data="pdf_word")],
        [InlineKeyboardButton("🖼 صورة ➜ PDF", callback_data="img_pdf")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "اختر نوع التحويل:",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_mode[query.from_user.id] = query.data

    await query.edit_message_text("📤 أرسل الملف للتحويل")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    if user_id not in user_mode:
        await update.message.reply_text("اختر نوع التحويل أولاً /start")
        return

    mode = user_mode[user_id]

    file = await update.message.document.get_file()
    filename = update.message.document.file_name

    await file.download_to_drive(filename)

    if mode == "pdf_word":

        output = "output.docx"

        cv = Converter(filename)
        cv.convert(output)
        cv.close()

        await update.message.reply_document(document=open(output,"rb"))

    elif mode == "img_pdf":

        output = "output.pdf"

        with open(output,"wb") as f:
            f.write(img2pdf.convert(filename))

        await update.message.reply_document(document=open(output,"rb"))

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

print("Bot Running...")

app.run_polling()
