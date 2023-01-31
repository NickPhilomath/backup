import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import filters, CallbackQueryHandler, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
import dbfunctions as db
import osfunctions as osf
import const

# from direction import get_info

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TEXT_0 = 'welcome! please select an option:'
TEXT_1 = 'login'
TEXT_2 = 'signup'
TEXT_3 = 'you are already authorized in this chat'
TEXT_4 = 'please send your username:'
TEXT_5 = 'please send your password:'
TEXT_6 = 'you are successfully authorized!'
TEXT_7 = 'username or password is incorrect'

TEXT_30 = 'saved!'


authorizing_chat_ids = []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = [
        [KeyboardButton(TEXT_1)],
        [KeyboardButton(TEXT_2)]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=TEXT_0, reply_markup=reply_markup)


async def main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id

    if update.message.text == TEXT_1:
        # check if user is authorized already
        chat_ids = db.all_chat_ids()
        if chat_id in chat_ids:
            await context.bot.send_message(chat_id=chat_id, text=TEXT_3)
        else:
            authorizing_chat_ids.append([chat_id, "", 0])
            await context.bot.send_message(chat_id=chat_id, text=TEXT_4)

        return

    # check if user is trying to authorize
    for a in authorizing_chat_ids:
        if a[0] == chat_id:
            # if user is typing a username
            if a[2] == 0:
                a[1] = update.message.text
                a[2] = 1
                await context.bot.send_message(chat_id=chat_id, text=TEXT_5)
            # if user is typing a password
            elif a[2] == 1:
                print(a[1], update.message.text)
                if db.authorize(username=a[1], password=update.message.text, chat_id=chat_id):
                    await context.bot.send_message(chat_id=chat_id, text=TEXT_6)
                else:
                    authorizing_chat_ids.remove(a)
                    await context.bot.send_message(chat_id=chat_id, text=TEXT_7)
            break


async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    fileID = update.message.photo[-1].file_id
    new_file = await context.bot.get_file(file_id=fileID)
    auth_username = db.authorized_username(chat_id)
    # new_file = await update.message.effective_attachment.get_file()
    await new_file.download_to_drive(custom_path=f'backup/{auth_username}/{fileID}.jpg')
    await context.bot.send_message(chat_id=chat_id, text=TEXT_30, reply_to_message_id=update.message.id)


async def myfiles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    auth_username = db.authorized_username(chat_id)
    for file in osf.get_files_list(auth_username):
        await context.bot.send_document(chat_id=update.effective_chat.id, document=f'backup/{auth_username}/{file}')


async def agree(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    myfiles_handler = CommandHandler('myfiles', myfiles)
    main_handler = MessageHandler(filters.TEXT, main)
    backup_handler = MessageHandler(filters.PHOTO, backup)
    # location_handler = MessageHandler(filters.LOCATION, location)
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(myfiles_handler)
    application.add_handler(main_handler)
    application.add_handler(backup_handler)
    # application.add_handler(location_handler)
    # application.add_handler(echo_handler)
    # application.add_handler(CallbackQueryHandler(button))
    application.add_handler(unknown_handler)
    
    application.run_polling()