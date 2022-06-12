import discord

from discord.ext import commands

from config import Channel, Config, Roles



class SetRoleView(discord.ui.View):
    def __init__(self, guild):
        super().__init__(timeout=None)
        self.guild = guild

        self.menu = discord.ui.Select(
            custom_id='role_menu',
            placeholder='Choose a custom role'
        )
        self.menu.callback = self.callback
        
        for role_id, role_icon in Roles.OPTIONAL_ROLES:
            button = discord.ui.Button(
                style=discord.ButtonStyle.gray,
                emoji=role_icon,
                custom_id=str(role_id),
            )
            button.callback = self.callback
            self.add_item(button)

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        role_value = int(interaction.data['custom_id'])
        role = guild.get_role(role_value)
        role_marker = guild.get_role(Roles.ROLES_MARKER)

        check_role = member.get_role(role_value)
        if not check_role:
            check_roles = discord.utils.find(lambda r: r.id == Roles.ROLES_MARKER, member.roles)
            if not check_roles:
                await member.add_roles(role_marker)
            await member.add_roles(role)
            em = discord.Embed(description=f'You got the {role.mention}', color=discord.Colour.green())
            await interaction.response.send_message(embed=em, ephemeral=True)
        else:
            member_roles = [i.id for i in member.roles]
            await member.remove_roles(role)
            number = 1
            for role in Roles.OPTIONAL_ROLES:
                if role[0] in member_roles:
                    pass
                else:
                    number += 1
            if number == len(Roles.OPTIONAL_ROLES):
                await member.remove_roles(role_marker)
            em = discord.Embed(description=f'The <@&{role_value}> role has been removed from you', color=discord.Colour.red())
            await interaction.response.send_message(embed=em, ephemeral=True)

class Role(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.client.add_view(SetRoleView(self.client.guild))

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def role(self, ctx):
        """Create new `Set Role` message"""

        channel = await self.client.fetch_channel(Channel.ROLES)

        async for message in channel.history(limit=None):
            await message.delete()



        embed = discord.Embed(
            title="➔ Set Role",
            description="Select your preferred role for more server access:",
            color=0xFB005B
        )

        str = ''
        index = 0
        for role_id, role_icon in Roles.OPTIONAL_ROLES:
            role_obj = self.client.guild.get_role(role_id)
            str += f'`{role_icon}` **- {role_obj.name}**\n'
            index += 1
            if index == 5:
                embed.add_field(name='\u200b', value=str)
                index = 0
                str = ''

        embed.set_footer(text= 'GamaBuild Team' , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')
        await channel.send(embed=embed, view=SetRoleView(self.client.guild))
        await ctx.reply('> **Set role message sended!**')


async def setup(client: commands.Bot):
    await client.add_cog(Role(client))