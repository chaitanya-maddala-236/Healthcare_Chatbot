from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers.command_handlers import start, input_symptom, disease_info, exit_chat
from handlers.message_handlers import handle_messages

def main() -> None:
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("symptom", input_symptom))
    dp.add_handler(CommandHandler("disease_info", disease_info))
    dp.add_handler(CommandHandler("exit", exit_chat))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
