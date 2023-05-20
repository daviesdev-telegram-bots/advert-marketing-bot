from telebot import TeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import os, dotenv
from models import User, session, Adrate
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
    # secs = {"ad": "Advertiser", "ms": "Media Sales", "mc": "Marketing consultant", "me": "Media expert"}
    # s = dict(sub_sections[user.section])[user.sub_section]
    kb = {"ad": Advertiser.start_kb}
    bot.send_message(message.chat.id, f"Welcome back {user.name}.\nHow may I help you today?.", reply_markup=kb[user.section])

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
    
    elif callback.data == "ad_rate":
        bot.edit_message_text("Ad rate for which platform?", message.chat.id, message.id, reply_markup=Advertiser.platforms_kb)

    elif callback.data.startswith("tv_states"):
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("Any State", callback_data="tv_station:any"))
        kb.add(*[InlineKeyboardButton(s, callback_data=f"tv_station:{s}") for s in states])
        bot.edit_message_text("Choose a state", message.chat.id, message.id, reply_markup=kb)

    elif callback.data.startswith("tv_station"):
        _, state = callback.data.split(":")
        tv_stations = session.query(Adrate).filter_by(state=state).all()
        station_names = set()
        for i in tv_stations:
            station_names.add(i.station_name)
        station_names = list(station_names)
        station_names.sort()
        tv_station_kb = InlineKeyboardMarkup(row_width=2)
        tv_station_kb.add(*[InlineKeyboardButton(station, callback_data=f"tv_time:{state}:{station}") for station in station_names])
        bot.edit_message_text("What TV channel?", message.chat.id, message.id, reply_markup=tv_station_kb)

    elif callback.data.startswith("tv_time"):
        _, state, station_name = callback.data.split(":")
        tv_stations = session.query(Adrate).filter_by(state=state, station_name=station_name).all()
        durations = set()
        for station in tv_stations:
            durations.add(station.duration)
        durations = list(durations)
        durations.sort()
        tv_time = InlineKeyboardMarkup(row_width=2)
        tv_time.add(*[InlineKeyboardButton(dur, callback_data=f"tv_sum:{state}:{station_name}:{dur}") for dur in durations])
        tv_time.add(InlineKeyboardButton("Any", callback_data=f"tv_sum:{state}:{station_name}:any"))
        bot.edit_message_text("Choose a duration for the ad", message.chat.id, message.id, reply_markup=tv_time)

    elif callback.data.startswith("tv_sum"):
        _, state, station_name, dur = callback.data.split(":")
        adrate = session.query(Adrate).filter_by(state=state, station_name=station_name, duration=dur).first()
        bot.edit_message_text(f"<b>Summary</b>\nStation: {adrate.station_name}\nState: {adrate.state}\nDuration: {adrate.duration}\n\nPrice: <b>₦{adrate.card_rate}</b>", message.chat.id, message.id)

    elif callback.data == "del":
        session.delete(session.query(User).get(message.chat.id))
        session.commit()
        bot.edit_message_text("Account deleted. Click /start to repeat the process", message.chat.id, message.id)

print("Started")
bot.infinity_polling()