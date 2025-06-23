import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, BotCommand
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
)
from gamebot.config import TELEGRAM_TOKEN, BOT_NAME
from db import init_db, get_user
from gamebot.handlers.recharge import recharge
from gamebot.handlers.withdraw import withdraw
from gamebot.handlers.transfer import transfer
from gamebot.handlers.collect import collect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main_menu = [
    [KeyboardButton("💵充值")],
    [KeyboardButton("💸提币")],
    [KeyboardButton("⏫转账")],
    [KeyboardButton("⏬收款")]
]

async def start(update: Update, context):
    user = update.effective_user
    db_user = get_user(user.id, user.username or user.full_name)
    usdt = db_user[2] if db_user else 0
    cny = db_user[3] if db_user else 0
    text = (
        f"欢迎使用【{BOT_NAME}】\n\n"
        f"昵称: {user.full_name or user.username}\n"
        f"ID: {user.id}\n"
        f"USDT: {usdt:.3f}\n"
        f"CNY: {cny:.2f}\n"
        f"---------------------------"
    )
    await update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )

async def support(update: Update, context):
    await update.message.reply_text("客服请联系 @YourSupportAccount")

async def menu_router(update: Update, context):
    text = update.message.text
    if "充值" in text:
        await recharge(update, context)
    elif "提币" in text:
        await withdraw(update, context)
    elif "转账" in text:
        await transfer(update, context)
    elif "收款" in text:
        await collect(update, context)

async def button_callback(update: Update, context):
    query = update.callback_query
    data = query.data
    await query.answer()
    if data == 'main_menu':
        await start(update, context)
    elif data == 'copy_address':
        from gamebot.config import RECHARGE_ADDRESS
        await query.edit_message_caption(caption=f"已复制钱包地址：\n`{RECHARGE_ADDRESS}`", parse_mode="Markdown")
    elif data.startswith('withdraw'):
        await query.edit_message_text("请输入提现地址和金额（开发中）")
    elif data == 'select_recipient':
        await query.edit_message_text("请输入收款人信息（开发中）")

def main():
    init_db()
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("support", support))
    app.add_handler(MessageHandler(filters.TEXT, menu_router))
    app.add_handler(CallbackQueryHandler(button_callback))
    # 设置菜单命令
    app.bot.set_my_commands([
        BotCommand("start", "启动机器人"),
        BotCommand("support", "客服支持")
    ])
    app.run_polling()

if __name__ == "__main__":
    main()
