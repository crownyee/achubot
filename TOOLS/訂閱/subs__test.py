from selenium.webdriver import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

#desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
#desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
#driver = webdriver.PhantomJS(executable_path='./test/phantomjs', desired_capabilities=desired_capabilities)
#options.chrome_executable_path = "C:/Users/chue0/AppData/Local/Programs/Python/Python39/chromedriver.exe"
#prefs = {"profile.default_content_setting_values.notifications": 2}
#options.add_experimental_option("prefs", prefs)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
time.sleep(0.2)

# 想爬取的youtube
youtuber = ['channel/UCt9H_RpQzhxzlyBxFqrdHqA' #FUWAMOCO
            ]
# 準備容器
subscription = []


driver.get('https://www.youtube.com/channel/UCt9H_RpQzhxzlyBxFqrdHqA/about')
getSubscription = driver.find_element_by_id('subscriber-count').text
getSubscription = getSubscription.replace('萬位訂閱者','')

print(eval(getSubscription))
