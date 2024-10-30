# 使い方
```
python main.py --nbeads 鎖長 --ouput 出力ファイル名 --topology <linear | ring> --style <bond | angle > 
```

一本鎖のデータファイルを作成。
環状高分子集合系のシミュレーションを行う場合は、トポロジー保存のため、一本鎖をlammps のコマンド `replicate` で複製してMDを実行することが一般的。
