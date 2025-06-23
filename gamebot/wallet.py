import db

def get_user_balance(user_id):
    return db.get_balance(user_id)

def change_user_balance(user_id, amount, reason, note):
    db.change_balance(user_id, amount, reason, note)

async def handle_balance(update, context):
    balance = get_user_balance(update.effective_user.id)
    await update.message.reply_text(f"您的余额为：{balance}")

async def handle_recharge(update, context):
    from config import RECHARGE_ADDRESS, RECHARGE_QR_PATH
    try:
        with open(RECHARGE_QR_PATH, "rb") as f:
            await update.message.reply_photo(f, caption=f"请向以下地址充值：\n{RECHARGE_ADDRESS}")
    except Exception:
        await update.message.reply_text(f"请向以下地址充值：\n{RECHARGE_ADDRESS}")

async def handle_withdraw(update, context):
    await update.message.reply_text("请输入提现金额：")
