import discord
import os

from discord import Intents, __version__
from discord.ext import commands

from config import Config
from utils import init_database


class BotClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(
            
            help_command = None,
            command_prefix = commands.when_mentioned_or(Config.PREFIX),
            intents=Intents.all()
        )
        self.persistent_views_added = False
    
    async def setup_hook(self):

        # Initial database
        await init_database(loop=self.loop)

        self.guild = await self.fetch_guild(Config.SERVER_ID)
        self.ctx_menus = []

        # Load extentions
        print('> Loading extentions...')
        for path, subdirs, files in os.walk('cogs/'):
            for name in files:
                if name.endswith('.py'):
                    filename = os.path.join(path, name).replace('/', '.').replace('\\', '.')[:-3]
                    if filename not in Config.IGNORE_EXTENTIONS:
                        try:
                            await self.load_extension(filename)
                        except Exception as e:
                            print(f'! Failed to load extension {filename}.')
                            raise e

        await self.tree.sync(guild=self.guild)
    
    async def on_ready(self):
        print(f"""
Alright we are ready! - Gama Team
    - Applicaion id -> {self.application_id}
    - Pong -> {round(self.latency * 1000)} ms
    - Library version -> {__version__}
""")
        print('> Loaded extensions --> ' + ', '.join(self.extensions.keys()))

        if not self.persistent_views_added:
                self.persistent_views_added = True

        members_number = 0
        async for member in self.guild.fetch_members(limit=None):
            if member.bot == False:
                members_number += 1
                
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{members_number} Members'))


if __name__ == '__main__':
    BotClient().run(Config.TOKEN)