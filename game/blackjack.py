import discord
from discord import app_commands
from discord.ext import commands
import random,asyncio, json
from core.__init__ import Cog_Extension
import random,logging,datetime
import motor.motor_asyncio
import core.__draw__ as draw_data

logging.basicConfig(filename='./json/error_log.txt', level=logging.ERROR)

with open('./json/setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

uri = jdata['MongoAPI']
class game():
    def __init__(self):
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.bat = 0
    # 生成一副牌
    def generate_deck(self):
        self.card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.card_suits = ['♥', '♠', '♣', '♦']
        self.deck = [(i, j) for i in self.card_values for j in self.card_suits]
        random.shuffle(self.deck)
        return self.deck

    # 計算手牌分數
    def calculate_score(self,hand):
        score = 0
        aces = 0
        for card in hand:
            if card[0] in ['J', 'Q', 'K']:
                score += 10
            elif card[0] == 'A':
                aces += 1
                score += 11
            else:
                score += int(card[0])
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score


class BJ(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongoConnect = motor.motor_asyncio.AsyncIOMotorClient(uri)
        database = self.mongoConnect['myproject1']
        self.collection = database['collect1']
        self.games = {}

    async def update_embed(self,interaction):
        user_id = interaction.user.id
        embed_n = discord.Embed(title="21點遊戲", color=0x00ff00)
        embed_n.set_thumbnail(url=f"{self.selected_photo}")
        embed_n.clear_fields()
        embed_n.add_field(name="玩家的手牌",
                        value=f"{self.games[user_id].player_hand} \n 點數為: {self.games[user_id].calculate_score(self.games[user_id].player_hand)}",
                        inline=False)
        embed_n.add_field(name=f"{self.selected_member}的手牌",
                        value=f"{self.games[user_id].dealer_hand} \n 點數為: {self.games[user_id].calculate_score(self.games[user_id].dealer_hand)}",
                        inline=False)
        return embed_n
        
    async def BJ_gaming(self, interaction):
        user_id = interaction.user.id
        #人
        self.bau =False
        #一次加牌
        self.games[user_id].player_hand.append(self.games[user_id].deck.pop())
        #牌面
        self.embed_gaming = await self.update_embed(interaction)
        
        if self.games[user_id].calculate_score(self.games[user_id].player_hand) > 21:
            session = await self.mongoConnect.start_session()
            async with session.start_transaction():
                game_userData = await self.collection.find_one({"_id": interaction.user.id})
                money = game_userData['money']  
                self.bau = True
                money = money - self.games[user_id].bat
                self.embed_gaming.add_field(name="結果",
                                value=f"你爆了 輸了{self.games[user_id].bat} 餘額: {money}",
                                inline=False)
                await self.collection.update_one(
                    {"_id": interaction.user.id},
                    {"$set": {"money": money}},
                    session=session
                )
                return
        

    async def BJ_double(self, interaction):
        user_id = interaction.user.id
        #人
        self.bau =False
        #一次加牌
        self.games[user_id].player_hand.append(self.games[user_id].deck.pop())
        #牌面
        self.embed_double = await self.update_embed(interaction)
        
        if self.games[user_id].calculate_score(self.games[user_id].player_hand) > 21:
            session = await self.mongoConnect.start_session()
            async with session.start_transaction():
                game_userData = await self.collection.find_one({"_id": interaction.user.id})
                money = game_userData['money']   
                self.bau = True 
                money = money - (self.games[user_id].bat * 2)
                self.embed_double.add_field(name="結果",
                                value=f"你爆了 輸了{self.games[user_id].bat * 2} 餘額: {money}",
                                inline=False)
                await self.collection.update_one(
                    {"_id": interaction.user.id},
                    {"$set": {"money": money}},
                    session=session
                )
                return

    async def BJ_Stop(self, interaction):
        user_id = interaction.user.id
        session = await self.mongoConnect.start_session()
        async with session.start_transaction():
            game_userData = await self.collection.find_one({"_id": interaction.user.id})
            money = game_userData['money']  
        
        # 玩牌面
        #13 13 # 15 13
        try:
            while (True):
                #12 < 15
                if (self.games[user_id].calculate_score(self.games[user_id].dealer_hand) < self.games[user_id].calculate_score(self.games[user_id].player_hand)):
                    self.games[user_id].dealer_hand.append(self.games[user_id].deck.pop())
                elif (self.games[user_id].calculate_score(self.games[user_id].dealer_hand) == self.games[user_id].calculate_score(self.games[user_id].player_hand) and self.games[user_id].calculate_score(self.games[user_id].dealer_hand) < 17):
                    #16 16
                    self.games[user_id].dealer_hand.append(self.games[user_id].deck.pop())
                else:
                    break
        except Exception as e:
            logging.error(f"blackjack.py  BJ_Stop: {e}")

        try:
            if self.games[user_id].calculate_score(self.games[user_id].dealer_hand) > 21 or self.games[user_id].calculate_score(self.games[user_id].player_hand) > self.games[user_id].calculate_score(self.games[user_id].dealer_hand):
                #當莊家>21 或是 莊家18點以上 玩家大於莊家
                money = money + self.games[user_id].bat
                self.embed_Stop = await self.update_embed(interaction)
                self.embed_Stop.add_field(name="結果",
                                value=f"你贏了 獲得{self.games[user_id].bat} 餘額: {money}",
                                inline=False)
                await self.collection.update_one(
                    {"_id": interaction.user.id},
                    {"$set": {"money": money}},
                    session=session 
                )
                return
            elif self.games[user_id].calculate_score(self.games[user_id].dealer_hand) > self.games[user_id].calculate_score(self.games[user_id].player_hand):
                #莊家 > 玩家
                money = money - self.games[user_id].bat
                self.embed_Stop = await self.update_embed(interaction)
                self.embed_Stop.add_field(name=f"結果",
                                value=f"你輸了 輸了{self.games[user_id].bat} 餘額: {money}",
                                inline=False)
                await self.collection.update_one(
                    {"_id": interaction.user.id},
                    {"$set": {"money": money}},
                    session=session
                )
                return
            else:
                #21 21
                self.embed_Stop = await self.update_embed(interaction)
                self.embed_Stop.add_field(name=f"結果",
                                value=f"平手 餘額: {money}",
                                inline=False)
                await self.collection.update_one(
                    {"_id": interaction.user.id},
                    {"$set": {"money": money}},
                    session=session
                )
                return
        except Exception as e:
            logging.error(f"blackjack.py  BJ_Stop: {e}")


    @app_commands.command(name="blackjack",description="21點(60秒後失效)")
    @app_commands.describe(bat = "下注金額")
    async def blackjack(self, interaction ,bat : int):
        #按鈕
        button1 = discord.ui.Button(label="要牌", style=discord.ButtonStyle.primary, custom_id="blackjack_gaming")
        button2 = discord.ui.Button(label="雙倍加注", style=discord.ButtonStyle.primary, custom_id="blackjack_double")
        button3 = discord.ui.Button(label="停牌", style=discord.ButtonStyle.red, custom_id="blackjack_stop")

        #選擇莊家
        self.selected_member = random.choice(list(draw_data.photo.keys()))
        self.selected_photo = draw_data.photo[self.selected_member]
        user_id  = interaction.user.id
        self.games[user_id] = game()
        self.games[user_id].bat = bat
        self.games[user_id].deck = self.games[user_id].generate_deck()
        self.games[user_id].player_hand = [self.games[user_id].deck.pop(), self.games[user_id].deck.pop()]
        self.games[user_id].dealer_hand = [self.games[user_id].deck.pop(), self.games[user_id].deck.pop()]
        # 玩牌面
        embed = discord.Embed(title="21點遊戲", color=0x00ff00)
        embed.set_thumbnail(url=f"{self.selected_photo}")
        embed.clear_fields()
        embed.add_field(name="玩家的手牌",
                        value=f"{self.games[user_id].player_hand} \n 點數為: {self.games[user_id].calculate_score(self.games[user_id].player_hand)}",
                        inline=False)
        embed.add_field(name=f"{self.selected_member}的手牌",
                        value=f"{self.games[user_id].dealer_hand} \n 點數為: {self.games[user_id].calculate_score(self.games[user_id].dealer_hand)}",
                        inline=False)
        
        
        async def gaming_callback(interaction):
            await interaction.response.defer()
            await self.BJ_gaming(interaction)
            if self.bau:
                await interaction.followup.edit_message(interaction.message.id, embed=self.embed_gaming, view=self.empty_view)
            else:
                await interaction.followup.edit_message(interaction.message.id, embed=self.embed_gaming, view=view)

        async def double_callback(interaction):
            await interaction.response.defer()  
            await self.BJ_double(interaction)
            if self.bau:
                await interaction.followup.edit_message(interaction.message.id, embed=self.embed_double, view=self.empty_view)
            else:
                await interaction.followup.edit_message(interaction.message.id, embed=self.embed_double, view=view)

        async def stop_callback(interaction):
            await interaction.response.defer()
            await self.BJ_Stop(interaction)
            # Disable all buttons after stopping the game
            await interaction.followup.edit_message(interaction.message.id, embed=self.embed_Stop, view=self.empty_view)


        button1.callback = gaming_callback
        button2.callback = double_callback
        button3.callback = stop_callback
        
        self.empty_view = discord.ui.View()
        view = discord.ui.View(timeout=60)
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        await interaction.response.send_message(embed=embed,view=view)
        

async def setup(bot):
    await bot.add_cog(BJ(bot))
