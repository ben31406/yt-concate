import logging
import sys
sys.path.append('../')
import getopt

from yt_concate.pipeline.steps.preflights import Preflight
from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.download_captions import DownloadCaptions
from yt_concate.pipeline.steps.read_caption import ReadCaption
from yt_concate.pipeline.steps.search import Search
from yt_concate.pipeline.steps.download_videos import DownloadVideos
from yt_concate.pipeline.steps.edit_video import EditVideo
from yt_concate.pipeline.steps.postflights import Postflight
from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.utils import Utils


def config_logger():
    # create logger
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)

    # create file formatter
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # file handler
    # create file handler and set level to debug
    file_handler = logging.FileHandler('log_file.log')
    file_handler.setLevel(logging.DEBUG)
    # add formatter to file_handler
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # create stream formatter
    stream_formatter = logging.Formatter('%(levelname)s:%(message)s')

    # stream handler
    # create stream handler and set level to WARNING (OR user decide)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    # add formatter to stream_handler
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)


def print_usage():
    print('python main.py OPTIONS')
    print('OPTIONS：')
    print('{:>6} {:<12}{}'.format('-c', '--channel', 'Channel id of the Youtube channel to download'))
    print('{:>6} {:<12}{}'.format('-s', '--search', 'Key word to search in videos'))
    print('{:>6} {:<12}{}'.format('-l', '--limit', 'limit of video clips in final output'))


def main():
    inputs = {
        'channel_id': '',
        'search_word': '',
        'limit': 20,
    }

    # 接收command line arguments
    short_opts = 'hc:s:l:'
    long_opts = 'help channel= search= limit='.split()
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_usage()
            sys.exit(0)
        elif opt in ('-c', '--channel'):
            inputs['channel_id'] = arg
        elif opt in ('-s', '--search'):
            inputs['search_word'] = arg
        elif opt in ('-l', '--limit'):
            try:
                limit = int(arg)
            except ValueError:
                print_usage()
                sys.exit(2)
            inputs['limit'] = limit

    if not inputs['channel_id'] or not inputs['search_word']:
        print_usage()
        sys,exit(2)

    steps = [
        Preflight(),
        GetVideoList(),
        InitializeYT(),
        DownloadCaptions(),
        ReadCaption(),
        Search(),
        DownloadVideos(),
        EditVideo(),
        Postflight(),
    ]

    config_logger()
    utils = Utils()
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()
