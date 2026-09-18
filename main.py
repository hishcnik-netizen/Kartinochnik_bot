import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from duckduckgo_search import DDGS

logging.basicConfig(level=logging.INFO)

# Поиск картинок через DuckDuckGo
def get_image_urls(query: str, max_results: int = 3):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(keywords=query, max_results=max_results))
            return [r['image'] for r in results]
    except Exception as e:
        logging.error(f"Ошибка поиска: {e}")
        return []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши, какую картинку найти.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"Ищу: «{query}»...")
    
    urls = get_image_urls(query)
    
    if not urls:
        await update.message.reply_text("Ничего не найдено.")
        return

    for url in urls:
        try:
            await update.message.reply_photo(photo=url)
        except Exception:
            await update.message.reply_text(url)

if __name__ == '__main__':
    token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
  
