import logging
import asyncio
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters
)
from telegram import BotCommand, Update
from config import TELEGRAM_TOKEN
import wallet

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    await update.message.reply_text("欢迎使用钱包机器人！")

async def handle_balance(update: Update, context):
    balance = wallet.get_user_balance(update.effective_user.id)
    await update.message.reply_text(f"您的余额为：{balance}")

async def handle_recharge(update: Update, context):
    await wallet.handle_recharge(update, context)

async def handle_withdraw(update: Update, context):
    await wallet.handle_withdraw(update, context)

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler(["start"], start))
    app.add_handler(CommandHandler(["balance"], handle_balance))
    app.add_handler(CommandHandler(["recharge"], handle_recharge))
    app.add_handler(CommandHandler(["withdraw"], handle_withdraw))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^余额$"), handle_balance))
    await app.bot.set_my_commands([
        BotCommand("start", "启动机器人"),
        BotCommand("balance", "查询余额"),
        BotCommand("recharge", "充值"),
        BotCommand("withdraw", "提现"),
    ])
    logger.info("钱包机器人已启动...")
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
