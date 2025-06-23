from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from walletbot.config import RECHARGE_ADDRESS, RECHARGE_QR_PATH

async def recharge(update: Update, context: ContextTypes.DEFAULT_TYPE, back_callback_data=None):
    text = (
        "【渔乐天天钱包】充值\n\n"
        "请使用下方二维码或钱包地址充值：\n"
        f"`{RECHARGE_ADDRESS}`\n"
        "支持：USDT(TRC20)、CNY\n"
        "最低1U，可重复充值。\n"
        "充值后，到账会自动通知。\n\n"
        "⚠️ 请勿向非官方地址充值！"
    )
    # 主菜单所有分支均有返回上一步
    keyboard_buttons = [
        [InlineKeyboardButton("复制地址", callback_data='copy_address')],
        [InlineKeyboardButton("返回上一步", callback_data=back_callback_data or 'main_menu')]
    ]
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    with open(RECHARGE_QR_PATH, 'rb') as qr:
        await update.message.reply_photo(qr, caption=text, reply_markup=keyboard, parse_mode="Markdown")