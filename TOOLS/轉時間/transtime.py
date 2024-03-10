import time
from datetime import datetime, timedelta

def pst_to_cst(pst_time):
    # 設定PST的時區
    pst_offset = timedelta(hours=-8)
    # 設定Taipei的時區
    tpi_offset = timedelta(hours=+8)
    
    # 解析輸入的PST時間
    pst_datetime = datetime.strptime(pst_time, "%m-%d %H:%M")
    # 將PST時間轉換為UTC時間
    utc_datetime = pst_datetime - pst_offset
    # 將UTC時間轉換為TST時間
    cst_datetime = utc_datetime + tpi_offset
    
    # 格式化TST時間
    tpi_time = cst_datetime.strftime("%m-%d %H:%M")
    
    return tpi_time

# 測試程式碼
#pst_time = ["8-7 8:00","8-7 18:00","8-8 16:00","8-9 08:00",
#            "8-9 18:00","8-10 18:00","8-11 08:00","8-11 18:00","8-12 13:00","8-12 18:00","8-13 13:00"]

with open('./TOOLS/轉時間/PT.txt', 'r') as file:
    # 读取文件内容
    contents = file.read()

pst_time = [line.strip() for line in contents.split(',')]
print(pst_time)
temp_time = []
for i in pst_time:
    time = pst_to_cst(i)
    temp_time.append(time)

tpi_times = ['2024-' + date for date in temp_time]

import time
final_stamp = []
for i in tpi_times:
    struct_time = time.strptime(i, "%Y-%m-%d %H:%M") # 轉成時間元組
    time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
    final_stamp.append(time_stamp)


formatted_dates = [f"<t:{timestamp}:F>" for timestamp in final_stamp]

earliest_date = pst_time[0].split()[0]
latest_date = (datetime.strptime(pst_time[-1].split()[0], "%m-%d") + timedelta(days=1)).strftime("%m-%d")

with open("./TOOLS/轉時間/周表.txt",'w',encoding='utf-8') as file:
    file.write(f":other_0_blueheart: :4a_pad2: SCHEDULE {earliest_date} ~ {latest_date} :4a_pad2: :other_0_pinkheart:\n")
    for i, date in enumerate(formatted_dates):
        line = f"### **【text】**{date}"
        file.write(line + "\n")