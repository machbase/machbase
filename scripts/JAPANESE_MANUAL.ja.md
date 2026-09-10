# 日本語マニュアルの保守

日本語の製品ページは、韓国語・英語と同じコンテンツパスに `.ja.md` 拡張子で配置します。
対象は DBMS 8.7、DBMS 8.5、Neo、Apps、Fluid、および開発者向け文書です。
DBMS 8.7 は韓国語を主な原文とし、英語のみのキャッシュページも翻訳します。
その他のセクションでは両言語を比較し、どちらか一方だけにある情報も保持します。
原文の選択と根拠のある修正は `scripts/japanese_manual_sources.json` に記録し、原文の誤りは
検証済みの製品ソースで確認します。SQL/API 識別子、値、オプション、明示的なアンカー、
ショートコード、表の行、例を保持してください。制約を要約して省かず、本文、説明、コメントを
翻訳します。

用語は、データベース、テーブル、テーブルタイプ、行、列、クエリ、取り込み、インデックス、
述語、永続、トランザクション、保持ポリシーに統一します。TAG、ROLLUP、BASETIME などの名前や
SQL コマンドは変更しません。

## サイトの動作

- 日本語の製品ページは `/ja/neo/`、`/ja/dbms/`、`/ja/dbms-8.5/`、`/ja/apps/` を使用します。
  `/ja/` と日本語のロゴは `/ja/neo/` に移動します。ナビゲーションにはこれらの製品、
  サイトのホーム、検索、GitHub を含めます。未翻訳ページで日本語を選択すると、
  日本語のホームページに移動します。
- 公開状態を維持します。Fluid は `ignoreFiles` で除外したままにし、Neo の下書きページは
  下書きのままにします。翻訳しただけで、非公開コンテンツや下書きを公開してはいけません。
- Hextra v0.12.3 が日本語の UI 文字列を提供します。プロジェクト独自の上書きは
  `i18n/ja.yaml` にあります。
- DBMS の `llms` 出力では、3 言語すべてで各言語のラベルを使用します。日本語 Markdown 出力は、
  コードフェンスの外にあるルート相対の製品ページリンクを日本語用に変換します。
  共有アセットのパスは保持します。相対リンクの基準は、元のページの正規 URL です。
- ローカルの FlexSearch カスタマイズは Hextra v0.12.3 に基づきます。入力、貼り付け、IME 変換に
  対応し、インデックスの読み込みを待ち、古いリクエストを無視します。見出しの表示名は
  プレーンテキストにし、フラグメント抽出用には元の HTML を保持します。テーマを更新したら、
  これらのカスタマイズを再確認してください。
- リファレンス生成ツールは、現在のフラットな Markdown パスで `en`、`kr`、`ja` に対応します。
  生のインベントリには登録済みのエラー定義を保持しますが、公開する 8.7 カタログからは、
  原文マニュアルでも除外している廃止機能の 24 項目を除きます。エラーメッセージは
  サーバーの元の言語で保持します。

## 検証

```bash
python3 -B -m unittest discover -s scripts/tests -v
hugo --gc --minify --printUnusedTemplates --printI18nWarnings \
  --destination /tmp/machbase-ja-all-preview
python3 -B scripts/check_japanese_manual.py --all-documents \
  --public-dir /tmp/machbase-ja-all-preview --expected-rendered-pages 564 --landing /ja/neo/ \
  --source-policy scripts/japanese_manual_sources.json \
  --review-file scripts/japanese_manual_reviews.json --json
```

文書チェッカーは、構造上のエラーと、人によるレビューが必要な変更を別々に報告します。
構造上のエラーが 0 件でも、意味の正確さが承認されたわけではありません。数値とコードの
差分をすべて確認し、さらに SQL/API、データ消失、バックアップ、認証に関する重要な手順を
独立して読んで確認します。レビューファイルでは、原文、比較対象の別言語原文、翻訳文の
ハッシュを使用して個々の検出事項を承認できます。編集すると、その承認は無効になります。
現在の対象は、製品文書 583 件と開発者向け文書 5 件の計 588 件です。通常のビルドで公開される
製品ページは 564 件で、Fluid の 8 件と Neo の下書き 11 件は非公開のままです。
対象が変わったら件数を再計算してください。レビューファイルのインターフェースは
`python3 scripts/check_japanese_manual.py --help` を参照してください。

ブラウザー回帰検証では、ランディングページ、同じ記事での言語切り替え、日本語検索、IME の
変換確定、インデックスの読み込み遅延、検索結果なし、クリップボード、テーマ、モバイルメニュー、
目次の移動を確認します。必要に応じて、ブラウザーテストの依存関係をソースチェックアウトの
外にインストールしてください。

```bash
npm install --prefix /tmp/machbase-ja-browser --no-save --package-lock=false playwright@1.58.2
/tmp/machbase-ja-browser/node_modules/.bin/playwright install chromium
python3 -m http.server 14313 --bind 127.0.0.1 --directory /tmp/machbase-ja-all-preview
```

サーバーを起動した状態で、別のターミナルから実行します。

```bash
NODE_PATH=/tmp/machbase-ja-browser/node_modules \
  node scripts/tests/japanese_browser.cjs http://127.0.0.1:14313 /tmp/machbase-ja-browser
```

`PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` で、インストール済みの Chromium バイナリーを指定できます。
出力ディレクトリにあるデスクトップとモバイルの両方のスクリーンショットを確認してください。
操作の検証に合格しただけでは、表示品質は確認できません。これらのテストでは、稼働中の DBMS に
対して SQL を実行しません。
