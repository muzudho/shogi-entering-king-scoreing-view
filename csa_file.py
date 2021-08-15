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
    __patternP0 = re.compile(r"P1-KY-KE-GI-KI-OU-KI-GI-KE-KY")
    __patternP1 = re.compile(r"P(\d)-KY-KE-GI-KI-OU-KI-GI-KE-KY")
    __patternP2 = re.compile(r"P(\d)(.{3})-KE-GI-KI-OU-KI-GI-KE-KY")
    # __patternP = re.compile(r"P1\-KY\-KE\-GI\-KI\-OU\-KI\-GI\-KE\-KY")
    # __patternP = re.compile(r"^P([A-Z-]+)$")
    # __patternP = re.compile(r"^\$P(\d)(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})$")

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

        # 将棋盤
        self._board = [""] * 100

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
            result = CsaFile.__patternP2.match(line)
            if result:
                # print(f"P> {line}")
                print(f"P> {result.group(0)}")
                rank = result.group(1)
                file9 = result.group(2)
                """
                file8 = result.group(3)
                file7 = result.group(4)
                file6 = result.group(5)
                file5 = result.group(6)
                file4 = result.group(7)
                file3 = result.group(8)
                file2 = result.group(9)
                file1 = result.group(10)
                print(f"P  8[{file8}] 7[{file7}] 6[{file6}] 5[{file5}] 4[{file4}] 3[{file3}] 2[{file2}] 1[{file1}]")
                """
                print(f"P Rank[{rank}] 9[{file9}]")
                continue

            # 開始局面
            result = CsaFile.__patternP1.match(line)
            if result:
                # print(f"P> {line}")
                print(f"P> {result.group(0)}")
                rank = result.group(1)
                """
                file8 = result.group(3)
                file7 = result.group(4)
                file6 = result.group(5)
                file5 = result.group(6)
                file4 = result.group(7)
                file3 = result.group(8)
                file2 = result.group(9)
                file1 = result.group(10)
                print(f"P  8[{file8}] 7[{file7}] 6[{file6}] 5[{file5}] 4[{file4}] 3[{file3}] 2[{file2}] 1[{file1}]")
                """
                print(f"P Rank[{rank}]")
                continue

            # 開始局面
            result = CsaFile.__patternP0.match(line)
            if result:
                # print(f"P> {line}")
                print(f"P> {result.group(0)}")
                """
                file8 = result.group(3)
                file7 = result.group(4)
                file6 = result.group(5)
                file5 = result.group(6)
                file4 = result.group(7)
                file3 = result.group(8)
                file2 = result.group(9)
                file1 = result.group(10)
                print(f"P Rank[{rank}] 9[{file9}] 8[{file8}] 7[{file7}] 6[{file6}] 5[{file5}] 4[{file4}] 3[{file3}] 2[{file2}] 1[{file1}]")
                """
                continue

            '''
            # 指し手
            result = CsaFile.__patternMove.match(line)
            if result:
                # print(f"M {result.group(0)}")
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
            '''

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
    def board(self):
        """将棋盤"""
        return self._board

    @property
    def endTime(self):
        """終了時間"""
        return self._endTime

    def printBoard(self):
        print(f"  9   8   7   6   5   4   3   2   1")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a = "{: >3}".format(self._board[91])
        b = "{: >3}".format(self._board[81])
        c = "{: >3}".format(self._board[71])
        d = "{: >3}".format(self._board[61])
        e = "{: >3}".format(self._board[51])
        f = "{: >3}".format(self._board[41])
        g = "{: >3}".format(self._board[31])
        h = "{: >3}".format(self._board[21])
        i = "{: >3}".format(self._board[11])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 1")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a = "{: >3}".format(self._board[92])
        b = "{: >3}".format(self._board[82])
        c = "{: >3}".format(self._board[72])
        d = "{: >3}".format(self._board[62])
        e = "{: >3}".format(self._board[52])
        f = "{: >3}".format(self._board[42])
        g = "{: >3}".format(self._board[32])
        h = "{: >3}".format(self._board[22])
        i = "{: >3}".format(self._board[12])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 2")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a = "{: >3}".format(self._board[93])
        b = "{: >3}".format(self._board[83])
        c = "{: >3}".format(self._board[73])
        d = "{: >3}".format(self._board[63])
        e = "{: >3}".format(self._board[53])
        f = "{: >3}".format(self._board[43])
        g = "{: >3}".format(self._board[33])
        h = "{: >3}".format(self._board[23])
        i = "{: >3}".format(self._board[13])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 3")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a = "{: >3}".format(self._board[94])
        b = "{: >3}".format(self._board[84])
        c = "{: >3}".format(self._board[74])
        d = "{: >3}".format(self._board[64])
        e = "{: >3}".format(self._board[54])
        f = "{: >3}".format(self._board[44])
        g = "{: >3}".format(self._board[34])
        h = "{: >3}".format(self._board[24])
        i = "{: >3}".format(self._board[14])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 4")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a = "{: >3}".format(self._board[95])
        b = "{: >3}".format(self._board[85])
        c = "{: >3}".format(self._board[75])
        d = "{: >3}".format(self._board[65])
        e = "{: >3}".format(self._board[55])
        f = "{: >3}".format(self._board[45])
        g = "{: >3}".format(self._board[35])
        h = "{: >3}".format(self._board[25])
        i = "{: >3}".format(self._board[15])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 5")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a = "{: >3}".format(self._board[96])
        b = "{: >3}".format(self._board[86])
        c = "{: >3}".format(self._board[76])
        d = "{: >3}".format(self._board[66])
        e = "{: >3}".format(self._board[56])
        f = "{: >3}".format(self._board[46])
        g = "{: >3}".format(self._board[36])
        h = "{: >3}".format(self._board[26])
        i = "{: >3}".format(self._board[16])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 6")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a = "{: >3}".format(self._board[97])
        b = "{: >3}".format(self._board[87])
        c = "{: >3}".format(self._board[77])
        d = "{: >3}".format(self._board[67])
        e = "{: >3}".format(self._board[57])
        f = "{: >3}".format(self._board[47])
        g = "{: >3}".format(self._board[37])
        h = "{: >3}".format(self._board[27])
        i = "{: >3}".format(self._board[17])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 7")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a = "{: >3}".format(self._board[98])
        b = "{: >3}".format(self._board[88])
        c = "{: >3}".format(self._board[78])
        d = "{: >3}".format(self._board[68])
        e = "{: >3}".format(self._board[58])
        f = "{: >3}".format(self._board[48])
        g = "{: >3}".format(self._board[38])
        h = "{: >3}".format(self._board[28])
        i = "{: >3}".format(self._board[18])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 8")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a = "{: >3}".format(self._board[99])
        b = "{: >3}".format(self._board[89])
        c = "{: >3}".format(self._board[79])
        d = "{: >3}".format(self._board[69])
        e = "{: >3}".format(self._board[59])
        f = "{: >3}".format(self._board[49])
        g = "{: >3}".format(self._board[39])
        h = "{: >3}".format(self._board[29])
        i = "{: >3}".format(self._board[19])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 9")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
