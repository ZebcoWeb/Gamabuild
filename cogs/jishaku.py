from jishaku.cog import Jishaku
from discord.ext import commands

async def setup(bot: commands.Bot):

    await bot.add_cog(Jishaku(bot=bot))