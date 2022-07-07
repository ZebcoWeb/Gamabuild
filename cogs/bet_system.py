import discord
import random
import re

from discord.ext import commands
from discord import app_commands

from config import Config, Channel
from models import MemberModel
from utils import error_embed, get_guide_number, success_embed


class GTNModal(discord.ui.Modal):
    def __init__(self, view, max_number):
        super().__init__(
            title='Guess the Number',
            timeout=None
        )
        self.view = view
        self.max_number = max_number

        self.guess = discord.ui.TextInput(
                label='Number', 
                placeholder=f'Enter a number between 1 and {self.max_number}'
        )
        self.add_item(self.guess)
    
    async def lose_callback(self, interaction: discord.Interaction, user_guess: int):
        guide_num, guide_msg = get_guide_number(self.view.secret_number, user_guess, self.max_number)

        if not self.view.first_guide_number and self.view.lose_time == 2 and self.view.member_model.cmd_guess_use == 0 and self.view.bet <= 15:
            print(guide_num)
            self.view.first_guide_number = guide_num

        if self.view.guess == 1:
            self.view.member_model.cmd_guess_lose += 1
            self.view.member_model.cmd_guess_use += 1
            self.view.member_model.gamacoin -= self.view.bet
            await self.view.member_model.save()

            await interaction.response.edit_message(
                content=f'🙁 Your chance to guess the secret number is over! You lost **{self.view.bet}** coin. The secret number was **{self.view.secret_number}**, ***Try later***', 
                embed=None,
                view=None,
            )
        else:
            self.view.guess -= 1
            self.view.lose_time += 1
            em = discord.Embed(
            title=f'You bet {self.view.bet} Coin',
            description=f'Guess the correct secret number to win 2x your bet Gamacoin \n\n> ❌ Number {user_guess} is incorrect!\n> {guide_msg}',
            color=discord.Color.yellow()
            )
            em.add_field(name='Guess time', value=f'**{self.view.guess}**', inline=True)
            em.add_field(name='\u200b', value=f'\u200b', inline=True)
            em.add_field(name='Number range', value=f'between **1** & **{self.view.max_number}**', inline=True)
            await interaction.response.edit_message(embed=em)

    async def won_callback(self, interaction: discord.Interaction):
        log_channel = await interaction.guild.fetch_channel(Channel.ACTIVITIES)
        won_coin = self.view.bet * 2

        self.view.member_model.cmd_guess_won += 1
        self.view.member_model.cmd_guess_use += 1
        self.view.member_model.gamacoin += won_coin
        await self.view.member_model.save()

        await interaction.response.edit_message(
            content=f'🤑 You found the secret number! You win **2x** your betting coin: **{won_coin}**',
            embed=None,
            view=None,
        )
        await log_channel.send(f'🎲 ***{interaction.user.name}*** bet {self.view.bet} coin on the guess number and won {won_coin} coin!')

    async def on_submit(self, interaction: discord.Interaction):
        if re.match(r'^[0-9]+$', self.guess.value):
            user_guess = int(self.guess.value)
            if user_guess <= self.max_number:
                if self.view.member_model.cmd_guess_use == 0 and self.view.lose_time >= 3 and self.view.bet <= 15:
                    if self.view.first_guide_number > self.view.secret_number:
                        if user_guess in list(range(1, self.view.first_guide_number)):
                            self.view.secret_number = user_guess
                    elif self.view.first_guide_number < self.view.secret_number:
                        if user_guess in list(range(self.view.first_guide_number, self.view.max_number + 1)):
                            self.view.secret_number = user_guess

                if user_guess == self.view.secret_number:
                    await self.won_callback(interaction)
                else:
                    await self.lose_callback(interaction, user_guess)
            else:
                await interaction.response.send_message(embed=error_embed(f'Please enter a number between 1 and {self.max_number}'), ephemeral=True)
        else:
            await interaction.response.send_message(embed=error_embed('Please enter a number!'), ephemeral=True)
    

class GTNBetView(discord.ui.View):
    def __init__(self, max_number, guess, bet, member_model):
        super().__init__(timeout=None)
        self.lose_time = 0
        self.max_number = max_number
        self.guess = guess
        self.bet = bet
        self.secret_number = random.randint(1, self.max_number)
        self.member_model = member_model
        self.first_guide_number = None

        self.add_item(GTNBet())


class GTNBet(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Guess the number',
            style=discord.ButtonStyle.green,
            custom_id='gtn_bet_button'
        )
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(GTNModal(self.view, self.view.max_number))


class GTNStartView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GTNStartSelect())

class GTNStartSelect(discord.ui.Select): 

    gtn_bets_entry = list(Config.GTN_BETS.keys())

    def __init__(self):
        super().__init__(
            placeholder='Enter your bet to start',
            custom_id='gtn_bet_entry',
        )
        
        for bet in self.gtn_bets_entry:
            self.add_option(
                label=f'{bet} Coin',
                value=str(bet),
            )
        
    async def callback(self, interaction: discord.Interaction):
        bet = int(self.values[0])
        guess_time = Config.GTN_BETS[bet]['guess']
        max_number = Config.GTN_BETS[bet]['max_number']
        member_model = await MemberModel.find_one(MemberModel.member_id == interaction.user.id)

        em = discord.Embed(
            title=f'You bet {bet} Coin',
            description='Guess the correct secret number to win 2x your bet Gamacoin',
            color=discord.Color.yellow()
        )
        em.add_field(name='Guess time', value=f'**{guess_time}**', inline=True)
        em.add_field(name='\u200b', value=f'\u200b', inline=True)
        em.add_field(name='Number range', value=f'between **1** & **{max_number}**', inline=True)
        await interaction.response.edit_message(content=None, embed=em, view=GTNBetView(max_number, guess_time, bet, member_model))

class WheelCoinForm(discord.ui.Modal):
    def __init__(self, cog):
        super().__init__(
            title='Wheel Coin', 
            timeout=None
        )
        self.cog = cog

        self.coin = discord.ui.TextInput(label='Coin', placeholder='Enter your coin to bet', style=discord.TextStyle.short, min_length=1)
        self.coin.callback = self.on_submit
        self.add_item(self.coin)


    async def on_submit(self, interaction: discord.Interaction):
        if re.match(r'^[0-9]+$', self.coin.value):
            coin = int(self.coin.value)
            await self.cog.start_wheel(interaction, coin)
        else:
            await interaction.response.send_message(embed=error_embed('Please enter a number!'), ephemeral=True)

class CasinoMenuView(discord.ui.View):
    def __init__(self, cog: commands.Cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label='Guess', style=discord.ButtonStyle.blurple, custom_id='GUESS_BUTTON', emoji='🎲')
    async def guess_callback(self, interaction: discord.Interaction, buttom: discord.ui.Button):
        await self.cog.start_guessthenumber(interaction)

    @discord.ui.button(label='Wheel', style=discord.ButtonStyle.blurple, custom_id='WHEEL_BUTTON', emoji='🎰')
    async def wheel_callback(self, interaction: discord.Interaction, buttom: discord.ui.Button):
        await interaction.response.send_modal(WheelCoinForm(self.cog))

    @discord.ui.button(label='Profile', style=discord.ButtonStyle.blurple, custom_id='PROFILE_BUTTON', emoji='😎')
    async def profile_callback(self, interaction: discord.Interaction, buttom: discord.ui.Button):
        await self.cog.profile(interaction)


class BetSystem(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client

        self.coefficients = []
        self.weights = []
        for c, w in Config.WHEEL_BETS:
            self.coefficients.append(c)
            self.weights.append(w)
    

    async def start_guessthenumber(self, interaction: discord.Interaction):
        member: MemberModel = await MemberModel.find_one(MemberModel.member_id == interaction.user.id)
        if member.gamacoin >= 5:
            em = discord.Embed(
                title='How much coins do you use to bet?',
                color=discord.Color.yellow()
            )
            await interaction.response.send_message(embed=em, view=GTNStartView(), ephemeral=True)
        else:
            await interaction.response.send_message(f'❗You need at least 5 Coin to play', ephemeral=True)


    async def start_wheel(self, interaction: discord.Interaction, coin: int = None):
        member = await MemberModel.find_one(MemberModel.member_id == interaction.user.id)
        if member.gamacoin >= coin:
            log_channel = await self.client.fetch_channel(Channel.ACTIVITIES)
            if member.wheel_use == 0:
                wheel_choice = 1.5
            else:
                wheel_choice = random.choices(self.coefficients, self.weights, k=1)[0]
            member.gamacoin = member.gamacoin - coin + (coin * wheel_choice)
            member.wheel_use += 1
            await member.save()
            await interaction.response.send_message(f'Your coin {wheel_choice}x, your balance: {member.gamacoin} coin', ephemeral=True)
            await log_channel.send(f'🎰 ***{interaction.user.name}*** bet {coin} coin on the wheel of chance and {wheel_choice}x coins.')
        else:
            await interaction.response.send_message(embed=error_embed(f'Your coin is not enough to start the bet. your balance: {member.gamacoin}'), ephemeral=True)

    
    async def profile(self, interaction: discord.Interaction):
        member = await MemberModel.find_one(MemberModel.member_id == interaction.user.id)
        em = discord.Embed(
            title=f'{interaction.user.name}',
            description=f'You are Level **{member.level}**',
            color=Config.DISCORD_COLOR
        )
        em.add_field(name='Gamacoin', value=f'{member.gamacoin} Coin', inline=True)
        em.add_field(name='\u200b', value=f'\u200b', inline=True)
        em.add_field(name='XP', value=f'{member.xp}', inline=True)
        em.set_thumbnail(url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=em, ephemeral=True)

    @app_commands.command(name='guess', description='🤔 Guess the secret number | 2x Coin')
    @app_commands.guilds(Config.SERVER_ID)
    @app_commands.checks.cooldown(1, 7200) # 2 hours
    async def guessthenumber(self, interaction: discord.Interaction):
        await self.start_guessthenumber(interaction)

    @app_commands.command(name='profile', description='😎 Display your profile')
    @app_commands.guilds(Config.SERVER_ID)
    async def display_profile(self, interaction: discord.Interaction):
        await self.profile(interaction)

    @app_commands.command(name='wheel', description='🎡 Put your money on the wheel of chance | 5x')
    @app_commands.guilds(Config.SERVER_ID)
    @app_commands.describe(coin='How much coins do you use to bet?')
    async def wheel(self, interaction: discord.Interaction, coin: int):
        await self.start_wheel(interaction, coin)

    @app_commands.command(name='coin', description='💰 Donate coins to a user')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guilds(Config.SERVER_ID)
    @app_commands.describe(coin='Coin to donate', member='Member to donate to')
    async def donate_coin(self, interaction: discord.Interaction, coin: int, member: discord.Member):
        log_channel = await self.client.fetch_channel(Channel.ACTIVITIES)
        member_model = await MemberModel.find_one(MemberModel.member_id == member.id)
        member_model.gamacoin += coin
        await member_model.save()
        await interaction.response.send_message(embed=success_embed(f'{member.mention} has received {coin} coin'), ephemeral=True)
        await log_channel.send(f'💸 {interaction.user.mention} has donated {coin} coin to {member.mention}')

    @app_commands.command(name='xp', description='🏆 Give xp to a user')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guilds(Config.SERVER_ID)
    @app_commands.describe(xp='XP to give', member='Member to give to')
    async def give_xp(self, interaction: discord.Interaction, xp: int, member: discord.Member):
        log_channel = await self.client.fetch_channel(Channel.ACTIVITIES)
        member_model = await MemberModel.find_one(MemberModel.member_id == member.id)
        member_model.xp += xp
        await member_model.save()
        await interaction.response.send_message(embed=success_embed(f'{member.mention} has received {xp}xp'), ephemeral=True)
        await log_channel.send(f'🪄 {member.mention} has received {xp}xp by {interaction.user.mention}')

    @commands.has_permissions(manage_guild=True)
    @commands.command(aliases=["minigame"])
    async def casino_context(self, ctx: commands.Context):
        casino_channel = await self.client.fetch_channel(Channel.CASINO)
        async for msg in casino_channel.history(limit=None):
            await msg.delete()
        em = discord.Embed(
            title='Mini Games',
            description='''<:CHEST:994300228108828734> ● Here's our mighty and shiny minigame section , in which you can invest your Gama Coins <:GamaCoin:994292311271944274> with the hope of increasing it!
<:stats:994300647082041534> ● Feel free to click on the profile button to check your status.
<:questionmark:994300948295983265> ● for more info type /help !''',
            color=0xff2a65
        )
        em.set_image(url='https://cdn.discordapp.com/attachments/980177765452099654/994309417124237432/MiniGames.png')
        em.set_footer(text= 'GamaBuild' , icon_url='https://media.discordapp.net/attachments/980177765452099654/994267291820769373/Logo.png')
        await casino_channel.send(embed=em, view=CasinoMenuView(cog=self))
        await ctx.reply(embed=success_embed('Games context sent'))


async def setup(client: commands.Bot):
    await client.add_cog(BetSystem(client))