import logging
import asyncio
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
)
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from config import TELEGRAM_TOKEN, ADMINS, BOT_USERNAME
import wallet

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_admin_link():
    admin_id = ADMINS[0] if ADMINS else None
    return f"https://t.me/{BOT_USERNAME}" if admin_id else "https://t.me/"

def get_bot_link():
    return f"https://t.me/{BOT_USERNAME}"

async def my_menu(update: Update, context):
    if update.effective_chat.type != 'private':
        return
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("充值", callback_data="recharge"),
         InlineKeyboardButton("提现", callback_data="withdraw")]
    ])
    await update.message.reply_text("请选择操作：", reply_markup=markup)

async def inline_recharge(update: Update, context):
    await wallet.handle_recharge(update, context)

async def inline_withdraw(update: Update, context):
    await wallet.handle_withdraw(update, context)

async def balance_cmd(update: Update, context):
    if update.effective_chat.type != 'private':
        return
    await wallet.handle_balance(update, context)

async def admin_add_balance_handler(update: Update, context):
    msg = update.message
    if msg.from_user.id not in ADMINS:
        return
    text = msg.text.strip().replace("＋", "+")
    if not text.startswith("+"):
        return
    try:
        amount = int(text[1:])
    except Exception:
        return
    target_id = msg.reply_to_message.from_user.id if msg.reply_to_message else None
    if not target_id:
        await msg.reply_text("请通过回复玩家消息加余额")
        return
    wallet.change_user_balance(target_id, amount, "管理员加余额", f"管理员@{msg.from_user.full_name} 操作")
    new_balance = wallet.get_user_balance(target_id)
    await msg.reply_text(f"已加余额{amount}，当前余额：{new_balance}")

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    # 只注册英文命令
    app.add_handler(CommandHandler(["start", "my"], my_menu))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^我的$"), my_menu))
    app.add_handler(CallbackQueryHandler(inline_recharge, pattern="^recharge$"))
    app.add_handler(CallbackQueryHandler(inline_withdraw, pattern="^withdraw$"))
    app.add_handler(CommandHandler(["balance"], balance_cmd))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^余额$"), balance_cmd))
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, admin_add_balance_handler))
    logger.info("游戏机器人已启动...")
    await app.run_polling()

if __name__ == "__main__":
    import sys
    import asyncio
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(main())
        loop.run_forever()
    except RuntimeError:
        asyncio.run(main())
