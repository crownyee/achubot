#Discord
import discord
from discord import app_commands
from discord.ext import commands
#Core
from core.__whitelist__ import mywhite
from core.__init__ import Cog_Extension
from core import __json__
#Tools
import asyncio,logging


class my_com(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    #Slash
    @app_commands.command(name='command_add',description='新增指令(admin only)')
    @app_commands.check(mywhite.iswhitelist)
    async def command_add(self, ita:discord.Interaction, command_name: str, command_content: str):
        try:
            await ita.response.defer()
            # 讀取現有的命令
            command_dict = __json__.get_commands_data()
            # 添加新命令
            command_dict[command_name] = command_content
            # 將修改後的命令字典寫回json檔中
            __json__.set_commands_data(command_dict)

            await ita.followup.send(f'指令已成功加入 "!{command_name}" 內容: `{command_content}`')
        except Exception as e:
            await ita.followup.send(f'指令加入錯誤 "{e}')
            logging.error(f"command_add.py  hello_1: {e}")

    @app_commands.command(name='command_del',description='刪除指令(admin only)')
    @app_commands.check(mywhite.iswhitelist)
    async def command_del(self, ita:discord.Integration, command_name:str): 
        try:
            await ita.response.defer()
            # 讀取現有的命令
            command_dict = __json__.get_commands_data()
            # 刪除指定的命令
            if command_name in command_dict:
                del command_dict[command_name]
                # 將修改後的命令字典寫回json檔案
                __json__.set_commands_data(command_dict)
                await ita.followup.send(f'指令 "!{command_name}" 已刪除')
            else:
                await ita.followup.send(f'指令 "{command_name}" 刪除失敗')
        except Exception as e:
            await ita.response.send_message(f'指令刪除錯誤 "{e}')
            logging.error(f"command_del {e}")

    @app_commands.command(name='command_rep',description='替換指令內容(admin only)')
    @app_commands.check(mywhite.iswhitelist)
    async def command_rep(self, ita:discord.Integration, command_name:str, new_command_content:str):
        try:   
            # 讀取現有的命令
            command_dict = __json__.get_commands_data()
                
            # 替換指定的命令內容
            if command_name in command_dict:
                command_dict[command_name] = new_command_content
                
                # 將修改後的命令字典寫回json檔案
                __json__.set_commands_data(command_dict)
                    
                await ita.response.send_message(f'指令 "{command_name}" 新內容: "`{new_command_content}`"')
            else:
                await ita.response.send_message(f'指令 "{command_name}" 替代失敗')
        except Exception as e:
            await ita.response.send_message(f"指令替代錯誤 {e}")
            logging.error(f"command_rep {e}")

    # 新增的斜線指令
    @app_commands.command(name='commands_list', description='列出所有指令')
    async def commands_list(self, ita:discord.Integration):
        try:
            # 讀取現有的命令
            command_dict = __json__.get_commands_data()
            # 將所有的命令連接成一個字串，並在每一個命令後面加上新行符號
            commands_list = '\n'.join(f'!{name}' for name, content in command_dict.items())
            
            if commands_list:
                await ita.response.send_message(f'```指令:\n{commands_list}```')
            else:
                await ita.response.send_message(f'No commands found.')
        except Exception as e:
            await ita.response.send_message(f"指令列表錯誤 {e}")
            logging.error(f"command_list {e}")


async def setup(bot):
    await bot.add_cog(my_com(bot))