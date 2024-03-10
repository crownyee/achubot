from googleapiclient.discovery import build

# 设置 YouTube API 密钥
api_key = 'AIzaSyB_H2kC6dbWDBov2Acq1bEmRLFMufOmxCw'

# 创建 YouTube 数据 API 客户端
youtube = build('youtube', 'v3', developerKey=api_key)

def get_channel_subscriber_count(channel_id):
    # 获取频道的订阅数量
    request = youtube.channels().list(
        part='statistics',
        id=channel_id
    )
    response = request.execute()

    # 提取订阅数量
    subscriber_count = response['items'][0]['statistics']['subscriberCount']
    return subscriber_count

# 指定频道的 ID
channel_id = 'UCt9H_RpQzhxzlyBxFqrdHqA'

# 获取频道的订阅数量
subscriber_count = get_channel_subscriber_count(channel_id)
print(f'频道的订阅数量：{subscriber_count}')