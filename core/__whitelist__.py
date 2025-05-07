import discord
import json
with open('./json/setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)


class mywhite():
    async def iswhitelist(interaction: discord.Interaction):  
        if interaction.user.guild_permissions.administrator:  
            return True
        target_role_id = jdata['white_ID']
        member_roles = [role.id for role in interaction.user.roles]  

        if target_role_id in member_roles:
            return True
        else:
            await interaction.response.send_message(f"沒有權限使用此指令", ephemeral=True)


'''
target_role_ids = {1234567890, 2345678901, 3456789012}  # 替换为目标身份组的ID集合
# 获取用户的角色列表
member_roles = {role.id for role in interaction.user.roles}
if member_roles.intersection(target_role_ids):

'''