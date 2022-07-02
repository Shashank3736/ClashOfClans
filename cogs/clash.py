from disnake.ext import commands
import disnake
import coc
import os
from core.bot import Shashank

class ClashOfClans(commands.Cog):
    """
    Commands related to clash of clans api.
    """

    def __init__(self, bot: Shashank) -> None:
        super().__init__()
        self.bot = Shashank
        self.coc_client = coc.login(os.environ['COC_EMAIL'], os.environ['COC_PASSWORD'])
    
    # slash commands
    @commands.slash_command()
    async def search(self, inter):
        pass

    @search.sub_command(name='player')
    async def search_player(self, inter: disnake.Interaction, tag: str):
        """
        Get information about a clash of clans player with their tag.

        Parameters
        ---------------------------
        tag: Player tag
        """
        try:
            player = await self.coc_client.get_player(tag)
        except coc.errors.NotFound:
            return await inter.response.send_message("Player not found!", ephemeral=True)
        
        embed = disnake.Embed(title=f"Information about player {player.name}")
        embed.add_field('Trophies', player.trophies)
        embed.add_field('Clan', player.clan)
