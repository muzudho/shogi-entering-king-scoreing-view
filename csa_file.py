import urllib.request as urlreq
import re
import datetime

class CsaFile:
    # 棋譜のCSA形式のバージョン
    __patternVersion = re.compile(r"^(V[\d\.]+)$")

    # 開始局面
    # Example:
    # P1-KY-KE-GI-KI-OU-KI-GI-KE-KY
    # P2 * -HI *  *  *  *  * -KA * 
    # P3-FU-FU-FU-FU-FU-FU-FU-FU-FU
    # P4 *  *  *  *  *  *  *  *  * 
    # P5 *  *  *  *  *  *  *  *  * 
    # P6 *  *  *  *  *  *  *  *  * 
    # P7+FU+FU+FU+FU+FU+FU+FU+FU+FU
    # P8 * +KA *  *  *  *  * +HI * 
    # P9+KY+KE+GI+KI+OU+KI+GI+KE+KY
    __patternP = re.compile(r"^\$P(\d)(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})$")

    # 指し手
    # Example: +7776FU
    # Example: -8384FU
    __patternMove = re.compile(r"^([+-])(\d{2})(\d{2})(\w{2})$")
    
    # 終了時間
    # Example: '$END_TIME:2021/08/10 21:14:45
    __patternEndTime = re.compile(r"^'\$END_TIME:(\d{4})/(\d{2})/(\d{2}) (\d{2}):(\d{2}):(\d{2})$")

    def __init__(self):
        # URL
        self._url = ""

        # 大会
        self._tournament = ""

        # 棋譜のCSA形式のバージョン
        self._version = ""

        # 入玉宣言時の得点 [未使用, 先手の得点, 後手の得点]
        self._enteringKingScoreing = [0,0,0]

        # 終了時間
        self._endTime = None

    @staticmethod
    def load(tournament, csaUrl):
        """棋譜ファイルの読取。
        CSA形式でないファイルを読み込んだ場合、エラーを返します

        Parameters
        ----------
        tournament : str
            電竜戦は "denryu-sen",
            floodgateは "floodgate"
        csaUrl : str
            .csa ファイルを指すURL
        """
        csaFile = CsaFile()
        csaFile._tournament = tournament
        csaFile._url = csaUrl

        # 棋譜ファイル（CSA形式）を読む
        f = urlreq.urlopen(csaUrl)
        if tournament=='floodgate':
            # floodgate用
            csa = f.read().decode("euc-jp")
        else:
            # 電竜戦、その他用
            csa = f.read().decode("utf8")
        # print(csa) # 開いたファイルの中身を表示する
        f.close()

        for i, line in enumerate(csa.split('\n')):
            if i==0:
                result = CsaFile.__patternVersion.match(line)
                if result:
                    # OK
                    pass
                else:
                    # Error
                    raise Exception(f'It\'s not a CSA file. Expected: "V2", etc. Found: {line}')

            # 開始局面
            result = CsaFile.__patternP.match(line)
            if result:
                print(f"P {result.group(0)}")
                rank = result.group(1)
                file9 = result.group(2)
                file8 = result.group(3)
                file7 = result.group(4)
                file6 = result.group(5)
                file5 = result.group(6)
                file4 = result.group(7)
                file3 = result.group(8)
                file2 = result.group(9)
                file1 = result.group(10)
                print(f"P Rank[{rank}] 9[{file9}] 8[{file8}] 7[{file7}] 6[{file6}] 5[{file5}] 4[{file4}] 3[{file3}] 2[{file2}] 1[{file1}]")
                continue

            # 指し手
            result = CsaFile.__patternMove.match(line)
            if result:
                print(f"M {result.group(0)}")
                continue

            # 終了時刻
            result = CsaFile.__patternEndTime.match(line)
            if result:
                # print(f"EndTime [1]={result.group(1)} [2]={result.group(2)} [3]={result.group(3)} [4]={result.group(4)} [5]={result.group(5)} [6]={result.group(6)}")
                csaFile._endTime = datetime.datetime(
                    int(result.group(1)),
                    int(result.group(2)),
                    int(result.group(3)),
                    int(result.group(4)),
                    int(result.group(5)),
                    int(result.group(6)))
                continue

            # print(f"> {line}")

        return csaFile

    @property
    def tournament(self):
        """大会
            電竜戦は "denryu-sen",
            floodgateは "floodgate"
        """
        return self._tournament

    @property
    def url(self):
        """.csa棋譜を指すURL"""
        return self._url

    @property
    def enteringKingScoreing(self):
        """入玉宣言時の得点 [未使用, 先手の得点, 後手の得点]"""
        return self._enteringKingScoreing

    @property
    def endTime(self):
        """終了時間"""
        return self._endTime
