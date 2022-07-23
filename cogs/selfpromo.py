import discord
import re

from discord.ext import commands

from config import Channel
from models import MemberModel
from utils import error_embed

class SelfPromoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Can\'t Send Any Message?', style=discord.ButtonStyle.blurple, custom_id='SELF_PROMO_BUTTON', emoji=discord.PartialEmoji.from_str('<:questionmark:994300948295983265>'))
    async def callback(self, interaction: discord.Interaction, button):
        await interaction.response.send_message(
            embed=error_embed(
                f'''
<:Warn:866761211945156628> You need to at least be <:stats:994300647082041534> Level 5 in order to send a message in this channel !
● Type /help in the <#{Channel.ACTIVITIES}> channel for more details
'''
            ),
            ephemeral=True
        )

class SelfPromo(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

        self.client.add_view(SelfPromoView())

    @commands.Cog.listener('on_message')
    async def promote_message_handler(self, message: discord.Message):
        if message.channel.id == Channel.SELFPROMO and message.author.bot == False:
            member = await MemberModel.find_one(MemberModel.member_id == message.author.id)
            if member.level >= 5:
                urls = re.findall("(?P<url>https?://[^\s]+)", message.content)
                if len(urls) > 0:
                    await message.delete()
                    promo_message = await message.channel.send(urls[0], view=SelfPromoView())
                    await promo_message.delete(delay=43200)
                else:
                    await message.delete()
            else:
                await message.delete()


async def setup(client: commands.Bot):
    await client.add_cog(SelfPromo(client))