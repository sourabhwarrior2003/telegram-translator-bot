# bot logic
from telegram.ext import ApplicationBuilder
from app.handlers import register_handlers
from app.config import BOT_TOKEN

def create_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    register_handlers(application)
    return application 
