import discord

from discord.ext import commands
from beanie.odm.operators.update.general import Set

from config import Config, Roles, Channel, Emoji
from models import MemberModel


class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Verify', custom_id='verify_button', style=discord.ButtonStyle.green, emoji=discord.PartialEmoji.from_str(Emoji.VERIFY))
    async def verify_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        guild = interaction.guild
        role_default = guild.get_role(Roles.TRAVELER)
        role_new = guild.get_role(Roles.NEW)
        channel_join = await interaction.client.fetch_channel(Channel.VERIFY)
        if role_default not in member.roles:
            await MemberModel.find_one(MemberModel.member_id == member.id).update(Set({MemberModel.is_verified: True}))
            await member.remove_roles(role_new)
            await member.add_roles(role_default)
            
            em = discord.Embed(
            title= f'**{member.name} <:omo_vmark:789798349569654805>**' ,
            description = f'ID: ``{member.id}``' ,
            color=0xFB005B
            )
            em.set_thumbnail(url= member.avatar.url)
            await channel_join.send(embed=em)
        await interaction.response.defer(ephemeral=True)


class Member(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: discord.client = client

        self.client.loop.create_task(self.leftover_members())

    async def leftover_members(self):
        guild = await self.client.fetch_guild(Config.SERVER_ID)
        registered_members = await MemberModel.members_id_list()

        members_number = 0
        async for member in guild.fetch_members(limit=None):
            if member.id not in registered_members and member.bot == False:
                check_role = member.get_role(Roles.TRAVELER)
                if check_role:
                    await MemberModel.join_member(member, verified=True)
                else:
                    await MemberModel.join_member(member)
                members_number += 1
        
        print(f'> {members_number} members added to database.')

    # Commands
    @commands.has_permissions(manage_guild=True)
    @commands.command(aliases=["verify"])
    async def _verify(self, ctx:commands.Context):
        """Create new `Verify` message"""

        channel = await self.client.fetch_channel(Channel.VERIFY)
        async for message in channel.history(limit=None):
            await message.delete()
        embed = discord.Embed(
            title='Welcome Traveler!',
            description='''**We're delighted to have you checking** 
<:Share:994295237205827636> ● GamaBuild's most recent social media posts and activities.
<:LevelUP:994295516206735440> ● Our fun Leveling system in which you can gain experience by chatting , inviting your friends, boosting the server and...
<:Games:994293396128673852> ● The fun minigames you can play and earn Gama Coin by doing so.
<:Market:994293107120160788> ● You can **download free Minecraft builds** in the marketplace !
<:Services:994294419115233322> ● The services section ! to strike a sponsor deal, place a commission or to simply get in contact with us.
<:Entertainment:994294738566008872> ● Other entertaining features such as memes, self promo, music and custom private voice channels !''',
            color=0xFB005B
        )
        embed.set_footer(text= 'By Clicking The Verify Button You Can Start Your Journey In This Server' , icon_url='https://cdn.discordapp.com/attachments/980177765452099654/994505425397485598/6979530.png')
        embed.set_image(url='https://cdn.discordapp.com/attachments/980177765452099654/994284759037513858/VerifyDiscord.png')
        await channel.send(embed=embed, view=VerifyView())
        await ctx.reply('> **Verify has been made!**')


    # Events

    async def add_unrole_members(self):
        guild = await self.client.fetch_guild(Config.SERVER_ID)
        async for user in guild.fetch_members(limit=None):
            await user.add_roles(Roles.NEW)
        
    @commands.Cog.listener('on_member_join')
    async def member_join_handler(self, member):
        await MemberModel.join_member(member)

        channel = await self.client.guild.fetch_channel(Channel.JOIN_LOG)
        role = self.client.guild.get_role(Roles.NEW)
        user = await self.client.guild.fetch_member(member.id)
        await user.add_roles(role)

        em = discord.Embed(
        title= f'**{member.name} <:Approved:789798412710445087>**' ,
        description = f'ID: ``{member.id}``' ,
        color=0xFB005B
        )
        em.set_thumbnail(url=member.avatar.url)
        await channel.send(embed=em)

        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{self.client.guild.member_count} Members'))
    

    @commands.Cog.listener('on_member_remove')
    async def on_member_remove(self, member):
        await MemberModel.leave_member(member)

        channel = await self.client.fetch_channel(Channel.JOIN_LOG)
        em = discord.Embed(
        title= f'**{member.name} <:Denied:789798455945199656>**' ,
        description = f'ID: ``{member.id}``' ,
        color=0xFB005B
        )
        # em.set_thumbnail(url= member.avatar.url)
        await channel.send(embed=em)
        
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{self.client.guild.member_count} Members'))

async def setup(client: commands.Bot):
    await client.add_cog(Member(client))
