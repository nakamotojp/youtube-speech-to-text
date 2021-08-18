import youtube_dl
import speech_recognition
from datetime import datetime
from multiprocessing import Pool, TimeoutError
from .movie_download import movie_download, mv_file
from .speech_to_text import SpeechToText
from .utils import make_logger


# log fileを作成
date = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
logger = make_logger(date)


def process(url: str) -> bool:
    try:
        # youtubeから動画ファイルをダウンロード
        logger.info('Downloading start ...')
        movie_download(url)
        wavf_dir, wavf = mv_file()
        logger.debug(f'output movie dir: {wavf_dir}')
        logger.info(f'output movie file: {wavf}')
        logger.info('Downloading done ...')

        # 音声ファイルからテキストファイルを生成
        logger.info('Speech to text start ...')
        speech_to_txt = SpeechToText(wavf_dir, wavf)
        result_text = speech_to_txt.wav_to_text()
        logger.info('Speech to text done ...')
        return ('成功', result_text)

    except youtube_dl.utils.DownloadError:
        logger.error(f'Unsupported URL: {url}')
        return ('ダウンロードに失敗', '')

    except speech_recognition.UnknownValueError:
        logger.error('Speech to text error!')
        return ('テキスト変換に失敗', '')


def main(url: str) -> None:
    try:
        with Pool() as p:
            apply_result = p.apply_async(process, (url,))
            is_finish = apply_result.get(timeout=600)
        return is_finish

    except TimeoutError:
        logger.error('process() Timeout!')
        return ('タイムアウト', '')
