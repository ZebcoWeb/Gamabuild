import discord
import re

from discord.ext import commands

from config import Channel

class SelfPromo(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.reply_message = None

    @commands.Cog.listener('on_message')
    async def promote_message_handler(self, message: discord.Message):
        if message.channel.id == Channel.SELFPROMO and message.author.bot == False:
            urls = re.findall("(?P<url>https?://[^\s]+)", message.content)
            if len(urls) > 0:
                await message.delete()
                promo_message = await message.channel.send(urls[0])
                if self.reply_message:
                    await self.reply_message.delete()
                em = discord.Embed(description=f'**Can\'t send any message?** [Click here for more information](https://discord.com)', color=discord.Colour.purple())
                self.reply_message = await promo_message.reply(embed=em)
                await promo_message.delete(delay=43200)
            else:
                await message.delete()


async def setup(client: commands.Bot):
    await client.add_cog(SelfPromo(client))