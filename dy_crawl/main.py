from dy_crawl.crawl import DouYinDownloader
from dy_crawl.input_urls import urls

if __name__ == '__main__':

    for url in urls:
        dy = DouYinDownloader(share_url=url)
        dy.run()