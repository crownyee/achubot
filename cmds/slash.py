import time, json
from datetime import datetime, timedelta
import twspace_dl
import subprocess,re

import discord
from discord import app_commands
from discord.ext import commands
from core.__init__ import Cog_Extension

import asyncio

class Cmd_Slash(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    #Slash 
    @app_commands.command(name = "hello_1", description="測試用")  
    async def hello_1(self, ita: discord.Interaction):  
        await ita.response.send_message(f"Hey {ita.user.mention} !",ephemeral=True)
    
    #:other_0_blueheart: :4a_pad2: SCHEDULE 11-06 ~ 11-13 :4a_pad2: :other_0_pinkheart:
    @app_commands.command(name='time_pstdate', description="PST轉CST時間")
    @app_commands.describe(all_pst_time = "範例:11-06 08:00,11-06 18:00")
    async def time_pstdate(self, ita: discord.Interaction, all_pst_time: str):
        converter = TimeConverter()
        pst_times = [time.strip() for time in all_pst_time.split(',')]
        formatted_dates = converter.convert_to_tpi_time(pst_times)
        await ita.response.send_message(
            f'## <:other_0_blueheart:1165151888984002611> <:4a_pad2:1135430223702278144> SCHEDULE {formatted_dates[0]} ~ {formatted_dates[1]} <:4a_pad2:1135430223702278144> <:other_0_pinkheart:1165151876887629904> \n'
            + "\n".join(formatted_dates[2:]))
    
    @app_commands.command(name='twitter_live_space', description="抓推特空間m3u8")
    async def twitter_live_space(self,ita: discord.Interaction, account: str):
        await ita.response.defer()

        txtfile = './json/cc.txt'
        try:
            if re.search(r'https?://(?:x\.com|twitter\.com)/i/spaces/\d+', account):
                replaced_message = re.sub(r'(?:x\.com|twitter\.com)', 'twitter.com',account)
                command = f"twspace_dl -i {replaced_message} -u -s -c {txtfile}"
                master_url = subprocess.run(command,shell=True,capture_output=True,text=True)
                await ita.edit_original_response(content=f'```{master_url.stdout}```')
            else:
                command = f"twspace_dl -U {account} -u -s -c {txtfile}"
                master_url = subprocess.run(command,shell=True,capture_output=True,text=True)
                await ita.edit_original_response(content=f'```{master_url.stdout}```')
        except Exception as e:
            print(e)
            await ita.edit_original_response(content=f'URL error 請使用twitter.com的帳號或是space')


#DEF
class TimeConverter():
    def __init__(self):
        self.pst_offset = timedelta(hours=-8)
        self.tpi_offset = timedelta(hours=+8)

    def pst_to_cst(self, pst_time):
        pst_datetime = datetime.strptime(pst_time, "%m-%d %H:%M")
        utc_datetime = pst_datetime - self.pst_offset
        cst_datetime = utc_datetime + self.tpi_offset
        tpi_time = cst_datetime.strftime("%m-%d %H:%M")
        return tpi_time

    def convert_to_tpi_time(self, pst_times):
        temp_time = []
        for pst_time in pst_times:
            time = self.pst_to_cst(pst_time)
            temp_time.append(time)
        tpi_times = ['2024-' + date for date in temp_time]
        final_stamp = []
        for tpi_time in tpi_times:
            struct_time = datetime.strptime(tpi_time, "%Y-%m-%d %H:%M")
            time_stamp = int(struct_time.timestamp())
            final_stamp.append(time_stamp)

        earliest_date = (datetime.strptime(pst_times[0].split()[0], "%m-%d") + timedelta(days=1)).strftime("%m-%d")
        latest_date = (datetime.strptime(pst_times[-1].split()[0], "%m-%d") + timedelta(days=1)).strftime("%m-%d")

        formatted_dates = [f"### **【text】** <t:{timestamp}:F>" for timestamp in final_stamp]
        formatted_dates.insert(0, earliest_date)
        formatted_dates.insert(1, latest_date)

        return formatted_dates


async def setup(bot):
    await bot.add_cog(Cmd_Slash(bot))


'''
網頁版
        try:
            if re.search(r'https?://(?:x\.com|twitter\.com)/i/spaces/\d+', account):
                replaced_message = re.sub(r'(?:x\.com|twitter\.com)', 'twitter.com',account)
                command = f"/home/container/.local/bin/twspace_dl -i {replaced_message} -u -s -c {txtfile}"
                master_url = subprocess.run(command,shell=True,capture_output=True,text=True)
                await ita.edit_original_response(content=f'```{master_url.stdout}```')
            else:
                command = f"/home/container/.local/bin/twspace_dl -U {account} -u -s -c {txtfile}"
                master_url = subprocess.run(command,shell=True,capture_output=True,text=True)
                await ita.edit_original_response(content=f'```{master_url.stdout}```')
        except Exception as e:
            print(e)
            await ita.edit_original_response(content=f'URL error 請使用twitter.com的帳號或是space')

class TimeConverter():
    def __init__(self):
        self.pst_offset = timedelta(hours=-8)
        self.tpi_offset = timedelta(hours=+8)

    def pst_to_cst(self, pst_time):
        pst_datetime = datetime.strptime(pst_time, "%m-%d %H:%M")
        utc_datetime = pst_datetime - self.pst_offset
        cst_datetime = utc_datetime + self.tpi_offset
        tpi_time = cst_datetime.strftime("%m-%d %H:%M")
        return tpi_time

    def convert_to_tpi_time(self, pst_times):
        temp_time = []
        for pst_time in pst_times:
            time = self.pst_to_cst(pst_time)
            temp_time.append(time)
        tpi_times = ['2024-' + date for date in temp_time]
        final_stamp = []
        for tpi_time in tpi_times:
            struct_time = datetime.strptime(tpi_time, "%Y-%m-%d %H:%M")
            time_stamp = int(struct_time.timestamp()) - 28800
            final_stamp.append(time_stamp)

        earliest_date = (datetime.strptime(pst_times[0].split()[0], "%m-%d") + timedelta(days=1)).strftime("%m-%d")
        latest_date = (datetime.strptime(pst_times[-1].split()[0], "%m-%d") + timedelta(days=1)).strftime("%m-%d")

        formatted_dates = [f"### **【text】** <t:{timestamp}:F>" for timestamp in final_stamp]
        formatted_dates.insert(0, earliest_date)
        formatted_dates.insert(1, latest_date)

        return formatted_dates
'''

