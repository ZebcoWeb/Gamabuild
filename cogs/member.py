import discord

from discord.ext import commands
from beanie.odm.operators.update.general import Set

from config import Config, Roles, Channel, Emoji
from models import MemberModel


class VerifyView(discord.ui.View):
    def __init__(self, client):
        super().__init__(timeout=None)
        self.client = client

    @discord.ui.button(label='Verify', custom_id='verify_button', style=discord.ButtonStyle.green, emoji=discord.PartialEmoji.from_str(Emoji.VERIFY))
    async def verify_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        guild = interaction.guild
        role_default = guild.get_role(Roles.TRAVELER)
        role_new = guild.get_role(Roles.NEW)
        channel_join = self.client.get_channel(847806714840875069)
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

        self.client.add_view(VerifyView(self.client))
        self.client.loop.create_task(self.leftover_members())

    async def leftover_members(self):
        guild = await self.client.fetch_guild(Config.SERVER_ID)
        registered_members = await MemberModel.members_id_list()

        members_number = 0
        async for member in guild.fetch_members(limit=None):
            if member.id not in registered_members:
                check_role = member.get_role(Roles.TRAVELER)
                if check_role:
                    await MemberModel.join_member(member, verified=True)
                else:
                    await MemberModel.join_member(member)
                members_number += 1
        
        print(f'> {members_number} members added to database.')

    # Commands
    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def verify(self, ctx):
        """Create new `Verify` message"""


        channel = await self.client.fetch_channel(Channel.PREMADE_MAPS)
        async for message in channel.history(limit=None):
            await message.delete()
        embed = discord.Embed(
            title='Hey There Traveler !',
            description='''**:ringed_planet: You are very welcomed in our planet (Gama)**

    Make yourself home , there are many places you can check here and explore such as :
    :bell: - Announcements : you can read the overall things that happen in this planet or get Friends with Ruler and place your add here !
    :page_facing_up: -Rules : The Rules you have to follow when wondering around here !
    :tv: -instagram : check our posts on instagram too , you might like what you see there !
    :camera: -Previous projects : The Recent Wonders We Created on this amazing planet !
    :interrobang: -FAQ : If you're still confused by the glory of this planet feel free to read this section 

    Now , there are many robots among the travelers and they are not accepted in this community ! you're not a robot are you traveler ?
    click on <:verifyy:867000676452925450> and verify yourself !''',
            color=0xFB005B
        )
        embed.set_footer(text= 'GamaBuild Team' , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/779789524431536129/907567032453718026/Welcome.png')
        await channel.send(embed=embed, view=VerifyView(self.client))
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
        em.set_thumbnail(url= member.avatar.url)
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
        em.set_thumbnail(url= member.avatar.url)
        await channel.send(embed=em)
        
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{self.client.guild.member_count} Members'))

async def setup(client: commands.Bot):
    await client.add_cog(Member(client))