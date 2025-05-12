from telegram import Update
from telegram.ext import ContextTypes
from keyboards.positions import get_position_keyboard
from parser.junglergg import fetch_champions_by_role

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выбери позицию:", reply_markup=get_position_keyboard())

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lane = query.data
    champions = fetch_champions_by_role(lane)

    if not champions:
        await query.edit_message_text("Не удалось получить данные.")
        return

    # Форматируем топ-10
    text = f"Топ чемпионы для {lane.replace('lane_', '').capitalize()}:\n\n"
    for champ in champions[:10]:
        text += f"{champ['name']}: Win Rate {champ['win_rate']}, Ban Rate {champ['ban_rate']}\n"

    await query.edit_message_text(text=text)