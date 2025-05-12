import logging
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler
from keyboards.positions import get_position_keyboard
from parser.junglergg import fetch_champions_by_role

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выбери позицию:", reply_markup=get_position_keyboard())

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    lane = query.data
    await query.answer()
    logger.info(f"Выбрана позиция: {lane}")

    await query.edit_message_text("Собираем данные...")

    champions = fetch_champions_by_role(lane)

    if not champions:
        await query.edit_message_text("Не удалось получить данные.")
        return

    message_lines = ["🏆 <b>Чемпионы и Win Rate</b>\n"]
    text = f"Топ чемпионы для {lane.replace('lane_', '').capitalize()}:\n\n"
    for champ in champions[:10]:
        message_lines.append(f"{champ\['name'\]}: {champ\['win_rate'\]}")

    message = "\\n".join(message_lines)
    await query.message.reply_text(message, parse_mode="HTML")