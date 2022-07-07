from operator import index
import discord

from discord.ext import commands
from discord import app_commands

from config import Channel, Config
from utils import error_embed, success_embed


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
                general_vc = await voice_category.create_voice_channel(
                    name=f'{member.name}',
                    overwrites=overwrites,
                    position=10,
                    bitrate=64000,
                    user_limit=10,
                    video_quality_mode=discord.VideoQualityMode.auto
                )
                await member.move_to(general_vc)
    
    @commands.Cog.listener('on_voice_state_update')
    async def filter_inactive_voices(self, member, before, after):
        if before.channel:
            if before.channel.id != Channel.NEW_VC_SESSION and before.channel.category_id == Channel.VOICE_CATEGORY:
                if len(before.channel.members) == 0:
                    await before.channel.delete()


    @app_commands.command(name='add', description='➕ Invite a user to a voice channel')
    @app_commands.guilds(Config.SERVER_ID)
    @app_commands.describe(user='The user to invite')
    async def add_user(self, interaction: discord.Interaction, user: discord.Member):
        if not interaction.user.voice:
            vc_channels = [vc for vc in interaction.guild.voice_channels if vc.id != Channel.NEW_VC_SESSION and vc.category_id == Channel.VOICE_CATEGORY]
            if interaction.user.voice.channel in vc_channels:
                await vc_channels[0].set_permissions(user, view_channel=True, connect=True)
                await interaction.response.send_message(embed=success_embed(f'{user.mention} now can see your voice channel'), ephemeral=True)
            else:
                await interaction.response.send_message(embed=error_embed('You are not in a private voice channel'), ephemeral=True)
        else:
            await interaction.response.send_message(embed=error_embed('You are not in a voice channel'), ephemeral=True)



async def setup(client: commands.Bot):
    await client.add_cog(VoiceGenerator(client))