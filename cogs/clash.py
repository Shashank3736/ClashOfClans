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
        self.coc_client.load_game_data = coc.LoadGameData(default=True)
    
    def get_rushed_unit(self, player: coc.Player):
        """
        Get rushed unit of a player.
        """
        heroes: list[coc.Hero] = player.heroes()
        hero_rush_percent = []

        for hero in heroes:
            hero_name = hero.name
            hero_lvl = hero.level
            hero_req_lvl = hero.get_max_level_for_townhall(player.town_hall - 1)
            if hero_lvl < hero_req_lvl:
                hero_rush_percent.append((hero_name, hero.level, hero_req_lvl))
        
        troops: list[coc.Troop] = player.home_troops()
        troop_rush_percent = []

        for troop in troops:
            troop_req_lvl: int = troop.get_max_level_for_townhall(player.town_hall - 1)
            if troop.level < troop_req_lvl:
                troop_rush_percent.append((troop.name, troop.level, troop_req_lvl))

        spells: list[coc.Spell] = player.spells()
        spell_rush_percent = []

        for spell in spells:
            spell_req_lvl: int = spell.get_max_level_for_townhall(player.town_hall - 1)
            if spell.level < spell_req_lvl:
                spell_rush_percent.append((spell.name, spell.level, spell_req_lvl))
        
        return (hero_rush_percent, troop_rush_percent, spell_rush_percent)
    
    def get_rushed_percentage(self, player: coc.Player):
        """
        Get rushed percentage of a player.
        """
        rushed_units = self.get_rushed_unit(player)
        rushed_unit = rushed_units[0] + rushed_units[1] + rushed_units[2]
        total_unit = len(rushed_unit)
        current_data = 0

        for unit in rushed_unit:
            current_data += unit[1]/unit[2]
        
        return (current_data/total_unit)*100


    # slash commands
    @commands.slash_command()
    async def search(self, inter):
        """
        Parent command for search of clan and player
        """
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
        
        embed = disnake.Embed(title=f"Information about player {player.name}", url=player.share_link)
        embed.add_field('Trophies', f"Current: {player.trophies}\nAll time best: {player.best_trophies}")

        player_clan = await player.get_detailed_clan()

        if player_clan is not None:
            embed.add_field('Clan', f"[{player_clan.name}]({player_clan.share_link})")
        
        embed.add_field('Rushed', self.get_rushed_percentage(player))
        return await inter.response.send_message(embed=embed)
        
def setup(bot: Shashank):
    bot.add_cog(ClashOfClans(bot))