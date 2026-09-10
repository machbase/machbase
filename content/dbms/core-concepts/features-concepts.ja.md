---
type: docs
title: '2.3 主要機能と用語の区別'
weight: 30
toc: true
aliases:
  - /dbms/core-concepts/terminology-distinction/
---
Machbase DBMS の長期データ運用に必要な ROLLUP、Retention Policy、Backup・Restore・Mount の
役割と選択基準を説明します。作成構文と運用手順は各機能の詳細文書で扱います。

元データは個々のイベントや計測値の再分析に、集計は多数の元データを要約した繰り返しクエリに使います。
保持ポリシーは何をいつ削除するかを決め、バックアップは障害後の復旧に必要なデータを用意します。
これらを区別すると、集計があるから必要な元データを削除する、複製があるからバックアップを省く、
といった誤りを避けられます。

- **[ROLLUP 統計の役割](#role-statistics-rollup)** — 繰り返し集計のクエリコストを削減する方法
- **[Retention Policy の役割](#role-retention-policy)** — 期間に応じてデータを自動削除する方法
- **[Backup・Restore・Mount の関係](#concepts-backup-restore-mount)** — 保護、復旧、参照の目的の区別

<a id="role-statistics-rollup"></a>

## ROLLUP 統計の役割

TAG の長期間のデータを毎回元の行から集計すると、クエリ範囲が広がるほど処理コストも増えます。
ROLLUP は、時間軸 TAG の指定した数値列などを区間ごとに集計し、繰り返しクエリに使う機能です。
集計対象の列と集計方式は ROLLUP の定義で決まります。

基本 ROLLUP は秒（SEC）、分（MIN）、時間（HOUR）の階層を構成します。テーブル作成時に
`WITH ROLLUP` を指定するか、通常の `CREATE ROLLUP` で必要な周期と条件を指定できます。
生成されるオブジェクト名や内部保存構造に依存せず、公開された ROLLUP SQL で管理してください。

### 選択基準

| クエリパターン | 選択 |
| --- | --- |
| 長期間の分・時間単位の統計を繰り返し取得 | 基本 ROLLUP を検討 |
| 集計周期やフィルター条件を指定 | 周期・条件を指定する通常の ROLLUP を検討 |
| 独自の集計 SELECT の結果を別の TAG に保存 | Standard Edition の Custom ROLLUP を検討 |
| 最初・最後の値が必要 | 拡張 ROLLUP を検討 |
| 元の値のクエリが中心、または集計頻度が低い | ROLLUP なしで開始して実行時間を測定 |

ROLLUP は元データの代わりとなる保持ポリシーではありません。元データの保持期間は Retention Policy で
別途設計し、TAG データを変更した場合は、その範囲の ROLLUP 再構築が必要かも確認します。

### 集計結果の解釈

集計すると情報の解像度が下がります。1分平均だけでは、その1分間の瞬間的な異常値や個々の計測順序を
復元できません。最大・最小値を併せて保持すれば範囲は分かりますが、元の情報がすべて残るわけではありません。

複数区間の平均をさらに平均すると、全体平均と異なる場合があります。2件の平均が10、8件の平均が20なら、
全体平均は `(2 × 10 + 8 × 20) / 10 = 18` であり、2つの平均の単純平均15ではありません。
再集計には合計と有効件数などの必要な統計を使い、ROLLUP の対応クエリ関数に従います。

ROLLUP 処理は元データの入力と別に進むため、最新の元データと集計が反映される時点は異なることがあります。
遅延到着や値の補正がある場合は、元データの範囲、集計の進行状態、再構築の必要性を併せて確認します。

作成構文、クエリ関数、再構築手順は [TAG・ROLLUP の利用](/dbms/tag-rollup-usage/)を参照してください。

<a id="role-retention-policy"></a>
<a id="retention-vs-delete-truncate"></a>

## Retention Policy の役割

Retention Policy は、LOG または TAG で保持期間を過ぎたデータを所定の周期で削除します。
データが流入し続けるテーブルの保存領域を、管理者が手動削除を繰り返さずに管理するために使います。

| 要件 | 選択 |
| --- | --- |
| 一定期間を過ぎたデータを継続的に自動削除 | Retention Policy |
| 誤入力した範囲を直ちに削除 | テーブルタイプが対応する `DELETE` |
| 対応テーブルの全データを削除 | `TRUNCATE TABLE` |

Retention を適用しても、すべての古いデータが直ちに消えるわけではありません。実行周期、
対象テーブルのサポート範囲、実際の削除状態を確認します。LOOKUP、VOLATILE、TRANSACTION の
データライフサイクルは、各テーブルが対応する明示的な DML で管理します。

保持期間は入力量とともに必要な保存容量を決めます。毎秒の入力件数に保持秒数を掛けると元の行数を
概算できますが、実際のディスク容量は型、圧縮、インデックス、複製、バックアップにも左右されます。
元データを削除する前に、集計の範囲・保持期間と、監査・再分析に必要な解像度を確認します。
ROLLUP を作成しても、元データの保持期間は自動的には変わりません。

ポリシーの作成・適用・解除構文と運用点検は、
[データ保持ポリシー](/dbms/operations-configuration-recovery/policy-data-retention/)を参照してください。

<a id="concepts-backup-restore-mount"></a>
<a id="backup-vs-restore-mount"></a>

## Backup・Restore・Mount の関係

3つともバックアップデータに関わる機能ですが、結果は異なります。

| 機能 | 目的 | 運用サーバー | 結果 |
| --- | --- | --- | --- |
| Backup | 復旧用コピーの作成 | 稼働中に実行可能 | 別のパスにバックアップを作成 |
| インスタンス Restore | バックアップからインスタンスを復旧 | オフライン手順が必要 | 運用データベースを復旧 |
| Mount | バックアップ内容を読み取り専用で確認 | 稼働中に実行可能 | 別名でバックアップを検索 |

インスタンスの復旧とは別に、論理データベースを復旧する `RESTORE DATABASE` SQL もあります。
稼働中のサーバーで実行するため、オフラインのインスタンス復旧とは対象と手順を区別します。

Backup の成功だけでは復旧手順を検証したことになりません。対応 Edition で Mount による内容確認、
または隔離環境での Restore を実施します。バックアップパスの権限と保持周期も管理してください。
Mount はバックアップを運用データへ戻す処理ではなく、マウントしたデータには書き込めません。
Restore と Mount は Standard Edition の機能なので、Cluster ではその Edition のバックアップ・障害復旧手順を確認します。

運用計画では、許容するデータ損失期間（RPO）とサービス復旧までの許容時間（RTO）を決めます。
前者はバックアップ・複製間隔、後者は復旧するデータ量と実際のリストア時間を検討する基準です。
特定の Edition やバックアップ周期だけで両方の目標が保証されるわけではありません。
誤った削除も複製先に反映されることがあるため、複製とバックアップの目的を区別します。

コマンド、権限、Edition 別サポート、復旧順序は
[バックアップ・リストア・マウント](/dbms/operations-configuration-recovery/backup-restore-mount/)を参照してください。
複数の論理データベースを運用する場合は、
[複数データベースの運用](/dbms/operations-configuration-recovery/multi-database/)も確認します。

<a id="machloader-vs-csvimport-csvexport-tagmetaimport"></a>
<a id="load-data-infile-vs-machloader"></a>

## 入力経路の比較

小さな SQL 演習には `INSERT`、アプリケーションの継続収集には対応 SDK の Append、ファイルの
読み込みには `machloader` などを検討します。対応テーブル、入力形式、失敗の確認方法が異なるため、
名前が似ているだけでツールを置き換えることはできません。

SQL、SDK、ファイル入力ツールの選択基準は、
[データの入力とエクスポート](/dbms/development-tools-integration/data-input-load-export/#machloader-vs-csvimport-csvexport-tagmetaimport)
を参照してください。
