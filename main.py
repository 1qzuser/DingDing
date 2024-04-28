import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# 基金网站的URL
fund_codes = ['018978', '004156']  # 添加需要查询的基金代码
messages = []

def get_latest_trading_day_data(data_rows, current_date):
    """
    Get the latest trading day's data from the data rows.

    Args:
    - data_rows (list): List of BeautifulSoup <tr> elements containing the data.
    - current_date (str): The current date in 'm-d' format.

    Returns:
    - str: The message containing the latest trading day's data or a message indicating no data found.
    """
    # Initialize a dictionary to map month-day to the corresponding row
    date_to_row = {row.find('td', class_='alignLeft').text.strip(): row for row in data_rows[1:] if row.find('td', class_='alignLeft')}

    # Get today's date object
    today = datetime.strptime(current_date, '%m-%d')

    # Initialize the message
    message = "数据未更新，且未找到昨天的数据。"

    # Loop through the previous days until we find a trading day's data
    for i in range(1, 10):  # Limiting the search to the last 10 days for practical purposes
        # Calculate the date for the previous day
        previous_day = today - timedelta(days=i)

        # Format the previous day to 'm-d' format
        previous_day_str = previous_day.strftime('%m-%d')

        # Check if the previous day is a weekend and skip if it is
        if previous_day.weekday() >= 5:  # 5 and 6 correspond to Saturday and Sunday
            continue

        # Check if the previous day's data exists
        if previous_day_str in date_to_row:
            # Get the row for the previous day
            row = date_to_row[previous_day_str]

            # Extract the rate from the row
            rate_element = row.find('td', class_='RelatedInfo alignRight10 bold')
            rate = rate_element.span.text.strip() if rate_element and rate_element.span else "数据未找到"

            # Update the message
            message = f"数据未更新，显示{previous_day_str}的数据：收益率: {rate}"
            break

    return message

for fund_code in fund_codes:
    url = f'https://fund.eastmoney.com/{fund_code}.html?spm=search'

    # 发送GET请求
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到标题元素
        title_element = soup.find('title')

        # 提取标题并指定编码为UTF-8
        title = title_element.text.encode('iso-8859-1').decode('utf-8') if title_element else "Title not found"

        # 提取基金名称部分
        fund_name = title.split('(')[0].strip()

        # 输出基金名称部分和当前时间
        current_time = datetime.now().strftime('%H:%M:%S')
        messages.append(f"基金名称: {fund_name} | 运行时间: {current_time}")

        # 找到包含时间和收益率的<tr>元素
        data_rows = soup.find_all('tr')

        # 获取当前日期
        current_date = datetime.now().strftime('%m-%d')

        # 获取最近一个交易日的数据
        message = get_latest_trading_day_data(data_rows, current_date)
        messages.append(message)

# 加入钉钉推送：
DINGTALK_WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=68af6ef5d26f1338bf529e20b641c93b645b8034e3a5e69e4a00152c4010f8ac"

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
