import discord
from core import __json__
 
class mywhite():
    @staticmethod
    async def iswhitelist(interaction: discord.Interaction): 
        jdata = __json__.get_setting_data()
        if interaction.user.guild_permissions.administrator: 
            return True
        target_role_ids = set(jdata['white_ID'])
        member_roles = {role.id for role in interaction.user.roles}
        if member_roles & target_role_ids:
            return True
        else:
            await interaction.response.send_message(f"沒有權限使用此指令", ephemeral=True)
            return
