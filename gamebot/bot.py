import logging
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TELEGRAM_TOKEN, BOT_NAME

START_MENU = [
    ["充值", "提现"],
    ["返回上一步"]
]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update, context):
    from telegram import ReplyKeyboardMarkup
    reply_markup = ReplyKeyboardMarkup(START_MENU, resize_keyboard=True)
    await update.message.reply_text(
        f"欢迎使用{BOT_NAME}！请选择操作：", reply_markup=reply_markup
    )

async def recharge(update, context):
    await update.message.reply_text("请点击钱包机器人进行充值：@你的钱包机器人用户名")

async def withdraw(update, context):
    await update.message.reply_text("请输入提现金额：")

async def unknown(update, context):
    await update.message.reply_text("无法识别的指令，请重新选择。")

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    await app.bot.set_my_commands([
        ("start", "开始使用"),
        ("充值", "充值到游戏"),
        ("提现", "从游戏提现")
    ])
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("^充值$"), recharge))
    app.add_handler(MessageHandler(filters.Regex("^提现$"), withdraw))
    app.add_handler(MessageHandler(filters.ALL, unknown))
    logger.info("游戏机器人已启动...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
