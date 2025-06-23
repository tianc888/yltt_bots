import logging
import os
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TELEGRAM_TOKEN, BOT_NAME

START_MENU = [
    ["充值", "提现"],
    ["转账", "收款"],
    ["余额", "返回上一步"]
]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update, context):
    from telegram import ReplyKeyboardMarkup
    reply_markup = ReplyKeyboardMarkup(START_MENU, resize_keyboard=True)
    await update.message.reply_text(
        f"欢迎使用{BOT_NAME}钱包机器人！请选择操作：", reply_markup=reply_markup
    )

async def recharge(update, context):
    qr_path = os.path.join(os.path.dirname(__file__), "../static/recharge_qr.png")
    if os.path.exists(qr_path):
        with open(qr_path, "rb") as f:
            await update.message.reply_photo(f, caption="请扫码充值")
    else:
        await update.message.reply_text("二维码图片未找到，请联系管理员。")

async def withdraw(update, context):
    await update.message.reply_text("请输入提现金额：")

async def balance(update, context):
    await update.message.reply_text("您的余额是：1000 元（演示）")

async def unknown(update, context):
    await update.message.reply_text("无法识别的指令，请重新选择。")

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    await app.bot.set_my_commands([
        ("start", "开始使用"),
        ("充值", "充值到钱包"),
        ("提现", "从钱包提现"),
        ("余额", "查询余额")
    ])
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("^充值$"), recharge))
    app.add_handler(MessageHandler(filters.Regex("^提现$"), withdraw))
    app.add_handler(MessageHandler(filters.Regex("^余额$"), balance))
    app.add_handler(MessageHandler(filters.ALL, unknown))
    logger.info("钱包机器人已启动...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
