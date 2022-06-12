import discord
import re

from discord.ext import commands
from discord import ButtonStyle

from config import Config, Roles, Channel, Emoji

class FollowView(discord.ui.View):
    def __init__(self, client):
        super().__init__(timeout=None)
        self.client = client

    @discord.ui.button(label='Follow', custom_id='follow_button', style=ButtonStyle.green, emoji=discord.PartialEmoji.from_str(Emoji.FOLLOW))
    async def follow(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.channel
        channel_product = await self.client.fetch_channel(Channel.PREMADE_MAPS)
        if channel_product == channel:
            guild = interaction.guild
            member = interaction.user
            role_mention = guild.get_role(Roles.NOTICE)

            if role_mention not in member.roles:
                await member.add_roles(role_mention)
                em = discord.Embed(description='<:notiff:867001613990363159> Channel notifications are enabled for you.',  color=0x17d34f)
                try:
                    await member.send(embed=em)
                except:
                    await interaction.response.send_message(embed=em, ephemeral=True, delete_after=30.0)
            else:
                em = discord.Embed(description=':exclamation: You have already __Followed__ this channel.',color=0xFF0000)
                try:
                    await member.send(embed=em)
                except:
                    await interaction.response.send_message(embed=em, ephemeral=True, delete_after=30.0)
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True)

    @discord.ui.button(label='Unfollow', custom_id='unfollow_button', style=ButtonStyle.red, emoji=discord.PartialEmoji.from_str(Emoji.UNFOLLOW))
    async def unfollow(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        member = interaction.user
        role_mention = guild.get_role(Roles.NOTICE)
        if role_mention in member.roles:
            await member.remove_roles(role_mention)
            em = discord.Embed(description='<:notiffoff:867082989363658773> Channel notifications are disabled for you.',color=0x17d34f)
            try:
                await member.send(embed=em)
            except:
                    await interaction.response.send_message(embed=em, ephemeral=True, delete_after=30.0)
        else:
            em = discord.Embed(description=':exclamation: You have already __Unfollowed__ this channel.',color=0xFF0000)
            try:
                await member.send(embed=em)
            except:
                    await interaction.response.send_message(embed=em, ephemeral=True, delete_after=30.0)
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True)


class PremadeMap(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client

        self.client.add_view(FollowView(self.client))

    # Commands
    @commands.has_permissions(manage_guild=True)
    @commands.command(aliases=["exclusive"])
    async def _exclusive(self, ctx , *, args=None):
        """Send exclusive product: `-exclusive [Image Link]^[Download link]^[Description]`"""
        if args == None:
            await ctx.reply(f'> `{Config.PREFIX}exclusive [Image Link]^[Download link]`')
        else:
            channel = await self.client.fetch_channel(Channel.PREMADE_MAPS)
            role_mention = ctx.guild.get_role(Roles.NOTICE)
            argslist = args.split(' ^ ')
            image_url = argslist[0]
            dl_url = argslist[1]
            des = argslist[2]
            em = discord.Embed(
                title='<a:Bell:866759095767400490> New Map',
                color=0xFB005B,
                description='<a:OK:866760492545343499> ' + des
                )
            view = FollowView(self.client)
            view.add_item(discord.ui.Button(
            label='Download', 
            url=dl_url,
            emoji=Emoji.DOWNLOAD,
                )
            )
            em.set_image(url=image_url)
            em.set_footer(text='Press the "Follow" button if you like to get notified when we upload our exclusive maps!')
            product = await channel.send(embed=em, view=view, content=f'||{role_mention.mention}||')
            await ctx.reply(f'> **Product sent.**\nmsg ID: `{product.id}`')


    @commands.has_permissions(manage_guild=True)
    @commands.command(aliases=["sold"])
    async def _sold(self, ctx , id:int = None, img = None):
        '''Change exclusive product to sold: `-sold [Massage ID]`'''
        channel = self.client.get_channel(Channel.PREMADE_MAPS)
        msg = await channel.fetch_message(id)
        if id or img != None:
            if msg.channel == channel:
                detail = msg.embeds[0].description
                url = re.search('\(.*\)', detail)
                url = url.group()
                em = discord.Embed(
                    title='<:Sold:866977659334557716> This map has been sold!',
                    description=f'>>> Full Detail of the map [Click here]{url}',
                    color=0xFB005B,
                    )
                em.set_image(url=img)
                em.set_footer(text='Press the "Follow" button if you like to get notified when we upload our exclusive maps!')
                await msg.edit(embed=em, view=FollowView(self.client))
                await ctx.reply('> **Product status changed to sold!**')
            else:
                await ctx.reply(f'> **This product does not exist in the {channel.mention} channel!**')
        else:
            await ctx.reply('> `{PREFIX}sold [Massage ID]`')

async def setup(client: commands.Bot):
    await client.add_cog(PremadeMap(client))