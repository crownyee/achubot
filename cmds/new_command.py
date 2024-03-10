import discord
import json

from discord import app_commands
from discord.ext import commands
from core.__init__ import Cog_Extension
import asyncio

src = './json/commands.json'

class my_com(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    #Slash
    @app_commands.command(name='command_add',description='新增指令')
    async def command_add(self, ita:discord.Integration, command_name: str, command_content: str):
        if not ita.user.permissions.administrator:
            await ita.response.send_message("抱歉，您沒有權限執行此指令。")
            return
    
        # 讀取現有的命令
        try:
            with open(src, 'r', encoding='utf-8') as f:
                command_dict = json.load(f)
        except FileNotFoundError:
            command_dict = {}

        # 添加新命令
        command_dict[command_name] = command_content

        # 將修改後的命令字典寫回json檔中
        with open(src, 'w', encoding='utf-8') as f:
            json.dump(command_dict, f,ensure_ascii=False, indent=4)

        await ita.response.send_message(f'Command "{command_name}" added with content: `{command_content}`')


    @app_commands.command(name='command_del',description='刪除指令')
    async def command_del(self, ita:discord.Integration, command_name:str):
        if not ita.user.permissions.administrator:
            await ita.response.send_message("抱歉，您沒有權限執行此指令。")
            return
        
        # 讀取現有的命令
        try:
            with open(src, 'r', encoding='utf-8') as f:
                command_dict = json.load(f)
        except FileNotFoundError:
            command_dict = {}
            
        # 刪除指定的命令
        if command_name in command_dict:
            del command_dict[command_name]
            
            # 將修改後的命令字典寫回json檔案
            with open(src, 'w', encoding='utf-8') as f:
                json.dump(command_dict, f,ensure_ascii=False, indent=4)
                
            await ita.response.send_message(f'Command "{command_name}" removed.')
        else:
            await ita.response.send_message(f'Command "{command_name}" does not exist.')


    @app_commands.command(name='command_rep',description='替換指令內容')
    async def command_rep(self, ita:discord.Integration, command_name:str, new_command_content:str):
        if not ita.user.permissions.administrator:
            await ita.response.send_message("抱歉，您沒有權限執行此指令。")
            return
    
        # 讀取現有的命令
        try:
            with open(src, 'r', encoding='utf-8') as f:
                command_dict = json.load(f)
        except FileNotFoundError:
            command_dict = {}
            
        # 替換指定的命令內容
        if command_name in command_dict:
            command_dict[command_name] = new_command_content
            
            # 將修改後的命令字典寫回json檔案
            with open(src, 'w', encoding='utf-8') as f:
                json.dump(command_dict, f,ensure_ascii=False, indent=4)
                
            await ita.response.send_message(f'Command "{command_name}" replaced with content: "`{new_command_content}`"')
        else:
            await ita.response.send_message(f'Command "{command_name}" does not exist.')

    # 新增的斜線指令
    @app_commands.command(name='commands_list', description='列出所有指令')
    async def commands_list(self, ita:discord.Integration):
        # 讀取現有的命令
        try:
            with open(src, 'r', encoding='utf-8') as f:
                command_dict = json.load(f)
        except FileNotFoundError:
            await ita.response.send_message(f'No commands found.')
            return

        # 將所有的命令連接成一個字串，並在每一個命令後面加上新行符號
        commands_list = '\n'.join(f'**{name}**: `{content}`' for name, content in command_dict.items())
        
        if commands_list:
            await ita.response.send_message(f'Commands:\n{commands_list}')
        else:
            await ita.response.send_message(f'No commands found.')


async def setup(bot):
    await bot.add_cog(my_com(bot))