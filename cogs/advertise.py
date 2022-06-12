import random
import discord

from datetime import datetime

from discord.ext import commands, tasks
from discord import app_commands, TextStyle

from config import Channel, Config
from models import AdvertiseModel


class AdvertiseView(discord.ui.View):
    def __init__(self, url: str):
        super().__init__(timeout=None)
        self.url = url
    
        self.add_item(
            discord.ui.Button(
                label='Go to website',
                url=self.url
            )
        )

class AdvertiseModal(discord.ui.Modal, title='Enter Advertise informations'):

    ad_title = discord.ui.TextInput(label='Ad title', placeholder='Enter title here...', style=TextStyle.short, custom_id='ad_title_input', min_length=3, max_length=200)
    context = discord.ui.TextInput(label='Ad context', placeholder='Enter context here...', style=TextStyle.long, custom_id='context_input', min_length=5, max_length=500)
    url = discord.ui.TextInput(label='Ad URL/Link', placeholder='Enter URL/Link here...', style=TextStyle.short, custom_id='url_input')
    banner_url = discord.ui.TextInput(label='Ad Banner URL', placeholder='Enter Banner URL here...', style=TextStyle.short, custom_id='banner_url_input', required=False)
    display_time = discord.ui.TextInput(label='Ad Display Time', placeholder='Enter Display Time here...(Only positive numbers)', style=TextStyle.short, custom_id='display_time_input', default='1')

    async def on_submit(self, interaction: discord.Interaction):
        display_time_value = int(self.display_time.value)
        if display_time_value > 0:
            await AdvertiseModel(
                advertiser=interaction.user.id,
                title=self.ad_title.value,
                context=self.context.value, 
                url=self.url.value,
                random_index=random.randint(1, 10),
                banner_url=self.banner_url.value, 
                display_time=display_time_value
            ).save()

            em = discord.Embed(
                title=self.ad_title.value,
                description=self.context.value,
                color=discord.Color.random()
            )
            if self.banner_url.value:
                em.set_image(url=self.banner_url.value)

            await interaction.response.send_message(
                '> **Advertise created successfully! Preview:**', 
                ephemeral=True, 
                embed=em, 
                view=AdvertiseView(url=self.url.value)
            )
        else:
            await interaction.response.send_message('> **Display time must be positive number!**', ephemeral=True)


class Advertise(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client

        self.display_ads.start()

    ads = app_commands.Group(name='ads', guild_ids=[Config.SERVER_ID], description='Advertise commands')


    @ads.command(name='new', description='Add new advertise')
    @app_commands.checks.has_permissions(administrator=True)
    async def ads_new(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AdvertiseModal())

    @ads.command(name='resend', description='Resend advertise')
    @app_commands.checks.has_permissions(administrator=True)
    async def ads_new(self, interaction: discord.Interaction):
        await self.display_ads()


    @tasks.loop(minutes=60)
    async def display_ads(self):
        channel: discord.TextChannel = await self.client.guild.fetch_channel(Channel.CHITCHAT)
        if channel.last_message:
            if channel.last_message.author == self.client.user:
                return
        ads = await AdvertiseModel.find_many(AdvertiseModel.is_active == True).sort(+AdvertiseModel.random_index).limit(1).to_list()
        if len(ads) > 0:
            ad: AdvertiseModel = ads[0]

            em = discord.Embed(
                title=ad.title,
                description=ad.context,
                color=discord.Color.random()
            )
            if ad.banner_url:
                em.set_image(url=ad.banner_url)
            
            await channel.send(
                embed=em,
                view=AdvertiseView(url= ad.url)
            )

            ad.last_display_dattime = datetime.now()
            ad.display_time -= 1
            await ad.save()

async def setup(client: commands.Bot):
    await client.add_cog(Advertise(client))