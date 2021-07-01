import logging

from yt_concate.pipeline.steps.step import Step
from yt_concate.model.yt import YT


class InitializeYT(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger(f'main.{__name__}')
        logger.info('in InitializeYT')
        return [YT(url) for url in data]
