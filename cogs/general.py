from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from core.bot import Shashank

class General(commands.Cog):
    """
    General slash command for everyone.
    """
    def __init__(self, bot: Shashank) -> None:
        super().__init__()
        self.bot = bot
    
    @commands.slash_command()
    async def ping(self, inter: ApplicationCommandInteraction):
        """
        Get the ping of the discord bot.
        """
        return await inter.response.send_message(f"Bot ping is {str(round(self.bot.latency))}ms")

def setup(bot: Shashank):
    bot.add_cog(General(bot))