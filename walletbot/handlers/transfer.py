from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

async def transfer(update: Update, context: ContextTypes.DEFAULT_TYPE, back_callback_data=None):
    text = (
        "请选择收款人方式：\n"
        "- 输入@username\n"
        "- 转发一条收款人消息\n"
        "- 输入对方账户ID"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("选择收款人", callback_data='select_recipient')],
        [InlineKeyboardButton("返回上一步", callback_data=back_callback_data or 'main_menu')]
    ])
    await update.message.reply_text(text, reply_markup=keyboard)
