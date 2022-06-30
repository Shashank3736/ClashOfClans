import os
from disnake.ext import commands
import disnake

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
    
    async def on_ready(self):
        print(f"Logged in as {self.user.name} on discord.")
        print(f"Currently I m in {str(self.guilds.count())} server(s).")
    
