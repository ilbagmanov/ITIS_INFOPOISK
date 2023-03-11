import os
import bs4
import requests
import config

def getLinks():
    links = []
    for i in range(1, config.HABR_PAGE_COUNT + 1):
        url = f'https://habr.com/ru/all/page{i}/'
        soup = bs4.BeautifulSoup(requests.get(url).text, features="lxml")
        for item in soup.select("a.tm-article-snippet__title-link"):
            links.append('https://habr.com' + item['href'])
    return links
    


if __name__ == '__main__':
    links = getLinks()
    index_file = open('index.txt', "w", encoding="utf-8")
    os.makedirs(os.path.dirname('Выкачка/'), exist_ok=True)
    for i, link in enumerate(links):
        soup = bs4.BeautifulSoup(requests.get(link).text, features="lxml")
        for data in soup(['style', 'script', 'meta', 'link', 'code']):
            data.decompose()
        html_of_url = str(soup)
        filename = f'{i}'
        index_file.write(f"{filename}\t{link}\n")
        path_result = f"Выкачка/{filename}.html"
        with open(path_result, "w", encoding="utf-8") as html_file:
            html_file.write(html_of_url)
    index_file.close()