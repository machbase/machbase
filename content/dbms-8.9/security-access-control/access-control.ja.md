---
type: docs
title: '14.5 アクセス制御'
weight: 50
toc: true
---

`GRANT_REMOTE_ACCESS`、`BIND_IP_ADDRESS`、OS またはクラウドのファイアウォールを併用して、
ネットワーク接続範囲を制限します。現在値は次のように確認します。

```sql
SELECT NAME, VALUE
  FROM V$PROPERTY
 WHERE NAME IN ('GRANT_REMOTE_ACCESS', 'BIND_IP_ADDRESS');
```

リスナー設定はサーバー起動時に適用されます。稼働中のリスナーが自動的に再バインドされるとは考えず、
`machbase.conf` を変更してから承認済みの再起動手順を実施してください。

<a id="remote-access-configuration"></a>

## リモート接続設定

`GRANT_REMOTE_ACCESS` はリモートクライアント接続の可否を制御します。

```ini
# リモート接続を許可
GRANT_REMOTE_ACCESS = 1

# リモート接続を遮断
GRANT_REMOTE_ACCESS = 0
```

変更前に次を確認します。

1. アプリケーション、監視、バックアップクライアントの接続元
2. ローカル管理接続を維持する方法
3. 再起動後にリモート・緊急接続の両方を試験する順序

`GRANT_REMOTE_ACCESS=1` で全リモートアドレスを許可することがないよう、
ファイアウォールの許可リストも設定してください。

<a id="network-exposure-bind-ip-address"></a>

## BIND_IP_ADDRESS とネットワーク公開範囲

`BIND_IP_ADDRESS` は IPv4 リスナーがバインドするアドレスです。

```ini
# すべての IPv4 インターフェース
BIND_IP_ADDRESS = 0.0.0.0

# ローカル IPv4 インターフェース
BIND_IP_ADDRESS = 127.0.0.1

# 指定した内部 IPv4 インターフェース
BIND_IP_ADDRESS = 10.0.0.5
```

サーバーにないアドレスを指定すると起動に失敗する場合があります。変更前に現在のインターフェースを
確認し、再起動後に OS ツールで実際の待ち受けアドレスとポートを検証します。

`0.0.0.0` が必要な場合は、ファイアウォールまたはセキュリティグループで接続元アドレスとポートを
制限します。具体的なコマンドは OS とネットワークポリシーで異なるため、本書の固定コマンドを
そのまま適用しないでください。
