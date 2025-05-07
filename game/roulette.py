import discord,logging
from discord import app_commands
import random,asyncio,json
import motor.motor_asyncio
from core.__init__ import Cog_Extension
logging.basicConfig(filename='./json/error_log.txt', level=logging.ERROR)

with open('./json/setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

uri = jdata['MongoAPI']


class RGame():
    def __init__(self):
        self.player_heart = ["<:heart:1237901918400020590>"] * 4
        self.gambler_heart = ["<:heart:1237901918400020590>"] * 4
        self.round = 0
        self.solid_bullet = '<:shotgun_shell:1221212914833166406>'
        self.empty_bomb = '<:shotgun_shell_green:1221212901256204328>'
        self.is_player = True
        self.message = ""
        self.items = ["啤酒(隨機清除一發子彈)","香菸(回復1點生命)"]
        self.Effect = {"beer":0, "health":0,"gun_total":0,"gun_o":0,"selfgun_o":0,"selfgun_x":0,"gun_x":0,"gun_f":0}

    def final_count(self):
        bat = 0
        bat += len(self.player_heart) * 1000
        bat += len(self.gambler_heart) * -800
        bat += self.Effect['gun_o'] * 500
        bat += self.Effect['gun_x'] * -1000
        bat += self.Effect['selfgun_o'] * 500
        bat += self.Effect['selfgun_x'] * -800
        bat += self.Effect['gun_f'] * 1200
        bat += self.Effect['beer'] * -800
        bat += self.Effect['health'] * -900
        return bat
    def generate_gun(self):
        magazine_size = random.randint(2, 8)
        # 確保至少有一發空彈和一發實彈
        guaranteed_bullets = [self.solid_bullet, self.empty_bomb]
        # 其餘的子彈隨機生成
        random_bullets = [random.choice([self.solid_bullet, self.empty_bomb]) for _ in range(magazine_size - 2)]
        self.magazine = guaranteed_bullets + random_bullets
        
    def shotgun(self):
        if len(self.magazine) <= 0:
            self.message += "子彈沒了，重新補充\n"
            self.generate_gun()

        self.shot = random.choice(self.magazine)
        self.magazine.remove(self.shot)  # 移除選中的子彈
        self.hit = self.shot == self.solid_bullet
        return self.hit

    def check_gun(self):
        if len(self.magazine) <= 0:
            self.message += "子彈沒了，重新補充\n"
            self.generate_gun()

        return self.magazine

    def check_game_over(self):
        if len(self.player_heart) <= 0:
            self.message +="\n遊戲結束\n"
            return True
        elif len(self.gambler_heart) <= 0:
            self.message += "\n遊戲結束\n"
            return True
        return False

class roulettegame(Cog_Extension):
    def __init__(self, *args, **kwargs):
        self.empty_view = discord.ui.View()
        self.mongoConnect = motor.motor_asyncio.AsyncIOMotorClient(uri)
        database = self.mongoConnect['myproject1']
        self.collection = database['collect1']
        self.games = {}  # 存放遊戲實例的字典
        super().__init__(*args, **kwargs)   

    async def update_embed(self,interaction, game_message):
        user_id = interaction.user.id

        embed = discord.Embed(title="俄羅斯輪盤", description=game_message, color=0x00ff00)
        self.games[user_id].check_gun()
        embed.add_field(name="子彈數量", value=" ".join(self.games[user_id].magazine), inline=False)
        embed.add_field(name="玩家的血量", value=" ".join(self.games[user_id].player_heart), inline=True)
        embed.add_field(name="荷官的血量", value=" ".join(self.games[user_id].gambler_heart), inline=True)
        return embed

    async def update_data(self, interaction):
        user_id = interaction.user.id

        session = await self.mongoConnect.start_session()
        async with session.start_transaction():
            game_userData = await self.collection.find_one({"_id": interaction.user.id})
            money = game_userData['money']  
            money += self.games[user_id].final_count()

            await self.collection.update_one(
                {"_id": interaction.user.id},
                {"$set": {"money": money}},
                session=session 
            )
            return        

    async def final_embed(self,interaction ,game_message):
        user_id = interaction.user.id
        bat = self.games[user_id].final_count()
        final_message = f"\n======  結算畫面 ======\n"
        final_message += f"玩家所剩下的生命 {len(self.games[user_id].player_heart)}次 x1000\n"
        final_message += f"荷官所剩下的生命 {len(self.games[user_id].gambler_heart)}次 x-800\n"
        final_message += f"成功向荷官開槍 {self.games[user_id].Effect['gun_o']}次 x500\n"
        final_message += f"被荷官射中了{self.games[user_id].Effect['gun_x']}次 x-1000\n"
        final_message += f"朝自己開槍無事{self.games[user_id].Effect['selfgun_o']}次 x500\n"
        final_message += f"朝自己開槍出事{self.games[user_id].Effect['selfgun_x']}次 x-800\n"
        final_message += f"躲過了荷官的子彈{self.games[user_id].Effect['gun_f']}次 x1200\n"
        final_message += f"啤酒使用了{self.games[user_id].Effect['beer']}次 x-800\n"
        final_message += f"香菸使用了{self.games[user_id].Effect['health']}次 x-900\n"
        final_message += f"=====================\n"
        final_message += f"最後得到了 {bat} 點數."
        embed_s = discord.Embed(title="俄羅斯輪盤", description=f"{final_message}", color=0xb25ca8)
        embed_s.add_field(name="子彈數量", value=" ".join(self.games[user_id].magazine), inline=False)
        embed_s.add_field(name="玩家的血量", value=" ".join(self.games[user_id].player_heart), inline=True)
        embed_s.add_field(name="荷官的血量", value=" ".join(self.games[user_id].gambler_heart), inline=True)

        return embed_s

    async def play_round(self,interaction,target):
        user_id = interaction.user.id
        user = interaction.user.mention

        self.games[user_id].round += 1
        self.games[user_id].message += f"====== 第 {self.games[user_id].round} 輪 ======\n"
        hit = self.games[user_id].shotgun()

        if self.games[user_id].is_player:
            self.games[user_id].message += f"- 玩家回合\n"
            if target == 'gambler':
                if hit:
                    self.games[user_id].gambler_heart.pop()
                    self.games[user_id].message += f"- 是**實彈**{self.games[user_id].shot}砰！{user}射中了荷官\n"
                    self.games[user_id].Effect['gun_o'] += 1
                    self.games[user_id].is_player = True #玩家回合
                else:
                    self.games[user_id].message += f"- 是**空包彈**{self.games[user_id].shot}！{user}射了個寂寞\n"
                    self.games[user_id].is_player = False #荷官回合
            else:
                if hit:
                    self.games[user_id].player_heart.pop()
                    self.games[user_id].message += f"- 是**實彈**{self.games[user_id].shot}砰！{user}朝自己射中了一槍！\n"
                    self.games[user_id].Effect['selfgun_x'] += 1
                    self.games[user_id].is_player = False #荷官回合
                else:
                    self.games[user_id].message += f"- 是**空包彈**{self.games[user_id].shot}安全！{user}沒射中自己。\n"
                    self.games[user_id].Effect['selfgun_o'] += 1
                    self.games[user_id].is_player = True #玩家回合
        else:
            gambler_shoot_self = random.random() < 0.1  # 随机选择射击玩家还是自己
            self.games[user_id].message += f"- 荷官回合\n"

            if gambler_shoot_self:
                if hit:
                    self.games[user_id].gambler_heart.pop()
                    self.games[user_id].message += f"- 是**實彈**{self.games[user_id].shot}砰！荷官射中自己！\n"
                    self.games[user_id].is_player = True #玩家回合
                else:
                    self.games[user_id].message += f"- 是**空包彈**{self.games[user_id].shot}荷官没事。\n"
                    self.games[user_id].is_player = False #荷官回合
            else:
                if hit:
                    self.games[user_id].player_heart.pop()
                    self.games[user_id].message += f"- 是**實彈**{self.games[user_id].shot}砰！荷官射中了玩家！\n"
                    self.games[user_id].Effect['gun_x'] += 1
                    self.games[user_id].is_player = False #荷官回合
                else:
                    self.games[user_id].message += f"- 是**空包彈**{self.games[user_id].shot}安全！荷官沒有射中玩家。\n"
                    self.games[user_id].Effect['gun_f'] += 1
                    self.games[user_id].is_player = True #玩家回合

        await asyncio.sleep(0.1)
        embed = await self.update_embed(interaction,self.games[user_id].message)
        return embed,self.games[user_id].is_player

    async def play_game(self, interaction, target):
        user_id = interaction.user.id
        while True:
            embed, is_player = await self.play_round(interaction,target)
            if self.games[user_id].check_game_over():
                embed_s = await self.final_embed(interaction,self.games[user_id].message)
                await interaction.followup.edit_message(interaction.message.id, embed=embed_s,view=self.empty_view)
                await self.update_data(interaction)
                del self.games[user_id]
                break
            elif is_player:
                await interaction.followup.edit_message(interaction.message.id, embed=embed,view=self.view)
                break
            else:
                await interaction.followup.edit_message(interaction.message.id, embed=embed,view=self.view)

    @app_commands.command(name="roulette",description="俄羅斯輪盤")
    async def roulette(self, interaction):
        try:
            # 檢查是否已有遊戲實例存在，如果沒有才創建新的實例
            user_id  = interaction.user.id
            self.games[user_id] = RGame()  # 將實例儲存到字典中
            self.games[user_id].generate_gun()  # 產生散彈槍
            #按鈕
            button1 = discord.ui.Button(label="朝自己開一槍", style=discord.ButtonStyle.blurple, custom_id=f"shot_player")
            button2 = discord.ui.Button(label="朝荷官開一槍", style=discord.ButtonStyle.red ,custom_id=f"shot_gambler")

            #工具
            select_item = discord.ui.Select(
                placeholder='請選擇道具',
                options=[discord.SelectOption(label=item) for item in self.games[user_id].items],
                custom_id="select_item"
            )

            async def select_callback(interaction):
                await interaction.response.defer() 
                self.player_select = interaction.data['values'][0]  
                initial_embed = discord.Embed(title="俄羅斯輪盤", color=0x00ff00) 
                   
                if self.player_select == "啤酒(隨機清除一發子彈)":  
                    self.games[user_id].shotgun()
                    self.games[user_id].message += f"- **選擇了啤酒(-800 bat)**\n"
                    self.games[user_id].Effect["beer"] += 1
                    embed = await self.update_embed(interaction,self.games[user_id].message)

                elif self.player_select == "香菸(回復1點生命)":  
                    self.games[user_id].message += f"- **選擇了香菸**(-1100 bat)**\n"
                    self.games[user_id].Effect["health"] += 1
                    self.games[user_id].player_heart.append("<:heart:1237901918400020590>")
                    embed = await self.update_embed(interaction,self.games[user_id].message)

                await interaction.followup.edit_message(interaction.message.id,embed=embed,view=self.view2)  

            #開局embed
            initial_embed = discord.Embed(title="俄羅斯輪盤",description=f"{self.games[user_id].message}",color=0x00ff00)
            initial_embed.add_field(name="子彈數量",
                            value=" ".join(self.games[user_id].magazine),
                            inline=False)        
            initial_embed.add_field(name="玩家的血量", 
                                    value=" ".join(self.games[user_id].player_heart), 
                                    inline=True)
            initial_embed.add_field(name="荷官的血量", 
                                    value=" ".join(self.games[user_id].gambler_heart), 
                                    inline=True)
                    

            async def shot_player_callback(interaction):
                await interaction.response.defer()

                await self.play_game(interaction, "player")

            async def shot_gambler_callback(interaction):
                await interaction.response.defer()
                await self.play_game(interaction, "gambler")
                
            select_item.callback = select_callback
            button1.callback = shot_player_callback
            button2.callback = shot_gambler_callback

            self.view2 = discord.ui.View()
            self.view2.add_item(button1)
            self.view2.add_item(button2)
            self.view = discord.ui.View()
            self.view.add_item(select_item)
            self.view.add_item(button1)
            self.view.add_item(button2)
            await interaction.response.send_message(embed=initial_embed,view=self.view)
        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(roulettegame(bot))