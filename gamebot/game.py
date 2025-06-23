import wallet
import datetime

class Round:
    def __init__(self, period_code):
        self.period_code = period_code
        self.bets = []  # (user_id, amount, username, bet_type)
        self.is_closed = False

    def add_bet(self, user_id, amount, username, bet_type):
        self.bets.append((user_id, amount, username, bet_type))

    def get_bets(self):
        return self.bets

    def get_bets_by_user(self, user_id):
        return [b for b in self.bets if b[0] == user_id]

    def remove_bets_by_user(self, user_id):
        self.bets = [b for b in self.bets if b[0] != user_id]

current_round = None
group_id = None

def config_group_id(gid):
    global group_id
    group_id = gid

def start_new_round():
    global current_round
    period_code = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    current_round = Round(period_code)
    return period_code

def parse_bet_message(text):
    # 这里应写下注格式解析，示例：大100、小50等
    return ("大", 100)  # 示例

async def handle_bet(update, context):
    msg = update.message
    if msg.chat.type not in ['group', 'supergroup']:
        return
    text = msg.text.strip()
    bet_parsed = parse_bet_message(text)
    if not bet_parsed:
        await msg.reply_text("下注格式有误，例：大100、小200、单50、双100")
        return
    bet_type, amount = bet_parsed
    if not current_round or current_round.is_closed:
        await msg.reply_text("投注无效，本期已封盘")
        return
    balance = wallet.get_user_balance(msg.from_user.id)
    if balance < amount:
        await msg.reply_text("余额不足，请先充值")
        return
    wallet.change_user_balance(msg.from_user.id, -amount, "下注", f"{current_round.period_code} {bet_type}{amount}")
    username = msg.from_user.full_name
    current_round.add_bet(msg.from_user.id, amount, username, bet_type)
    await msg.reply_text(f"下注成功！本期[{current_round.period_code}] 你的投注：{bet_type}{amount}")

async def handle_cancel(update, context):
    msg = update.message
    if not current_round or current_round.is_closed:
        await msg.reply_text("本期已封盘，无法取消下注")
        return
    bets = current_round.get_bets_by_user(msg.from_user.id)
    if not bets:
        await msg.reply_text("你本期没有下注，无需取消")
        return
    total_refund = sum([b[1] for b in bets])
    for b in bets:
        wallet.change_user_balance(msg.from_user.id, b[1], "取消下注", f"{current_round.period_code} {b[2]}{b[1]}")
    current_round.remove_bets_by_user(msg.from_user.id)
    await msg.reply_text(f"已取消本期所有下注并返还{total_refund}余额。")

async def settle_round(app, group_id, period_code, close_time):
    # 这里只做演示，未实现骰子投掷与结算
    await app.bot.send_message(group_id, f"--YLttK3第{period_code}期结算。功能待完善。")
