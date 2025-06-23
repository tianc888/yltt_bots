import logging
import asyncio
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
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
    # 只注册英文命令
    app.add_handler(CommandHandler(["start"], start))
    app.add_handler(CommandHandler(["balance"], handle_balance))
    app.add_handler(CommandHandler(["recharge"], handle_recharge))
    app.add_handler(CommandHandler(["withdraw"], handle_withdraw))
    # 支持输入“余额”也能触发
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^余额$"), handle_balance))
    # 你可以根据需要添加更多 MessageHandler 做中文兼容

    # 设置 bot 命令菜单（只能用英文命令，描述可以用中文）
    await app.bot.set_my_commands([
        BotCommand("start", "启动机器人"),
        BotCommand("balance", "查询余额"),
        BotCommand("recharge", "充值"),
        BotCommand("withdraw", "提现"),
    ])

    logger.info("钱包机器人已启动...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
