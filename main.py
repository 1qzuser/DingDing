import http.client
import json

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

# 提取基金名字和今日涨幅
fund_names = []
day_growth_values = []

for fund in response_data.get("data", []):
    fund_name = fund.get("name", "数据没更新")
    day_growth = fund.get("dayGrowth", "数据没更新")
    fund_names.append(fund_name)
    day_growth_values.append(day_growth)

# 打印基金名字和今日涨幅
for i, fund_name in enumerate(fund_names):
    day_growth = day_growth_values[i]
    if day_growth == "0.00":
        print(f"基金名称: {fund_name} 今日涨幅: {day_growth}% 说实话不如买余额宝")
    elif day_growth.startswith("-"):  # 如果是负数，则表示亏损
        print(f"基金名称: {fund_name} 今日涨幅: {day_growth}% 跌{float(day_growth[1:]) * 100}个🥚噶牢弟 ^^_")
    else:
        print(f"基金名称: {fund_name} 今日涨幅: {day_growth}% 涨{float(day_growth) * 100}个🥚 爽！！！！ ")
