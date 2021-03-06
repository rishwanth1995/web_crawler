import requests
from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import sys
import validators
 
 
class WebCrawler:
 
    def __init__(self, base_url):
 
        self.base_url = base_url
        self.root_url = '{}://{}'.format(urlparse(self.base_url).scheme, urlparse(self.base_url).netloc)
        self.threadPool = ThreadPoolExecutor(max_workers=16)
        self.visited_url = set([])
        self.unvisited_url = Queue()
        self.unvisited_url.put(self.base_url)
 
    def parse_html(self, html):
        # background  thread
        if html is None:
            return
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            url = link['href']
            if url.startswith('/'):
                url = urljoin(self.root_url, url)
                if url not in self.visited_url:
                    self.unvisited_url.put(url)
            else:
                if url not in self.visited_url:
                    self.unvisited_url.put(url)
 
 
    def post_fetch(self, res):
        #  background thread
        result = res.result()
        if result and result.status_code == 200:
            self.parse_html(result.text)
 
    def fetch(self, url):
        #  background thread
        try:
            res = requests.get(url, timeout=(3, 30))
            return res
        except requests.RequestException:
            return
 
    def run_crawler(self):
        while True:
            # main thread
            try:
                target_url = self.unvisited_url.get(timeout=10)
                if target_url not in self.visited_url:
                    print(target_url)
                    self.visited_url.add(target_url)
                    job = self.threadPool.submit(self.fetch, target_url)
                    job.add_done_callback(self.post_fetch)
            except Empty:
                return
            except Exception as e:
                print(e)
                continue

def main(arguments):
    if len(arguments) != 2:
        print("Expecting 1 argument, enter website url to crawl")
        return
    url = arguments[1]
    valid=validators.url(url)
    if valid != True:
        print("Invalid url")
        return
    webCrawler = WebCrawler(url)
    webCrawler.run_crawler()
    
if __name__ == '__main__':
    main(sys.argv)
