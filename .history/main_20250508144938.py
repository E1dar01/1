import aiohttp
import asyncio
from bs4 import BeautifulSoup

# Список URL-ов для скрапинга
urls = [
    'https://example.com/news1',
    'https://example.com/news2',
    'https://example.com/news3',
]

# Функция для асинхронного запроса и парсинга HTML
async def fetch_page(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()  # Проверка на ошибки
            html = await response.text()
            return html
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")
        return None

# Функция для извлечения заголовков с HTML
def parse_headlines(html):
    soup = BeautifulSoup(html, 'html.parser')
    headlines = []

    # Пример: ищем заголовки в теге <h2> с классом 'news-title'
    for headline in soup.find_all('h2', class_='news-title'):
        headlines.append(headline.get_text().strip())
    
    return headlines

# Асинхронная функция для обработки нескольких страниц
async def scrape_headlines(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch_page(session, url))
        
        html_responses = await asyncio.gather(*tasks)
        all_headlines = []
        
        for html in html_responses:
            if html:
                headlines = parse_headlines(html)
                all_headlines.extend(headlines)

        return all_headlines

# Функция для сохранения заголовков в файл
def save_headlines_to_file(headlines):
    with open('headlines.txt', 'w') as file:
        for headline in headlines:
            file.write(headline + '\n')

# Основная функция для запуска
async def main():
    headlines = await scrape_headlines(urls)
    save_headlines_to_file(headlines)
    print(f"Заголовки новостей сохранены в файл 'headlines.txt'.")

# Запуск программы
if __name__ == "__main__":
    asyncio.run(main())


