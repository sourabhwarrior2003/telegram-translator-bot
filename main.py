from app.bot import create_bot
from app.utils import setup_logging
from app.database import init_db


def main():

    setup_logging()

    init_db()

    app = create_bot()

    print("🚀 Telegram Translator Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()