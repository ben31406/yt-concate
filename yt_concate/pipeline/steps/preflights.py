from yt_concate.pipeline.steps.step import Step
import logging


class Preflight(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger(f'main.{__name__}')
        logger.info('in Preflights')
        utils.create_dirs()
