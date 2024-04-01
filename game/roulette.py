import discord
from discord import app_commands
import random,asyncio

from core.__init__ import Cog_Extension
import core.__draw__ as draw_data
from core.__mogo__ import my_mongodb

class RGame():
    def __init__(self):
        self.player_heart = 3
        self.gambler_heart = 3
        self.round = 0
        self.solid_bullet = '<:shotgun_shell:1221212914833166406>'
        self.empty_bomb = '<:shotgun_shell_green:1221212901256204328>'
        self.is_gambler_turn = True
    def generate_gun(self):
        magazine_size = random.randint(2, 8)
        self.magazine = [random.choice([self.solid_bullet, self.empty_bomb]) for _ in range(magazine_size)]
        return self

    def shotgun(self):
        shot = random.choice(self.magazine)
        self.magazine.remove(shot)  # 射击后将该弹药从弹夹中移除
        return 1 if shot == self.solid_bullet else 0
    
    def gambler_turn(self):
        pass

    def check_game_over(self):
        print(self.player_heart)
        print(self.gambler_heart)
        if self.player_heart <= 0:
            print("游戏结束，你输了。")
            return True
        elif self.gambler_heart <= 0:
            print("恭喜，你赢了！")
            return True
        return False
    
class roulettegame(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    async def shot_player_fc(self,interaction):
        try:
            self.RG.round += 1
            self.embed_sp = discord.Embed(title="俄羅斯輪盤",colour=0x00b0f4)
            if self.RG.shotgun() == 1:
                self.RG.player_heart -= 1
                
                self.embed_sp.add_field(name=f"第{self.RG.round}回合",
                    value=f"{interaction.user.mention}向自己開了一槍，糟糕的是{self.RG.solid_bullet}",
                    inline=False)
                
                self.RG.is_gambler_turn = True

            else:
                self.embed_sp.add_field(name=f"第{self.RG.round}回合",
                    value=f"{interaction.user.mention}向自己開了一槍，幸運的是{self.RG.empty_bomb}",
                    inline=False)
                
            self.embed_sp.add_field(name="子彈數量",
                            value=" ".join(self.RG.magazine),
                            inline=False)        
            self.embed_sp.add_field(name="玩家的血量",
                            value=f"{self.RG.player_heart}",
                            inline=True)
            self.embed_sp.add_field(name="賭徒的血量",
                            value=f"{self.RG.gambler_heart}",
                            inline=True)
        except Exception as e:
            print(f"s {e}")
        
    async def shot_gambler_fc(self,interaction):
        self.RG.round += 1
        self.embed_sg = discord.Embed(title="俄羅斯輪盤",colour=0x00b0f4)
        if self.RG.shotgun() == 1:
            self.RG.gambler_heart -= 1
            
            self.embed_sg.add_field(name=f"第{self.RG.round}回合",
                value=f"第{self.RG.round}回合\n {interaction.user.mention}向賭徒開了一槍，幸運的是{self.RG.solid_bullet}",
                inline=False)
        else:
            self.embed_sg.add_field(name=f"第{self.RG.round}回合",
                value=f"第{self.RG.round}回合\n {interaction.user.mention}向賭徒開了一槍，糟糕的是{self.RG.empty_bomb}",
                inline=False)
            #print("这是一颗空弹，现在是赌徒的回合。")
            self.RG.is_gambler_turn = True

        self.embed_sg.add_field(name="子彈數量",
                        value=" ".join(self.RG.magazine),
                        inline=False)        
        self.embed_sg.add_field(name="玩家的血量",
                        value=f"{self.RG.player_heart}",
                        inline=True)
        self.embed_sg.add_field(name="賭徒的血量",
                        value=f"{self.RG.gambler_heart}",
                        inline=True)
        pass
    
    async def gambler_shot_fc(self,interaction):
        try:
            gambler_action = random.choice(["射自己", "射玩家"])
            self.RG.round += 1
            self.embed_g = discord.Embed(title="俄羅斯輪盤",colour=0x00b0f4)
            if gambler_action == "射自己":
                if self.RG.shotgun() == 1:
                    #print("赌徒中了实弹！")
                    
                    self.embed_g.add_field(name=f"第{self.RG.round}回合",
                        value=f"賭徒向自己開了一槍 糟糕的是{self.RG.solid_bullet}",
                        inline=False)
                    self.RG.is_gambler_turn = False
                    self.RG.gambler_heart -= 1

                else:
                    #print("幸运的是，赌徒没有中弹。")
                    self.embed_g.add_field(name=f"第{self.RG.round}回合",
                        value=f"賭徒向自己開了一槍 幸運的是{self.RG.empty_bomb}",
                        inline=False)
            elif gambler_action == "射玩家":
                if self.RG.shotgun() == 1:
                    #print("你中了实弹！")
                    self.embed_g.add_field(name=f"第{self.RG.round}回合",
                        value=f"賭徒向{interaction.user.mention}開了一槍 糟糕的是{self.RG.solid_bullet}",
                        inline=False)
                    self.player_heart -= 1
                else:
                    self.RG.is_gambler_turn = False
                    #print("赌徒没中你。")
        
            self.embed_g.add_field(name="子彈數量",
                            value=" ".join(self.RG.magazine),
                            inline=False)        
            self.embed_g.add_field(name="玩家的血量",
                            value=f"{self.RG.player_heart}",
                            inline=True)
            self.embed_g.add_field(name="賭徒的血量",
                            value=f"{self.RG.gambler_heart}",
                            inline=True)
            
            await interaction.followup.edit_message(interaction.message.id, embed=self.embed_g,view=self.view)
        except Exception as e:
            print(f"g: {e}")
    @app_commands.command(name="roulette",description="俄羅斯輪盤")
    async def roulette(self, interaction):
        try:
            self.RG = RGame()
            self.gun = self.RG.generate_gun()
            button1 = discord.ui.Button(label="朝自己開一槍", style=discord.ButtonStyle.blurple, custom_id="shot_player")
            button2 = discord.ui.Button(label="朝賭徒開一槍", style=discord.ButtonStyle.red ,custom_id="shot_gambler")

            #開局
            self.embed = discord.Embed(title="俄羅斯輪盤",color=0x00ff00)
            self.embed.add_field(name="子彈數量",
                            value=" ".join(self.RG.magazine),
                            inline=False)        
            self.embed.add_field(name="玩家的血量",
                            value=f"{self.RG.player_heart}",
                            inline=True)
            self.embed.add_field(name="賭徒的血量",
                            value=f"{self.RG.gambler_heart}",
                            inline=True)
    
            async def shot_player_callback(interaction):
                await interaction.response.defer()
                await self.shot_player_fc(interaction)
                await interaction.followup.edit_message(interaction.message.id, embed=self.embed_sp,view=self.view)
            async def shot_gambler_callback(interaction):
                await interaction.response.defer()
                await self.shot_gambler_fc(interaction)
                await interaction.followup.edit_message(interaction.message.id, embed=self.embed_sg,view=self.view)


            button1.callback = shot_player_callback
            button2.callback = shot_gambler_callback
            
            self.empty_embed = discord.ui.View()
            self.view = discord.ui.View(timeout=60)
            self.view.add_item(button1)
            self.view.add_item(button2)

            await interaction.response.send_message(embed=self.embed,view=self.view)
        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(roulettegame(bot))


'''
            select_item = discord.ui.Select(
                placeholder='請選擇道具',
                options=[discord.SelectOption(label=item) for item in self.RG.items],
                custom_id="select_item"
            )

            select_item.callback = select_callback

            async def select_callback(interaction):
                await interaction.response.defer()
                self.player_select = interaction.data['values'][0]
                self.embed = discord.Embed(title="俄羅斯輪盤", color=0x00ff00)

                if self.player_select == "啤酒(隨機清除一發子彈)":
                    if random.choice(["solid_bullet", "empty_bomb"]) == "solid_bullet":
                        self.gun.solid_bullet -= 1
                    else:
                        self.gun.empty_bomb -= 1
                    self.embed.add_field(name="選擇道具",
                                    value=f"{self.player_select}",
                                    inline=False)
                elif self.player_select == "鉅子(雙倍傷害)":
                    self.embed.add_field(name="選擇道具",
                                    value=f"{self.player_select}",
                                    inline=False)
                    self.Effect = "double"
                elif self.player_select == "手銬(禁止對方一回合)":
                    self.embed.add_field(name="選擇道具",
                                    value=f"{self.player_select}",
                                    inline=False)
                    self.Effect = "stop"
                elif self.player_select == "香菸(回復1點生命)":
                    self.RG.player_heart += 1
                    self.embed.add_field(name="選擇道具",
                                    value=f"{self.player_select}",
                                    inline=False)
                    
                self.embed.add_field(name="子彈數量",
                        value=f"實彈: {self.gun.solid_bullet}  空彈: {self.gun.empty_bomb}",
                        inline=False) 
                self.embed.add_field(name="玩家的血量",
                                value=f"{self.RG.player_heart}",
                                inline=False)
                self.embed.add_field(name="賭徒的血量",
                                value=f"{self.RG.gambler_heart}",
                                inline=False)
                
                await interaction.followup.edit_message(interaction.message.id, embed=self.embed,view=view2)


'''