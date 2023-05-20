from telebot import TeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import os, dotenv
from models import User, session

dotenv.load_dotenv()


bot_token = os.getenv("bot_token")
bot = TeleBot(bot_token, parse_mode="HTML")

@bot.message_handler(["start"])
def start(message):
    user = session.query(User).get(message.chat.id)
    if not user:
        bot.send_message(message.chat.id, "Hello there. It seems you're not registered.\n\nPlease send your Email address")
        bot.register_next_step_handler(message, register_email)
        return
    bot.send_message(message.chat.id, f"Welcome back {user.name}")

def register_email(message):
    details = {}
    if message.text:
        details["email"] = message.text
        bot.send_message(message.chat.id, "Please send your phone number (07000000101)")
        bot.register_next_step_handler(message, register_phone, details)

def register_phone(message:Message, details):
    if message.text:
        details["phone"] = message.text
        user = User(id=message.chat.id, name=message.chat.username, **details)
        session.add(user)
        session.commit()
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("Advertiser", callback_data="reg_mode:ad"))
        kb.add(InlineKeyboardButton("Media seller", callback_data="reg_mode:ms"))
        kb.add(InlineKeyboardButton("Media expert", callback_data="reg_mode:me"))
        kb.add(InlineKeyboardButton("Marketing consultant", callback_data="reg_mode:ms"))
        bot.send_message(message.chat.id, "What best describes you?", reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data != None)
def callback_handler(callback: CallbackQuery):
    message = callback.message

    if callback.data.startswith("reg_mode"):
        _, section = callback.data.split(":")
        user = session.query(User).get(message.chat.id)
        user.section = section
        session.commit()
        kb = InlineKeyboardMarkup()
        bot.send_message(message.chat.id, "What category do you fall under?", reply_markup=kb)

