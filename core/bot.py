from disnake.ext import commands
import disnake

class Shashank(commands.Bot):
    """
    A discord bot made with love by Shashank.
    """

    def __init__(self):
        intents = disnake.Intents.all()
        super().__init__(intents=intents, description="A discord bot made with love by Shashank#3736.", command_prefix="coc ")
    
    async def on_ready(self):
        print(f"Logged in as {self.user.name} on discord.")
    
