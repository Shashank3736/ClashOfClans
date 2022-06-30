from disnake.ext.commands.errors import NoPrivateMessage, NoEntryPointError
from core.bot import Shashank
import os
from dotenv import load_dotenv

load_dotenv('.env')

bot = Shashank()

@bot.check
async def only_guild(ctx):
    if ctx.guild is None:
        raise NoPrivateMessage("Bot do not support DM commands.")
    else:
        return True
  
# ----------------------- Get env ----------------------------- #
if os.environ.get("BOT_TOKEN") is None:
    with open('.env', 'w') as fl:
        token = input("BOT TOKEN> ")
        fl.write(f"BOT_TOKEN={token}")
    load_dotenv('.env')

bot.load_extension('cogs.owner')

# ----------------------- load plugins ------------------------------ #

# ------------------------------------------------------------------- #

bot.run(os.environ['BOT_TOKEN'])