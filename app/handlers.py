# message handlers
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
from app.translator import translate_text, detect_language
from app.speech import transcribe_audio
import os

# Simple in-memory storage for last translation per user
user_last_translation = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send text in any language.\nI will translate it into English."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/detect - Detect language only\n"
        "Or send any text to translate."
    )

async def detect_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /detect <text>")
        return

    text = " ".join(context.args)
    lang = detect_language(text)

    await update.message.reply_text(
        f"Detected Language Code: {lang}"
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌍 Telegram Translator Bot\n\n"
        "This bot translates any language into English.\n"
        "It automatically detects the input language and converts it.\n\n"
        "✨ Features:\n"
        "• Auto language detection\n"
        "• English translation\n"
        "• Inline re-translate button\n"
        "• Voice message translation\n\n"
        "👨‍💻 Meet the Developer:\n"
        "@Thewarrior2003"
    )

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎙 Processing voice message...")

    voice = update.message.voice
    file = await context.bot.get_file(voice.file_id)

    file_path = f"temp_{update.effective_user.id}.ogg"
    await file.download_to_drive(file_path)

    try:
        # Transcribe
        text = transcribe_audio(file_path)

        # DEBUG: Show what Whisper heard
        print("DEBUG - Transcribed text:", text)
        await update.message.reply_text(f"🔍 DEBUG - Transcribed:\n{text}")

        # Translate using existing function
        result = translate_text(text)

        response = (
            f"🎙 Voice Detected Language: {result['language_name']} {result['flag']}\n\n"
            f"📝 English Translation:\n{result['translated_text']}"
        )

        await update.message.reply_text(response)

    except Exception as e:
        await update.message.reply_text("Voice translation failed.")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()

    if not user_text:
        await update.message.reply_text("Please send valid text.")
        return

    try:
        result = translate_text(user_text)

        response = (
            f"Detected Language: {result['language_name']} {result['flag']}\n\n"
            f"English Translation:\n{result['translated_text']}"
        )

        # Save last translation for this user
        user_last_translation[update.effective_user.id] = user_text

        # Add inline button
        keyboard = [
            [InlineKeyboardButton("🔁 Translate Again", callback_data="translate_again")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(response, reply_markup=reply_markup)

    except Exception:
        await update.message.reply_text("Translation failed. Please try again.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "translate_again":
        if user_id in user_last_translation:
            text = user_last_translation[user_id]
            result = translate_text(text)

            response = (
                f"Detected Language: {result['language_name']} {result['flag']}\n\n"
                f"English Translation:\n{result['translated_text']}"
            )

            await query.edit_message_text(response)
        else:
            await query.edit_message_text("No previous translation found.")

def register_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("detect", detect_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(button_handler))
