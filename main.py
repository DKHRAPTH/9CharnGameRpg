import discord
import os
from dotenv import load_dotenv
from flask import Flask
from discord.ext import commands
from module.data_game.Player.player_manager import load_player_data, load_inventory_data
from discord import Embed, Color
#------------commands----------#
from module.commands.register import regis
from module.commands.profile_command import stats
from module.commands.hunt import hunt
from module.commands.shop import shop
from module.commands.inventory import inventory
from module.commands.use_function import use_item
#-------------------------------#
#-------------------------------#
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True  # สำคัญมาก ต้องเปิดสำหรับอ่านข้อความ
bot = commands.Bot(command_prefix="!", intents=intents)
player = load_player_data()
player_inventory = load_inventory_data()
bot.tree.add_command(regis)
bot.tree.add_command(stats)
bot.tree.add_command(hunt)
bot.tree.add_command(shop)
bot.tree.add_command(inventory)
bot.tree.add_command(use_item)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"บอท {bot.user} ออนไลน์แล้ว!")
    load_player_data()
@bot.tree.command(name="_help", description="ดูคำสั่งทั้งหมด")
async def _help(interaction: discord.Interaction):
    embed = Embed(title="**คำสั่งทั้งหมดที่ใช้ได้**",description= "`/regis` - ลงทะเบียนผู้เล่นใหม่\n`/stats` - ดูค่าสถานะของคุณ\n`/hunt` - ออกล่า\n`/shop` - เปิดร้านค้า\n`/inventory` - ดูกระเป๋า\n`/use_item` - ใช้ไอเท็ม\n", color=Color.blurple())
    await interaction.response.send_message(embed=embed, ephemeral=True)
bot.run(TOKEN)