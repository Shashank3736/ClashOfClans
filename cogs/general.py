from disnake import ApplicationCommandInteraction
import disnake
from disnake.ext import commands
import json

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
        return await inter.response.send_message(f"Bot ping is {str(round(self.bot.latency*1000))}ms")
    
    @commands.slash_command()
    async def about(self, inter: ApplicationCommandInteraction):
        """
        Information about the bot.
        """
        with open('bot_info.json') as f:
            data = json.load(f)
        
        embed = disnake.Embed(
            title=f"About {self.bot.user.name} bot", 
            description=data['info'], 
            color=disnake.Color.blurple()).add_field('Creator', data['creator']).add_field('Version', data['version'])
        embed.add_field('Uptime', self.bot.uptime())
        return await inter.response.send_message(embed=embed)

def setup(bot: Shashank):
    bot.add_cog(General(bot))
