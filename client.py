import asyncio
import discord
import re
import os

from discord.enums import ButtonStyle

from discord.ext import commands


TOKEN = os.getenv.get('BOTTOKEN')
PREFIX = '-'

client = commands.Bot(
command_prefix=PREFIX,
help_command=None,
intents=discord.Intents.all()
)
client.persistent_views_added = False

@client.event
async def on_ready():
    print("Alright we are ready! - Gama Team")

    if not client.persistent_views_added:
            client.add_view(VerifyView())
            client.add_view(TicketView())
            client.add_view(FollowView())
            client.persistent_views_added = True


    guild = client.get_guild(769855661223313413)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{guild.member_count} Members'))

@client.event
async def on_member_join(member):
    guild = client.get_guild(769855661223313413)
    channel = client.get_channel(847806714840875069)
    role = guild.get_role(842843180608127038)
    user = guild.get_member(member.id)
    await user.add_roles(role)
    em = discord.Embed(
    title= f'**{member.name} <:Approved:789798412710445087>**' ,
    description = f'ID: ``{member.id}``' ,
    color=0xFB005B
    )
    em.set_thumbnail(url= member.avatar.url)
    await channel.send(embed=em)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{guild.member_count} Members'))

@client.event
async def on_member_remove(member):
    guild = client.get_guild(769855661223313413)
    channel = client.get_channel(847806714840875069)
    em = discord.Embed(
    title= f'**{member.name} <:Denied:789798455945199656>**' ,
    description = f'ID: ``{member.id}``' ,
    color=0xFB005B
    )
    em.set_thumbnail(url= member.avatar.url)
    await channel.send(embed=em)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{guild.member_count} Members'))

    # ------
    # Views
    # ------

verify_emoji = '<:verifyy:867000676452925450>'
ticket_emoji = '<:tickett:867127185134714910>'
follow_emoji = '<:notiff:867001613990363159>'
unfollow_emoji = '<:notiffoff:867082989363658773>'
download_emoji = '<:download:908033302345179136>'

class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.channel_verify = client.get_channel(842431646648369224)

    @discord.ui.button(label='Verify', custom_id='verify_button', style=ButtonStyle.green, emoji=verify_emoji)
    async def verify_user(self, button: discord.ui.Button, interaction: discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        channel = interaction.channel 
        if channel == self.channel_verify:
            role_default = guild.get_role(781407403211620393)
            role = guild.get_role(842843180608127038)
            channel_join = client.get_channel(847806714840875069)
            if role_default not in member.roles:
                await member.add_roles(role_default)
                await member.remove_roles(role)
                #log
                em = discord.Embed(
                title= f'**{member.name} <:omo_vmark:789798349569654805>**' ,
                description = f'ID: ``{member.id}``' ,
                color=0xFB005B
                )
                em.set_thumbnail(url= member.avatar.url)
                await channel_join.send(embed=em)
            else:
                pass
        await interaction.response.defer(ephemeral=True)


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.channel_ticket = client.get_channel(789777105201397811)
        self.ticketscat = client.get_channel(789787201981382656)

    @discord.ui.button(label='Create Ticket', custom_id='ticket_button', style=ButtonStyle.green, emoji=ticket_emoji)
    async def create_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        channel = interaction.channel

        if channel == self.channel_ticket and member.id != 840644679358873642:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                member: discord.PermissionOverwrite(read_messages=True)
            }
            title = '╠ '+member.name
            created = await self.ticketscat.create_text_channel(title, overwrites=overwrites)

            embed = discord.Embed(
                title="Please be patient while team members handle this ticket.",
                description="You have successfully created a ticket. Please wait for the response of team members/Or you can ask your question here and wait for team members to response.",
                color=0xFB005B
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text="GamaBuild Team" , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')
            await created.send(embed=embed, content=member.mention)
        await interaction.response.defer(ephemeral=True)


class FollowView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.channel_product = client.get_channel(866752986083491840)

    @discord.ui.button(label='Follow', custom_id='follow_button', style=ButtonStyle.green, emoji=follow_emoji)
    async def follow(self, button: discord.ui.Button, interaction: discord.Interaction):
        channel = interaction.channel
        if self.channel_product == channel:
            guild = interaction.guild
            member = interaction.user
            role_mention = guild.get_role(866976860625043456)

            if role_mention not in member.roles:
                await member.add_roles(role_mention)
                em = discord.Embed(description='<:notiff:867001613990363159> Channel notifications are enabled for you.',  color=0x17d34f)
                await member.send(embed=em)
            else:
                em = discord.Embed(description=':exclamation: You have already __Followed__ this channel.',color=0xFF0000)
                await member.send(embed=em)
        await interaction.response.defer(ephemeral=True)

    @discord.ui.button(label='Unfollow', custom_id='unfollow_button', style=ButtonStyle.red, emoji=unfollow_emoji)
    async def unfollow(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        role_mention = guild.get_role(866976860625043456)
        if role_mention in member.roles:
            await member.remove_roles(role_mention)
            em = discord.Embed(description='<:notiffoff:867082989363658773> Channel notifications are disabled for you.',color=0x17d34f)
            await member.send(embed=em)
        else:
            em = discord.Embed(description=':exclamation: You have already __Unfollowed__ this channel.',color=0xFF0000)
            await member.send(embed=em)
        await interaction.response.defer(ephemeral=True)

    # --------------------------------

#ticket

@commands.has_permissions(manage_guild=True)
@client.command(aliases=["help"])
async def _help(ctx):
    """Manage server commands help"""
    
    commands = client.commands
    help_des = []

    for c in commands:
        aliases = '|'.join(c.aliases)
        help = c.help if c.help else 'No help'
        help_des.append(f'``{PREFIX}{aliases}`` - {help}\n')
    help_des = '\n'.join(help_des)

    embed = discord.Embed(
        title = f'<:Rules4:871705388918128640> {client.user.name} manage commands help',
        description = help_des,
        color = 0xFB005B
    )
    embed.set_footer(text= 'GamaBuild Team' , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')
    
    await ctx.send(embed=embed)

@commands.has_permissions(manage_guild=True)
@client.command(aliases=["new"])
async def _new (ctx , *, args=None):
    """send embed news: `-new [Tilte]^[Description]^[Image = Optional]`"""
    if args == None:
        await ctx.reply(f'> `{PREFIX}new [Tilte]^[Description]^[Image = Optional]`')
    else:
        channel = client.get_channel(781409442545008640)
        argslist = args.split('^')
        title = argslist[0]
        description = argslist[1]
        embed = discord.Embed(title = f'{title}' , description= f'''{description}''' , color=0xFB005B)
        embed.set_footer(text= 'GamaBuild Team' , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')
        try:
            image = argslist[2]
            embed.set_image(url=f'{image}')
        except IndexError:
            pass
        finally:
            await channel.send(embed=embed,content='@everyone')
            await ctx.reply(f'> **Message sent.**')

@commands.has_permissions(manage_guild=True)
@client.command(aliases=["insta"])
async def _insta(ctx , *, args=None):
    """Send msg to insta channel: `-insta [Tilte]^[Description]^[Image = Optional]`"""
    if args == None:
        await ctx.reply(f'> `{PREFIX}insta [Tilte]^[Description]^[Image = Optional]`')
    else:
        channel = client.get_channel(841982534502187008)
        argslist = args.split('^')
        title = argslist[0]
        description = argslist[1]
        embed = discord.Embed(title = f'{title}' , description= f'''{description}''' , color=0xFB005B)
        embed.set_footer(text= 'GamaBuild Team' , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')
        try:
            image = argslist[2]
            embed.set_image(url=f'{image}')
        except IndexError:
            pass
        finally:
            await channel.send(embed=embed)
            await ctx.reply(f'> **Message sent.**')

#verify
@commands.has_permissions(manage_guild=True)
@client.command(aliases=["verify"])
async def _verify(ctx):
    """Create new `Verify` message"""
    channel = client.get_channel(842431646648369224)
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
    await channel.send(embed=embed, view=VerifyView())
    await ctx.reply('> **Verify has been made!**')


@commands.has_permissions(manage_guild=True)
@client.command(aliases=["create"])
async def _create(ctx):
    """Create new `Create ticket` message"""
    channel = client.get_channel(789777105201397811)
    embed = discord.Embed(
        title="Please react with <:ticket1:841743660622282762> to open a ticket.",
        description='''By clicking the <:tickett:867127185134714910> you can create a ticket and order your custom made minecraft maps/project.
        **Make sure to click the icon if you have an order.**''',
        color=0xFB005B
    )
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/841291473332207662/841744350962909184/Ticket.png')
    embed.set_footer(text= 'GamaBuild Team' , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')
    await channel.send(embed=embed, view=TicketView())
    await ctx.reply('> **Ticket has been made!**')

#Terms
@commands.has_permissions(manage_guild=True)
@client.command(aliases=["terms"])
async def _terms(ctx:commands.Context):
    """Create new `TERMS OF SERVICE` message"""
    term_channel = client.get_channel(769856028425977876)
    embed=discord.Embed(
        title="<a:OK:866760492545343499> **TERMS OF SERVICE**",
     description='''
<:Rules1:871703799918657558> Our work comes with quality , detail and attention to your personal liking and for that reason we do not accept any negotiation for the price !

<:Rules2:871704398810726432> The funds and chargebacks are decided by us to protect the rights of our team and our dear clients .

<:Rules3:871704922465398905> Products you receive from us do not have resell rights in any ways .

<a:MC:866762262227714069> **OUR WAYS**

<:Rules4:871705388918128640> We are flexible with our work and respect our clients opinion so...edits and small changes are always available .

<:Rules5:871710416110248006> Making new and impossible styles is a pleasant practice for us so...don't be afraid to bring your own ideas to us !

By opening a <#789777105201397811> you agree to all of these terms !
''',
      color=0xFB005B
    )
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/779789524431536129/871700348534947900/Rules.png')
    embed.set_footer(text= 'GamaBuild Team' , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')
    await term_channel.send(embed=embed)
    await ctx.reply('> **Terms has been made!**')


#send product
@commands.has_permissions(manage_guild=True)
@client.command(aliases=["exclusive"])
async def _exclusive(ctx , *,args=None):
    """Send exclusive product: `-exclusive [Image Link]^[Download link]`"""
    if args == None:
        await ctx.reply(f'> `{PREFIX}exclusive [Image Link]^[Download link]`')
    else:
        channel = client.get_channel(866752986083491840)
        role_mention = ctx.guild.get_role(866976860625043456)
        argslist = args.split('^')
        image_url = argslist[0]
        dl_url = argslist[1]
        em = discord.Embed(
            title='<a:Bell:866759095767400490> New Map For Sell!',
            color=0xFB005B,
            description=f'''<a:OK:866760492545343499> To Purchase this map open a <#789777105201397811> or contact <@548461329418289153>\n'''
            )
        view = FollowView()
        view.add_item(discord.ui.Button(
        label='Download', 
        url=dl_url,
        emoji=download_emoji
            )
        )
        em.set_image(url=image_url)
        em.set_footer(text='Press the "Follow" button if you like to get notified when we upload our exclusive maps!')
        product = await channel.send(embed=em, view=view, content=f'||{role_mention.mention}||')
        await ctx.reply(f'> **Product sent.**\nmsg ID: `{product.id}`')


#product change status
@commands.has_permissions(manage_guild=True)
@client.command(aliases=["sold"])
async def _sold(ctx , id:int = None, img = None):
    '''Change exclusive product to sold: `-sold [Massage ID]`'''
    channel = client.get_channel(866752986083491840)
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
            await msg.edit(embed=em, view=FollowView())
            await ctx.reply('> **Product status changed to sold!**')
        else:
            await ctx.reply(f'> **This product does not exist in the {channel.mention} channel!**')
    else:
        await ctx.reply('> `{PREFIX}sold [Massage ID]`')

    
    #clear msg
@commands.has_permissions(manage_guild=True)
@client.command(aliases=["clear"])
async def _clear(ctx , number:int):
    """Clear messages by value: `-clear [Number]`"""
    await ctx.channel.purge(limit=number+1)
    await ctx.reply(f'`{number}` message deleted!')

@commands.has_permissions(manage_guild=True)
@client.command(aliases=["close"])
async def _close(ctx):
    """Close a active ticket `Send in the active channel`"""
    channel = ctx.channel
    if channel.category_id == 789787201981382656:
        embed = discord.Embed(
            title="Thanks for giving your time!",
            description="We are closing this ticket automatically in 10 seconds...",
            color=0xFB005B
        )
        embed.set_footer(text="GamaBuild Team" , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("\U0001f1f9")
        await asyncio.sleep(1)
        await msg.add_reaction("\U0001f1ed")
        await asyncio.sleep(1)
        await msg.add_reaction("\U0001f1fd")
        await asyncio.sleep(10)
        await channel.delete()



client.run(TOKEN)