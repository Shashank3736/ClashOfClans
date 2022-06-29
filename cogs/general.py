from disnake.ext import commands

from core.bot import Shashank

class General(commands.Cog):
    """
    General slash command for everyone.
    """
    def __init__(self, bot: Shashank) -> None:
        super().__init__()
        self.bot = bot
    
    