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
    with open('cogs/cogs.json') as f:
      self.cogs = json.load(f)
    
    for key in self.cogs.keys():
      try:
        bot.load_extension(self.cogs[key])
      except ExtensionAlreadyLoaded:
        pass
  
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
  
  @commands.is_owner()
  @commands.command()
  async def load(self, ctx: commands.Context, name: str):
    self.bot.load_extension(self.cogs[name])
    embed=disnake.Embed(color=disnake.Color.blurple(), title="Load Extension", description=f"Loaded extension **{name}** from `{self.cogs[name]}`.")
    return await ctx.reply(embed=embed)

  @commands.is_owner()
  @commands.command()
  async def unload(self, ctx: commands.Context, name: str):
    data = self.cogs[name]
    if data is None:
      raise disnake.NotFound(f"Module {name} is not found in database.")
    
    self.bot.unload_extension(data)
    embed=disnake.Embed(color=disnake.Color.blurple(), title="Unload Extension", description=f"Unloaded extension **{name}** from `{data}`.")
    return await ctx.reply(embed=embed)
    
  @commands.is_owner()
  @commands.command(name='reload')
  async def _reload(self, ctx: commands.Context, name: str):
      pass

  @commands.is_owner()
  @commands.command()
  async def block(self, ctx: commands.Context, user: disnake.User):
    pass

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
  