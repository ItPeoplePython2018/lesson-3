import bs4
import requests


def get_links(url):
    """
    Получает список ссылок на страницы по заданном URL в википедии
    """
    # Получаем текст страницы
    resp = requests.get(url)

    # Парсим HTML разметку
    soup = bs4.BeautifulSoup(resp.text, "html.parser")

    # Получаем заголовок
    heading = soup.find(id='firstHeading')
    print(heading.text)

    # Получаем контент страницы
    content = soup.find(id='mw-content-text')

    # Получаем ссылки из контента страницы
    def find_good_links(tag):
        if tag.name != 'a':
            return False
        if not tag.has_attr('href'):
            return False
        if not tag['href'].startswith('/wiki'):
            return False
        if ':' in tag['href']:
            return False
        return True

    all_a = set()
    for tag in content.find_all(find_good_links):
        href = 'https://en.wikipedia.org{}'.format(tag['href'])
        all_a.add(href)

    return all_a


def crawl(url, limit=100):
    """
    Обходит страницы по очереди, получая новый список URL с каждой страницы
    """

    urls = [url]
    while urls and limit:
        limit -= 1
        url = urls.pop(0)
        print(url)
        links = get_links(url)
        urls.extend(links)


crawl('https://en.wikipedia.org/wiki/George_Pfister')
