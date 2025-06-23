from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from gamebot.config import RECHARGE_ADDRESS, RECHARGE_QR_PATH

# 钱包机器人用户名
WALLET_BOT_USERNAME = "Ylttpay_bot"

async def recharge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "【渔乐天天游戏】充值\n\n"
        "请使用下方二维码或钱包地址充值：\n"
        f"`{RECHARGE_ADDRESS}`\n"
        "支持：USDT(TRC20)、CNY\n"
        "最低1U，可重复充值。\n"
        "充值后，到账会自动通知。\n\n"
        "⚠️ 请勿向非官方地址充值！"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("复制地址", callback_data='copy_address')],
        [InlineKeyboardButton("钱包", url=f"https://t.me/{WALLET_BOT_USERNAME}")]
    ])
    with open(RECHARGE_QR_PATH, 'rb') as qr:
        await update.message.reply_photo(qr, caption=text, reply_markup=keyboard, parse_mode="Markdown")
