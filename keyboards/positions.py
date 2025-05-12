from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def get_position_keyboard():
    keyboard = [ 
        [InlineKeyboardButton("Top", callback_data="lane_baron")],
        [InlineKeyboardButton("Mid", callback_data="lane_mid")],
        [InlineKeyboardButton("Jungle", callback_data="lane_jungle")],
        [InlineKeyboardButton("ADC", callback_data="lane_adc")],
        [InlineKeyboardButton("Support", callback_data="lane_support")]
    ]
    return InlineKeyboardMarkup(keyboard)