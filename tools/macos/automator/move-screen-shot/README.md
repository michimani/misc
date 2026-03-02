# move-screen-shot

macOS のスクリーンショットを日付ごとのフォルダに自動整理するスクリプト。

## 概要

Automator のフォルダアクションとして使用し、指定フォルダに保存されたスクリーンショットを年/月（または年/月/日）のディレクトリ構造に自動で振り分けます。

## 対応フォーマット

| アプリ | ファイル名例 |
|--------|-------------|
| macOS 標準スクリーンショット | `sc 2020-03-05_21.39.57.png` |
| CleanShot X | `CleanShot 2026-03-03 at 01.37.17.png` |

## 設定項目

`main.py` 内の定数を環境に合わせて変更してください。

| 定数 | 説明 | デフォルト値 |
|------|------|-------------|
| `FILE_TYPE` | 対象ファイルの拡張子 | `png` |
| `SC_DIR` | スクリーンショットの保存先（監視対象） | `/Users/michimani/Pictures/__ss_tmp` |
| `SC_OUT_DIR` | 整理後の出力先ディレクトリ | `/Users/michimani/Pictures/ScreenShots` |
| `DIR_TYPE` | フォルダ分けの粒度（`MONTH` または `DAY`） | `MONTH` |

## 出力ディレクトリ構造

### `DIR_TYPE = 'MONTH'` の場合

```
SC_OUT_DIR/
├── 2026/
│   ├── 01/
│   ├── 02/
│   └── 03/
│       ├── sc_2026-03-01_120000.png
│       └── CleanShot_2026-03-03_at_013717.png
```

### `DIR_TYPE = 'DAY'` の場合

```
SC_OUT_DIR/
├── 2026/
│   └── 03/
│       ├── 01/
│       │   └── sc_2026-03-01_120000.png
│       └── 03/
│           └── CleanShot_2026-03-03_at_013717.png
```

## Automator での設定方法

1. Automator を開き「フォルダアクション」を選択
2. 「フォルダアクションは、次の場所に追加されたファイルやフォルダを受け取る」で `SC_DIR` に設定したフォルダを選択
3. 「シェルスクリプトを実行」アクションを追加
4. 以下のスクリプトを設定:
   ```bash
   /usr/bin/python3 /path/to/main.py
   ```
5. 保存して有効化

## macOS のスクリーンショット保存先変更

macOS 標準のスクリーンショット保存先を `SC_DIR` に変更するには:

```bash
defaults write com.apple.screencapture location /Users/michimani/Pictures/__ss_tmp
killall SystemUIServer
```
