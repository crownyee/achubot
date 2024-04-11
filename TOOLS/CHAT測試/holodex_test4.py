import asyncio
from holodex.client import HolodexClient
import pytchat, datetime
from emoji import emojize



async def main():
    async with HolodexClient() as client:
        client = HolodexClient('df1fab08-008b-42cf-8620-4a8776e9dd0d')
        #search = await client.autocomplete("ときのそら")
        #channel_id = search.contents[0].value
        channel =  await client.channel(channel_id='UCt9H_RpQzhxzlyBxFqrdHqA')
        print(channel.subscriber_count)
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