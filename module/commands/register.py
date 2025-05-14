import discord
from discord.ext import commands
from discord import Embed, Color
from module.data_game.Player.SharedMoney import SharedMoney
from module.data_game.Player.player_manager import save_player_data, save_inventory_data, load_player_data, load_inventory_data

player = load_player_data()
player_inventory = load_inventory_data()

intents = discord.Intents.default()
intents.message_content = True  # สำคัญมาก ต้องเปิดสำหรับอ่านข้อความ
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.tree.command(name="regis", description="ลงทะเบียนเข้าสู่โลก RPG")
async def regis(interaction:discord.Interaction):
    player = load_player_data()
    player_inventory = load_inventory_data()
    user_id = str(interaction.user.id)
    if not user_id in player:
        share_money = SharedMoney(100)
        player[user_id] = {
            "name": interaction.user.display_name,
            "hp": 20,
            "durability":0,
            "max_hp":20,
            "level": 0,
            "money": share_money.to_dict(),
            "exp":0,
            "damage":1,
            "equip":0,
            "armor":"None",
            "inventory":{},
        }
        save_player_data(player)
        player_inventory[user_id] ={
            "money":player[user_id]['money'],
        }
        save_inventory_data(player_inventory)
        embed = Embed(
            title=f"🎉 ยินดีต้อนรับสู่โลก RPG, {interaction.user.display_name}!",
            description="การผจญภัยของคุณกำลังจะเริ่มต้นขึ้น...\nเตรียมตัวให้พร้อมสำหรับการต่อสู้ การล่าขุมทรัพย์ และมิตรภาพ!",
            color=Color.blurple()
        )
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
        embed.set_footer(text="พิมพ์ /_help เพื่อดูคำสั่งทั้งหมด")
        embed.set_image(url="https://sdmntpreastus.oaiusercontent.com/files/00000000-6730-61f9-90c7-2011dc1c7919/raw?se=2025-05-12T00%3A37%3A48Z&sp=r&sv=2024-08-04&sr=b&scid=00000000-0000-0000-0000-000000000000&skoid=9ccea605-1409-4478-82eb-9c83b25dc1b0&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-05-11T07%3A54%3A20Z&ske=2025-05-12T07%3A54%3A20Z&sks=b&skv=2024-08-04&sig=o3HWIfTgCwAj7Lb74rME2WzD/hVQ7dPK2Cv5K4cCcOE%3D")  # เปลี่ยนลิงก์รูปด้านล่างตามต้องการ
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(f"คุณได้ลงทะเบียนไปแล้ว", ephemeral=True)
