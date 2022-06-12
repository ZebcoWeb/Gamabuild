import discord
import asyncio

from discord.ext import commands

from config import Channel, Config

class TicketMenu(discord.ui.Select):
    def __init__(self, client):
        super().__init__(
            custom_id='ticket_menu',
            placeholder='Select one of the sections...', 
            options=self.ticket_options(),
        )
        self.client = client

    def ticket_options(self):
        options = []
        for section, emoji in Config.TICKET_SECTIONS:
            options.append(discord.SelectOption(
                    label=section, 
                    value=emoji + ' ' + section,
                    emoji=emoji
                )
            )
        return options
        
    async def callback(self, interaction: discord.Interaction):
        if len(self.values) > 0:
            member = interaction.user
            guild = interaction.guild
            category = await self.client.fetch_channel(Channel.TICKET_CATEGORY)
            section_value = self.values[0]

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                member: discord.PermissionOverwrite(read_messages=True)
            }
            title = '╠ '+ member.name
            ticket_channel = await category.create_text_channel(title, overwrites=overwrites)

            embed = discord.Embed(
                title="Please be patient while team members handle this ticket.",
                description="You have successfully created a ticket. Please wait for the response of team members/Or you can ask your question here and wait for team members to response. \n\n **- Section:** " + section_value,
                color=0xFB005B
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text="GamaBuild Team" , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')
            await ticket_channel.send(embed=embed, content=member.mention)
            await interaction.response.edit_message(view=TicketView(self.client))
        else:
            await interaction.response.defer()
    


class TicketView(discord.ui.View):
    def __init__(self, client):
        super().__init__(timeout=None)
        self.client = client
        self.add_item(TicketMenu(self.client))


class Ticket(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

        self.client.add_view(TicketView(self.client))
    
    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def ticket(self, ctx):
        """Create new `Create ticket` message"""

        channel = await self.client.fetch_channel(Channel.TICKET)

        async for message in channel.history(limit=None):
            await message.delete()

        embed = discord.Embed(
            title="title",
            description='''Ticket description context''',
            color=0xFB005B
        )
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/841291473332207662/841744350962909184/Ticket.png')
        embed.set_footer(text= 'GamaBuild Team' , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')
        await channel.send(embed=embed, view=TicketView(self.client))
        await ctx.reply('> **Ticket has been made!**')
    
    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def close(self, ctx, mode: str = None):
        """Close a active ticket `Send in the active channel`"""

        channel = ctx.channel
        if channel.category_id == Channel.TICKET_CATEGORY:
            embed = discord.Embed(
                title="Thanks for giving your time!",
                color=0xFB005B
            )
            if mode == 'fast':
                embed.description = "We are closing this ticket automatically in 10 seconds..."
                CLOSE_DELAY = 10
            elif not mode:
                embed.description = "We are closing this ticket automatically in 24 hours..."
                CLOSE_DELAY = 86400

            embed.set_footer(text="GamaBuild Team" , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("\U0001f1f9")
            await asyncio.sleep(1)
            await msg.add_reaction("\U0001f1ed")
            await asyncio.sleep(1)
            await msg.add_reaction("\U0001f1fd")
            await asyncio.sleep(CLOSE_DELAY)
            await channel.delete()


async def setup(client: commands.Bot):
    await client.add_cog(Ticket(client))