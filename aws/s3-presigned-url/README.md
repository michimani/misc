# s3-presigned-url

Amazon S3 の Pre-signed URL の挙動を確認するためのプロトタイプ。[floci](https://floci.io/) で S3 をローカルエミュレートし、ブラウザからの直接アップロード / ダウンロードを Pre-signed URL 経由で行う。

## 構成

- `frontend/` — TypeScript (Vite, フレームワークなし) 製のアップロード画面 / ファイル一覧画面
- `backend/` — Go 製の API サーバー (`prepare` / `commit` / `file-list`)
- `docker-compose.yml` — floci, バケット作成用の初期化コンテナ, backend, frontend, devcontainer 用 workspace をまとめて起動
- `.devcontainer/` — 上記一式を devcontainer で起動するための設定

```
┌────────────┐   POST /api/prepare    ┌─────────┐
│  frontend  │ ─────────────────────▶ │ backend │
│ (:55174)   │ ◀───────────────────── │ (:58080)│
└─────┬──────┘   { uuid, uploadUrl }  └────┬────┘
      │                                    │ internal S3 calls
      │ PUT (direct upload)                │ (Copy/Delete/List)
      ▼                                    ▼
┌─────────────────────────────────────────────────┐
│                 floci (:54566)                   │
│   presigned-tmp/{uuid}  →  presigned-store/{uuid}/{fileName}
└─────────────────────────────────────────────────┘
```

Pre-signed URL はブラウザに渡されるため、backend は 2 つの S3 クライアントを使い分けている。

- `S3_INTERNAL_ENDPOINT` (`http://floci:4566`) — docker-compose 内部からの Copy/Delete/List に使用（コンテナ間通信のためホスト公開ポートとは独立）
- `S3_PUBLIC_ENDPOINT` (`http://localhost:54566`) — Pre-signed URL の署名対象ホストに使用（ブラウザから解決可能なアドレスである必要がある）

## 起動方法

### devcontainer で起動する場合

1. VS Code でこのディレクトリ (`aws/s3-presigned-url`) を開き、"Reopen in Container" を実行する
2. `docker compose up` 相当の処理が自動的に走り、floci / バケット作成 / backend / frontend が起動する
3. ブラウザで http://localhost:55174 を開く

### devcontainer を使わず直接起動する場合

```sh
docker compose up --build
```

起動後、以下にアクセスできる。

| サービス | URL | 用途 |
| --- | --- | --- |
| frontend | http://localhost:55174 | アップロード / ファイル一覧 UI |
| backend | http://localhost:58080 | API |
| floci (S3) | http://localhost:54566 | S3 互換 API |

ホストマシン上で他プロセスとポートが競合しないよう、ポートは一般的に使われにくい番号（49152–65535 の動的/私用ポート範囲）を割り当てている。

停止する場合は `docker compose down`。

## 画面の流れ

1. ファイル選択 (複数可) すると、選択したファイルの数だけ `POST /api/prepare` を呼び出し、返ってきた Pre-signed URL に対して直接 `PUT` でアップロードする
2. すべてのアップロードが完了すると「登録」ボタンが有効になる
3. 「登録」を押すと `POST /api/commit` を呼び出し、成功すると登録済みファイル一覧画面に遷移する

## API

| Method | Path | 概要 |
| --- | --- | --- |
| POST | `/api/prepare` | 一時バケットの `/{uuid}` に対するアップロード用 Pre-signed **POST** (`PresignPostObject`, 15分) を発行。フォーム用の `uploadUrl` と `fields`（`key` / `policy` / `X-Amz-*` など）を返す |
| POST | `/api/commit` | uuid ごとに PDF かどうかを検証したうえで一時バケット→登録済みバケットへ Copy し、成功したものは一時バケットから Delete (=move) |
| GET | `/api/file-list` | 登録済みバケットの一覧と、各ファイルのダウンロード用 Pre-signed URL (GET, 15分) を返す |

`commit` はファイル種別を PDF に限定している。判定はファイル全体を読み込まず、一時バケットのオブジェクトに対して `Range: bytes=0-4` を指定した `GetObject` でマジックナンバー (`%PDF-`) の 5 バイトだけを取得して行う。結果は `results[].status` に `committed` / `not_found` / `invalid_file_type` / `error` のいずれかで返る。

## Pre-signed POST によるファイルサイズ / MIME type の制御

`prepare` は `PresignPutObject`（PUT 用の単純な署名 URL）ではなく `PresignPostObject` を使い、ブラウザから直接 `multipart/form-data` で S3 (floci) に POST させる方式に変更した。`PresignPostOptions.Conditions` に以下の 2 条件を付与しており、これらは返却される `fields.policy`（Base64 エンコードされた JSON）に埋め込まれ、`fields["X-Amz-Signature"]` はこのポリシー文書に対して署名される。

```go
o.Conditions = []any{
    []any{"content-length-range", 0, 500 * 1024}, // 0〜500KB
    map[string]string{"Content-Type": "application/pdf"},
}
```

デコードすると次のような `policy` になる（`bucket` / `X-Amz-*` / `key` は SDK が自動付与するもの）。

```json
{
  "conditions": [
    { "X-Amz-Algorithm": "AWS4-HMAC-SHA256" },
    { "bucket": "presigned-tmp" },
    { "X-Amz-Credential": "..." },
    { "X-Amz-Date": "..." },
    ["content-length-range", 0, 512000],
    { "Content-Type": "application/pdf" },
    { "key": "..." }
  ],
  "expiration": "..."
}
```

フロントエンド (`api.ts`) は `fields` をそのまま `FormData` に詰め、実際に選択されたファイルの `file.type` を `Content-Type` フィールドとして追加し（S3 の POST ポリシー仕様に合わせて `file` フィールドを最後に追加）、`uploadUrl` へ POST する。仕様上 S3 は POST リクエストがこのポリシーの条件を満たさない場合（サイズ超過 / `Content-Type` 不一致）、オブジェクトを作成せず `4xx` を返す。

この構成により、**ファイルサイズと MIME type の制御を、アプリケーションサーバーを経由せずブラウザ→S3 の直接アップロード時点で行える**ことを確認した（少なくとも Pre-signed POST の署名対象ポリシーとしては正しく構築できている。実機での動作は下記「floci に関する制約」を参照）。

ただし `Content-Type` 条件はあくまで **クライアントが送ってきたフォームフィールドの値との一致** を見ているだけで、ファイルの中身までは検証しない。そのため画像ファイルの拡張子・Content-Type を `application/pdf` と偽って送れば、この条件だけではすり抜けてしまう。`commit` 時点でのマジックナンバー検証（ファイル先頭バイトの実データ確認）は、この抜け道に対する二段目のチェックとして引き続き必要であり、削除せず残している。

## floci に関する制約

動作確認の結果、floci は Pre-signed URL の **有効期限 (`X-Amz-Expires`) は検証するが、署名 (`X-Amz-Signature`) 自体は検証しない**（署名を改ざんしても、あるいは全く付与しなくてもリクエストが成功する）。そのため、このプロトタイプでは Pre-signed URL の基本的な発行〜利用の流れと有効期限切れの挙動は確認できるが、署名改ざん・不正な認証情報によるリクエスト拒否といった署名検証まわりの挙動は確認できない。

Pre-signed POST の `content-length-range` / `Content-Type` 条件についても、floci が実際にポリシーを評価して拒否するかどうかは本リポジトリの CI 環境では確認できていない（Docker Hub からのイメージ取得がネットワークポリシーでブロックされており、`docker compose up` を実行できなかったため）。ローカル環境で `docker compose up --build` を実行し、500KB超のファイルや PDF 以外のファイル（`Content-Type` を偽らない場合）をアップロードして、S3 (floci) 側で拒否されるかどうかを実際に確認することを推奨する。
