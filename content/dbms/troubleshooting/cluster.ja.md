---
type: docs
title: '15.6 Cluster の問題'
weight: 60
toc: true
---

<a id="node-state-status-abnormal-cluster"></a>

## Cluster ノードの状態が異常な場合

トポロジー変更や再起動の前に、全体状態と最初のエラーを収集します。

```bash
machcoordinatoradmin --cluster-status
machclusterctl status
```

1. Coordinator、Broker、Warehouse のどの役割が最初に異常となったか確認します。
2. 対象ノードと先行する役割のログ時刻を合わせて比較します。
3. ホスト、プロセス、ディスク、ネットワーク、設定変更履歴を確認します。
4. 複製・再配置の状態とクライアントへの影響を記録します。
5. 13章の承認済み復旧手順で1ノードずつ対応し、全体状態を再検証します。

ノード名やサービス・ノード間ポートを推測して start/add/remove を実行しないでください。
実際の `cluster.yaml` とデプロイツールのヘルプを使います。詳細な制約は
[Cluster の運用](/dbms/operations-configuration-recovery/cluster/)を参照してください。

<a id="error-cluster-edition"></a>

## Cluster Edition の制限エラー

```sql
SELECT * FROM V$VERSION;
```

Edition の制限か判断する際は、現行 Edition と
[Edition 別サポート範囲](/dbms/reference/support-scope-constraints/)を比較します。Standard 専用機能の
非公式な回避手順は使わず、同じ要件を満たす Cluster 対応機能や別の Standard 環境を検討してください。
