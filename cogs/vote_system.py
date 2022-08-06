import discord
import copy

from discord.ext import commands
from discord import app_commands, Interaction

from models import VoteModel
from config import Config, Channel, Emoji
from utils import success_embed


class UpVoteView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='ㅤ0ㅤ', style=discord.ButtonStyle.red, emoji=discord.PartialEmoji.from_str(Emoji.VOTE), custom_id='vote_to_build')
    async def callback(self, interaction: Interaction, button: discord.ui.Button):
        self.vote_button = button
        try:
            vote = await VoteModel.find_one(VoteModel.message_id == interaction.message.id, fetch_links=True)

            if interaction.user.id in vote.voters:
                await self.downvote_handler(interaction)
                vote.voters.remove(interaction.user.id)
                await vote.save()
            else:
                await self.upvote_handler(interaction)
                vote.voters.append(interaction.user.id)
                await vote.save()
        except Exception as e:
            print(e)
        
    def calculate_voters(self):
        if self.vote_button.label is None:
            return 0
        else:
            return int(self.vote_button.label[1])
    
    async def upvote_handler(self, interaction: Interaction):
        self.vote_button.label = 'ㅤ' + str(self.calculate_voters() + 1) + 'ㅤ'
        await interaction.response.edit_message(view=self)

    async def downvote_handler(self, interaction: Interaction):
        self.vote_button.label = 'ㅤ' + str(self.calculate_voters() - 1) + 'ㅤ'
        if self.vote_button.label == 'ㅤ0ㅤ':
            self.vote_button.label =  None
        await interaction.response.edit_message(view=self)


class Vote(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

        self.client.add_view(UpVoteView())

    @app_commands.command(name='vote', description='❎ Send vote challenge post (admin only)')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guilds(Config.SERVER_ID)
    @app_commands.describe(picture = 'Picture of building', builder = 'Builder User')
    async def _vote(self, interaction: discord.Interaction, picture: discord.Attachment, builder: str):
        vote_channel = await interaction.client.fetch_channel(Channel.VOTE)
        vote_model = VoteModel(
            builder=builder,
            picture_url=picture.url
        )
        em = discord.Embed(
            title=f'**{builder}**',
            color=discord.Colour.random(),
        )
        em.set_image(url=picture.url)
        em.set_footer(text='Choose the build you think is best and vote for your favorite content creator by clicking on the [❤️] button!', icon_url='https://cdn.discordapp.com/attachments/980177765452099654/995383740144549919/twotone_info_white_24dp.png')
        vote_message = await vote_channel.send(embed=em, view=UpVoteView())

        vote_model.message_id = vote_message.id
        await vote_model.save()
        await interaction.response.send_message(embed=success_embed(f'`{builder}`\'s vote posted successfully'), ephemeral=True)
        

async def setup(client: commands.Bot):
    await client.add_cog(Vote(client))