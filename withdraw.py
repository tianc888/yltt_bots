from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

# 钱包机器人用户名
WALLET_BOT_USERNAME = "Ylttpay_bot"

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "请选择提现币种：\n"
        "⛔为避免风险，请勿直接提币到交易所！"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("USDT(TRC20)", callback_data='withdraw_usdt')],
        [InlineKeyboardButton("CNY", callback_data='withdraw_cny')],
        [InlineKeyboardButton("钱包", url=f"https://t.me/{WALLET_BOT_USERNAME}")]
    ])
    await update.message.reply_text(text, reply_markup=keyboard)