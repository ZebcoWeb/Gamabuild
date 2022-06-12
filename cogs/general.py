import discord
import re

from discord.ext import commands

from config import Channel, Config

class General(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

 
    @commands.has_permissions(manage_guild=True)
    @commands.command(aliases=["terms"])
    async def _terms(self, ctx:commands.Context):
        """Create new `TERMS OF SERVICE` message"""

        term_channel = await self.client.fetch_channel(Channel.TERM)
        embed=discord.Embed(
            title="<a:OK:866760492545343499> **TERMS OF SERVICE**",
            description='''
    <:Rules1:871703799918657558> Our work comes with quality , detail and attention to your personal liking and for that reason we do not accept any negotiation for the price !

    <:Rules2:871704398810726432> The funds and chargebacks are decided by us to protect the rights of our team and our dear clients .

    <:FF:912767067491557376> The PayPal payments will be done with F&F method **Families & Friends** for smaller projects **under 4JUdGzvrMFDWrUUwY3toJATSeNwjn54LkCnKBPRzDuhzi5vSepHfUckJNxRL2gjkNrSqtCoRUrEDAgRwsQvVCjZbRyFTLRNyDmT1a1boZVcontracts will be set and signed to protect the rights of the team and our dear clients .

    <:Rules3:871704922465398905> Products you receive from us do not have resell rights in any ways .

    <a:MC:866762262227714069> **OUR WAYS**

    <:Rules4:871705388918128640> We are flexible with our work and respect our clients opinion so...edits and small changes are always available .

    <:Rules5:871710416110248006> Making new and impossible styles is a pleasant practice for us so...don't be afraid to bring your own ideas to us !

    <:Media:912767137322504243> We will have the accessibility of making media content from the ordered projects .

    By opening a <#789777105201397811> you agree to all of these terms !
    ''',
            color=0xFB005B
        )
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/779789524431536129/871700348534947900/Rules.png')
        embed.set_footer(text= 'GamaBuild Team' , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')
        await term_channel.send(embed=embed)
        await ctx.reply('> **Terms has been made!**')
    
    @commands.has_permissions(manage_guild=True)
    @commands.command(aliases=["clear"])
    async def _clear(self, ctx , number:int):
        """Clear messages by value: `-clear [Number]`"""

        await ctx.channel.purge(limit=number + 1)
        await ctx.reply(f'`{number}` message deleted!')
    


    @commands.has_permissions(manage_guild=True)
    @commands.command(aliases=["help"])
    async def _help(self, ctx):
        """Manage server commands help"""
        
        commands = self.client.commands
        help_des = []

        for c in commands:
            aliases = '|'.join(c.aliases)
            help = c.help if c.help else 'No help'
            help_des.append(f'``{Config.PREFIX}{aliases}`` - {help}\n')
        help_des = '\n'.join(help_des)

        embed = discord.Embed(
            title = f'<:Rules4:871705388918128640> {self.client.user.name} manage commands help',
            description = help_des,
            color = 0xFB005B
        )
        embed.set_footer(text= 'GamaBuild Team' , icon_url='https://cdn.discordapp.com/attachments/841291473332207662/841736355847077888/Gama.png')
        
        await ctx.send(embed=embed)


    @commands.has_permissions(manage_guild=True)
    @commands.command(aliases=["insta"])
    async def _insta(self, ctx , *, args=None):
        """Send msg to insta channel: `-insta [Tilte]^[Description]^[Image = Optional]`"""

        if args == None:
            await ctx.reply(f'> `{Config.PREFIX}insta [Tilte]^[Description]^[Image = Optional]`')
        else:
            channel = self.client.get_channel(Channel.INSTA)
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
    @commands.command()
    async def new (self, ctx , *, args=None):
        """send embed news: `-new [Tilte]^[Description]^[Image = Optional]`"""

        if args == None:
            await ctx.reply(f'> `{Config.PREFIX}new [Tilte]^[Description]^[Image = Optional]`')
        else:
            channel = await self.client.fetch_channel(Channel.ANNOUNCEMENT)
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
    

    # Events 
    
    def check_media(self, message):
        if message.content:
            if not re.match(r'(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png|mp4|jpeg|webm|mov|mp3)', message.content):
                return False
        if len(message.attachments) > 0:
            for attachment in message.attachments:
                if not attachment.content_type.startswith(('image/', 'video/', 'audio/')):
                    return False
        return True

    @commands.Cog.listener('on_message')
    async def meme_channel_handler(self, message: discord.Message):
        if message.channel.id == Channel.MEME and message.author.bot == False:
            if message.content or message.attachments != []:
                if self.check_media(message):
                    await message.create_thread(name='💭 Comments', auto_archive_duration=10080)
                else:
                    await message.delete()

async def setup(client: commands.Bot):
    await client.add_cog(General(client))