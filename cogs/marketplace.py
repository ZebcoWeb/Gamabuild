import re
import discord
from discord.ext import commands
from discord import app_commands

from config import Config, Channel, Emoji
from utils import success_embed, error_embed
from models import ProductModel, MemberModel


class PurchaseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(PurchaseButtom())

class PurchaseButtom(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Purchase',
            style=discord.ButtonStyle.green,
            emoji=discord.PartialEmoji.from_str(Emoji.PURCHASE),
            custom_id='purchase_button'
        )
    
    async def callback(self, interaction: discord.Interaction):
        buyer = await MemberModel.find_one(MemberModel.member_id == interaction.user.id)
        product = await ProductModel.find_one(ProductModel.message_id == interaction.message.id, fetch_links=True)
        if buyer not in product.buyers:
            if buyer.gamacoin >= product.price:
                product.buyers.append(buyer)
                buyer.gamacoin -= product.price
                await buyer.save()
                await product.save()
                await interaction.response.send_message(
                    embed=success_embed(f'You have purchased ***{product.title}***\n\n {Emoji.DOWNLOAD} Download Link: [[Click Here]]({product.product_url})'),
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    embed=error_embed(f'You have not enough **Gamacoins [{product.price}]** to purchase this product.'),
                    ephemeral=True
                )
        else:
            await interaction.response.send_message(
                embed=success_embed(f'You have already purchased this product!\n\n {Emoji.DOWNLOAD} Download Link: [[Click Here]]({product.product_url})'),
                ephemeral=True
            )

class AddProductForm(discord.ui.Modal):
    def __init__(self, product_file = None) -> None:
        super().__init__(
            title='Add Product',
            timeout=None,
            custom_id='add_product_form'
        )
        self.product_file: discord.Attachment = product_file

        self.titlee = discord.ui.TextInput(label='Title', placeholder='Enter a title', min_length=3, style=discord.TextStyle.short)
        self.description = discord.ui.TextInput(label='Description', placeholder='Enter product description', min_length=5, style=discord.TextStyle.long)
        self.media = discord.ui.TextInput(label='Media URL', placeholder='Enter a media link to show', min_length=3, style=discord.TextStyle.short, required=False)
        self.price = discord.ui.TextInput(label='Price', placeholder='Enter product price', min_length=1, style=discord.TextStyle.short)
        self.add_item(self.titlee)
        self.add_item(self.description)
        self.add_item(self.media)
        self.add_item(self.price)
        if not self.product_file:
            self.product_url = discord.ui.TextInput(label='Product URL', placeholder='Enter product dowload link', min_length=3, style=discord.TextStyle.short)
            self.add_item(self.product_url)
    
    async def on_submit(self, interaction: discord.Interaction):
        if not re.match(r'^[0-9]*$', self.price.value):
            await interaction.response.send_message(
                embed=error_embed('Price must be a number'),
                ephemeral=True
            )
            return
        price = int(self.price.value)
        product_url = self.product_file.url if self.product_file else self.product_url.value

        marketplace_channel = await interaction.guild.fetch_channel(Channel.MARKETPLACE)
        em = discord.Embed(
            title='🛍️ ' + self.titlee.value,
            description=self.description.value,
            color=discord.Color.blue()
        )
        if self.media.value:
            em.set_image(url=self.media.value)
        em.add_field(name='Price', value=self.price.value, inline=True)

        product_message = await marketplace_channel.send(embed=em, view=PurchaseView())
        product_model = ProductModel(
            title=self.titlee.value,
            message_id=product_message.id,
            product_url=product_url,
            price=price,
        )

        if self.media.value:
            product_model.media_url = self.media.value
        await product_model.save()
        await interaction.response.send_message(
            embed=success_embed(f'Product added successfully: [[Click here]]({product_message.jump_url})'), 
            ephemeral=True
        )



class Marketplace(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

        self.client.add_view(PurchaseView())

    market = app_commands.Group(name='market', description='🛒 Marketplace moderation commands', guild_ids=[Config.SERVER_ID])

    @market.command(name='new', description='Add new product to marketplace')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(product_file = 'Product file (Optional)')
    async def guessthenumber(self, interaction: discord.Interaction, product_file: discord.Attachment = None):
        await interaction.response.send_modal(AddProductForm(product_file))

    
    @market.command(name='remove', description='Remove product from marketplace')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(message_id = 'Product message id')
    async def guessthenumber(self, interaction: discord.Interaction, message_id: str):
        message_id = int(message_id)
        product = await ProductModel.find_one(ProductModel.message_id == message_id)
        if product:
            marketplace_channel = await interaction.guild.fetch_channel(Channel.MARKETPLACE)
            await marketplace_channel.delete_messages([discord.Object(id=product.message_id)])
            await product.delete()
            await interaction.response.send_message(
                embed=success_embed(f'Product removed successfully'),
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                embed=error_embed(f'Product not found'),
                ephemeral=True
            )


async def setup(client: commands.Bot):
    await client.add_cog(Marketplace(client))