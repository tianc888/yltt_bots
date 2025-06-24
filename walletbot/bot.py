import asyncio
from telegram.ext import ApplicationBuilder

# 从 config.py 中导入你的 Token
from config import WALLETBOT_TOKEN

async def main():
    app = ApplicationBuilder().token(WALLETBOT_TOKEN).build()

    # 在这里注册你的各类命令和 handler
    # 例如: app.add_handler(CommandHandler("start", start_callback))
    # 你自己的其它初始化逻辑...

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
