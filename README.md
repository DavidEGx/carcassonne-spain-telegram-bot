# 🤖 carcassonne-spain-telegram-bot
Send updates about [Carcassonne Spain](https://carcassonnespain.es/) league to Telegram groups.

![Bot demo](img/demo.png)

## 📦 Setup

### Telegram bot

You need to create a Telegram bot in case you don't have one:

1. Open a chat with [BotFather](https://t.me/BotFather).
2. Type */newbot* and follow BotFather instructions.

Once you are done, edit [config.yml](config.yml) and fill your Telegram token.

### Dependencies

```bash
$ pip install --no-cache-dir -r requirements.txt
```

Or using Docker:

```bash
$ docker build -t carcassonnespain .
```

## 🚀 Usage

```bash
$ bin/bot
```

Again, if you prefer to use Docker:

```bash
$ docker run carcassonnespain
```

Once it is running, go to the Telegram application and add the bot to any group you want. It will start to send daily updates to all the groups.

## 👷 Contributing

Not much to do here.

In any case, if you want to change something simply check the [bot](bin/bot) file.

## 📜 License

[GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html)

