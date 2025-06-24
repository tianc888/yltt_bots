import asyncio
from telegram.ext import ApplicationBuilder

# 如果你有配置文件，比如 config.py，可以这样导入：
# from config import TELEGRAM_TOKEN

async def main():
    # 用你的实际钱包机器人 token 替换下面的 YOUR_WALLETBOT_TOKEN
    app = ApplicationBuilder().token("YOUR_WALLETBOT_TOKEN").build()

    # 在这里注册你的各类命令和 handler
    # 例如: app.add_handler(CommandHandler("start", start_callback))
    # 可以加入你自己的其它初始化逻辑...

    print("钱包机器人已启动...")
    await app.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except RuntimeError:
        asyncio.run(main())
