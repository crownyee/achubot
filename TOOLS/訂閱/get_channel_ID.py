from googleapiclient.discovery import build

# 輸入您的API金鑰
API_KEY = 'AIzaSyB_H2kC6dbWDBov2Acq1bEmRLFMufOmxCw'

# 要搜索的頻道名稱
CHANNEL_NAME = 'AkaiHaato'

# 建立YouTube API客戶端
youtube = build('youtube', 'v3', developerKey=API_KEY)

# 使用search().list方法搜索頻道
request = youtube.search().list(part='id', q=CHANNEL_NAME, type='channel')
response = request.execute()

# 從回應中提取第一個頻道的ID
channel_id = response['items'][0]['id']['channelId']

# 輸出頻道ID
print(f'頻道ID: {channel_id}')