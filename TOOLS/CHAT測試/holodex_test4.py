import asyncio
from holodex.client import HolodexClient
import pytchat, datetime
from emoji import emojize



async def main():
    async with HolodexClient() as client:
        client = HolodexClient('df1fab08-008b-42cf-8620-4a8776e9dd0d')

        ID = {
        #JP-staff
        "友人A":"",
        "春先のどか":"",
        "YAGOO":":",
        #JP-0gen
        "ときのそら":"",
        "ロボ子":"",
        "星街すいせい":"",
        "さくらみこ":"",
        "AZKi":"",
        #JP-1gen
        "赤井はあと":"",
        "夜空メル":"",
        "白上フブキ":"",
        "アキ・ローゼンター":"",
        "夏色まつり":"",
        #JP-Ggen
        "戌神ころね":"",
        "大神ミオ":"",
        "猫又おかゆ":"",
        #JP-2gen
        "湊あくあ":"",
        "癒月ちょこ":"",
        "百鬼あやめ":"",
        "大空スバル":"",
        "紫咲シオン":"",
        #JP-3gen
        "兎田ぺこら":"",
        "宝鐘マリン":"",
        "白銀ノエル":"",
        "不知火フレア":"",
        "潤羽るしあ":"",
        #JP-4gen
        "常闇トワ":"",
        "姫森ルーナ":"",
        "角巻わため":"",
        "天音かな":"",
        "桐生ココ":"",
        #JP-5gen
        "桃鈴ねね":"",
        "雪花ラミィ":"",
        "尾丸ポルカ":"",
        "獅白ぼたん":"",
        "魔乃アロエ":"",
        #JP-HoloX
        "博衣こより":"",
        "ラプラス・ダークネス":"",
        "沙花叉クロヱ":"",
        "鷹嶺ルイ":"",
        "風真いろは":"",
        #REGLOSS
        "轟はじめ":"",
        "儒烏風亭らでん":"",
        "火威青":"",
        "一条莉々華":"",
        "音乃瀬奏":"",
        #EN-1gen
        "Takanashi Kiara":"",
        "Mori Calliope":"",
        "Ninomae Ina'nis":"",
        "Gawr Gura":"",
        "Watson Amelia":"",
        #EN-2gen
        "IRyS":"",
        "Nanashi Mumei":"",
        "Hakos Baelz":"",
        "Ouro Kronii":"",
        "Ceres Fauna":"",
        "Tsukumo Sana":"",
        #EN-3gen
        "Koseki Bijou":"",
        "Shiori Novella":"",
        "Nerissa Ravencroft":"",
        "FuwawaMoco Abyssgard":"",
        #ID-1gen
        "Airani Iofifteen":"",
        "Ayunda Risu":"",
        "Moona Hoshinova":"",
        #ID-2gen
        "Anya Melfissa":"",
        "Pavolia Reine":"",
        "Kureiji Ollie":"",
        #ID-3gen
        "Kobo Kanaeru":"",
        "Vestia Zeta":"",
        "Kaela Kovalskia":"",
        }
        search = await client.autocomplete("ときのそら")
        channel_id = search.contents[0].value
        channel =  await client.channel(channel_id=channel_id)
        print(channel.photo)
        #print(fwmc_status)
        #print(fwmc_id)
        #print(live_time)
        #print(fwmc_type)

    await client.close()
 


asyncio.run(main())


'''
        #search = await client.autocomplete("Sora")
        channel_id = search.contents[0].value
        fwmc_live = await client.live_streams(channel_id=channel_id)
        fwmc_status = fwmc_live.contents[0].status
        fwmc_id = fwmc_live.contents[0].id
        live_time = fwmc_live.contents[0].start_scheduled
        fwmc_type = fwmc_live.contents[0].type

        arr = []
        
        holo_channel = await client.live_streams(org='Hololive',lang='all',status='live')
        for index in range(len(holo_channel.contents)):
            if holo_channel.contents[index].channel.org == 'Hololive':
                arr.append(holo_channel.contents[index].id)
        print(arr)
        #print(holo_channel.contents)
'''

'''
        search = await client.autocomplete("UC9V3Y3_uzU5e-usObb6IE1w")
        channel_id = search.contents[0].value
        print(channel_id)

        channel = await client.channel(channel_id)
        print(channel.name)
        print(channel.subscriber_count)
'''


'''
        live_search = await client.live_streams(channel_id=channel_id)
        print(live_search.contents[0].id)
        print(live_search.contents[0].status)
        print(live_search.contents[0].live_viewers)
        arr.append(live_search.contents[0].live_tl_count)
'''

'''
        client = HolodexClient('533d4a71-c7e4-4b75-ba49-f0f9c2808ad2')
        search = await client.autocomplete("Bijou")
        channel_id = search.contents[0].value
        live_search = await client.live_streams(channel_id=channel_id)

        print(live_search.contents[0].id)
        timestamp = live_search.contents[0].start_scheduled
        utc_time = datetime.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        cst_time = utc_time + datetime.timedelta(hours=8)
        print(cst_time.strftime)

'''