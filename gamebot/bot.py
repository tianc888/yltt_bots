import asyncio
from telegram.ext import ApplicationBuilder

async def main():
    app = ApplicationBuilder().token("YOUR_GAMEBOT_TOKEN").build()
    # ... 你的业务逻辑和 handler 注册
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
