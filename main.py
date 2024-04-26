import http.client
import json
import requests
import datetime

# 钉钉webhook URL，直接硬编码
DINGTALK_WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=68af6ef5d26f1338bf529e20b641c93b645b8034e3a5e69e4a00152c4010f8ac"

# 获取基金数据
conn = http.client.HTTPSConnection("api.autostock.cn")
payload = ''
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
}
conn.request("GET", "/v1/fund?code=018978&code=004156", payload, headers)
res = conn.getresponse()
data = res.read()

# 解析JSON数据
response_data = json.loads(data.decode("utf-8"))

# 获取当前时间戳
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 提取基金名字和今日涨幅
fund_names = []
day_growth_values = []

for fund in response_data.get("data", []):
    fund_name = fund.get("name", "数据没更新")
    day_growth = fund.get("dayGrowth", "数据没更新")
    fund_names.append(fund_name)
    day_growth_values.append(day_growth)

# 构造推送消息
messages = []
for i, fund_name in enumerate(fund_names):
    day_growth = day_growth_values[i]
    if day_growth == "0.00":
        message = f"{fund_name} +{now}\n今日涨幅: {day_growth}% 说实话不如买余额宝"
    elif day_growth.startswith("-"):  # 如果是负数，则表示亏损
        message = f"{fund_name} +{now}\n今日涨幅: {day_growth}% 跌{float(day_growth[1:]) * 100}个🥚噶牢弟 ^^_"
    else:
        message = f"{fund_name} +{now}\n今日涨幅: {day_growth}% 涨{float(day_growth) * 100}个🥚 爽！！！"
    messages.append(message)

# 发送推送
if DINGTALK_WEBHOOK_URL:
    # 构造钉钉消息
    dingtalk_message = {
        "msgtype": "text",
        "text": {
            "content": "\n\n".join(messages)
        }
    }
    # 发送消息
    response = requests.post(url=DINGTALK_WEBHOOK_URL, json=dingtalk_message)
    print(response.text)

# 打印消息内容
print("\n\n".join(messages))
