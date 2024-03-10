import discord
from discord import app_commands
from discord.ext import commands, tasks
from core.__init__ import Cog_Extension
import asyncio
import mysql.connector
from mysql.connector import Error
from datetime import datetime, time
from typing import Union

# 設定 MySQL 資料庫連線
db = mysql.connector.connect(
    host="localhost",
    user="chuchu",
    password="0927",
    database="mydiscord"
)
 
class Mydata(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        async def Signin():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                now = datetime.now().strftime('%H%M')

                if now == '0000':
                    cursor = db.cursor()
                    update_query = "UPDATE members SET sign_in = 1 "
                    cursor.execute(update_query)
                    db.commit()
                    await asyncio.sleep(60)

                await asyncio.sleep(10)

        self.bg_subs = self.bot.loop.create_task(Signin())

        
    @commands.hybrid_command()
    async def 加入(self, ctx,member: discord.Member=None):
        # 確認訊息不是機器人自身發出的
        if member == self.bot.user:
            return
        member = ctx.author if  not member else member
 
        # 解析使用者資料
        username = member.display_name
        user_id = member.id
        user_photo = str(member.avatar.url)

        # 建立資料庫游標
        cursor = db.cursor()

        # 檢查資料是否已存在
        select_query = "SELECT * FROM members WHERE user_id = %s"
        select_value = (user_id,)
        cursor.execute(select_query, select_value)
        result = cursor.fetchone()

        if result:
            await ctx.send(f"<@{user_id}> 您的資料已存在！")
        else:
            # 執行插入資料的 SQL 命令
            insert_query = "INSERT INTO members (username, user_id, user_photo) VALUES (%s, %s, %s)"
            insert_values = (username, user_id, user_photo)
            cursor.execute(insert_query, insert_values)
            # 提交更改
            db.commit()
            await ctx.send(f"<@{user_id}> 已成功加入！")

    @commands.has_permissions(administrator=True)
    @commands.hybrid_command()
    async def 刪除(self, ctx, member: discord.Member):
        # 確認訊息不是機器人自身發出的
        if member == self.bot.user:
            return
        # 解析使用者資料
        user_id = member.id
        # 建立資料庫游標
        cursor = db.cursor()
        # 檢查資料是否存在
        select_query = "SELECT * FROM members WHERE user_id = %s"
        select_value = (user_id,)
        cursor.execute(select_query, select_value)
        result = cursor.fetchone()
        if result:
            # 執行刪除資料的 SQL 命令
            delete_query = "DELETE FROM members WHERE user_id = %s"
            delete_value = (user_id,)
            cursor.execute(delete_query, delete_value)
            # 提交更改
            db.commit()
            await ctx.send(f"<@{user_id}> 的資料已成功刪除！")
        else:
            await ctx.send(f"<@{user_id}> 的資料不存在！")

    @commands.hybrid_command()
    async def 顯示(self, ctx, member: discord.Member = None):
        # 確認訊息不是機器人自身發出的
        if member == self.bot.user:
            return
        member = ctx.author if not member else member

        user_id = member.id
        cursor = db.cursor()
        #更新 使用者在伺服器的名字
        username = member.display_name
        update_query = "UPDATE members SET username = %s WHERE user_id = %s"
        update_values = (username,user_id)
        cursor.execute(update_query, update_values)
        db.commit()

        select_query_mem = "SELECT * FROM members WHERE user_id = %s"
        select_value = (user_id,)
        cursor.execute(select_query_mem, select_value)
        result = cursor.fetchone()

        if result:
            # 使用者資料存在，建立 embed 物件並顯示資料
            embed = discord.Embed(title="使用者資料", color=discord.Color.blue())
            embed.add_field(name="使用者名稱", value=result[0], inline=False)
            embed.add_field(name="使用者ID", value=result[1], inline=False)
            embed.add_field(name="點數: ", value=result[4], inline=False)
            embed.set_thumbnail(url=result[2])  # 使用者頭像連結
            await ctx.send(embed=embed)
        else:
            await ctx.send("找不到使用者資料！")

    @commands.hybrid_command()
    async def 簽到(self, ctx, member: discord.Member = None):
        # 確認訊息不是機器人自身發出的
        if member == self.bot.user:
            return
        member = ctx.author if not member else member

        user_id = member.id
        cursor = db.cursor()
        select_query_sign = "SELECT sign_in, point FROM members WHERE user_id = %s"
        select_value = (user_id,)
        cursor.execute(select_query_sign, select_value)
        result = cursor.fetchone()
        
        if result:
            sign_in_status = result[0]
            if sign_in_status == 0:
                await ctx.send(f"<@{user_id}> 您已經簽到過了！")
            else:
                point = result[1] + 60 #更新點數
                await ctx.send(f"<@{user_id}> 簽到成功！ 獲得 60 點數")
                # 更新使用者的簽到狀態為已簽到
                update_query_sign = "UPDATE members SET sign_in = 0, point = %s WHERE user_id = %s"
                update_value = (point, user_id)
                cursor.execute(update_query_sign, update_value)
                db.commit()
        else:
            await ctx.send("找不到使用者資料！")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def 補充(self, ctx):
        # 確認訊息不是機器人自身發出的
        if ctx.author == self.bot.user:
            return
        
        cursor = db.cursor()
        update_query_sign_in = "UPDATE members SET sign_in = 1"
        cursor.execute(update_query_sign_in)
        db.commit()
        
        await ctx.send("補充完畢")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def all(self, ctx, amount: int):
        # 確認訊息不是機器人自身發出的
        if ctx.author == self.bot.user:
            return
        
        cursor = db.cursor()
        select_query_point = "SELECT user_id FROM members"
        cursor.execute(select_query_point)
        results = cursor.fetchall()
        
        for result in results:
            user_id = result[0]
            select_query_point = "SELECT point FROM members WHERE user_id = %s"
            select_value = (user_id,)
            cursor.execute(select_query_point, select_value)
            current_point = cursor.fetchone()[0]
            new_point = current_point + amount
            update_query_point = "UPDATE members SET point = %s WHERE user_id = %s"
            update_value = (new_point, user_id)
            cursor.execute(update_query_point, update_value)
        
        db.commit()
        await ctx.send(f"已將 {amount} 點數發放給所有人")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def give(self, ctx, amount: int, member: discord.Member):
        # 確認訊息不是機器人自身發出的
        if member == self.bot.user:
            return
        user_id = member.id
        cursor = db.cursor()
        select_query_point = "SELECT point FROM members WHERE user_id = %s"
        select_value = (user_id,)
        cursor.execute(select_query_point, select_value)
        result = cursor.fetchone()
        
        # 確認使用者存在於資料庫中
        if result:
            current_point = result[0]
            new_point = current_point + amount
            update_query_point = "UPDATE members SET point = %s WHERE user_id = %s"
            update_value = (new_point, user_id)
            cursor.execute(update_query_point, update_value)
            db.commit()
            await ctx.send(f"已給予 {member.mention} {amount} 點數")
        else:
            await ctx.send(f"使用者 {member.mention} 不存在於資料庫中")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def dataclose(self,ctx):
        # 關閉資料庫連線 
        cursor = db.cursor()
        cursor.close() 
        db.close()
        await ctx.send(f"資料庫關閉")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def dataopen(self,ctx):
        # 重新建立資料庫連線
        db = mysql.connector.connect(
            host="localhost",
            user="chuchu",
            password="0927",
            database="mydiscord"
        )
        await ctx.send("資料庫已打開")
    
async def setup(bot):
    await bot.add_cog(Mydata(bot))