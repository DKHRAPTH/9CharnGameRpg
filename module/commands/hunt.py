import discord
import copy
import random
import asyncio
import os
from discord.ext import commands
from discord.ui import Button, View
from discord import Embed, Color
from module.data_game.Player.SharedMoney import SharedMoney
from module.data_game.Player.player_manager import save_player_data, load_player_data, load_inventory_data
from module.data_game.Monters.data_monters import monters
from module.data_game.Player.level import level
intents = discord.Intents.default()
intents.message_content = True  # สำคัญมาก ต้องเปิดสำหรับอ่านข้อความ
bot = commands.Bot(command_prefix="!", intents=intents)
player = load_player_data()
player_inventory = load_inventory_data()



@bot.tree.command(name="hunt", description="หาศัตรูเพื่อขนะและล่ารางวัล หรือ เพื่อความตาย")
async def hunt(interaction:discord.Integration):
    await do_hunt(interaction)

async def do_hunt(interaction:discord.Interaction):
    player = load_player_data()
    player_inventory = load_inventory_data()
    user_id = str(interaction.user.id)
    await interaction.response.defer(ephemeral=True)
    if user_id in player and player[user_id]['hp']>1:
        name, monter = random.choice(list(monters.items()))
        view = View()
        async def fight_callback(interaction):
            await interaction.response.defer()
            await interaction.followup.send(f"คุณเลือกสู้กับ {name}!", ephemeral=True)
            monter_clone = copy.deepcopy(monter)
            await take_damage(interaction, name, monter_clone)
            view = View()
        async def refresh_callback(interaction):
            #await interaction.response.defer(ephemeral=True)
            await do_hunt(interaction)
        view.add_item(Button(label="⚔️ สู้", style=discord.ButtonStyle.danger, custom_id="fight"))
        view.add_item(Button(label="🔄 หามอนสเตอร์ใหม่", style=discord.ButtonStyle.gray, custom_id="refresh"))

        # ผูก callback กับปุ่มแต่ละปุ่ม
        view.children[0].callback = fight_callback
        view.children[1].callback = refresh_callback

        embed = Embed(
            title="🔎 พบมอนสเตอร์!",
            description=f"👾 {name}\n❤️ Hp: {monter['hp']}\n🗡️ Damage: {monter['damage']}",
            color=Color.blurple()
        )
        image = monters[name]['image']
        if image:
            chosen_image = random.choice(image)
            embed.set_thumbnail(url=chosen_image)
        else:
            return
        if interaction.response.is_done():  # ถ้าตอบไปแล้ว
            await interaction.edit_original_response(embed=embed, view=view)
        else:
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)
    else:
        await interaction.followup.send("คุณยังไม่ได้ลงทะเบียนหรือคุณเสียชีวิตไปแล้ว \nคุณสามารถลงทะเบียนโดย /regis / ตรวจสอบข้อมุลผู้เล่นโดย /stats หรือ /shop เพื่อฟื้นฟูเลือด", ephemeral=True)

async def take_damage(interaction:discord.Interaction, mon_name, monter):
    player = load_player_data()
    player_inventory = load_inventory_data()
    monter_inbattle = {"name":mon_name, "data":monter}
    user_id = str(interaction.user.id)
    if user_id in player :
        p = player[user_id]
        await in_battle(p,mon_name,monter,interaction)
        while True:
            
            if p['hp'] <=0 or monter_inbattle["data"]['hp'] <=0 :
                p['hp'] = 0
                break
            else:
                if p['durability'] >0 and p['hp'] >0:
                    p['durability'] -=monter_inbattle['data']['damage']
                    monter_inbattle['data']['hp']-=p['damage']
                else:
                    p['hp'] -= monter_inbattle["data"]['damage']
                    monter_inbattle["data"]['hp'] -=p['damage']
                await asyncio.sleep(0.01) #ใช้แทนtime.sleep เพราะ สามารถทำให้funcอื่นทำงานได้ด้วย
        
        if p['hp'] <= 0 and monter_inbattle["data"]['hp'] > 0:
            p['hp'] = 0
            save_player_data(player)
            embed_1 = Embed(
                title="💀 Game Over",
                description="คุณได้เสียชีวิตในระหว่างการต่อสู้",
                color=Color.red(),
            )
            embed_1.add_field(
                name=f"ถูกฆ่าโดย {monter_inbattle['name']} 👾",
                value=f"❤️ Hp: {monter_inbattle['data']['hp']}/{monters[mon_name]['hp']}\n🗡️ Damage: {monter_inbattle['data']['damage']}",
                inline=True,
            )
            await interaction.followup.send(embed=embed_1, ephemeral=True)
        else:
            embed_2 = Embed(
                title="🏆 Victory!",
                description=f"คุณได้ล่า {monter_inbattle['name']} สำเร็จ!",
                color=Color.green(),
            )
            embed_2.add_field(
                name="🎁 รางวัลที่ได้รับ",
                value=f"💰 Money: {monter_inbattle['data']['money']}\n✨ Exp: {monter_inbattle['data']['exp']}",
                inline=True,
            )
            await player_manager(p, monter_inbattle)
            save_player_data(player)
            await interaction.edit_original_response(embed=embed_2, view=None)
    else:
        await interaction.response.send_message("คุณยังไม่ได้ลงทะเบียน \nคุณสามารถลงทะเบียนโดย /regis", ephemeral=True)



async def in_battle(p,name,monter,interaction:discord.Interaction):
    player = load_player_data()
    player_inventory = load_inventory_data()
    if p:
        embed = Embed(
            title="⚔️ การต่อสู้เริ่มต้น!",
            description="ศึกระหว่างคุณและมอนสเตอร์เริ่มขึ้นแล้ว!",
            color=Color.red()
        )
        embed.add_field(
            name=f"🧍‍♂️ ผู้เล่น: {p['name']}",
            value=f"HP: {p['hp']}\nDMG: {p['damage']}",
            inline=True
        )
        embed.add_field(
            name=f"👾 มอนสเตอร์: {name}",
            value=f"HP: {monter['hp']}\nDMG: {monter['damage']}",
            inline=True
        )
        embed.set_footer(text="ระบบต่อสู้ RPG Bot")
        await interaction.edit_original_response(embed=embed, view=None)

async def player_manager(p,data_mon):
    load_player_data()
    if p:
        p['money'].add(data_mon["data"]['money'])
        p['exp'] += (data_mon["data"]['exp'])
        for i ,ex in level.items():
            if p['exp']>=level[i]['exp'] and int(p['level']) < int(i):
                print(1)
                add_max_hp = float(i) * 0.15
                p['level'] = i
                p['max_hp'] += add_max_hp
                p['hp'] = p['max_hp']
                p['exp'] -=level[i]['exp']
        save_player_data()
    else:
        return