import discord
import random

from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta

from config import Channel, Config
from models import MemberModel



class LevelSystem(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
    
    
    @commands.Cog.listener('on_message')
    async def increase_xp_chitchat(self, message: discord.Message):
        if not message.author.bot:
            if message.channel.id == Channel.CHITCHAT:
                await MemberModel.find_one(MemberModel.member_id == message.author.id).inc({MemberModel.xp: Config.INC_XP_CHITCHAT})
    

    @commands.Cog.listener('on_guild_update')
    async def increase_xp_boost(self, before: discord.Guild, after: discord.Guild):
        if before.premium_subscription_count < after.premium_subscription_count:
            booster = [i for i in after.premium_subscribers if i not in before.premium_subscribers]
            await MemberModel.find_one(MemberModel.member_id == booster[0]).inc({MemberModel.xp: Config.INC_XP_BOOST})
    

    @app_commands.command(name='daily', description='🎁 Get daily xp reward')
    @app_commands.guilds(Config.SERVER_ID)
    async def daily(self, interaction: discord.Interaction):
        member: MemberModel = await MemberModel.find_one(MemberModel.member_id == interaction.user.id)
        log_channel = await self.client.fetch_channel(Channel.ACTIVITIES)
        if not member.last_do_daily:
            member.last_do_daily = datetime.now()
            random_xp = random.randint(25, Config.MAX_XP_DAILY) # Having more chances for the first time
            member.xp += random_xp
            await member.save()
            await interaction.response.send_message(f'🎁 You got **{random_xp}**xp for daily!', ephemeral=True)
            await log_channel.send(f'🎁 ● {interaction.user.mention} got {random_xp}xp <:stats:994300647082041534> for daily!')
        else:
            if (datetime.now() - member.last_do_daily).days >= 1:
                member.last_do_daily = datetime.now()
                random_xp = random.randint(Config.MIN_XP_DAILY, Config.MAX_XP_DAILY)
                member.xp += random_xp
                await member.save()
                await interaction.response.send_message(f'🎁 You got **{random_xp}**xp for daily!', ephemeral=True)
                await log_channel.send(f'🎁 ● {interaction.user.mention} got {random_xp}xp <:stats:994300647082041534> for daily!')
            else:
                remaining_time = (member.last_do_daily + timedelta(days=1) - datetime.now())
                await interaction.response.send_message(f'❗You already did `daily` today!\n\n➔ Try again in `{remaining_time.seconds // 3600}` hours, `{remaining_time.seconds // 60 % 60}` minutes and `{remaining_time.seconds % 60}` seconds.', ephemeral=True)


    @app_commands.command(name='weekly', description='🚀 Get weekly xp reward')
    @app_commands.guilds(Config.SERVER_ID)
    async def weekly(self, interaction: discord.Interaction):

        member: MemberModel = await MemberModel.find_one(MemberModel.member_id == interaction.user.id)
        log_channel = await self.client.fetch_channel(Channel.ACTIVITIES)
        if not member.last_do_weekly:
            member.last_do_weekly = datetime.now()
            random_xp = random.randint(140, Config.MAX_XP_WEEKLY) # Having more chances for the first time
            member.xp += random_xp
            await member.save()
            await interaction.response.send_message(f'🚀 You got **{random_xp}**xp for weekly!', ephemeral=True)
            await log_channel.send(f'🚀 ● {interaction.user.mention} got {random_xp}xp <:stats:994300647082041534> for weekly!')
        else:
            if (datetime.now() - member.last_do_weekly).days >= 7:
                member.last_do_weekly = datetime.now()
                random_xp = random.randint(Config.MIN_XP_WEEKLY, Config.MAX_XP_WEEKLY)
                member.xp += random_xp
                await member.save()
                await interaction.response.send_message(f'🚀 You got **{random_xp}**xp for weekly!', ephemeral=True)
                await log_channel.send(f'🚀 ● {interaction.user.mention} got {random_xp}xp <:stats:994300647082041534> for weekly!')
            else:
                remaining_time = (member.last_do_weekly + timedelta(weeks=1) - datetime.now())
                await interaction.response.send_message(f'❗You already did `weekly` this week!\n\n➔ Try again in `{remaining_time.days}` days, `{remaining_time.seconds // 3600}` hours, `{remaining_time.seconds // 60 % 60}` minutes and `{remaining_time.seconds % 60}` seconds.', ephemeral=True)


async def setup(client: commands.Bot):
    await client.add_cog(LevelSystem(client))