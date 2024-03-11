import discord
from discord.ext import commands
import random,asyncio, json
from core.__init__ import Cog_Extension

import motor.motor_asyncio
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

with open('./json/setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

uri = jdata['MongoAPI']

class game():     
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

    @commands.command()
    async def blackjack(self, ctx):
        BJG = game()
        while True:
            deck = BJG.generate_deck()
            player_hand = [deck.pop(), deck.pop()]
            dealer_hand = [deck.pop(), deck.pop()]

            flag = True
            while flag:
                await ctx.send(f"玩家的手牌 : {player_hand} 點數為: {BJG.calculate_score(player_hand)}")
                await ctx.send(f"莊家的手牌: {dealer_hand} 點數為: {BJG.calculate_score(dealer_hand)}")

                if BJG.calculate_score(player_hand) > 21:
                    await ctx.send("你爆了!")
                    flag = False
                    break

                await ctx.send("是否繼續加牌? (Y/N)")
                
                def check(m: discord.Message):
                    return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['y', 'n']
                try:
                    action = await self.bot.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    await ctx.send("操作過時，遊戲结束。")
                    flag = False
                    break

                if action.content.lower() == "y":
                    player_hand.append(deck.pop())
                elif action.content.lower() == "n":
                    while BJG.calculate_score(dealer_hand) < 17:
                        dealer_hand.append(deck.pop())

                    await ctx.send(f"莊家的手牌: {dealer_hand} 點數為: {BJG.calculate_score(dealer_hand)}")

                    if BJG.calculate_score(dealer_hand) > 21 or BJG.calculate_score(player_hand) > BJG.calculate_score(dealer_hand):
                        await ctx.send("你赢了")
                    else:
                        await ctx.send("你輸了")
                    flag = False
                    break

            await ctx.send("是否繼續遊玩? (Y/N)")
            try:
                play_again = await self.bot.wait_for('message', check=check, timeout=30)
            except asyncio.TimeoutError:
                await ctx.send("操作過時，遊戲结束。")
                flag = False
                break
            if play_again.content.lower() != "y":
                await ctx.send("結束遊戲")
                break

            await ctx.send("重新發牌！")

async def setup(bot):
    await bot.add_cog(BJ(bot))