import discord
import copy
import random
import asyncio
from discord.ext import commands
from discord.ui import Button, View
from discord import Embed, Color
from module.data_game.Player.SharedMoney import SharedMoney
from module.data_game.Player.player_manager import save_player_data, save_inventory_data, load_player_data, load_inventory_data
from module.data_game.Shop.data_shop import shop_items
intents = discord.Intents.default()
intents.message_content = True  # สำคัญมาก ต้องเปิดสำหรับอ่านข้อความ
bot = commands.Bot(command_prefix="!", intents=intents)
player = load_player_data()
player_inventory = load_inventory_data()
@bot.tree.command(name="inventory", description="กระเป๋าของคุณ มันจะแฟบหรือเปล่านะ")
async def inventory(interaction:discord.Interaction):
    player = load_player_data()
    player_inventory = load_inventory_data()
    user_id = str(interaction.user.id)
    await interaction.response.defer(ephemeral=True)
    if user_id not in player or not player[user_id]:
        await interaction.followup.send("คุณยังไม่มีไอเท็มในคลัง.", ephemeral=True)
    inventory = player[user_id]['inventory']
    embed = Embed(title="📦 คลังของคุณ", color=Color.blue())
    embed.set_footer(text="ใช้ไอเท็มโดย /use_item")
    # แสดงไอเท็มในคลัง
    for item_name, quantity in inventory.items():
        for types, des in shop_items[item_name].items():
            if item_name != "money" and types == 'des':
                embed.add_field(
                    name=f"🛍️ {item_name}",
                    value=f"\nรายละเอียด: {des}\nจำนวน: {quantity}",
                    inline=False
                )
    await interaction.followup.send(embed=embed, ephemeral=True)
