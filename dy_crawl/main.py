import time

from dy_crawl.concat import concat_mp4
from dy_crawl.crawl import DouYinDownloader
from dy_crawl.input_urls import urls

if __name__ == '__main__':

    for url in urls:
        dy = DouYinDownloader(share_url=url)
        dy.run()
        time.sleep(5)
    concat_mp4()
