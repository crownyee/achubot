import discord
import re
from discord import app_commands
from discord.ext import commands
from core.__init__ import Cog_Extension
import asyncio
import subprocess

class Mywork(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #指令
    @commands.command()
    async def clean(self, ctx, num: int):
        await ctx.channel.purge(limit=num + 1)

    
    @commands.command()
    async def bau(self, ctx, *,mes):
        await asyncio.sleep(0.5)
        try:
            await ctx.message.delete()
            await ctx.send(mes)
        except discord.errors.NotFound:
            pass

    @commands.command()
    async def send_role(self,ctx):
        try:
            await ctx.message.delete()
            embed_1 = discord.Embed(title="點選對應圖示獲得該身分組",
                                colour=0xdca1dd)
            embed_2 = discord.Embed()
            embed_3 = discord.Embed()
            embed_4 = discord.Embed()
            embed_5 = discord.Embed()
            embed_1.add_field(name="基本身分組",
                            value="<:1a_fuwawa_wink:1136226802063388754>FUWAWA<:1a_fuwawa_wink:1136226802063388754>、<:1a_mococo_hi:1136226824599384154>MOCOCO<:1a_mococo_hi:1136226824599384154>\n顏色(同時選擇只會顯示最左邊的顏色)：\n**__FUWA色__**<:1b_fuwawa_teetee:1133815712536854578>\n**__MOCO色__**<:1b_mococo_teetee:1133815803611983943>",
                            inline=False)
            embed_2.add_field(name="功能身分組",
                            value="**__直播通知__**  → <:4a_pad:1134166843641319484>\n**__R18__**  → <:other_2_dog_bonk:1135594518767476746>\n**__FWMC突襲在其他直播影片__**   →  <:2_fuwamoco_look:1158740290853671013>\n**__FWMC活動企劃身分組__**   →  <:1_fuwamoco_lazy:1134082059434991696>\n**__小公告通知(通販、語音等)__**  → <:1l_richFuwawa_:1322580864093393037>",
                            inline=False)
            embed_3.add_field(name="紀念身分組(不時會過期)",
                            value="**__FWMC百萬紀念__** → <:other_one:1322584488974487613>\n**__雙子一年身分組__** → 1️⃣\n**__雙子半年身分組__** → (過期)",
                            inline=False)
            embed_4.add_field(name="特殊身分組說明",
                            value="繪BAU 烤BAU 等 身分組可以向管理員申請",
                            inline=False)
            embed_5.add_field(name="活動身分組說明",
                            value="當有線上活動開始或線下活動時會不定時出現",
                            inline=False)

            await ctx.send(embed=embed_1)
            await ctx.send(embed=embed_2)
            await ctx.send(embed=embed_3)
            await ctx.send(embed=embed_4)
            await ctx.send(embed=embed_5)
        except discord.errors.NotFound:
            pass

    @commands.command()
    async def edit_role_embed(self, ctx, message_id: int):
        try:
            # 獲取指定 ID 的訊息
            message = await ctx.channel.fetch_message(message_id)
            
            # 創建新的 embed 以替換舊的
            new_embed = discord.Embed()
            new_embed.add_field(name="特殊身分組說明",
            value="繪BAU 烤BAU 等 身分組可以向管理員申請",
                            inline=False)
            
            # 編輯訊息，更新 embed
            await message.edit(embed=new_embed)
            await ctx.message.delete()  # 刪除觸發指令的訊息
            
        except discord.errors.NotFound:
            await ctx.send("找不到指定的訊息", delete_after=5)
        except Exception as e:
            await ctx.send(f"發生錯誤: {e}", delete_after=5)


    @commands.command()
    async def get_user_info(self,ctx, user_id):

        user = ctx.guild.get_member(int(user_id))
        if user is not None:

            avatar_url = str(user.display_avatar)
            await ctx.send(f"{avatar_url}")
            
            display_name = user.display_name
            await ctx.send(f"{display_name}")
        else:
            await ctx.send("AAAAAA")
            
async def setup(bot):
    await bot.add_cog(Mywork(bot))

#廢棄
'''
@commands.command()
async def sayed(self, ctx,*,message):
    await ctx.message.delete()
    await ctx.send(message)

command = f"twspace_dl -U {account} -u -s -c {txtfile}"
master_url = subprocess.run(command, shell=True, capture_output=True, text=True)
await ctx.send(f'```{master_url.stdout}```')
'''