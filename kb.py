from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

sub_sections = {"ad": [("individual", "Individual"), ("business", "Corporate Business")],
                "mm": [("3rdparty", "3rd Party Marketer"), ("mediaowner", "Media Owner staff"), ("producer", "Independent Producer")],
                "mc": [("audiovisual", "Audio Visual Production"), ("graphicdesign", "Graphics Designer"), ("voiceover", "Voice over Artist"), ("ooh", "OOH Services Support"), ("newspaper", "Newspaper Services Support")],
                "me": [("mediaplanner", "Media Planner"), ("mediabuyer", "Media Buyer")]}

tv_states = ['Nasarawa', 'Bauchi', 'Rivers', 'Oyo', 'Anambra', 'Delta', 'Benue', 'Yobe', 'Network', 'Plateau', 'Adamawa', 'Edo', 'Taraba', 'Borno', 'Kaduna', 'Sokoto', 'Ogun', 'Katsina', 'Kano', 'Abia', 'Akwa Ibom', 'Lagos', 'Enugu', 'Imo', 'Ekiti', 'Kogi', 'FCT Abuja', 'Jigawa', 'Syndication', 'Bayelsa', 'Ondo', 'Zamfara', 'Kebbi', 'Ebonyi', 'Gombe', 'Kwara', 'Osun', 'Cross River', 'Niger']
tv_states.sort()
radio_states = ['Kebbi', 'Syndication', 'FCT Abuja', 'Cross River', 'Akwa Ibom', 'Nasarawa', 'Ekiti', 'Osun', 'Bayelsa', 'Network', 'Niger', 'Abia', 'Kogi', 'Ebonyi', 'Kaduna', 'Plateau', 'Gombe', 'Edo', 'Katsina', 'Delta', 'Adamawa', 'Bauchi', 'Oyo', 'Ogun', 'Kano', 'Lagos', 'Imo', 'Ondo', 'Anambra', 'Benue', 'Kwara', 'Taraba', 'Rivers', 'Enugu', ' Kwara', 'Sokoto', 'Borno']
radio_states.sort()

class Register():
    sec_kb = InlineKeyboardMarkup()
    sec_kb.add(InlineKeyboardButton("Advertiser", callback_data="reg_mode:ad"))
    sec_kb.add(InlineKeyboardButton("Media Marketer", callback_data="reg_mode:mm"))
    sec_kb.add(InlineKeyboardButton("Media expert", callback_data="reg_mode:me"))
    sec_kb.add(InlineKeyboardButton("Marketing consultant", callback_data="reg_mode:mc"))

    def media_marketing_platform():
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("Television", callback_data="reg_mm_tv"))
        kb.add(InlineKeyboardButton("Radio", callback_data="reg_mm_radio"))
        kb.add(InlineKeyboardButton("OOH", callback_data="reg_mm_ooh"))
        kb.add(InlineKeyboardButton("Newspaper", callback_data="reg_mm_newspaper"))
        kb.add(InlineKeyboardButton("Digital", callback_data="reg_mm_digital"))
        return kb

class MediaMarketer:
    start_kb = InlineKeyboardMarkup()
    start_kb.add(InlineKeyboardButton("Upload Inventory", callback_data="nothing"))
    start_kb.add(InlineKeyboardButton("Modify Inventory", callback_data="nothing"))
    start_kb.add(InlineKeyboardButton("Delete Inventory", callback_data="nothing"))
    start_kb.add(InlineKeyboardButton("Delete Account", callback_data="del"))

class Advertiser:
    start_kb = InlineKeyboardMarkup()
    start_kb.add(InlineKeyboardButton("Check Advert rates", callback_data="ad_rate"))
    start_kb.add(InlineKeyboardButton("Run a media campaign", callback_data="media_campaign"))
    start_kb.add(InlineKeyboardButton("Send a media brief", callback_data="media_brief"))
    start_kb.add(InlineKeyboardButton("Engage a media expert", callback_data="media_expert"))
    start_kb.add(InlineKeyboardButton("Delete Account", callback_data="del"))

    platforms_kb = InlineKeyboardMarkup()
    platforms_kb.add(InlineKeyboardButton("Television", callback_data="state:tv"))
    platforms_kb.add(InlineKeyboardButton("Radio", callback_data="state:radio"))
    platforms_kb.add(InlineKeyboardButton("Billboard", callback_data="billboard"))
    platforms_kb.add(InlineKeyboardButton("NewsPaper", callback_data="newspaper"))
    platforms_kb.add(InlineKeyboardButton("Others", callback_data="other"))
    
    def back_btn(step):
        return InlineKeyboardButton("Back", callback_data=step)
