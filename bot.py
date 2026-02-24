import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# التحقق من المتغيرات
if not TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN غير موجود في متغيرات البيئة")

if not NEWS_API_KEY:
    raise ValueError("❌ NEWS_API_KEY غير موجود في متغيرات البيئة")


# ✅ دالة start (لازم async)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("تقنية", callback_data="technology")],
        [InlineKeyboardButton("رياضة", callback_data="sports")],
        [InlineKeyboardButton("أخبار عامة", callback_data="general")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "اختر نوع الأخبار:",
        reply_markup=reply_markup
    )


# ✅ دالة الأزرار
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category = query.data
    url = f"https://newsapi.org/v2/top-headlines?country=eg&category={category}&apiKey={NEWS_API_KEY}"

    try:
        response = requests.get(url).json()
        articles = response.get("articles", [])[:5]

        if not articles:
            message = "لا توجد أخبار حالياً."
        else:
            message = ""
            for art in articles:
                title = art.get("title", "بدون عنوان")
                link = art.get("url", "")
                message += f"{title}\n{link}\n\n"

        await query.edit_message_text(text=message)

    except Exception as e:
        await query.edit_message_text(
            text=f"حدث خطأ أثناء جلب الأخبار:\n{e}"
        )


# تشغيل البوت
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("✅ البوت يعمل…")
app.run_polling()
