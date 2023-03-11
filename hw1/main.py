import os
import bs4
import requests
import config

def getLinks():
    links = []
    for i in range(1, config.HABR_PAGE_COUNT + 1):
        url = f'https://habr.com/ru/all/page{i}/'
        soup = bs4.BeautifulSoup(requests.get(url).text, features="lxml")
        for data in soup.select("a.tm-article-snippet__title-link"):
            links.append('https://habr.com' + data['href'])
    return links
    


if __name__ == '__main__':
    links = getLinks()
    index_file = open('index.txt', "w", encoding="utf-8")
    os.makedirs(os.path.dirname(f'{config.FOLDER}/'), exist_ok=True)
    for i, link in enumerate(links):
        html = bs4.BeautifulSoup(requests.get(link).text, features="lxml")
        for data in html(config.TAGS):
            data.decompose()
        index_file.write(f"{str(i)}\t{link}\n")
        with open(f"{config.FOLDER}/{str(i)}.html", "w", encoding="utf-8") as html_file:
            html_file.write(str(html))
    index_file.close()