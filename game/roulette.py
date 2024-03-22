import discord
from discord import app_commands
import random,asyncio

from core.__init__ import Cog_Extension
import core.__draw__ as draw_data
from core.__mogo__ import my_mongodb

class RGame():
    def __init__(self):
        self.items = ["啤酒(隨機清除一發子彈)","鉅子(雙倍傷害)","手銬(禁止對方一回合)","香菸(回復1點生命)"]
        self.player_heart = 4
        self.gambler_heart = 4

    def generate_gun(self):
        self.shotgun_bullets = random.randint(2, 8)
        self.solid_bullet = random.randint(1, self.shotgun_bullets - 1)
        self.empty_bomb = self.shotgun_bullets - self.solid_bullet
        return self


class roulettegame(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.collection = my_mongodb.collection

    async def shot_player(self,interaction):
        pass
    async def shot_player(self,interaction):
        pass

    @app_commands.command(name="roulette",description="俄羅斯輪盤")
    #@app_commands.describe(bat = "下注金額")
    async def roulette(self, interaction):
        try:
            self.RG = RGame()
            self.gun = self.RG.generate_gun()
            button1 = discord.ui.Button(label="朝自己開一槍", style=discord.ButtonStyle.blurple, custom_id="shot_player")
            button2 = discord.ui.Button(label="朝賭徒開一槍", style=discord.ButtonStyle.red ,custom_id="shot_gambler")
            select_item = discord.ui.Select(
                placeholder='請選擇道具',
                options=[discord.SelectOption(label=item) for item in self.RG.items]
            )

            #開局
            embed = discord.Embed(title="俄羅斯輪盤", color=0x00ff00)
            embed.add_field(name="子彈數量",
                            value=f"實彈: {self.gun.solid_bullet}  空彈: {self.gun.empty_bomb}",
                            inline=False)        
            embed.add_field(name="玩家的血量",
                            value=f"{self.RG.player_heart}",
                            inline=False)
            embed.add_field(name="賭徒的血量",
                            value=f"{self.RG.gambler_heart}",
                            inline=False)
    
            async def shot_player_callback(interaction):
                await interaction.response.defer() 
                await self.shot_player_fc(interaction)
            async def shot_gambler_callback(interaction):
                await interaction.response.defer() 
                await self.shot_gambler_fc(interaction)
            async def select_callback(interaction):
                self.player_select = selected_item = interaction.component[0].label
                if self.player_select == "啤酒(隨機清除一發子彈)":
                    embed = discord.Embed(title="俄羅斯輪盤", color=0x00ff00)
                    embed.add_field(name="子彈數量",
                                    value=f"實彈: {self.gun.solid_bullet}  空彈: {self.gun.empty_bomb}",
                                    inline=False)        
                    embed.add_field(name="玩家的血量",
                                    value=f"{self.RG.player_heart}",
                                    inline=False)
                    embed.add_field(name="賭徒的血量",
                                    value=f"{self.RG.gambler_heart}",
                                    inline=False)
                elif self.player_select == "鉅子(雙倍傷害)":
                    print("")
                elif self.player_select == "手銬(禁止對方一回合)":
                    print("")
                elif self.player_select == "香菸(回復1點生命)":
                    print("")
            button1.callback = shot_player_callback
            button2.callback = shot_gambler_callback
            select_item.callback = select_callback

            self.empty_view = discord.ui.View()

            view = discord.ui.View(timeout=60)
            view.add_item(button1)
            view.add_item(button2)
            view.add_item(select_item)

            view2 = discord.ui.View()
            view2.add_item(button1)
            view2.add_item(button2)
            await interaction.response.send_message(embed=embed,view=view)
        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(roulettegame(bot))
