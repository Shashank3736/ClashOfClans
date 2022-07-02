import os
from disnake.ext import commands
import disnake
import time, datetime

class Shashank(commands.Bot):
    """
    A discord bot made with love by Shashank.
    """

    def __init__(self):
        intents = disnake.Intents.all()
        super().__init__(
            intents=intents, 
            description="A discord bot made with love by Shashank#3736.", 
            command_prefix="coc ", test_guilds=list(map(int, os.environ["GUILD_ID"].split(' '))),
            sync_commands_debug=True
            )
        self.start_time = time.time()
    
    async def on_ready(self):
        print(f"Logged in as {self.user.name} on discord.")
        print(f"Currently I m in {str(len(self.guilds))} server(s).")

    def uptime(self):
        return str(datetime.timedelta(seconds=round(time.time()-self.start_time)))
