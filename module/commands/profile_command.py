import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import Embed, Color
from module.data_game.Player.SharedMoney import SharedMoney
from module.data_game.Player.player_manager import save_player_data, save_inventory_data, load_player_data, load_inventory_data

intents = discord.Intents.default()
intents.message_content = True  # สำคัญมาก ต้องเปิดสำหรับอ่านข้อความ
bot = commands.Bot(command_prefix="!", intents=intents)
player = load_player_data()

@bot.tree.command(name="stats", description="ดูโปรไฟล์ของคุณ")
async def stats(interaction: discord.Interaction):
    player = load_player_data()
    player_inventory = load_inventory_data()
    user_id = str(interaction.user.id)  # รับ user_id จากผู้ใช้
    if user_id in player:  # ถ้าผู้ใช้มีข้อมูลใน player
        p = player[user_id]  # ดึงข้อมูลของผู้ใช้
        await interaction.response.defer(ephemeral=True)
        if isinstance(p['money'], dict):
            p['money'] = SharedMoney.from_dict(p['money'])
        embed = Embed(title="📜 ข้อมูลตัวละคร", color=Color.blurple())  # สร้าง embed
        # แสดงข้อมูลตัวละคร
        embed.add_field(name=f"👤 ชื่อ: {p['name']}", value='', inline=False)
        embed.add_field(name=f"❤️ HP: {(str(p['hp']))}/{(str(p['max_hp']))}", value='', inline=True)
        embed.add_field(name=f"🧬 Level: {(str(p['level']))}", value='', inline=True)
        
        # ตรวจสอบว่า p['money'] เป็นอ็อบเจกต์ของ SharedMoney หรือไม่
        if isinstance(p['money'], SharedMoney):
            embed.add_field(name=f"💰 Money: {(str(p['money'].get()))}", value='', inline=True)
        else:
            embed.add_field(name="💰 Money: ไม่พบข้อมูล", value='', inline=True)
        
        embed.add_field(name=f"✨ EXP: {(str(p['exp']))}", value='', inline=True)
        embed.add_field(name=f"🗡️ Damage: {(str(p['damage']))}", value='', inline=True)
        await interaction.followup.send(embed=embed, ephemeral = True)  # ส่ง embed ไปยัง Discord
    else:
        await interaction.response.send_message("คุณยังไม่ได้ลงทะเบียน \nคุณสามารถลงทะเบียนโดย /regis", ephemeral = True)