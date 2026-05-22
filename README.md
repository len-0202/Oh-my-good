# Oh-my-good-morning-_pbl07
NITIC 4th grade PBL group 7

# memo
Raspberry pi
ユーザー名
```Bash
pbl7
```

pass
```Bash
ohmygood
```

#### ラズパイ本体への上書きはSSH接続する必要があります
#### 持ち帰って作業を行う際はPC上でのデバッグのみになります


# TODO
[x] 画像認識
[x] スピーカー出力
[x] 居眠り検知
[x] メイン関数
[x] ハード制御
[x] モード選択

# ラズパイに変更を反映
```Bash
git pull
```

# リポジトリを各自PCにclone
保存したいディレクトリでcmd
PowerShell
```Bash
git clone https://github.com/len-0202/Oh-my-good-morning-_pbl07
```

cloneしたフォルダをVSCで開く→開発


# PCからSSH接続

以下はRenのwifiに接続した際のIPなので、適宜@以降を変更して実行すること。

PowerShell
```Bash
ssh pi@10.158.66.79
```
```Bash
yes
```

# VSCからラズパイへ接続
拡張機能をインストール：
Remote-SSH

左下の >< マーク
<img width="516" height="304" alt="スクリーンショット 2026-05-08 143137" src="https://github.com/user-attachments/assets/74c25a60-613b-4252-98a9-4154db105447" />

Connect to Host
<img width="996" height="348" alt="スクリーンショット 2026-05-08 143816" src="https://github.com/user-attachments/assets/54bdd852-c08c-426a-b554-70122f2b50f1" />

pbl6@10.158.66.79
<img width="988" height="245" alt="スクリーンショット 2026-05-08 143925" src="https://github.com/user-attachments/assets/4c39e551-d5b4-48ce-8d01-e4593e486480" />

# フローチャート
<img width="622" height="689" alt="スクリーンショット 2026-05-15 13 30 15" src="https://github.com/user-attachments/assets/93caad8e-ed09-40d3-9bca-fe193f6cb8f9" />


