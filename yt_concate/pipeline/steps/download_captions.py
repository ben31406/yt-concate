import logging

from pytube import YouTube

from yt_concate.pipeline.steps.step import Step
from yt_concate.pipeline.steps.step import StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger(f'main.{__name__}')
        logger.info('in DownloadCaptions')
        for yt in data:
            if utils.caption_file_exists(yt):
                logger.info('found existing caption file for ' + yt.id)
                continue
            logger.info('downloading caption for ' + yt.id)
            try:
                source = YouTube(yt.url)
                en_caption = source.captions.get_by_language_code('a.en')
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            except (KeyError, AttributeError):
                logger.error('Error when downloading caption for ' + yt.url)
                continue
            text_file = open(yt.caption_filepath, "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()
        return data
