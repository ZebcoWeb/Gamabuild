from asyncio import *
from discord import channel
from discord import embeds
from discord.ext import commands , tasks
from discord_components import *
import aiohttp
import asyncio
import discord
import io
import re

TOKEN = "ODQwNjQ0Njc5MzU4ODczNjQy.YJbNXQ.IOx_JzwkI510F85xDIHUpSLohvw"
PREFIX = '-'

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
            await channel.send(embed=embed)
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
click on <:omo_vmark:789798349569654805> and verify yourself !''',
        color=0xFB005B
    )
    embed.set_footer(text= 'GamaBuild Team' , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/803345280828571688/843054375278215178/Welcome.png')
    massage = await channel.send(embed=embed)
    await massage.add_reaction("<:omo_vmark:789798349569654805>")
    await ctx.reply('> **Verify has been made!**')


#ticket

@commands.has_permissions(manage_guild=True)
@client.command()
async def create(ctx):
    channel = client.get_channel(789777105201397811)
    embed = discord.Embed(
        title="Please react with <:ticket1:841743660622282762> to open a ticket.",
        description='''By clicking the <:ticket1:841743660622282762> you can create a ticket and order your custom made minecraft maps/project.
        **Make sure to click the icon if you have an order.**''',
        color=0xFB005B
    )
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/841291473332207662/841744350962909184/Ticket.png')
    embed.set_footer(text= 'GamaBuild Team' , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')

    message_create = await channel.send(embed=embed)
    await message_create.add_reaction("<:ticket1:841743660622282762>")
    await ctx.reply('> **Ticket has been made!**')


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
async def sold(ctx , id:int , img):
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

    await res.respond(type=6)
    

#reaction tracker
@client.event
async def on_raw_reaction_add(payload):
    #ticket_reaction_tracker
    if payload.message_id == 842795228527067198 and payload.user_id != 840644679358873642:
        guild = client.get_guild(payload.guild_id)
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = client.get_user(payload.user_id)
        emoji = "<:ticket1:841743660622282762>"
        # builder_role = guild.get_role(769896654832664596)
        await message.remove_reaction(emoji, user)

        ticketscat = client.get_channel(789787201981382656)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            user: discord.PermissionOverwrite(read_messages=True)
            # builder_role: discord.PermissionOverwrite(read_messages=True)
        }
        title = '╠'+user.name
        created = await ticketscat.create_text_channel(title, overwrites=overwrites)

        embed = discord.Embed(
            title="Please be patient while team members handle this ticket.",
            description="You have successfully created a ticket. Please wait for the response of team members/Or you can ask your question here and wait for team members to response.",
            color=0xFB005B
        )
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text="GamaBuild Team" , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')
        await created.send(embed=embed, content=user.mention)

    #verify_reaction_tracker
    elif payload.message_id == 843067411343343616 and payload.user_id != 840644679358873642:
        guild = client.get_guild(payload.guild_id)
        channel = client.get_channel(payload.channel_id)
        channel_join = client.get_channel(847806714840875069)
        massage = await channel.fetch_message(payload.message_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(842843180608127038)
        new_role = guild.get_role(781407403211620393)
        role_members = discord.utils.get(role.members , id=payload.user_id)
        if role_members is not None:
            emoji = '<:omo_vmark:789798349569654805>'
            await member.add_roles(new_role)
            await member.remove_roles(role)
            await massage.remove_reaction(emoji , member)
            em = discord.Embed(
            title= f'**{member.name} <:omo_vmark:789798349569654805>**' ,
            description = f'ID: ``{member.id}``' ,
            color=0xFB005B
            )
            em.set_thumbnail(url= member.avatar_url)
            await channel_join.send(embed=em)
        else:
            emoji = '<:omo_vmark:789798349569654805>'
            await massage.remove_reaction(emoji , member)
    else:
        pass


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