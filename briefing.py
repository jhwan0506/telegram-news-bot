"""
매일 아침 크립토 / 빅테크 / 거시경제 뉴스를 RSS로 모아서
텔레그램으로 브리핑 메시지를 보내는 스크립트.

필요한 환경변수 (GitHub Actions Secrets에 등록):
- TELEGRAM_BOT_TOKEN : BotFather에게 받은 봇 토큰
- TELEGRAM_CHAT_ID   : 메시지를 받을 채팅방 ID (본인 개인 챗 or 그룹)
"""

import os
from datetime import datetime

import feedparser
import requests

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# 카테고리별 RSS 피드. 필요하면 여기 URL만 추가/삭제하면 됩니다.
FEEDS = {
    "🪙 크립토": [
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://cointelegraph.com/rss",
    ],
    "💻 빅테크": [
        "https://techcrunch.com/feed/",
        "https://www.theverge.com/rss/index.xml",
    ],
    "📊 거시경제": [
        "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    ],
}

MAX_PER_CATEGORY = 4  # 카테고리당 최대 헤드라인 개수


def fetch_headlines(urls, max_items):
    headlines = []
    for url in urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:max_items]:
                headlines.append((entry.title, entry.link))
        except Exception:
            # 특정 피드가 일시적으로 죽어있어도 나머지는 계속 진행
            continue
    return headlines[:max_items]


def build_message():
    today = datetime.now().strftime("%Y년 %m월 %d일")
    lines = [f"📰 {today} 데일리 브리핑"]

    for category, urls in FEEDS.items():
        lines.append(f"\n{category}")
        headlines = fetch_headlines(urls, MAX_PER_CATEGORY)
        if not headlines:
            lines.append("• (오늘은 가져올 소식이 없음)")
            continue
        for title, link in headlines:
            lines.append(f"• {title}")
            lines.append(f"  {link}")

    return "\n".join(lines)


def send_telegram_message(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    # 텔레그램 메시지 길이 제한(4096자) 대비 안전하게 자르기
    if len(text) > 3900:
        text = text[:3900] + "\n\n...(내용 생략)"

    resp = requests.post(
        url,
        data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "disable_web_page_preview": True,
        },
        timeout=15,
    )
    resp.raise_for_status()


if __name__ == "__main__":
    message = build_message()
    send_telegram_message(message)
    print("브리핑 전송 완료")
