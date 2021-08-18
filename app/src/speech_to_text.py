import os
import wave
import math
import struct
import speech_recognition as sr
from typing import List
from scipy import fromstring, int16


class SpeechToText:
    def __init__(self, wavf_dir: str, wavf: str, cuttime=30) -> None:
        self.wavf_dir = wavf_dir
        self.wavf = wavf
        self.cuttime = cuttime

    def cut_wav(self) -> List[str]:
        """
        wavファイル分割を分割、保存する
        上記処理で保存されたファイル名のリストを返す
        """
        # ファイル情報を取得
        wavf_path = os.path.join(self.wavf_dir, self.wavf)
        wr = wave.open(wavf_path, 'r')
        ch = wr.getnchannels()
        width = wr.getsampwidth()
        fr = wr.getframerate()
        fn = wr.getnframes()
        total_time = 1.0 * fn / fr
        integer = math.floor(total_time)
        t = int(self.cuttime)
        frames = int(ch * fr * t)
        num_cut = int(integer // t)

        # waveファイルを数値化
        data = wr.readframes(wr.getnframes())
        wr.close()
        X = fromstring(data, dtype=int16)

        outf_list = []
        for i in range(num_cut):
            # 出力データを生成
            outf = os.path.join(self.wavf_dir, f'{str(i).zfill(3)}.wav')
            start_cut = i * frames
            end_cut = i * frames + frames
            Y = X[start_cut:end_cut]
            outd = struct.pack('h' * len(Y), *Y)

            # 書き出し
            ww = wave.open(outf, 'w')
            ww.setnchannels(ch)
            ww.setsampwidth(width)
            ww.setframerate(fr)
            ww.writeframes(outd)
            ww.close()
            outf_list.append(outf)

        return outf_list

    def cut_wavs_str(self, outf_list: List[str]) -> str:
        """
        wavファイルから文字列を生成
        """
        output_text = ''
        for fwav in outf_list:
            r = sr.Recognizer()

            with sr.AudioFile(fwav) as source:
                audio = r.record(source)
            text = r.recognize_google(audio, language='ja-JP')
            output_text += text + '¥n'
        return output_text

    def wav_to_text(self) -> str:
        cut_wavs = self.cut_wav()               # 音声ファイルの分割
        out_text = self.cut_wavs_str(cut_wavs)  # 音声ファイルから文字列を取得
        txt_file = os.path.join('text', self.wavf.replace('.wav', '.txt'))
        with open(txt_file, 'w') as f:
            f.write(out_text)
        return out_text
