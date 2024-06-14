from telegram import Update
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Hello! I'm your Healthcare Chatbot. How can I assist you today?\n"
        "You can use the following commands:\n"
        "/symptom - Input your symptom and get a remedy\n"
        "/disease_info - Get information about a specific disease\n"
        "/exit - End the conversation"
    )

def input_symptom(update: Update, context: CallbackContext) -> None:
    context.user_data['symptom_input'] = True
    update.message.reply_text("Please type your symptom.")

def disease_info(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Please type the name of the disease you want information about.")

def exit_chat(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Goodbye! Take care.")
    context.user_data.clear()
