from telegram import Update
from telegram.ext import ContextTypes
from keyboards.positions import get_position_keyboard

lane_map = {
    "lane_baron": "baron",
    "lane_mid": "mid",
    "lane_jungle": "jungle",
    "lane_dragon": "dragon",
    "lane_support": "support"
}

from parser.junglergg import fetch_champions

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выбери позицию:", reply_markup=get_position_keyboard())

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("lane_"):
        lane = lane_map[query.data]
        champions = fetch_champions(lane)

        message = f"Топ чемпионы для линии {lane.title()}:\n\n"
        for champ in champions[:10]:
            message += f"{champ['name']}: Win {champ['win_rate']}, Ban {champ['ban_rate']}\n"

        await query.edit_message_text(text=message)