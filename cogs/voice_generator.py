import discord

from datetime import datetime, timedelta

from beanie.odm.operators.update.general import Inc
from discord.ext import commands
from discord import app_commands

from config import Channel, Config
from models import MemberModel
from utils import error_embed, success_embed
from cache import VoiceTime


class VoiceGenerator(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.inactive_session = []

        
    @commands.Cog.listener('on_voice_state_update')
    async def member_join_handler(self, member, before, after):
        if after.channel:
            if after.channel.id == Channel.NEW_VC_SESSION and member.bot == False:
                voice_category = await self.client.fetch_channel(Channel.VOICE_CATEGORY)
                overwrites = {
                    voice_category.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    member: discord.PermissionOverwrite(mute_members=True, moderate_members=True, deafen_members=True, move_members=True, use_voice_activation=True),
                }
                newsession_channel = await self.client.fetch_channel(Channel.NEW_VC_SESSION)
                general_vc = await voice_category.create_voice_channel(
                    name=f'╠ 👤 {member.name}',
                    overwrites=overwrites,
                    position= newsession_channel.position - 1,
                    bitrate=64000,
                    user_limit=10,
                    video_quality_mode=discord.VideoQualityMode.auto
                )
                await member.move_to(general_vc)
                VoiceTime(
                    member_id=member.id
                ).save()
    
    @commands.Cog.listener('on_voice_state_update')
    async def filter_inactive_voices(self, member, before, after):
        if before.channel:
            if before.channel.id not in [Channel.NEW_VC_SESSION, Channel.INVITE, Channel.PUBLIC, Channel.MUSIC] and before.channel.category_id == Channel.VOICE_CATEGORY:
                if len(before.channel.members) == 0:
                    await before.channel.delete()
                    voice_status = VoiceTime.get_by(member_id=member.id)
                    if voice_status:
                        voicetime = datetime.now() - voice_status.join_time
                        if voicetime > timedelta(minutes=1):
                            bonus_xp = (int(voicetime.total_seconds() // 60)) * 5
                            member = await MemberModel.find_one(MemberModel.member_id == member.id)
                            member.xp += bonus_xp
                            await member.save()

                        voice_status.delete()


    @app_commands.command(name='add', description='➕ Invite a user to a voice channel')
    @app_commands.guilds(Config.SERVER_ID)
    @app_commands.describe(user='The user to invite')
    async def add_user(self, interaction: discord.Interaction, user: discord.Member):
        if interaction.user.voice:
            vc_channels = [vc for vc in interaction.guild.voice_channels if vc.id != Channel.NEW_VC_SESSION and vc.category_id == Channel.VOICE_CATEGORY]
            if interaction.user.voice.channel in vc_channels:
                await vc_channels[0].set_permissions(user, view_channel=True, connect=True)
                await interaction.response.send_message(embed=success_embed(f'{user.mention} now can see your voice channel'), ephemeral=True)
            else:
                await interaction.response.send_message(embed=error_embed('You are not in a private voice channel'), ephemeral=True)
        else:
            await interaction.response.send_message(embed=error_embed('You are not in a voice channel'), ephemeral=True)

    @commands.has_permissions(manage_guild=True)
    @commands.command(aliases=["vcinvite"])
    async def vc_invite(self, ctx:commands.Context):

        '''Create new `VOICE INVITE` message'''

        term_channel = await self.client.fetch_channel(Channel.INVITE)
        embed=discord.Embed(
            title="Private Voice Channels",
            description=f'''
<:lock:994508434554761216> ● By Joining the **New Session** voice channel you can create your own **private** voice channel.

<:add:994525256289108069> ● By typing /add [username] you can invite your friends to **see and join your private voice channel**''',
            color=0xFB005B
        )
        embed.set_image(url='https://media.discordapp.net/attachments/980177765452099654/994524746567909446/Voice.png')
        embed.set_footer(text= "Type /add and click on your friend's username to add him to the voice channel" , icon_url='https://cdn.discordapp.com/attachments/980177765452099654/994526233981374525/add.png')
        await term_channel.send(embed=embed)
        await ctx.reply('> **vc invite has been made!**')
    
    @commands.Cog.listener('on_message')
    async def delete_invite_messages(self, message: discord.Message):
        if message.author.bot == False and message.channel.id == Channel.INVITE:
            await message.delete()

async def setup(client: commands.Bot):
    await client.add_cog(VoiceGenerator(client))