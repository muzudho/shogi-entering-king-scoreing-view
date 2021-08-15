import os
import time
from csa_file import CsaFile

intervalSeconds = 15 # 棋譜読取間隔15秒
heartBeatSeconds = 0 # 画面が止まってないことをアピールするために増えていくだけの数
score = []
while True:

    try:
        # 棋譜ファイル（CSA形式）のURLを指定してください

        # 電竜戦
        # csaFile = CsaFile.load('denryu-sen', 'https://golan.sakura.ne.jp/denryusen/dr2_tsec/kifufiles/dr2tsec+buoy_james8nakahi_dr2b3-11-bottom_43_dlshogi_xylty-60-2F+dlshogi+xylty+20210718131042.csa')

        # floodgate (将棋盤の画面ではなく、CSA棋譜のURLを入れるように注意)
        csaFile = CsaFile.load('floodgate', 'http://wdoor.c.u-tokyo.ac.jp/shogi/LATEST//2021/08/10/wdoor+floodgate-300-10F+Qhapaq_WCSC29_8c+Kristallweizen_R9-3950X+20210810230009.csa')
        # このURLは CSA棋譜ではありません。
        # × csaFile = CsaFile.load('floodgate', 'http://wdoor.c.u-tokyo.ac.jp/shogi/view/2021/08/10/wdoor+floodgate-300-10F+python-dlshogi2+Krist_483_473stb_1000k+20210810213010.csa')

    except Exception as e:
        print(e)
        # デバッグ情報
        print(f'もしかして？') 
        print(f'* CsaFile.load( ) の第１引数を確認してください。 "denryu-sen" または "floodgate" です。') 
        print(f'* floodgateのGUIページのURLを指定していませんか？ (csa) のリンクから CSA棋譜のURLへ移動できます。')
        print(f'ハートビート {heartBeatSeconds}') # 生きてますよ
        heartBeatSeconds += intervalSeconds
        time.sleep(intervalSeconds)
        continue

    # 残り時間が変わらなかったら更新しない
    if score == [0, csaFile.enteringKingScoreing[1], csaFile.enteringKingScoreing[2]] :
        heartBeatSeconds += intervalSeconds
        time.sleep(intervalSeconds)
        continue

    # Windows用のコマンド　コンソール消去
    os.system('cls')

    # 残り時間の算出
    score = csaFile.enteringKingScoreing

    # 時計表示
    # そんなに精度出ないから、秒は消すのもあり
    print(f'') 
    print(f'') 
    print(f'') 
    print(f'    先手{score[1]:>3}点        後手{score[2]:>3}点')
    print(f'') 
    print(f'') 
    print(f'') 
    # デバッグ用情報
    print(f'    大会モード {csaFile.tournament}') 
    print(f'    URL {csaFile.url}') 
    # 盤表示
    # csaFile.printBoard()
    print(f'    ハートビート {heartBeatSeconds}') # 生きてますよ

    if csaFile.endTime:
        # 終了してんだったら　ループを抜けよ（＾～＾）
        print(f'    終了時刻 {csaFile.endTime}')
        print(f'おわり')
        break

    heartBeatSeconds += intervalSeconds
    time.sleep(intervalSeconds)
