# 渔乐天天钱包 & 游戏机器人

## 功能
- 钱包机器人：充值（USDT/CNY）、提币、转账、收款、所有菜单均可返回上一步
- 游戏机器人：充值、提现时自动跳转“钱包”机器人并余额互通

## 文件结构

```
.
├── db.py
├── wallet.db  # 自动生成
├── static/
│   └── recharge_qr.png
├── gamebot/
│   ├── bot.py
│   ├── config.py
│   ├── requirements.txt
│   └── handlers/
│       └── ...
├── walletbot/
│   ├── bot.py
│   ├── config.py
│   ├── requirements.txt
│   └── handlers/
│       └── ...
```

## 快速开始（GitHub Codespaces）

1. 上传二维码图片到 `static/recharge_qr.png`
2. 修改 `gamebot/config.py` 和 `walletbot/config.py` 分别填入两个机器人的 TOKEN 和 BOT_NAME
3. 安装依赖（推荐分别在两个终端窗口中运行）

    ```bash
    # 运行钱包机器人
    cd walletbot
    pip install -r requirements.txt
    python bot.py
    # 运行游戏机器人
    cd ../gamebot
    pip install -r requirements.txt
    python bot.py
    ```

4. 在 Telegram 分别体验两机器人
    - 游戏机器人充值/提现时会有“钱包”按钮跳转到钱包机器人
    - 钱包机器人所有菜单分支均有“返回上一步”按钮
    - 余额数据完全互通

## 重要说明

- wallet.db 会自动创建，无需手动建立
- 若需正式部署，请用公网服务器并配置 Webhook
- 如需更换二维码，直接覆盖 static/recharge_qr.png

---

> **作者：tianc888**