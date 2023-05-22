from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

sub_sections = {"ad": [("indi", "Individual"), ("bm", "Business manager"), ("mm","Marketing manager"), ("bus","Business")],
                "ms": [("tv", "Television"), ("radio", "radio"), ("ip", "Independent producer")],
                "mc": [("copy", "Copyrighter"), ("vo", "Voice over Artist")],
                "me": [("na", "Not available for now")]}

tv_states = ['Nasarawa', 'Bauchi', 'Rivers', 'Oyo', 'Anambra', 'Delta', 'Benue', 'Yobe', 'Network', 'Plateau', 'Adamawa', 'Edo', 'Taraba', 'Borno', 'Kaduna', 'Sokoto', 'Ogun', 'Katsina', 'Kano', 'Abia', 'Akwa Ibom', 'Lagos', 'Enugu', 'Imo', 'Ekiti', 'Kogi', 'FCT Abuja', 'Jigawa', 'Syndication', 'Bayelsa', 'Ondo', 'Zamfara', 'Kebbi', 'Ebonyi', 'Gombe', 'Kwara', 'Osun', 'Cross River', 'Niger']
tv_states.sort()
radio_states = ['Kebbi', 'Syndication', 'FCT Abuja', 'Cross River', 'Akwa Ibom', 'Nasarawa', 'Ekiti', 'Osun', 'Bayelsa', 'Network', 'Niger', 'Abia', 'Kogi', 'Ebonyi', 'Kaduna', 'Plateau', 'Gombe', 'Edo', 'Katsina', 'Delta', 'Adamawa', 'Bauchi', 'Lagos ', 'Oyo', 'Ogun', 'Kano', 'Lagos', 'Imo', 'Ondo', 'Anambra', 'Benue', 'Kwara', 'Taraba', 'Rivers', 'Enugu', ' Kwara', 'Sokoto', 'Borno']
radio_states.sort()

class Register():
    sec_kb = InlineKeyboardMarkup()
    sec_kb.add(InlineKeyboardButton("Advertiser", callback_data="reg_mode:ad"))
    sec_kb.add(InlineKeyboardButton("Media seller", callback_data="reg_mode:ms"))
    sec_kb.add(InlineKeyboardButton("Media expert", callback_data="reg_mode:me"))
    sec_kb.add(InlineKeyboardButton("Marketing consultant", callback_data="reg_mode:mc"))

class Advertiser:
    start_kb = InlineKeyboardMarkup()
    start_kb.add(InlineKeyboardButton("Check Advert rates", callback_data="ad_rate"))
    start_kb.add(InlineKeyboardButton("Run a media campaign", callback_data="media_camp"))
    start_kb.add(InlineKeyboardButton("Send a media brief", callback_data="media_brief"))
    start_kb.add(InlineKeyboardButton("Engage a media expert", callback_data="media_exp"))
    start_kb.add(InlineKeyboardButton("Delete Account", callback_data="del"))

    platforms_kb = InlineKeyboardMarkup()
    platforms_kb.add(InlineKeyboardButton("Television", callback_data="state:tv"))
    platforms_kb.add(InlineKeyboardButton("Radio", callback_data="state:radio"))
    platforms_kb.add(InlineKeyboardButton("Billboard", callback_data="state:billboard"))
    platforms_kb.add(InlineKeyboardButton("NewsPaper", callback_data="state:newspaper"))
    platforms_kb.add(InlineKeyboardButton("Others", callback_data="state:other"))
    
