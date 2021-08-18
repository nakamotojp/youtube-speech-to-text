import logging


def make_logger(date: str):
    logger = logging.getLogger(__name__)   # ロガーを取得
    logger.setLevel(logging.DEBUG)         # 出力レベルを設定
    fmt = logging.Formatter(
        '[%(levelname)s] - %(asctime)s - %(message)s'
    )                                      # フォーマッターを設定
    handler_s = logging.StreamHandler()    # ストリームハンドラーを生成
    handler_f = logging.FileHandler(
        f'log/{date[:10]}.log'
    )                                      # ファイルハンドラーを生成
    handler_s.setLevel(logging.DEBUG)      # 出力レベルを設定
    handler_f.setLevel(logging.INFO)       # 出力レベルを設定
    handler_s.setFormatter(fmt)            # ハンドラーにフォーマッターを設定
    handler_f.setFormatter(fmt)            # ハンドラーにフォーマッターを設定
    logger.addHandler(handler_s)           # ロガーにハンドラーを設定
    logger.addHandler(handler_f)           # ロガーにハンドラーを設定
    logger.propagate = False

    return logger
