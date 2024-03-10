import json

def load_draw_data():
    with open('./json/mydraw.json', 'r', encoding='utf8') as jfile:
        jdata = json.load(jfile)

    global rec_id, rec_emoji, rec_channel, emoji_name
    global FWMC_LUCKY, MID_LUCKY, SMALL_LUCKY, LUCKY, LAST_LUCKY, BAD
    global FWMC_LUCKY_ID, MID_LUCKY_ID, SMALL_LUCKY_ID, LUCKY_ID, LAST_LUCKY_ID, BAD_ID
    global LUCKY_ROLES,LUCKY_ROLES_IDS

    rec_id = int(jdata['Reaction_msg'])
    rec_emoji = jdata['Reaction_emoji']
    rec_channel = int(jdata["DRAW_Channel"])
    
    split_parts = rec_emoji.strip("<:>").split(":")
    emoji_name = split_parts[1]  # 這裡我們取得是表情的名稱作為 emoji_name
    
    # 抽籤圖片URL
    FWMC_LUCKY = jdata['FWMC_LUCKY']
    MID_LUCKY = jdata['MID_LUCKY']
    SMALL_LUCKY = jdata['SMALL_LUCKY']
    LUCKY = jdata['LUCKY']
    LAST_LUCKY = jdata['LAST_LUCKY']
    BAD = jdata['BAD']
    
    # 身分組ID
    FWMC_LUCKY_ID = jdata['FWMCLUCKY_ID']
    MID_LUCKY_ID = jdata['MID_LUCKY_ID']
    SMALL_LUCKY_ID = jdata['SMALL_LUCKY_ID']
    LUCKY_ID = jdata['LUCKY_ID']
    LAST_LUCKY_ID = jdata['LAST_LUCKY_ID']
    BAD_ID = jdata['BAD_ID']
    
    LUCKY_ROLES = [FWMC_LUCKY, MID_LUCKY, SMALL_LUCKY, LUCKY, LAST_LUCKY, BAD]
    LUCKY_ROLES_IDS = [FWMC_LUCKY_ID, MID_LUCKY_ID, SMALL_LUCKY_ID, LUCKY_ID, LAST_LUCKY_ID, BAD_ID]

load_draw_data()