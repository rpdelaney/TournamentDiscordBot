# Tournament Discord Bot

A bot for organizing online game tournaments via
[Discord](https://discord.com/).

## Self-hosting

### Create a bot in the developer portal

You need to set up a bot on the Discord developer portal. Follow the
[instructions](https://discordpy.readthedocs.io/en/stable/discord.html). Under
"Privileged Gateway Intents", enable the following settings:

- Server Members Intent
- Message Content Intent

### Run the code locally

These environment variables must be set:

DISCORD_TOKEN: The bot token. APP_ID: The Application ID for the bot in the
developer portal.

To start the bot:

```console
$ python3 -m tdb.main
```
