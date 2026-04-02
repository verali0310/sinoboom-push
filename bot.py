import feedparser
import requests
import json
import os

# 配置你要监控的4个社媒账号
FEEDS = [
    {
        "name": "微信公众号",
        "icon": "📱",
        "url": "https://rsshub.app/wechat/mp/星邦智能SINOBOOM"
    },
    {
        "name": "LinkedIn",
        "icon": "🌍",
        "url": "https://rsshub.app/linkedin/company/sinoboom-intelligent-equipment"
    },
    {
        "name": "抖音",
        "icon": "🎵",
        "url": "https://rsshub.app/douyin/user/星邦智能"
    },
    {
        "name": "视频号",
        "icon": "📺",
        "url": "https://rsshub.app/wechat/channels/星邦智能"
    }
]

# 读取已发送过的链接，避免重复推送
def get_sent():
    try:
        with open("sent.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_sent(sent):
    with open("sent.json", "w", encoding="utf-8") as f:
        json.dump(sent, f, ensure_ascii=False)

# 发送消息到企业微信群
def push(title, link, name, icon, date):
    webhook = os.getenv("WEBHOOK_URL")
    msg = f"""【星邦智能·新内容发布】
{icon} {name}
🔖 标题：{title}
🔗 链接：{link}
⏰ 发布时间：{date}

—— 自动监控 · 实时推送 ——"""

    data = {
        "msgtype": "text",
        "text": {"content": msg}
    }
    try:
        requests.post(webhook, json=data, timeout=10)
    except Exception as e:
        print(f"推送失败：{e}")

# 主逻辑：抓取RSS+去重+推送
def main():
    sent = get_sent()
    new_sent = sent.copy()

    for feed in FEEDS:
        try:
            # 解析RSS内容
            d = feedparser.parse(feed["url"])
            if not d.entries:
                continue
            # 取最新1条内容
            item = d.entries[0]
            title = item.get("title", "")
            link = item.get("link", "")
            date = item.get("pubDate", "")[:25]

            # 去重判断：只推送没发过的新内容
            if link and link not in sent:
                push(title, link, feed["name"], feed["icon"], date)
                new_sent.append(link)
        except Exception as e:
            print(f"监控{feed['name']}出错：{e}")

    # 保存已推送链接，下次轮询用
    save_sent(new_sent)

if __name__ == "__main__":
    main()
