import sys
import logging

from yt_concate.pipeline.steps.step import Step
from yt_concate.model.found import Found


class Search(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger(f'main.{__name__}')
        logger.info('in Search')
        search_word = inputs['search_word']

        found = []
        for yt in data:
            captions = yt.captions
            if not captions:
                continue
            for caption in captions:
                if search_word.lower() in caption.lower():
                    time = captions[caption]
                    found.append(Found(yt, caption, time))

        logger.info(f'Found ' + str(len(found)) + ' times of keyword in channel')
        if not found:
            sys.exit(0)
        return found
