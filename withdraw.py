from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE, back_callback_data=None):
    text = (
        "请选择提现币种：\n"
        "⛔为避免风险，请勿直接提币到交易所！"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("USDT(TRC20)", callback_data='withdraw_usdt')],
        [InlineKeyboardButton("CNY", callback_data='withdraw_cny')],
        [InlineKeyboardButton("返回上一步", callback_data=back_callback_data or 'main_menu')]
    ])
    await update.message.reply_text(text, reply_markup=keyboard)