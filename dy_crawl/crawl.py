# coding=utf-8
import glob
import os
import sys
import time
from contextlib import closing
from urllib.parse import urlparse

import requests
import urllib3
from bs4 import BeautifulSoup

from dy_crawl.settings import Config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if not os.path.exists(Config.OUTPUT_PATH):
    os.makedirs(Config.OUTPUT_PATH)


class DouYinDownloader(object):
    def __init__(self, share_url):
        if not share_url:
            raise ImportError("Url can't be empty")
        self.share_url = share_url

    def get_video_location(self):
        response = requests.get(self.share_url, headers=Config.HEADERS, allow_redirects=False)
        if 'Location' in response.headers.keys():
            return response.headers['Location']
        else:
            return self.share_url

    def is_duplicated(self, filename):
        mp4s = glob.glob(os.path.join(Config.OUTPUT_PATH, "*.mp4"))
        return True if filename in mp4s else False

    def download(self, url):
        response = requests.get(url, headers=Config.HEADERS)
        bf = BeautifulSoup(response.text, 'lxml')
        video = bf.find_all('video')
        video_url = video[0].get('src').replace('playwm', 'play')

        print('[INFO]: Downloading from url: ' + str(video_url))

        response = requests.get(video_url, headers=Config.HEADERS, allow_redirects=False)
        print('[INFO]: Response headers are ' + str(response.headers.keys()))

        inputs = bf.find_all('input')
        video_name = time.time()

        for item in inputs:
            temp = item.get('name')
            if temp == 'shareDesc':
                video_name = item.get('value')
                break

        size = 0
        chunk_size = 1024
        with closing(requests.get(video_url, headers=Config.HEADERS, stream=True, verify=False)) as response:

            content_size = int(response.headers['content-length'])

            if response.status_code == 200:
                print('[INFO]: File Size is :%0.2f MB %s \n' % (content_size / chunk_size / 1024, video_name + '.mp4'))
                # check dup
                filename = os.path.join(Config.OUTPUT_PATH, video_name + '.mp4')
                if self.is_duplicated(filename):
                    print(f'[INFO]: File {filename} is duplicated.')
                else:
                    with open(filename, 'wb') as file:
                        for data in response.iter_content(chunk_size=chunk_size):
                            file.write(data)
                            size += len(data)
                            file.flush()
                            sys.stdout.write('[INFO]: Downloading: %.2f%% %s' % (
                                float(size / content_size * 100), video_name + '.mp4 \r'))
                            sys.stdout.flush()
                    sys.stdout.write('\n')

    def run(self):

        self.share_url = self.get_video_location()
        share_url_parse = urlparse(self.share_url)

        # if not share_url_parse.scheme in ['http', 'https'] or not share_url_parse.netloc in Config.DOMAINS:
        #     return self.run()

        html_url = share_url_parse.scheme + "://" + share_url_parse.netloc + \
                   share_url_parse.path + "?" + share_url_parse.query

        self.download(html_url)
