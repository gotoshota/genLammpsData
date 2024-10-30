# 使い方
## main.py
```
python main.py --nchains 鎖の本数 --nbeads 鎖の長さ --output 出力ファイル名
```

で実行できます。`--nchains` と `--nbeads` は必須です。`--output` は省略可能です。省略した場合は`lmp.data`に出力されます。

## em.in
```
lmp -in in.em
```

でエネルギー最小化を行なってくれます。
`em.in` の中の変数を適宜変更すること。
