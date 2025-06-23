import logging
import asyncio
import datetime
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
)
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from config import TELEGRAM_TOKEN, GROUP_ID, ADMINS, BOT_USERNAME

import game, wallet, group, risk, rebate, admin

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_admin_link():
    admin_id = ADMINS[0] if ADMINS else None
    if admin_id:
        return f"https://t.me/{BOT_USERNAME}" if isinstance(admin_id, str) else f"https://t.me/user?id={admin_id}"
    return "https://t.me/"

def get_bot_link():
    return f"https://t.me/{BOT_USERNAME}"

### 私聊菜单
async def my_menu(update: Update, context):
    if update.effective_chat.type != 'private':
        return
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("充值", callback_data="recharge"),
         InlineKeyboardButton("提现", callback_data="withdraw")],
        [InlineKeyboardButton("返利日志", callback_data="rebatelog"),
         InlineKeyboardButton("邀请信息", callback_data="inviteinfo")]
    ])
    await update.message.reply_text("请选择操作：", reply_markup=markup)

async def inline_recharge(update: Update, context):
    await wallet.handle_recharge(update, context)

async def inline_withdraw(update: Update, context):
    await wallet.handle_withdraw(update, context)

async def inline_rebatelog(update: Update, context):
    await rebate.handle_rebate_log(update, context)

async def inline_inviteinfo(update: Update, context):
    await rebate.handle_invite_info(update, context)

async def balance_cmd(update: Update, context):
    if update.effective_chat.type != 'private':
        return
    await wallet.handle_balance(update, context)

async def walletlog_cmd(update: Update, context):
    if update.effective_chat.type != 'private':
        return
    await wallet.handle_wallet_log(update, context)

async def recharge_cmd(update: Update, context):
    if update.effective_chat.type != 'private':
        return
    await wallet.handle_recharge(update, context)

async def withdraw_cmd(update: Update, context):
    if update.effective_chat.type != 'private':
        return
    await wallet.handle_withdraw(update, context)

async def rebatelog_cmd(update: Update, context):
    if update.effective_chat.type != 'private':
        return
    await rebate.handle_rebate_log(update, context)

async def inviteinfo_cmd(update: Update, context):
    if update.effective_chat.type != 'private':
        return
    await rebate.handle_invite_info(update, context)

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
    # 获取目标用户
    target_id = None
    target_name = "用户"
    if msg.reply_to_message:
        target_id = msg.reply_to_message.from_user.id
        target_name = msg.reply_to_message.from_user.full_name
    elif '@' in text:
        username = text.split('@')[-1]
        target_id = wallet.get_uid_by_username(username)
        target_name = f"@{username}"
    if not target_id:
        await msg.reply_text("请通过回复玩家消息或@玩家来增加余额。")
        return
    wallet.change_user_balance(target_id, amount, "管理员加余额", f"管理员@{msg.from_user.full_name} 操作")
    new_balance = wallet.get_user_balance(target_id)
    await msg.reply_text(f"{target_name} 已加余额{amount}，当前余额：{new_balance}")

async def group_bet_handler(update: Update, context):
    await game.handle_bet(update, context)

async def cancel_bet_handler(update: Update, context):
    await game.handle_cancel(update, context)

async def report_cmd(update: Update, context):
    await admin.handle_report(update, context)

async def kick_cmd(update: Update, context):
    await group.handle_kick(update, context)

async def mute_cmd(update: Update, context):
    await group.handle_mute(update, context)

async def blacklist_cmd(update: Update, context):
    await risk.handle_blacklist(update, context)

async def whitelist_cmd(update: Update, context):
    await risk.handle_whitelist(update, context)

async def keyword_reply_hook(update: Update, context):
    await group.handle_keyword_reply(update, context)

async def lottery_round(app):
    group_id = GROUP_ID
    game.config_group_id(group_id)
    while True:
        period_code = game.start_new_round()
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        open_time = now
        close_time = open_time + datetime.timedelta(seconds=45)
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("联系客服", url=get_admin_link()),
             InlineKeyboardButton("充值/提现", url=get_bot_link())]
        ])
        open_text = (
            f"--YLttK3第{period_code}期\n"
            f"本期封盘：{close_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"\n" * 5 +
            "--本期已开盘，玩家请开始下注"
        )
        await app.bot.send_message(group_id, open_text, reply_markup=markup)
        await asyncio.sleep(43)
        await game.settle_round(app, group_id, period_code, close_time)
        await asyncio.sleep(1)

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler(["start", "我的"], my_menu))
    app.add_handler(CallbackQueryHandler(inline_recharge, pattern="^recharge$"))
    app.add_handler(CallbackQueryHandler(inline_withdraw, pattern="^withdraw$"))
    app.add_handler(CallbackQueryHandler(inline_rebatelog, pattern="^rebatelog$"))
    app.add_handler(CallbackQueryHandler(inline_inviteinfo, pattern="^inviteinfo$"))
    app.add_handler(CommandHandler(["balance", "余额"], balance_cmd))
    app.add_handler(CommandHandler(["walletlog", "钱包日志"], walletlog_cmd))
    app.add_handler(CommandHandler(["recharge", "充值"], recharge_cmd))
    app.add_handler(CommandHandler(["withdraw", "提现"], withdraw_cmd))
    app.add_handler(CommandHandler(["rebatelog", "返利日志"], rebatelog_cmd))
    app.add_handler(CommandHandler(["inviteinfo", "邀请信息"], inviteinfo_cmd))
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, admin_add_balance_handler))
    app.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.Regex(r"^(取消|取消下注)$"), cancel_bet_handler))
    app.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.TEXT, group_bet_handler))
    app.add_handler(CommandHandler(["report", "报表"], report_cmd))
    app.add_handler(CommandHandler(["kick", "踢人"], kick_cmd))
    app.add_handler(CommandHandler(["mute", "禁言"], mute_cmd))
    app.add_handler(CommandHandler(["blacklist", "拉黑"], blacklist_cmd))
    app.add_handler(CommandHandler(["whitelist", "白名单"], whitelist_cmd))
    app.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.TEXT, keyword_reply_hook))
    asyncio.create_task(lottery_round(app))
    logger.info("游戏机器人已启动...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
