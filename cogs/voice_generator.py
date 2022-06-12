import discord

from discord.ext import commands, tasks
from datetime import datetime

from config import Channel



class VoiceGenerator(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.inactive_session = []

        self.delete_inactive_voices.start()

    @commands.Cog.listener('on_voice_state_update')
    async def member_join_handler(self, member, before, after):
        if after.channel:
            if after.channel.id == Channel.NEW_VC_SESSION and member.bot == False:
                voice_category = await self.client.fetch_channel(Channel.VOICE_CATEGORY)
                voices_number = len(voice_category.voice_channels) - 1

                overwrites = {
                    member: discord.PermissionOverwrite(mute_members=True, moderate_members=True, deafen_members=True, move_members=True, use_voice_activation=True),
                }
                general_vc = await voice_category.create_voice_channel(
                    name=f'General # {voices_number}',
                    overwrites=overwrites,
                    position=10,
                    bitrate=64000,
                    user_limit=10,
                    video_quality_mode=discord.VideoQualityMode.auto
                )
                await member.move_to(general_vc)
    
    @commands.Cog.listener('on_voice_state_update')
    async def filter_inactive_voices(self, member, before, after):
        if member.bot == False:
            if before.channel:
                channel = before.channel
                vc_type = 'before'
            if after.channel:
                channel = after.channel
                vc_type = 'after'

            if channel.id != Channel.NEW_VC_SESSION and channel.category_id == Channel.VOICE_CATEGORY:
                if vc_type == 'before' and len(channel.members) == 0:
                    self.inactive_session.append(
                        (channel, datetime.now())
                    )
                    print(self.inactive_session)
                elif vc_type == 'after' and len(channel.members) > 0:
                    for channel_inactive, datetime_inactive in self.inactive_session:
                        if channel == channel_inactive:
                            del self.inactive_session[self.inactive_session.index((channel_inactive, datetime_inactive))]
                    
                    print(self.inactive_session)

    @tasks.loop(seconds=15)
    async def delete_inactive_voices(self):
        index = 0
        for channel, create_time in self.inactive_session:
            if (datetime.now() - create_time).seconds >= 1800: # 30 minutes
                await channel.delete()
                del self.inactive_session[index]
                index = 0
            else:
                index += 1

async def setup(client: commands.Bot):
    await client.add_cog(VoiceGenerator(client))