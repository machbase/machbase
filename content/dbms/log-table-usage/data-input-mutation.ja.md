---
type: docs
title: '7.4 データ入力'
weight: 40
toc: true
---

1、2行の入力に成功しても、収集の準備が完了したとは限りません。
継続的な収集では、送信バッファ、一部の行の失敗、切断後の再送も考慮する必要があります。
まずSQLでカラムと時刻を確認し、実際のスループットに適した入力方法を選択してください。

<a id="original-85-inserting-data"></a>

<a id="작은-insert로-입력-계약을-확인합니다"></a>

## SQL INSERT

```sql
CREATE LOG TABLE ch7_input (
    event_time DATETIME,
    event_id   VARCHAR(32),
    device     VARCHAR(32),
    message    VARCHAR(128)
);

INSERT INTO ch7_input(event_time, event_id, device, message)
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        'evt-001', 'DEV-01', 'connection timeout');

SELECT _arrival_time, event_time, event_id, device, message
  FROM ch7_input;
```

1行が返され、`event_time`は固定の発生時刻です。
`_arrival_time`を省略したため、入力処理でサーバー時刻が使用されます。
デフォルト設定では時刻逆転時に補正が発生し得るため、常に実際の受信時刻と正確に一致するとは限りません。
詳細な規則は[時間モデル](../arrival-time-model/)を参照してください。

同じイベントを再度入力した場合の動作も確認します。

```sql
INSERT INTO ch7_input(event_time, event_id, device, message)
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        'evt-001', 'DEV-01', 'connection timeout');

SELECT event_id, COUNT(*) AS received_rows
  FROM ch7_input
 GROUP BY event_id;

DROP TABLE ch7_input;
```

`evt-001`の件数は2です。名前が同じでもLOGは重複を除去しません。
収集アプリケーションの「送信完了」と、元のイベントを「一度だけ保存すること」は別の問題です。

<a id="입력-경로는-데이터-위치와-발생-방식으로-고릅니다"></a>

## 入力方法の選択

| 状況 | 最初に検討する方法 | 併せて確認する項目 |
|---|---|---|
| 少量入力・機能確認 | SQL INSERT | カラムリスト、型、日付書式 |
| アプリケーションからの継続的な大量入力 | SDK Append | バッファ送信、行単位の失敗、再接続ポリシー |
| クライアントが読み込むCSV | csvimport・machloader | カラムマッピング、失敗行ファイル |
| サーバーから読み込めるロード用ファイル | LOAD DATA INFILE | サーバー上のパスとファイルアクセス権限 |

SQL INSERTには文ごとの処理コストがあります。継続的な大量入力には、複数行をまとめて送信するAppend APIを検討してください。
言語別の実行コードは[開発とアプリケーション連携](/dbms/development-tools-integration/)から選択できます。

<a id="append에서는-전송과-결과-확인을-분리해-생각하세요"></a>

## Appendの送信とエラー処理

Appenderに行を渡した時点では、データがクライアントバッファに残っている場合があります。
使用するSDKのflush・closeの動作を確認し、正常終了時だけでなく例外発生時にも、残りのバッファと接続を処理してください。

呼び出しが成功しても、すべての行が保存されたとは限りません。
SDKによって、戻り値、エラーコールバック、終了時の成功・失敗件数など、結果の確認方法が異なります。
長さ超過、NULL、日付変換エラーを意図的に含めた小さなバッチで、先に確認することを推奨します。

応答を受け取る前に接続が切れる場合は特に注意が必要です。
保存済みのバッチを再送する可能性があるため、元のイベントIDと処理位置を記録してください。
LOGのINSERT・Appendは、TRANSACTIONテーブルのトランザクションのROLLBACK対象でもありません。

<a id="파일-적재는-성공-건수보다-매핑을-먼저-봅니다"></a>

## ファイルロードとマッピング

韓国語・空文字列・NULL・長いメッセージ・異なるタイムゾーンを含むサンプルを用意してください。
元のフィールド数と対象カラムの順序が一致することを確認してから、ファイル全体を処理します。
同じエラーを再分析できるよう、失敗行ファイルとログも保存してください。

コマンド全体は[データ入力・ロード・エクスポート](/dbms/development-tools-integration/data-input-load-export/)を参照してください。
過去データの移行で`_arrival_time`を保持するには、ソート順と移行先の既存データも確認する必要があります。
通常の収集で過去の発生時刻を扱う場合は、別の`event_time`に保存するほうが安全です。

問題が起きたら、バッチ全体より先に、失敗した元の1行を確認してください。
フィールド値、対象の型、使用した入力APIを合わせて確認すると原因を特定しやすくなります。
