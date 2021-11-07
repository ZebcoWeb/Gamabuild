import asyncio
import discord
import re

from discord.ext import commands
from discord_components import *

TOKEN = "ODQwNjQ0Njc5MzU4ODczNjQy.YJbNXQ.IOx_JzwkI510F85xDIHUpSLohvw"
PREFIX = '='

intents = discord.Intents.all()
intents.members = True
intents.reactions = True
client = commands.Bot(command_prefix=PREFIX, intents=intents)
client.remove_command('help')


@client.event
async def on_ready():
    print("Alright we are ready! - Gama Team")
    DiscordComponents(client)
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
    em.set_thumbnail(url= member.avatar_url)
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
    em.set_thumbnail(url= member.avatar_url)
    await channel.send(embed=em)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{guild.member_count} Members'))

@commands.has_permissions(manage_guild=True)
@client.command()
async def new (ctx , *, args=None):
    global PREFIX
    if args == None:
        await ctx.reply(f'> `{PREFIX}new [Tilte] ^ [Description] ^ [Image = Optional]`')
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
@client.command()
async def insta (ctx , *, args=None):
    global PREFIX
    if args == None:
        await ctx.reply(f'> `{PREFIX}insta [Tilte] ^ [Description] ^ [Image = Optional]`')
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
@client.command()
async def verify(ctx):
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
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/779789524431536129/871700348534947900/Rules.png')
    comp = [
                [
            Button(style=ButtonStyle.green,emoji=client.get_emoji(867000676452925450),label='Verify',id='verify_button'),
                ]
           ]
    massage = await channel.send(embed=embed,components=comp)
    await ctx.reply('> **Verify has been made!**')


#ticket

@commands.has_permissions(manage_guild=True)
@client.command()
async def create(ctx):
    channel = client.get_channel(789777105201397811)
    embed = discord.Embed(
        title="Please react with <:ticket1:841743660622282762> to open a ticket.",
        description='''By clicking the <:tickett:867127185134714910> you can create a ticket and order your custom made minecraft maps/project.
        **Make sure to click the icon if you have an order.**''',
        color=0xFB005B
    )
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/841291473332207662/841744350962909184/Ticket.png')
    embed.set_footer(text= 'GamaBuild Team' , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')
    comp = [
                [
            Button(style=ButtonStyle.green,emoji=client.get_emoji(867127185134714910),label='Create Ticket',id='ticket_button'),
                ]
           ]
    message_create = await channel.send(embed=embed,components=comp)
    await ctx.reply('> **Ticket has been made!**')

#Terms
@commands.has_permissions(manage_guild=True)
@client.command(aliases=["terms",'Terms'])
async def _terms(ctx:commands.Context):
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
@client.command()
async def exclusive(ctx , *,args=None):
    if args == None:
        await ctx.reply(f'> `{PREFIX}exclusive [Image Link] ^ [Post Link]`')
    else:
        channel = client.get_channel(866752986083491840)
        role_mention = ctx.guild.get_role(866976860625043456)
        argslist = args.split('^')
        image_url = argslist[0]
        post_url = argslist[1]
        em = discord.Embed(
            title='<a:Bell:866759095767400490> New Map For Sell!',
            color=0xFB005B,
            description=f'''<a:OK:866760492545343499> To Purchase this map open a <#789777105201397811> or contact <@548461329418289153>\n\n >>> Full Detail of the map [Click here]({post_url})'''
            )
        em.set_image(url=image_url)
        em.set_footer(text='Press the "Follow" button if you like to get notified when we upload our exclusive maps!')
        comp = [
            [
            Button(style=ButtonStyle.green,emoji=client.get_emoji(867001613990363159),label='Follow',id='follow_button'),
            Button(style=ButtonStyle.red,emoji=client.get_emoji(867082989363658773),label='Unfollow',id='unfollow_button'),
            ]
        ]
        product = await channel.send(embed=em,components=comp,content=f'||{role_mention.mention}||')
        await ctx.reply(f'> **Product sent.**\nmsg ID: `{product.id}`')


#product change status
@commands.has_permissions(manage_guild=True)
@client.command()
async def sold(ctx , id:int = None, img = None):
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
            comp = [
                [
            Button(style=ButtonStyle.green,emoji=client.get_emoji(867001613990363159),label='Follow',id='follow_button'),
            Button(style=ButtonStyle.red,emoji=client.get_emoji(867082989363658773),label='Unfollow',id='unfollow_button'),
                ]
                   ]
            await msg.edit(embed=em,components=comp)
            await ctx.reply('> **Product status changed to sold!**')
        else:
            await ctx.reply(f'> **This product does not exist in the {channel.mention} channel!**')
    else:
        await ctx.reply('> `{PREFIX}sold [Massage ID]`')

    
    #clear msg
@commands.has_permissions(manage_guild=True)
@client.command()
async def clear(ctx , number:int):
    await ctx.channel.purge(limit=number+1)
    await ctx.reply(f'`{number}` message deleted!')

#follow button
@client.event
async def on_button_click(res):
    guild = res.guild
    channel_product = client.get_channel(866752986083491840)
    channel_verify = client.get_channel(842431646648369224)
    channel_ticket = client.get_channel(789777105201397811)
    payload_button = res.component
    channel = res.message.channel
    member = guild.get_member(res.user.id)
    role_mention = guild.get_role(866976860625043456)

    #follow
    if payload_button.id == 'follow_button' and channel == channel_product:
        if role_mention not in member.roles:
            await member.add_roles(role_mention)
            em = discord.Embed(description='<:notiff:867001613990363159> Channel notifications are enabled for you.',color=0x17d34f)
            await member.send(embed=em)
        else:
            em = discord.Embed(description=':exclamation: You have already __Followed__ this channel.',color=0xFF0000)
            await member.send(embed=em)

    #unfollow        
    if payload_button.id == 'unfollow_button' and channel == channel_product:
        if role_mention in member.roles:
            await member.remove_roles(role_mention)
            em = discord.Embed(description='<:notiffoff:867082989363658773> Channel notifications are disabled for you.',color=0x17d34f)
            await member.send(embed=em)
        else:
            em = discord.Embed(description=':exclamation: You have already __Unfollowed__ this channel.',color=0xFF0000)
            await member.send(embed=em)

    #verify
    if payload_button.id == 'verify_button' and channel == channel_verify:
        role_default = guild.get_role(781407403211620393)
        role = guild.get_role(842843180608127038)
        channel_join = client.get_channel(847806714840875069)
        if role_default not in member.roles:
            emoji = '<:omo_vmark:789798349569654805>'
            await member.add_roles(role_default)
            await member.remove_roles(role)
            #log
            em = discord.Embed(
            title= f'**{member.name} <:omo_vmark:789798349569654805>**' ,
            description = f'ID: ``{member.id}``' ,
            color=0xFB005B
            )
            em.set_thumbnail(url= member.avatar_url)
            await channel_join.send(embed=em)
        else:
            pass

    #ticket
    if payload_button.id == 'ticket_button' and channel == channel_ticket and member.id != 840644679358873642:
        ticketscat = client.get_channel(789787201981382656)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            member: discord.PermissionOverwrite(read_messages=True)
            # builder_role: discord.PermissionOverwrite(read_messages=True)
        }
        title = '╠'+member.name
        created = await ticketscat.create_text_channel(title, overwrites=overwrites)

        embed = discord.Embed(
            title="Please be patient while team members handle this ticket.",
            description="You have successfully created a ticket. Please wait for the response of team members/Or you can ask your question here and wait for team members to response.",
            color=0xFB005B
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text="GamaBuild Team" , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')
        await created.send(embed=embed, content=member.mention)

    await res.respond(type=6)


@commands.has_permissions(manage_guild=True)
@client.command()
async def close(ctx):
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