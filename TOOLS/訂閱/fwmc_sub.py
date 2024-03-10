import discord
from discord.ext import commands
from core.__init__ import Cog_Extension
import asyncio
import json,asyncio

with open('./json/setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)
CHANNEL_ID = jdata['FWMC']
CHANNELSUBS = jdata['SUBs_Channel']  

from selenium.webdriver import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


#desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
#desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
#driver = webdriver.PhantomJS(executable_path='./json/phantomjs', desired_capabilities=desired_capabilities)
#prefs = {"profile.default_content_setting_values.notifications": 2}
options = webdriver.ChromeOptions()
#options.add_experimental_option("prefs", prefs)
options.chrome_executable_path = "./cmds/chromedriver.exe"
options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

last_subs = '0'
driver.get('https://www.youtube.com/channel/UCt9H_RpQzhxzlyBxFqrdHqA/about')


class FWMCsub(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        async def fwmcsub():
            await self.bot.wait_until_ready()

            while not self.bot.is_closed():
                driver.get('https://www.youtube.com/channel/UCt9H_RpQzhxzlyBxFqrdHqA/about')
                getSubscription = driver.find_element_by_id('subscriber-count').text
                getSubscription = getSubscription.replace('萬位訂閱者','')
                global last_subs

                if eval(getSubscription) - eval(last_subs) > 0:
                    self.channel = self.bot.get_channel(int(CHANNELSUBS))
                    await self.channel.send(f'FUWAMOCO訂閱更新: {getSubscription}萬')
                    if self.channel:
                        numbers = getSubscription.split('.')
                        d = "․"
                        last_subs = getSubscription
                        await self.channel.edit(name=f"fuwamoco訂閱-{numbers[0] + d + numbers[1]}萬")
                        await asyncio.sleep(5)
    

                await asyncio.sleep(120)
        
        self.bg_subs = self.bot.loop.create_task(fwmcsub())

async def setup(bot):
    await bot.add_cog(FWMCsub(bot))