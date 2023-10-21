import discord

from discord.ext import commands
from discord import app_commands, Interaction

from models import VoteModel
from config import Config, Channel, Emoji
from utils import success_embed, error_embed

class VoteView(discord.ui.View):
    def __init__(self, instagram_url: str, initial_vote_number: int = None):
        self.instagram_url = instagram_url
        super().__init__(timeout=None)

        self.vote_button = discord.ui.Button(label=f'ㅤ{initial_vote_number}ㅤ' if initial_vote_number else None, style=discord.ButtonStyle.red, emoji=discord.PartialEmoji.from_str(Emoji.VOTE))
        self.vote_button.callback = self.vote_callback

        self.add_item(self.vote_button)
        self.add_item(
            discord.ui.Button(label='Instagram', url=self.instagram_url, emoji='📺')
        )

    async def vote_callback(self, interaction: Interaction):
        vote = await VoteModel.find_one(VoteModel.message_id == interaction.message.id, fetch_links=True)

        if interaction.user.id in vote.voters:
            vote.voters.remove(interaction.user.id)
            await self.downvote_handler(interaction, len(vote.voters))
            await vote.save()
        else:
            vote.voters.append(interaction.user.id)
            await self.upvote_handler(interaction, len(vote.voters))
            await vote.save()
    
    async def upvote_handler(self, interaction: Interaction, vote_number: int):
        self.vote_button.label = 'ㅤ' + str(vote_number) + 'ㅤ'
        await interaction.response.edit_message(view=self)

    async def downvote_handler(self, interaction: Interaction, vote_number: int):
        if vote_number == 0:
            self.vote_button.label = None
        else:
            self.vote_button.label = 'ㅤ' + str(vote_number) + 'ㅤ'
        await interaction.response.edit_message(view=self)


class Vote(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='vote', description='❎ Send vote challenge post (admin only)')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guilds(Config.SERVER_ID)
    @app_commands.describe(picture = 'Picture of building', builder = 'Builder User', instagram_profile = 'Participant\'s Instagram profile', caption = 'Caption of vote')
    async def _vote(self, interaction: discord.Interaction, picture: discord.Attachment, builder: str, instagram_profile: str, caption: str):
        vote_channel = await interaction.client.fetch_channel(Channel.VOTE)
        vote_model = VoteModel(
            builder=builder,
            caption=caption,
            picture_url=picture.url,
            instagram_profile_url=instagram_profile,
        )
        em = discord.Embed(
            description=f'👤 {builder}\n\n<:Terms:994313748556808253> {caption}',
            color=discord.Colour.random(),
        )
        em.set_image(url=picture.url)
        vote_message = await vote_channel.send(embed=em, view=VoteView(instagram_url=instagram_profile))

        vote_model.message_id = vote_message.id
        await vote_model.save()
        await interaction.response.send_message(embed=success_embed(f'`{builder}`\'s vote posted successfully'), ephemeral=True)
    
    @app_commands.command(name='vote_resend', description='❎ Resend vote challenge post (admin only)')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guilds(Config.SERVER_ID)
    @app_commands.describe(message_id = 'Message id of old post')
    async def _vote_resend(self, interaction: discord.Interaction, message_id: str):
        old_vote = await VoteModel.find_one(VoteModel.message_id == int(message_id), fetch_links=True)
        if not old_vote:
            await interaction.response.send_message(embed=error_embed('Vote not found'), ephemeral=True)
            return
        vote_channel = await interaction.client.fetch_channel(Channel.VOTE)
        vote_model = VoteModel(
            builder=old_vote.builder,
            caption=old_vote.caption,
            picture_url=old_vote.picture_url,
            instagram_profile_url=old_vote.instagram_profile_url,
            voters=old_vote.voters,
        )
        em = discord.Embed(
            description=f'👤 {old_vote.builder}\n\n<:Terms:994313748556808253> {old_vote.caption}',
            color=discord.Colour.random(),
        )
        em.set_image(url=old_vote.picture_url)
        vote_message = await vote_channel.send(embed=em, view=VoteView(instagram_url=old_vote.instagram_profile_url, initial_vote_number=len(old_vote.voters)))

        vote_model.message_id = vote_message.id

        try:
            old_vote_message = await vote_channel.fetch_message(old_vote.message_id)
            await old_vote_message.delete()
        except Exception as e:
            pass

        await old_vote.delete()
        await vote_model.save()
        await interaction.response.send_message(embed=success_embed(f'`{old_vote.builder}`\'s vote resent'), ephemeral=True)
        

async def setup(client: commands.Bot):
    await client.add_cog(Vote(client))