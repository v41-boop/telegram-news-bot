import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# دالة لعرض قائمة الأخبار حسب الفئة
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("تقنية", callback_data='technology')],
        [InlineKeyboardButton("رياضة", callback_data='sports')],
        [InlineKeyboardButton("أخبار عامة", callback_data='general')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('اختر نوع الأخبار:', reply_markup=reply_markup)

# دالة لجلب الأخبار من NewsAPI
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    category = query.data
    url = f'https://newsapi.org/v2/top-headlines?country=eg&category={category}&apiKey={NEWS_API_KEY}'
    response = requests.get(url).json()
    articles = response.get('articles', [])[:5]
    message = ""
    for art in articles:
        message += f"{art['title']}\n{art['url']}\n\n"
    query.edit_message_text(text=message if message else "لا توجد أخبار حالياً.")

# تشغيل البوت
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("البوت يعمل…")
app.run_polling()
