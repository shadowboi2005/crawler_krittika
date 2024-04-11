import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls
        self.pdf_links = []
        self.img_links=[]

    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path
        for link in soup.find_all('img'):
            path = link.get('src')
            if path and path.startswith('/'):
                path = urljoin(url,path)
            if path not in self.img_links:
                self.img_links.append(path)
    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            if(url[0:4]=='http' and url[-4:-1] != ".pd"):
                self.add_url_to_visit(url)
            if(url[-4:-1] == ".pd"):
                if url not in self.pdf_links:
                    self.pdf_links.append(url)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            self.visited_urls.append(url)
            try:
                if("krittikaiitb.github.io" in url):
                    self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')

        print("<----collected urls---->")
        count = 0
        for j in self.visited_urls:
            count += 1
            print(f'{count}){j}')
        print("<----collected pdfs---->")
        count= 0
        for i in self.pdf_links:
            count += 1
            print(f"{count}){i}")
        print("<----collected image links---->")
        count =0 
        for k in self.img_links:
            count+=1
            print(f'{count}){k}')

if __name__ == '__main__':
    url = 'https://krittikaiitb.github.io/'
    Crawler(urls=[url]).run()