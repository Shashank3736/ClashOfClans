import io
from disnake.ext.commands.errors import ExtensionAlreadyLoaded, NoPrivateMessage
from core.bot import Shashank
import sqlite3
import disnake
from disnake.ext import commands
import json
import textwrap
import traceback
from contextlib import redirect_stdout

SQLITE_FILE_NAME="json.sqlite"

class OwnerOnly(commands.Cog):
  def __init__(self, bot: Shashank):
    self.bot: Shashank = bot
    con = sqlite3.connect(SQLITE_FILE_NAME)
    con.execute(f'CREATE TABLE IF NOT EXISTS COGS (ID text, path text)')
    cogs = con.execute(f"SELECT * FROM COGS").fetchall() or []
    con.close()
    for cog_dict in cogs:
      try:
        bot.load_extension(cog_dict[1])
      except ExtensionAlreadyLoaded:
        pass

  def _get_(self, name):
    """
    Get data from a cog name.
    returns (ID, path)
    """
    con = sqlite3.connect(SQLITE_FILE_NAME)
    data = con.execute(f'SELECT * FROM COGS WHERE ID="{name}"').fetchone() or None
    con.close()
    return data
  
  @commands.command(name='eval', hidden=True)
  @commands.is_owner()
  async def _eval(self, ctx: commands.Context, *, body: str):
    """Evaluates a code."""

    env = {
      'bot': self.bot,
      'ctx': ctx,
      'channel': ctx.channel,
      'author': ctx.author,
      'guild': ctx.guild,
      'message': ctx.message
    }

    env.update(globals())
    body=self.cleanup_code(body)

    stdout = io.StringIO()

    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
    try:
      exec(to_compile, env)
    except Exception as e:
      return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

    func = env['func']
    try:
      with redirect_stdout(stdout):
        ret = await func()
    except Exception as e:
      value = stdout.getvalue()
      await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
      value = stdout.getvalue()
      try:
        await ctx.message.add_reaction('\u2705')
      except Exception:
        pass

      if ret is None:
        if value:
          await ctx.send(f'```py\n{value}\n```')
      else:
        await ctx.send(f'```py\n{value}{ret}\n```')

  def cleanup_code(self, content):
      """Automatically removes code blocks from the code."""
      # remove ```py\n```
      if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

      # remove `foo`
      return content.strip('` \n')

  async def cog_check(self, ctx):
    return await self.bot.is_owner(ctx.author)

  def _get_all_(self):
    con = sqlite3.connect(SQLITE_FILE_NAME)
    data = con.execute(f'SELECT * FROM COGS').fetchall() or []
    con.close()
    return data
  
  def _add_(self, cog_name: str, cog_path: str):
    con = sqlite3.connect(SQLITE_FILE_NAME)
    if self._has_(cog_name):
      con.close()
      return "Already Added."
    con.execute(f"INSERT INTO COGS VALUES ('{cog_name}', '{cog_path}')")
    con.commit()
    con.close()
    return True
  
  def _has_(self, name: str):
    con = sqlite3.connect(SQLITE_FILE_NAME)
    cog = con.execute(f'SELECT * FROM COGS WHERE ID="{name}"').fetchall()
    con.close()
    return True if len(cog) > 0 else False

  def _remove_(self, name: str):
    con = sqlite3.connect(SQLITE_FILE_NAME)
    con.execute(f"DELETE from COGS WHERE ID='{name}'")
    con.commit()
    con.close()
    return True
  
  @commands.is_owner()
  @commands.command()
  async def load(self, ctx: commands.Context, name: str, path: str):
    self.bot.load_extension(path)
    embed=disnake.Embed(color=disnake.Color.blurple(), title="Load Extension", description=f"Loaded extension **{name}** from `{path}`.")
    self._add_(name, path)
    return await ctx.reply(embed=embed)

  @commands.is_owner()
  @commands.command()
  async def unload(self, ctx: commands.Context, name: str):
    data = self._get_(name=name)
    if data is None:
      raise disnake.NotFound(f"Module {name} is not found in database.")
    
    self.bot.unload_extension(data[1])
    embed=disnake.Embed(color=disnake.Color.blurple(), title="Unload Extension", description=f"Unloaded extension **{name}** from `{data[1]}`.")
    self._remove_(name)
    return await ctx.reply(embed=embed)
    
  @commands.is_owner()
  @commands.command(name='reload')
  async def _reload(self, ctx: commands.Context, name: str):
      data=self._get_(name=name)
      if data is not None:
        self.bot.reload_extension(data[1])
        embed=disnake.Embed(color=disnake.Color.blurple(), title="Reload Extension", description=f"Reloaded extension **{name}** from `{data[1]}`.")
        # self._add_(name, data[name])
        return await ctx.reply(embed=embed)
      else:
        return await ctx.reply(f"Module {name} is not loaded.")

  @commands.is_owner()
  @commands.command()
  async def block(self, ctx: commands.Context, user: disnake.User):
    self.bot.db.push('blocked_users', user.id)
    embed=disnake.Embed(title="User Blocked", description=f"**{user.name}#{user.discriminator}** is blocked from using the bot.", color=disnake.Color.blurple())
    return await ctx.reply(embed=embed)

  @commands.is_owner()
  @commands.command()
  async def loaded(self, ctx: commands.Context):
    description=f"**List of loaded cogs:**\n{', '.join(self.bot.cogs)}"
    embed=disnake.Embed(color=disnake.Color.blurple(),description=description)
    return await ctx.reply(embed=embed)

  @commands.Cog.listener()
  async def on_command_error(self, ctx: commands.Context, exception: commands.CommandError):
    if isinstance(exception, (NoPrivateMessage, commands.CommandNotFound)):
      return
    embed = disnake.Embed(color=disnake.Color.red(), title="Oops! Something is wrong",
    description=f"{exception}")
    embed.set_footer(text='Contact Shashank#3736 for solution')
    print(exception.__module__)
    return await ctx.reply(embed=embed)

def setup(bot: commands.Bot):
  bot.add_cog(OwnerOnly(bot=bot))
  