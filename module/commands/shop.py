import discord
import copy
import random
import asyncio
from discord.ext import commands
from discord.ui import Button, View, Select
from discord import Embed, Color
from module.data_game.Player.SharedMoney import SharedMoney
from module.data_game.Player.player_manager import save_player_data, save_inventory_data, load_player_data, load_inventory_data
from module.data_game.Shop.data_shop import shop_items
intents = discord.Intents.default()
intents.message_content = True  # สำคัญมาก ต้องเปิดสำหรับอ่านข้อความ
bot = commands.Bot(command_prefix="!", intents=intents)
player = load_player_data()
player_inventory = load_inventory_data()

@bot.tree.command(name="shop", description="ช็อปสินค้าที่มีคุณภาพตามราคา และอาวุธ")
async def shop(interaction: discord.Interaction):
    player = load_player_data()
    player_inventory = load_inventory_data()
    user_id = str(interaction.user.id)
    if user_id not in player:
        await interaction.response.send_message("คุณยังไม่ได้ลงทะเบียน \nคุณสามารถลงทะเบียนโดย /regis", ephemeral=True)
        return    
    # เมนูแรกให้เลือกประเภทสินค้า
    options = [
        discord.SelectOption(label="weapon", description="อาวุธ"),
        discord.SelectOption(label="potion", description="โพชั่น"),
        discord.SelectOption(label="armor", description='ชุดเกราะ'),
    ]
    select = Select(placeholder="เลือกหมวดหมู่สินค้า", options=options)

    async def type_item_callback(inner_interaction: discord.Interaction):
        selected_type = select.values[0]
        # สร้างรายการสินค้าในหมวดนั้น
        select.disabled = True
        await item_list(inner_interaction, selected_type)
    select.callback = type_item_callback
    view = View()
    view.add_item(select)
    await interaction.response.send_message(content="เลือกหมวดหมู่:", view=view, ephemeral=True)

    async def item_list(inner_interaction:discord.Interaction, selected_type:str):
        item_options = []
        for item_name, details in shop_items.items():
            if details["type"] == selected_type:
                item_options.append(
                    discord.SelectOption(label=item_name, description=f"ราคา {details['price']}\n{details["des"]}")
                )
        if not item_options:
            await inner_interaction.followup.edit_message("ไม่พบสินค้าในหมวดหมู่นี้", ephemeral=True)
            return
        # สร้างเมนูเลือกสินค้า
        select_item = Select(placeholder="เลือกสินค้าที่ต้องการ", options=item_options)
        async def item_list_callback(sub_interaction: discord.Interaction):
            chosen_item = select_item.values[0]
            await sub_interaction.response.defer(ephemeral=True)
            select_item.disabled = True
            select.disabled = True
            await sub_interaction.edit_original_response(content=f"คุณเลือก: {chosen_item}", view=None)
            await buy_item(sub_interaction, chosen_item)
        select_item.callback = item_list_callback
        new_view = View()
        new_view.add_item(select_item)
        await inner_interaction.response.send_message(view=new_view, ephemeral=True)

async def buy_item(intreaction:discord.Interaction, item_name):
    player = load_player_data()
    player_inventory = load_inventory_data()
    user_id = str(intreaction.user.id)
    if user_id in player:
        #await intreaction.response.defer()
        p = player[user_id]
        invent = p['inventory']
        item = shop_items[item_name]
        price = item['price']
        if isinstance(p['money'], dict):
            p['money'] = SharedMoney.from_dict(p['money'])
        if isinstance(p['money'], SharedMoney):
            if p['money'].get() >= price:
                print(p['money'].get())
                if item_name in invent:
                    invent[item_name] += 1
                else:
                    invent[item_name] = 1
                p['money'].subt(price)
                save_player_data(player)
                save_inventory_data(player_inventory)
                await intreaction.followup.send(f"คุณได้ซื้อ {item_name} สำเร็จ\nสามารถใช้ /inventory", ephemeral=True)
            else:
                await intreaction.followup.send("คุณมีเงินไม่เพียงพอ", ephemeral=True)
        else:
            print("p['money'] is not an instance of SharedMoney")
        
    else:
        await intreaction.response.send_message("คุณยังไม่ได้ลงทะเบียน \nคุณสามารถลงทะเบียนโดย /regis", ephemeral=True)