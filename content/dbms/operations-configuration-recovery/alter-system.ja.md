---
type: docs
title: '13.4 ALTER SYSTEM の運用'
weight: 40
toc: true
---

`ALTER SYSTEM` はインスタンス全体に影響する可能性がある管理コマンドです。実行前に対象、権限、
進行中の処理、ロールバックまたは解除コマンドを確認します。構文全体は
[システム・セッション ALTER 構文](/dbms/reference/sql/syntax/system-session-alter-syntax/)を参照してください。

## 共通手順

1. 現在のサーバー、データベース、リリースを確認します。
2. 関連セッション、文、バックアップ、チェックポイントの状態を記録します。
3. ブロッキング、I/O、メモリへの影響を確認します。
4. メンテナンス時間と失敗時の対応を決めます。
5. 実行直後に結果、関連仮想テーブル、ログを確認します。

<a id="checkpoint"></a>

## CHECKPOINT

```text
ALTER SYSTEM CHECKPOINT;
```

チェックポイントはストレージ I/O を増加させることがあります。バックアップ・停止前に必要性を検討し、
同時に行う大量入力やクエリへの影響を観察します。単に遅いという理由で繰り返し実行しないでください。

<a id="check-disk-usage"></a>

## CHECK DISK_USAGE

```text
ALTER SYSTEM CHECK DISK_USAGE;
```

ファイルシステムの状態とデータベースのストレージメタデータを点検する際に使用します。事前に
空き容量とマウント状態を確認し、結果ログを調べます。数値を合わせるために内部ファイルを編集してはいけません。

<a id="install-license"></a>

## INSTALL LICENSE

```text
ALTER SYSTEM INSTALL LICENSE;
ALTER SYSTEM INSTALL LICENSE = '/absolute/path/license.dat';
```

ライセンスの入手元、対象インスタンス、Edition、有効期限を確認します。内容を文書やログへコピーせず、
アクセス権限を制限します。インストール後は `V$LICENSE_INFO` と新しい接続で適用を確認します。

<a id="kill-cancel-session"></a>

## KILL と CANCEL SESSION

```text
ALTER SYSTEM CANCEL SESSION session_id;
ALTER SYSTEM KILL SESSION session_id;
```

まず `V$SESSION` と `V$STMT` でユーザー、クライアント IP、SQL、状態を確認します。実行中の文を
止める場合は `CANCEL`、接続自体の終了が必要なら `KILL` を検討します。トランザクション、Appender、
アプリケーションの再試行が引き起こす重複とロールバックへの影響を確認します。

<a id="freeze-unfreeze"></a>

## FREEZE と UNFREEZE

```text
ALTER SYSTEM FREEZE;
ALTER SYSTEM UNFREEZE;
```

freeze は、公開バックアップ機能で代替できないファイルシステムスナップショットの手順でのみ検討します。
事前に許容する読み書きと最大 freeze 時間を定め、すべてのエラー経路で `UNFREEZE` を実行する
担当者と確認手順を用意します。セッションを freeze 状態のまま放置してはいけません。

<a id="flush-ager"></a>

## FLUSH AGER

```text
ALTER SYSTEM FLUSH AGER;
```

削除済み領域の回収遅延を調査する際に、使用を検討します。保持ポリシー、DELETE の状態、
ストレージの余裕を先に確認し、正常なバックグラウンド処理を繰り返し強制しないでください。

<a id="flush-pvo-cache"></a>

## FLUSH PVO_CACHE

```text
ALTER SYSTEM FLUSH PVO_CACHE;
```

実行計画キャッシュを消去すると、後続クエリが再解析・再最適化されます。スキーマや実行計画の問題を
切り分ける場合だけ実行し、同時クエリの一時的な遅延増大を観察します。継続的な性能問題の
対策としてキャッシュ消去を使わないでください。

<a id="flush-sys-stat"></a>

## FLUSH SYS_STAT

```text
ALTER SYSTEM FLUSH SYS_STAT;
```

累積統計を初期化する前に、必要な基準値を保存します。初期化時刻を監視に記録し、
変化率計算や障害分析が不正確にならないようにします。

<a id="flush-page-cache"></a>

## FLUSH PAGE_CACHE

```text
ALTER SYSTEM FLUSH PAGE_CACHE;
```

ページキャッシュの消去は、後続クエリの I/O と遅延を大きく変えることがあります。コールドキャッシュの
比較や限定的な診断だけに使い、運用のピーク負荷時には実行しないでください。

## 権限と監査

必要最小限の管理権限を持つアカウントで実行し、コマンド、対象、時刻、実行者、理由、結果を
監査記録に残します。例のセッション ID、パス、設定値をそのまま運用環境に使わないでください。
