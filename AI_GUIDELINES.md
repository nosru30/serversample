# AI 開発ガイドライン（このひな形用）

本プロジェクトは「**初回のみオンライン / 以後オフライン開発**」を前提とした FastAPI + PostgreSQL ひな形です。  
LLM など AI ツールが自動で機能追加やテストを実装・修正するときは、以下のルールを守ってください。

---

## 1. 依存関係

1. **オンライン時（初回）**  
   `make setup` が実行され、`vendor/` に wheel がキャッシュされます。  
2. **オフライン時**  
   以降の `make setup` / `pip install` は  
   `pip install --no-index --find-links=vendor -r requirements.txt` で完結するようにしてください。  
3. 新しいライブラリを追加する場合は **極力既存依存に代替手段が無いか検討** し、 unavoidable なときのみ  
   - `requirements.txt` にバージョンを pin して追加  
   - **必ず** `vendor/` への wheel 取得方法（人間がオンライン時に実行する想定の `pip download` コマンド）を記述したうえで PR を出してください。

---

## 2. データベース

- ローカル開発は `docker-compose` の Postgres が **推奨 & デフォルト** です。  
  `make start` で起動し、FastAPI がマイグレーション後 `http://localhost:8000` で待ち受けます。  
- テストやオフライン環境では SQLite フォールバックが自動使用されます。  
  明示的に SQLite を使いたい場合は環境変数 `FORCE_SQLITE=true` を設定してください。

---

## 3. コード品質 (Lint)

- 変更後は **Ruff** で静的解析を実行してください。  
  `make lint` でエラー 0 を確認したうえでコミット / PR を作成すること。  

---

## 4. テスト

- 追加テストは `tests/` 配下へ。`pytest -q` が **必ずグリーン** になること。  
- DB を使うテストは SQLite で動くことを確認しつつ、標準 Postgres に依存しない SQL 記述を心掛けてください。

---

## 5. コマンドとスクリプト

| 用途              | コマンド                          |
|-------------------|-----------------------------------|
| 依存セットアップ  | `make setup`                      |
| Docker起動        | `make start`                      |
| ローカル起動      | `make start-local`                |
| DBマイグレーション | `make migrate`                    |
| テスト実行        | `make test`                       |

AI はこれらコマンドを前提にドキュメントやスクリプトを生成してください。

---

## 6. コーディング規約

- PEP8 / black 互換のコードを書いてください（auto-format に任せる）。  
- 可能な限り型ヒントを付け、MyPy で通る実装を推奨します。  
- 新規 API には OpenAPI スキーマが自動生成される FastAPI ルーターを利用し、単体テストを必ず用意してください。

---

## 7. ドキュメント更新

- README と本ガイドラインを最新状態に保つこと。  
- 主要変更がある場合は **変更点・手順** を README に追記してください。

---

Happy offline coding! 🚀
