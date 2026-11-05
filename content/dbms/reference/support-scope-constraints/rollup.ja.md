---
type: docs
title: '16.6.6 ROLLUPのサポート範囲'
weight: 60
toc: true
aliases:
  - /dbms/tag-rollup-usage/support-scope-rollup/
---

<a id="support-scope-rollup-rebuild-cluster"></a>

## Editionとテーブルの範囲

| 機能 | Standard | Cluster |
|---|:---:|:---:|
| 時間軸TAGの通常・条件付き・拡張ROLLUPの作成・参照・制御 | O | O |
| WITH ROLLUPによる自動作成 | O | O |
| 対応するJSONパス・ドキュメント全体の集計 | O | O |
| Custom INTO...AS | O | X |
| ROLLUP_REBUILD | 限定された対象・引数でサポート | X |

距離軸TAG、LOG、TRANSACTION、VOLATILE、LOOKUPには時間軸ROLLUPを適用しません。
Clusterの状態は、関連するノードと階層ごとに確認します。

## 作成タイプと列

| タイプ | 必要な条件 |
|---|---|
| 通常の数値 | 対応する数値DATA列。明示的に作成する場合はSUMMARIZEDは必須ではない |
| JSONパス | JSON DATA列と集計対象の数値パス |
| JSONドキュメント全体 | JSON SUMMARIZED列 |
| WITH ROLLUP | 時間軸TAGの3番目のSUMMARIZED列 |
| FROM階層 | より大きな整数倍の間隔と、同一の拡張・モード条件 |
| Custom | ソースとなる時間軸TAGが1つ、事前作成した互換性のある出力先TAG |

## 集計と選択

通常の数値ROLLUPはMIN/MAX/SUM/COUNT/AVG/SUMSQを提供し、拡張ROLLUPはFIRST/LASTも提供します。
Customの部分結果はユーザーが再集計します。平均は合計と有効件数を使い、FIRST/LASTは対応する元時刻と補助キーを
保持して統合します。JSONドキュメント全体のCOUNTは保存された集計件数であり、元のCOUNT(value)と
常に一致するわけではありません。

候補の選択は条件・列・パス・モード・間隔に依存します。通常/拡張だけで優先順位を断定したり、
日単位のバケットに24 HOUR ROLLUPが自動適用されると仮定したりしないでください。
[クエリ規則](../../../tag-rollup-usage/query-syntax-rollup/)を確認してください。

## REBUILDと作成のサポート範囲の違い

REBUILDの対象は、完全な自動SEC/MIN/HOUR階層と、対応するCustom経路です。任意の手動名、
一部のみの自動階層、10 MIN Customなど、作成可能なすべての構成を再構築できるわけではありません。
現在のCustomの時間境界処理間隔は1 SEC・1 MIN・1 HOURであり、SELECTのバケットにも一致する必要があります。
定数の時刻引数、バケット全体への拡張、状態遷移、エラー後の確認は
[REBUILDリファレンス](../../sql/syntax/rollup-rebuild-syntax/)に従います。

## 権限

作業用アカウントに、対象データベースへの接続と作成・削除・参照などの必要な権限を付与します。
次は既存の作業用アカウントに作成・削除権限を付与する例であり、必要な権限をすべて一括設定する
スクリプトではありません。

```sql
GRANT CREATE, DROP ON DATABASE MACHBASEDB TO rollup_user;
```

[権限管理](../../../security-access-control/privileges/)で所有者と作業範囲を確認してください。

## 複合キーFIRST/LASTの対応範囲

> 複合キーFIRST/LASTとソート付きEXTENSION ROLLUPはMachbase 8.7.3から対応します。エディション別の制約は以下を確認してください。

複合キーの元データ照会と数値対象のソート付きEXTENSION ROLLUPは、8.7.3からStandard・Clusterで対応します。
Custom ROLLUPの作成とworkerはStandard専用であり、Clusterは`ERR-02837`を返します。
通常のTAGに保存済みの要約行を複合FIRST/LASTで再集計するSELECTは、Clusterでも
通常の分散TAG照会として対応します。ソート付きROLLUP定義の第1キーはBASETIMEですが、
通常のTAG再集計で使う元の候補時刻にこの制約は適用しません。

公開ROWID補助キーはStandard専用で、明示的に指定します。元の行識別子を保持しますが、
入力順序を意味せず、既存のROWID制限も維持します。Clusterは非対応です。
DECIMALソートキーにも対応します。照会キー・方向は保存定義と一致する必要があります。
Clusterの全ノードに同じ対応ビルドを配備し、異なるバイナリの混在は避けてください。

ソート付きROLLUPのDBを非対応の旧バイナリで開く、またはMOUNTする運用は、
メタバージョン検査を通過しても非対応です。戻す場合は導入前のバックアップを復元します。
ソート付きオブジェクトのDROPだけでは互換性を保証しません。
[移行・ロールバック制約](../../../tag-rollup-usage/extension-rollup/#ordered-rollup-compatibility)を確認してください。

[完全なデータとソート付きROLLUPの例](../../../tag-rollup-usage/extension-rollup/#composite-first-last)。
