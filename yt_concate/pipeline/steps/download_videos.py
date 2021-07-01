import logging
from threading import Thread
import time

from pytube import YouTube

from yt_concate.pipeline.steps.step import Step
from yt_concate.settings import VIDEOS_DIR


class DownloadVideos(Step):
    def __init__(self):
        self.yt_set = None

    def process(self, data, inputs, utils):
        start = time.time()

        logger = logging.getLogger(f'main.{__name__}.process')
        logger.info('in DownloadVideos')
        yt_set = set([found.yt for found in data])
        self.yt_set = yt_set

        threads = []
        for _ in range(4):
            threads.append(Thread(target=self.download, args=[utils]))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        end = time.time()
        print(f'Total download videos time：{end - start} seconds')
        return data

    def download(self, utils):
        logger = logging.getLogger(f'main.{__name__}.download')
        while self.yt_set:
            yt = self.yt_set.pop()
            url = yt.url

            if utils.video_file_exists(yt):
                logger.info(f'found existing video file for ' + url + ', skipping')
                continue

            logger.info('downloading video for ' + url)
            YouTube(url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id)
        print('thread finished')
