from telebot import TeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import os, dotenv
from models import User, session
from kb import *
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
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Delete Account", callback_data="del"))
    secs = {"ad": "Advertiser", "ms": "Media Sales", "mc": "Marketing consultant", "me": "Media expert"}
    s = dict(sub_sections[user.section])[user.sub_section]
    bot.send_message(message.chat.id, f"Welcome back {user.name}.\nHow may I help you today?.\n\n<b>Profile</b>\nEmail: {user.email}\nPhone: {user.phone}\nAccount Type: {secs[user.section]} • {s}", reply_markup=kb)

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
        bot.send_message(message.chat.id, "What best describes you?", reply_markup=Register.sec_kb)


@bot.callback_query_handler(func=lambda call: call.data != None)
def callback_handler(callback: CallbackQuery):
    message = callback.message

    if callback.data.startswith("reg_mode"):
        _, section = callback.data.split(":")
        user = session.query(User).get(message.chat.id)
        user.section = section
        session.commit()
        kb = InlineKeyboardMarkup()
        for d, n in sub_sections[section]:
            kb.add(InlineKeyboardButton(n, callback_data="sub_sec:"+d))
        bot.edit_message_text("What category do you fall under?", message.chat.id, message.id, reply_markup=kb)

    elif callback.data.startswith("sub_sec"):
        _, sub_section = callback.data.split(":")
        user = session.query(User).get(message.chat.id)
        user.sub_section = sub_section
        session.commit()
        bot.edit_message_text("Successfully Registered✅",message.chat.id, message.id)
        start(message)

    elif callback.data == "del":
        session.delete(session.query(User).get(message.chat.id))
        session.commit()
        bot.edit_message_text("Account deleted. Click /start to repeat the process", message.chat.id, message.id)

print("Started")
bot.infinity_polling()