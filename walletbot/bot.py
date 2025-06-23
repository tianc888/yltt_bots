import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
)
from walletbot.config import TELEGRAM_TOKEN, BOT_NAME
from db import init_db, get_user
from walletbot.handlers.recharge import recharge
from walletbot.handlers.withdraw import withdraw
from walletbot.handlers.transfer import transfer
from walletbot.handlers.collect import collect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main_menu = [
    [KeyboardButton("💵充值")],
    [KeyboardButton("💸提币")],
    [KeyboardButton("⏫转账")],
    [KeyboardButton("⏬收款")]
]

# 用于回退上一步的简单栈（可改为更复杂的状态管理）
user_steps = {}

def push_step(user_id, step):
    if user_id not in user_steps:
        user_steps[user_id] = []
    user_steps[user_id].append(step)

def pop_step(user_id):
    if user_id in user_steps and user_steps[user_id]:
        user_steps[user_id].pop()
        if user_steps[user_id]:
            return user_steps[user_id][-1]
    return "main_menu"

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
    user_steps[update.effective_user.id] = ["main_menu"]

async def support(update: Update, context):
    await update.message.reply_text("客服请联系 @YourSupportAccount")

async def menu_router(update: Update, context):
    user_id = update.effective_user.id
    text = update.message.text
    if "充值" in text:
        push_step(user_id, "recharge")
        await recharge(update, context, back_callback_data='back')
    elif "提币" in text:
        push_step(user_id, "withdraw")
        await withdraw(update, context, back_callback_data='back')
    elif "转账" in text:
        push_step(user_id, "transfer")
        await transfer(update, context, back_callback_data='back')
    elif "收款" in text:
        push_step(user_id, "collect")
        await collect(update, context, back_callback_data='back')

async def button_callback(update: Update, context):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    await query.answer()
    if data == 'main_menu':
        user_steps[user_id] = ["main_menu"]
        await start(update, context)
    elif data == 'copy_address':
        from walletbot.config import RECHARGE_ADDRESS
        await query.edit_message_caption(caption=f"已复制钱包地址：\n`{RECHARGE_ADDRESS}`", parse_mode="Markdown")
    elif data.startswith('withdraw'):
        await query.edit_message_text("请输入提现地址和金额（开发中）")
    elif data == 'select_recipient':
        await query.edit_message_text("请输入收款人信息（开发中）")
    elif data == 'back':
        prev_step = pop_step(user_id)
        # 回到上一步
        if prev_step == "main_menu":
            await start(update, context)
        elif prev_step == "recharge":
            await recharge(update, context, back_callback_data='back')
        elif prev_step == "withdraw":
            await withdraw(update, context, back_callback_data='back')
        elif prev_step == "transfer":
            await transfer(update, context, back_callback_data='back')
        elif prev_step == "collect":
            await collect(update, context, back_callback_data='back')

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
