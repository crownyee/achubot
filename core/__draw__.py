import json

def load_draw_data():
    with open('./json/mydraw.json', 'r', encoding='utf8') as jfile:
        jdata = json.load(jfile)

    global rec_id, rec_emoji, DRAW_channel, emoji_name
    global FWMC_LUCKY, MID_LUCKY, SMALL_LUCKY, LUCKY, LAST_LUCKY, BAD,PERO_draw
    global FWMC_LUCKY_ID, MID_LUCKY_ID, SMALL_LUCKY_ID, LUCKY_ID, LAST_LUCKY_ID, BAD_ID
    global LUCKY_ROLES,LUCKY_ROLES_IDS
    global luck_colors, luck_data,photo
    rec_id = int(jdata['Reaction_msg'])
    rec_emoji = jdata['Reaction_emoji']
    DRAW_channel = int(jdata["DRAW_Channel"])
    
    split_parts = rec_emoji.strip("<:>").split(":")
    emoji_name = split_parts[0]  # 這裡我們取得是表情的名稱作為 emoji_name
    
    # 抽籤圖片URL
    PERO_draw = jdata['PERO_draw']
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

    #顏色
    luck_colors = [
        '紅色', '藍色', '綠色', '黃色', '粉紅色', '橙色', '紫色', '淺藍色', '灰色', 
        '棕色', '黑色', '白色', '金色', '銀色', '靛藍色', '土耳其藍', '薰衣草色', 
        '橄欖綠', '淺綠色', '海軍藍', '淺黃色', '象牙色', '淺灰色', '天藍色', '亮紫色', 
        '暗紅色', '酒紅色', '淺粉色', '亮橙色', '淺紫色', '珊瑚色', '青色', '青綠色', 
        '森林綠', '深綠色', '淺藍綠色', '深藍色', '檸檬黄', '薄荷綠', '墨绿色', '杏色', 
        '栗色', '赭色', '米色', '天青色', '石灰色', '巧克力色', '櫻桃色', '番茄色'
    ]
    #DD
    luck_data = {
        "staff": "友人A,春先のどか,YAGOO",
        "0th": "ときのそら,ロボ子,星街すいせい,さくらみこ,AZKi",
        "JP_1gen": "白上フブキ,アキ・ローゼンター,夏色まつり,赤井はあと,夜空メル",
        "JP_2gen": "湊あくあ,紫咲シオン,百鬼あやめ,癒月ちょこ,大空スバル",
        "JP_Ggen": "大神ミオ,猫又おかゆ,戌神ころね",
        "JP_3gen": "兎田ぺこら,不知火フレア,白銀ノエル,宝鐘マリン,潤羽るしあ",
        "JP_4gen": "天音かな,角巻わため,常闇トワ,姫森ルーナ,桐生ココ",
        "JP_5gen": "雪花ラミィ,桃鈴ねね,獅白ぼたん,尾丸ポルカ,魔乃アロエ",
        "JP_HoloX": "ラプラス・ダークネス,鷹嶺ルイ,博衣こより,沙花叉クロヱ,風真いろは",
        "JP_ReGLOSS": "火威青,音乃瀬奏,一条莉々華,儒烏風亭らでん,轟はじめ",
        "EN_Myth": "Gawr Gura,Watson Amelia,Ninomae Ina'nis,Takanashi Kiara,Mori Calliope",
        "EN_Promise": "Hakos Baelz,Nanashi Mumei,Ouro Kronii,IRyS,Ceres Fauna,Tsukumo Sana",
        "EN_Advent": "Fuwawa Abyssgard,Mococo Abyssgard,Nerissa Ravencroft,Koseki Bijou,Shiori Novella",
        "ID_1gen": "Ayunda Risu,Moona Hoshinova,Airani Iofifteen",
        "ID_2gen": "Kureiji Ollie,Anya Melfissa,Pavolia Reine",
        "ID_3gen": "Vestia Zeta,Kaela Kovalskia,Kobo Kanaeru"
    }
    #photo 
    photo = {
        #JP-staff
        "友人A":"https://cdn.discordapp.com/attachments/1216685771336060976/1216697864869384246/OBwoJysj_400x400.png",
        "春先のどか":"https://cdn.discordapp.com/attachments/1216685771336060976/1216697829863723018/bfm5HYQ7_400x400.png",
        "YAGOO":"https://cdn.discordapp.com/attachments/1216685771336060976/1216697909026750494/GS2b2-TE_400x400.png",
        #JP-0gen
        "ときのそら":"https://holodex.net/statics/channelImg/UCp6993wxpyDPHUpavwDFqgg/100.png",
        "ロボ子":"https://holodex.net/statics/channelImg/UCDqI2jOz0weumE8s7paEk6g/100.png",
        "星街すいせい":"https://holodex.net/statics/channelImg/UC5CwaMl1eIgY8h02uZw7u8A/100.png",
        "さくらみこ":"https://holodex.net/statics/channelImg/UC-hM6YJuNYVAmUWxeIr9FeA/100.png",
        "AZKi":"https://holodex.net/statics/channelImg/UC0TXe_LYZ4scaW2XMyi5_kw/100.png",
        #JP-1gen
        "赤井はあと":"https://holodex.net/statics/channelImg/UCp6993wxpyDPHUpavwDFqgg/100.png",
        "夜空メル":"https://holodex.net/statics/channelImg/UCD8HOxPs4Xvsm8H0ZxXGiBw/100.png",
        "白上フブキ":"https://holodex.net/statics/channelImg/UCdn5BQ06XqgXoAxIhbqw5Rg/100.png",
        "アキ・ローゼンター":"https://holodex.net/statics/channelImg/UCFTLzh12_nrtzqBPsTCqenA/100.png",
        "夏色まつり":"https://holodex.net/statics/channelImg/UCQ0UDLQCjY0rmuxCDE38FGg/100.png",
        #JP-Ggen
        "戌神ころね":"https://holodex.net/statics/channelImg/UChAnqc_AY5_I3Px5dig3X1Q/100.png",
        "大神ミオ":"https://holodex.net/statics/channelImg/UCp-5t9SrOQwXMU7iIjQfARg/100.png",
        "猫又おかゆ":"https://holodex.net/statics/channelImg/UCvaTdHTWBGv3MKj3KVqJVCw/100.png",
        #JP-2gen
        "湊あくあ":"https://holodex.net/statics/channelImg/UC1opHUrw8rvnsadT-iGp7Cg/100.png",
        "癒月ちょこ":"https://holodex.net/statics/channelImg/UC1suqwovbL1kzsoaZgFZLKg/100.png",
        "百鬼あやめ":"https://holodex.net/statics/channelImg/UC7fk0CB07ly8oSl0aqKkqFg/100.png",
        "大空スバル":"https://holodex.net/statics/channelImg/UCvzGlP9oQwU--Y0r9id_jnA/100.png",
        "紫咲シオン":"https://holodex.net/statics/channelImg/UCXTpFs_3PqI41qX2d9tL2Rw/100.png",
        #JP-3gen
        "兎田ぺこら":"https://holodex.net/statics/channelImg/UC1DCedRgGHBdm81E1llLhOQ/100.png",
        "宝鐘マリン":"https://holodex.net/statics/channelImg/UCCzUftO8KOVkV4wQG1vkUvg/100.png",
        "白銀ノエル":"https://holodex.net/statics/channelImg/UCdyqAaZDKHXg4Ahi7VENThQ/100.png",
        "不知火フレア":"https://holodex.net/statics/channelImg/UCvInZx9h3jC2JzsIzoOebWg/100.png",
        "潤羽るしあ":"https://holodex.net/statics/channelImg/UCl_gCybOJRIgOXw6Qb4qJzQ/100.png",
        #JP-4gen
        "常闇トワ":"https://holodex.net/statics/channelImg/UC1uv2Oq6kNxgATlCiez59hw/100.png",
        "姫森ルーナ":"https://holodex.net/statics/channelImg/UCa9Y57gfeY0Zro_noHRVrnw/100.png",
        "角巻わため":"https://holodex.net/statics/channelImg/UCqm3BQLlJfvkTsX_hvm0UmA/100.png",
        "天音かな":"https://holodex.net/statics/channelImg/UCZlDXzGoo7d44bwdNObFacg/100.png",
        "桐生ココ":"https://holodex.net/statics/channelImg/UCS9uQI-jC3DE0L4IpXyvr6w/100.png",
        #JP-5gen
        "桃鈴ねね":"https://holodex.net/statics/channelImg/UCAWSyEs_Io8MtpY3m-zqILA/100.png",
        "雪花ラミィ":"https://holodex.net/statics/channelImg/UCFKOVgVbGmX65RxO3EtH3iw/100.png",
        "尾丸ポルカ":"https://holodex.net/statics/channelImg/UCK9V2B22uJYu3N7eR_BT9QA/100.png",
        "獅白ぼたん":"https://holodex.net/statics/channelImg/UCUKD-uaobj9jiqB-VXt71mA/100.png",
        "魔乃アロエ":"https://holodex.net/statics/channelImg/UCgZuwn-O7Szh9cAgHqJ6vjw/100.png",
        #JP-HoloX
        "博衣こより":"https://holodex.net/statics/channelImg/UC6eWCld0KwmyHFbAqK3V-Rw/100.png",
        "ラプラス・ダークネス":"https://holodex.net/statics/channelImg/UCENwRMx5Yh42zWpzURebzTw/100.png",
        "沙花叉クロヱ":"https://holodex.net/statics/channelImg/UCIBY1ollUsauvVi4hW4cumw/100.png",
        "鷹嶺ルイ":"https://holodex.net/statics/channelImg/UCs9_O1tRPMQTHQ-N_L6FU2g/100.png",
        "風真いろは":"https://holodex.net/statics/channelImg/UC_vMYWcDjmfdpH6r4TTn1MQ/100.png",
        #REGLOSS
        "轟はじめ":"https://holodex.net/statics/channelImg/UC1iA6_NT4mtAcIII6ygrvCw/100.png",
        "儒烏風亭らでん":"https://holodex.net/statics/channelImg/UCdXAk5MpyLD8594lm_OvtGQ/100.png",
        "火威青":"https://holodex.net/statics/channelImg/UCMGfV7TVTmHhEErVJg1oHBQ/100.png",
        "一条莉々華":"https://holodex.net/statics/channelImg/UCtyWhCj3AqKh2dXctLkDtng/100.png",
        "音乃瀬奏":"https://holodex.net/statics/channelImg/UCWQtYtq9EOB4-I5P-3fh8lA/100.png",
        #EN-1gen
        "Takanashi Kiara":"https://holodex.net/statics/channelImg/UCHsx4Hqa-1ORjQTh9TYDhww/100.png",
        "Mori Calliope":"https://holodex.net/statics/channelImg/UCL_qhgtOy0dy1Agp8vkySQg/100.png",
        "Ninomae Ina'nis":"https://holodex.net/statics/channelImg/UCMwGHR0BTZuLsmjY_NT5Pwg/100.png",
        "Gawr Gura":"https://holodex.net/statics/channelImg/UCoSrY_IQQVpmIRZ9Xf-y93g/100.png",
        "Watson Amelia":"https://holodex.net/statics/channelImg/UCyl1z3jo3XHR1riLFKG5UAg/100.png",
        #EN-2gen
        "IRyS":"https://holodex.net/statics/channelImg/UC8rcEBzJSleTkf_-agPM20g/100.png",
        "Nanashi Mumei":"https://holodex.net/statics/channelImg/UC3n5uGu18FoCy23ggWWp8tA/100.png",
        "Hakos Baelz":"https://holodex.net/statics/channelImg/UCgmPnx-EEeOrZSg5Tiw7ZRQ/100.png",
        "Ouro Kronii":"https://holodex.net/statics/channelImg/UCmbs8T6MWqUHP1tIQvSgKrg/100.png",
        "Ceres Fauna":"https://holodex.net/statics/channelImg/UCmbs8T6MWqUHP1tIQvSgKrg/100.png",
        "Tsukumo Sana":"https://holodex.net/statics/channelImg/UCsUj0dszADCGbF3gNrQEuSQ/100.png",
        #EN-3gen
        "Koseki Bijou":"https://holodex.net/statics/channelImg/UC9p_lqQ0FEDz327Vgf5JwqA/100.png",
        "Shiori Novella":"https://holodex.net/statics/channelImg/UCgnfPPb9JI3e9A4cXHnWbyg/100.png",
        "Nerissa Ravencroft":"https://holodex.net/statics/channelImg/UC_sFNM0z0MWm9A6WlKPuMMg/100.png",
        "FuwawaMoco Abyssgard":"https://holodex.net/statics/channelImg/UCt9H_RpQzhxzlyBxFqrdHqA/100.png",
        #ID-1gen
        "Airani Iofifteen":"https://holodex.net/statics/channelImg/UCAoy6rzhSf4ydcYjJw3WoVg/100.png",
        "Ayunda Risu":"https://holodex.net/statics/channelImg/UCOyYb1c43VlX9rc_lT6NKQw/100.png",
        "Moona Hoshinova":"https://holodex.net/statics/channelImg/UCP0BspO_AMEe3aQqqpo89Dg/100.png",
        #ID-2gen
        "Anya Melfissa":"https://holodex.net/statics/channelImg/UC727SQYUvx5pDDGQpTICNWg/100.png",
        "Pavolia Reine":"https://holodex.net/statics/channelImg/UChgTyjG-pdNvxxhdsXfHQ5Q/100.png",
        "Kureiji Ollie":"https://holodex.net/statics/channelImg/UCYz_5n-uDuChHtLo7My1HnQ/100.png",
        #ID-3gen
        "Kobo Kanaeru":"https://holodex.net/statics/channelImg/UCjLEmnpCNeisMxy134KPwWw/100.png",
        "Vestia Zeta":"https://holodex.net/statics/channelImg/UCTvHWSfBZgtxE4sILOaurIQ/100.png",
        "Kaela Kovalskia":"https://holodex.net/statics/channelImg/UCZLZ8Jjx_RN2CXloOmgTHVg/100.png",
    }
load_draw_data()