from app.bot import create_bot
from app.utils import setup_logging

def main():
    setup_logging()
    app = create_bot()
    print("Telegram Translator Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
