import json

def load_draw_data():
    with open('./json/mydraw.json', 'r', encoding='utf8') as jfile:
        jdata = json.load(jfile)

    global rec_id, rec_emoji, DRAW_channel, emoji_name
    global FWMC_LUCKY, MID_LUCKY, SMALL_LUCKY, LUCKY, LAST_LUCKY, BAD,PERO_draw
    global FWMC_LUCKY_ID, MID_LUCKY_ID, SMALL_LUCKY_ID, LUCKY_ID, LAST_LUCKY_ID, BAD_ID
    global LUCKY_ROLES,LUCKY_ROLES_IDS
    global luck_colors, luck_data
    rec_id = int(jdata['Reaction_msg'])
    rec_emoji = jdata['Reaction_emoji']
    DRAW_channel = int(jdata["DRAW_Channel"])
    
    split_parts = rec_emoji.strip("<:>").split(":")
    emoji_name = split_parts[1]  # 這裡我們取得是表情的名稱作為 emoji_name
    
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

load_draw_data()