from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

async def collect(update: Update, context: ContextTypes.DEFAULT_TYPE, back_callback_data=None):
    text = (
        "请输入收款金额 (U)：\n"
        "在下方输入框输入金额并发送。"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("返回上一步", callback_data=back_callback_data or 'main_menu')]
    ])
    await update.message.reply_text(text, reply_markup=keyboard)
