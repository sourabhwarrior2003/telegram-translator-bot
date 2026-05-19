from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from app.translator import (
    translate_text,
    detect_language
)

from app.database import (
    save_translation,
    get_user_history
)


# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [InlineKeyboardButton(
            "🌍 Translate",
            callback_data="translate"
        )],

        [InlineKeyboardButton(
            "🎤 Voice Translate",
            callback_data="voice"
        )],

        [InlineKeyboardButton(
            "📜 History",
            callback_data="history"
        )],

        [InlineKeyboardButton(
            "ℹ️ About",
            callback_data="about"
        )]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚀 Welcome to Telegram Translator Bot\n\n"
        "Choose an option below:",
        reply_markup=reply_markup
    )


# BUTTON CALLBACKS
async def button_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if query.data == "translate":

        await query.message.reply_text(
            "🌍 Send any text message.\n"
            "I will translate it."
        )

    elif query.data == "voice":

        await query.message.reply_text(
            "🎤 Send a voice message for translation."
        )

    elif query.data == "history":

        history = get_user_history(
            update.effective_user.id
        )

        if not history:

            await query.message.reply_text(
                "📭 No translation history found."
            )

            return

        response = (
            "📜 *Recent Translation History*\n\n"
        )

        for item in history:

            original = item[0]
            translated = item[1]
            language = item[2]
            timestamp = item[3]

            response += (
                f"📝 Original: {original}\n"
                f"🌍 Translation: {translated}\n"
                f"🔎 Language: {language}\n"
                f"⏰ {timestamp}\n\n"
            )

        await query.message.reply_text(
            response,
            parse_mode="Markdown"
        )

    elif query.data == "about":

        await query.message.reply_text(
            "👨‍💻 Developer: @Thewarrior2003"
        )


# HELP COMMAND
async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "📌 Commands:\n\n"
        "/start - Start bot\n"
        "/help - Help menu\n"
        "/translate - Translate text\n"
        "/history - Show history"
    )


# MULTI LANGUAGE TRANSLATION
async def translate_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        args = context.args

        if len(args) < 3:

            await update.message.reply_text(
                "⚠️ Usage:\n"
                "/translate <source_lang> "
                "<target_lang> <text>\n\n"

                "Example:\n"
                "/translate hi fr नमस्ते"
            )

            return

        source_lang = args[0]

        target_lang = args[1]

        text = " ".join(args[2:])

        translated_text = translate_text(
            text,
            target_language=target_lang
        )

        response = (
            "🌍 *Translation Complete*\n\n"

            f"📝 *Original Text:*\n"
            f"{text}\n\n"

            f"🔎 *Source Language:*\n"
            f"{source_lang}\n\n"

            f"🎯 *Target Language:*\n"
            f"{target_lang}\n\n"

            f"✅ *Translated Text:*\n"
            f"{translated_text}"
        )

        await update.message.reply_text(
            response,
            parse_mode="Markdown"
        )

    except Exception:

        await update.message.reply_text(
            "❌ Translation failed."
        )


# HISTORY COMMAND
async def history_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    history = get_user_history(
        update.effective_user.id
    )

    if not history:

        await update.message.reply_text(
            "📭 No translation history found."
        )

        return

    response = (
        "📜 *Recent Translation History*\n\n"
    )

    for item in history:

        original = item[0]
        translated = item[1]
        language = item[2]
        timestamp = item[3]

        response += (
            f"📝 Original: {original}\n"
            f"🌍 Translation: {translated}\n"
            f"🔎 Language: {language}\n"
            f"⏰ {timestamp}\n\n"
        )

    await update.message.reply_text(
        response,
        parse_mode="Markdown"
    )


# HANDLE NORMAL TEXT
async def handle_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_text = update.message.text.strip()

    if not user_text:

        await update.message.reply_text(
            "⚠️ Please send valid text."
        )

        return

    try:

        detected_language = detect_language(
            user_text
        )

        translated_text = translate_text(
            user_text
        )

        # SAVE TO DATABASE
        save_translation(
            update.effective_user.id,
            user_text,
            translated_text,
            detected_language
        )

        response = (
            "🌍 *Translation Complete*\n\n"

            f"📝 *Original Text:*\n"
            f"{user_text}\n\n"

            f"🔎 *Detected Language:*\n"
            f"{detected_language}\n\n"

            f"🇬🇧 *English Translation:*\n"
            f"{translated_text}"
        )

        await update.message.reply_text(
            response,
            parse_mode="Markdown"
        )

    except Exception:

        await update.message.reply_text(
            "❌ Translation failed."
        )


# REGISTER ALL HANDLERS
def register_handlers(app):

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CommandHandler(
            "translate",
            translate_command
        )
    )

    app.add_handler(
        CommandHandler(
            "history",
            history_command
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            button_callback
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text
        )
    )