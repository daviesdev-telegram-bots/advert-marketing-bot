from telebot import TeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import os, dotenv, re
from models import User, session, MediaAdRate, MediaPlatform
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
    kb = {"ad": Advertiser.start_kb, "mm": MediaMarketer.start_kb}
    bot.send_message(message.chat.id, f"Welcome back {user.name}.\nHow may I help you today?.", reply_markup=kb[user.section])

def register_email(message):
    details = {}
    if message.text:
        pattern = re.compile(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$")
        if not pattern.fullmatch(message.text.lower()):
            bot.send_message(message.chat.id, "Please send a valid email address")
            bot.register_next_step_handler(message, register_email)
            return
        details["email"] = message.text.lower()
        bot.send_message(message.chat.id, "Please send your phone number (e.g 07000000101)")
        bot.register_next_step_handler(message, register_phone, details)

def register_phone(message:Message, details):
    if message.text:
        pattern = re.compile(r"0[789]{1}[0-9]{9}")
        if not pattern.fullmatch(message.text):
            bot.send_message(message.chat.id, "Please send a valid phone number (e.g 07000000101)")
            bot.register_next_step_handler(message, register_phone, details)
            return
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
        if user.section == "mm":
            bot.edit_message_text("Select the media channels you manage", message.chat.id, message.id, reply_markup=Register.media_marketing_platform())
            return
        bot.edit_message_text("Successfully Registered✅",message.chat.id, message.id)
        start(message)
    
    elif callback.data.startswith("reg_mm_"):
        data = callback.data[7:]
        if data == "done":
            bot.edit_message_text("Successfully Registered✅",message.chat.id, message.id)
            start(message)
            return
        user = session.query(User).get(message.chat.id)
        if data == "reset":
            for i in user.media_platforms:
                session.delete(i)
            session.commit()
            bot.edit_message_text("Select the media channels you manage", message.chat.id, message.id, reply_markup=Register.media_marketing_platform())
            return
        if not session.query(MediaPlatform).filter_by(user=user.id, platform=data).first():
            session.add(MediaPlatform(platform=data, user=user.id))
            session.commit()
            txt = ", ".join([i.platform.title() for i in user.media_platforms])
            bot.edit_message_text(f"Select the media channels you manage\n\nAdded: {txt}", message.chat.id, message.id,
                                reply_markup=Register.media_marketing_platform().add(InlineKeyboardButton("Done ✅", callback_data="reg_mm_done"), InlineKeyboardButton("Reset ❌", callback_data="reg_mm_reset")))

    elif callback.data == "ad_rate":
        bot.edit_message_text("Ad rate for which platform?", message.chat.id, message.id, reply_markup=Advertiser.platforms_kb)
    
    elif callback.data == "media_campaign":
        bot.edit_message_text("Send an email to campaigns@awari.com ", message.chat.id, message.id, reply_markup=InlineKeyboardMarkup().add(Advertiser.back_btn("ad_rate")))
    elif callback.data == "media_brief":
        bot.edit_message_text("Send an email to briefs@awari.com ", message.chat.id, message.id, reply_markup=InlineKeyboardMarkup().add(Advertiser.back_btn("ad_rate")))
    elif callback.data == "media_expert":
        bot.edit_message_text("Send an email to expert@awari.com ", message.chat.id, message.id, reply_markup=InlineKeyboardMarkup().add(Advertiser.back_btn("ad_rate")))

    elif callback.data.startswith("state"):
        _, media_type = callback.data.split(":")
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("Any State", callback_data="tv_station:any"))
        states = {"tv": tv_states, "radio": radio_states}
        kb.add(*[InlineKeyboardButton(s, callback_data=f"station:{media_type}:{s}") for s in states[media_type]])
        bot.edit_message_text("Choose a state", message.chat.id, message.id, reply_markup=kb)

    elif callback.data.startswith("station"):
        _, media_type, state = callback.data.split(":")
        tv_stations = session.query(MediaAdRate).filter_by(state=state, media_type=media_type).all()
        station_names = set()
        for i in tv_stations:
            station_names.add(i.station_name)
        station_names = list(station_names)
        station_names.sort()
        tv_station_kb = InlineKeyboardMarkup(row_width=2)
        tv_station_kb.add(*[InlineKeyboardButton(station, callback_data=f"time:{media_type}:{state}:{station}") for station in station_names])
        if media_type == "tv":
            text = "TV channel"
        elif media_type == "radio":
            text = "radio station"
        bot.edit_message_text(f"What {text} ?", message.chat.id, message.id, reply_markup=tv_station_kb)

    elif callback.data.startswith("time"):
        _, media_type, state, station_name = callback.data.split(":")
        tv_stations = session.query(MediaAdRate).filter_by(state=state, station_name=station_name, media_type=media_type).all()
        durations = set()
        for station in tv_stations:
            durations.add(station.duration) 
        durations = list(durations)
        durations.sort()
        tv_time = InlineKeyboardMarkup(row_width=2)
        tv_time.add(*[InlineKeyboardButton(dur, callback_data=f"sum:{media_type}:{state}:{station_name}:{dur}") for dur in durations])
        tv_time.add(InlineKeyboardButton("Any", callback_data=f"sum:{media_type}:{state}:{station_name}:any"))
        bot.edit_message_text("Choose a duration for the ad", message.chat.id, message.id, reply_markup=tv_time)

    elif callback.data.startswith("sum"):
        _, media_type, state, station_name, dur = callback.data.split(":")
        adrate = session.query(MediaAdRate).filter_by(state=state, station_name=station_name, duration=dur, media_type=media_type).first()
        bot.edit_message_text(f"<b>Summary</b>\n{media_type.title()} Station: {adrate.station_name}\nState: {adrate.state}\nDuration: {adrate.duration}\n\nPrice: <b>₦{adrate.card_rate}</b>", message.chat.id, message.id)

    elif callback.data == "del":
        session.delete(session.query(User).get(message.chat.id))
        session.commit()
        bot.edit_message_text("Account deleted. Click /start to repeat the process", message.chat.id, message.id)

print("Started")
bot.infinity_polling()