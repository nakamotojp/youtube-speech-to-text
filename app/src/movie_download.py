import os
import shutil
from typing import Tuple
import youtube_dl
import glob


def movie_download(path: str) -> None:
    ydl_opts = {
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav'
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([path])


def mv_file() -> Tuple[str, str]:
    before_path = glob.glob('*.wav')[0]
    filename = before_path.split('/')[-1]
    after_dir = f'movies/{filename[:-4]}'
    os.makedirs(after_dir, exist_ok=True)
    after_path = os.path.join(after_dir, filename)
    shutil.move(before_path, after_path)
    return after_dir, filename
