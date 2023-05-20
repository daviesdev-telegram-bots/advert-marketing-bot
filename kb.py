from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

sub_sections = {"ad": [("indi", "Individual"), ("bm", "Business manager"), ("mm","Marketing manager"), ("bus","Business")],
                "ms": [("tv", "Television"), ("radio", "radio"), ("ip", "Independent producer")],
                "mc": [("copy", "Copyrighter"), ("vo", "Voice over Artist")],
                "me": [("na", "Not available for now")]}


class Register():
    sec_kb = InlineKeyboardMarkup()
    sec_kb.add(InlineKeyboardButton("Advertiser", callback_data="reg_mode:ad"))
    sec_kb.add(InlineKeyboardButton("Media seller", callback_data="reg_mode:ms"))
    sec_kb.add(InlineKeyboardButton("Media expert", callback_data="reg_mode:me"))
    sec_kb.add(InlineKeyboardButton("Marketing consultant", callback_data="reg_mode:mc"))

