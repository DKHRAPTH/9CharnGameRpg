import discord
import copy
import random
import asyncio
from discord.ext import commands
from discord.ui import Button, View
from discord import Embed, Color
from module.data_game.Player import SharedMoney
from module.data_game.Player.player_manager import save_player_data, save_inventory_data, load_player_data, load_inventory_data
from module.data_game.Shop.data_shop import shop_items
intents = discord.Intents.default()
intents.message_content = True  # สำคัญมาก ต้องเปิดสำหรับอ่านข้อความ
bot = commands.Bot(command_prefix="!", intents=intents)
player = load_player_data()
player_inventory = load_inventory_data()

@bot.tree.command(name="use_item", description="ใช้ไอเท็มจากกระเป๋าของคุณ")
async def use_item(interaction: discord.Interaction):
    player = load_player_data()
    player_inventory = load_inventory_data()
    user_id = str(interaction.user.id)

    if user_id not in player or not player[user_id]['inventory']:
        await interaction.followup.send(embed=Embed(title="คุณไม่มีไอเท็มในคลัง", color=Color.red()), ephemeral=True)
    items = player[user_id]['inventory']
    options = [discord.SelectOption(label=item_name, description=f"มีจำนวน {amount}  รายละเอียด {des}") for item_name, amount in items.items()
                for i, des in shop_items[item_name].items() if i == "damage"
    if isinstance(amount, int) and amount > 0
    ]
    
    select = discord.ui.Select(placeholder="เลือกไอเท็ม", options=options)
    async def select_callback(select_inter: discord.Interaction):
        selected_item = select.values[0]
        #await interaction.response.defer(ephemeral=True)
        if selected_item in shop_items:
            item_data = shop_items.get(selected_item, {})
            if "hp" in item_data and player[user_id]['inventory'][selected_item] >= 1:
                heal = item_data["hp"]
                player[user_id]["hp"] += heal
                if player[user_id]["hp"] > player[user_id]["max_hp"]:
                    player[user_id]["hp"] = player[user_id]["max_hp"]
                player[user_id]['inventory'][selected_item] -= 1
                select.disabled = True
                await interaction.edit_original_response(content=f"คุณใช้ {selected_item} และฟื้น HP +{heal}" ,view=None)
            elif "weapon" in item_data['type'] and player[user_id]['equip'] != selected_item and player[user_id]['inventory'][selected_item] >=1:
                player[user_id]['damage'] = 1
                player[user_id]["equip"] = selected_item
                player[user_id]["damage"] += shop_items[player[user_id]["equip"]]['damage']
                select.disabled = True
                await interaction.edit_original_response(content=f"คุณสวมใส่อาวุธ: {selected_item}", view=None)
            elif "armor" in item_data['type'] and player[user_id]['armor'] != selected_item and player[user_id]['inventory'][selected_item] >=1:
                player[user_id]['durability'] = 0
                player[user_id]['armor'] = "None"
                player[user_id]['armor'] = selected_item
                player[user_id]['durability'] += shop_items[player[user_id]["armor"]]["durability"]
                select.disabled = True
                await interaction.edit_original_response(content=f"คุณสวมใส่อาวุธ: {selected_item}", view=None)
            else:
                select.disabled = True
                await interaction.edit_original_response(content="ไม่สามารถใช้ไอเท็มนี้ได้/สวมใส่อยู่แล้ว", view=None)
            save_player_data(player)
            save_inventory_data(player_inventory)
        else:
            select.disabled = True
            await select_inter.edit_original_response(content=f"ไม่สามารถใช้ไอเท็มนี้ได้: {selected_item}", view=None)

    select.callback = select_callback

    view = discord.ui.View()
    view.add_item(select)

    await interaction.response.send_message("เลือกไอเท็มที่คุณต้องการใช้:", view=view, ephemeral=True)
