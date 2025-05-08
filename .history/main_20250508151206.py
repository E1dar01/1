import asyncio
import aiohttp
from bs4 import BeautifulSoup

urls = [
    'https://news.ycombinator.com',
    'https://www.bbc.com/news/technology',
    'https://news.ycombinator.com/news?p=3',
]

async def fetch(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        print(f"❌ Ошибка при загрузке {url}: {e}")
        return ""

def extract_headlines(html):
    soup = BeautifulSoup(html, 'html.parser')
    headlines = []

    for tag in soup.select('.titleline > a'):
        headlines.append(tag.get_text(strip=True))

    return headlines

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        pages = await asyncio.gather(*tasks)

        all_headlines = []
        for html in pages:
            if html:
                all_headlines.extend(extract_headlines(html))

        all_headlines = list(set(all_headlines))

        with open('headlines.txt', 'w', encoding='utf-8') as f:
            for h in all_headlines:
                f.write(h + '\n')

        print(f"✅ Сохранено {len(all_headlines)} заголовков в headlines.txt")

asyncio.run(main())
