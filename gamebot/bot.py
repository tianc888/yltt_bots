import asyncio
from telegram.ext import ApplicationBuilder

# 这里可以引入你自己的模块和配置
# from config import TELEGRAM_TOKEN

async def main():
    # 用你的实际token替换下面的YOUR_GAMEBOT_TOKEN，或者用 config 里的 TELEGRAM_TOKEN
    app = ApplicationBuilder().token("YOUR_GAMEBOT_TOKEN").build()

    # 在这里注册你的各类命令和handler
    # 例如: app.add_handler(CommandHandler("start", start_callback))
    # 你自己的其它初始化逻辑...

    print("游戏机器人已启动...")
    await app.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except RuntimeError:
        asyncio.run(main())
