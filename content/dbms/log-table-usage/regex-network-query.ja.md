---
type: docs
title: '7.12 ネットワーク型のクエリ'
weight: 120
toc: true
---

IPアドレスを文字列で保存すると読みやすい反面、文字列のソート順とアドレス範囲の順序が同じだと考えがちです。
アドレスの比較が目的ならIPV4・IPV6型を使用し、元の表記も必要な場合だけ別の文字列を併せて保存してください。

<a id="design-type-network-data-types"></a>

<a id="범위의-양-끝과-null을-함께-준비합니다"></a>

## ネットワークデータの準備

```sql
CREATE LOG TABLE ch7_network (
    event_id INTEGER,
    src_ip   IPV4,
    dst_ip   IPV6,
    dst_port INTEGER
);
INSERT INTO ch7_network VALUES (1, '192.0.2.1',   '2001:db8::1', 80);
INSERT INTO ch7_network VALUES (2, '192.0.2.255', '2001:db8::2', 65535);
INSERT INTO ch7_network VALUES (3, '198.51.100.1', '2001:db8::3', 443);
INSERT INTO ch7_network VALUES (4, NULL, NULL, NULL);

SELECT event_id, src_ip, dst_ip, dst_port FROM ch7_network ORDER BY event_id;
```

4行が返されます。ポートにはINTEGERを使用します。
USHORTの最大値65535はNULLの予約値なので、ポートの全範囲をそのまま表現する用途には適しません。

<a id="동등-비교와-범위-조회를-구분합니다"></a>

## 等価比較と範囲検索

```sql
SELECT event_id FROM ch7_network
 WHERE src_ip BETWEEN '192.0.2.1' AND '192.0.2.255'
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE src_ip IN ('192.0.2.1', '198.51.100.1')
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE dst_ip = '2001:db8::2'
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE dst_ip BETWEEN '2001:db8::1' AND '2001:db8::2'
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE src_ip IS NULL
 ORDER BY event_id;
```

| 条件 | 選択されるevent_id |
|---|---|
| IPv4 BETWEEN | 1, 2 |
| IPv4 IN | 1, 3 |
| IPv6等価比較 | 2 |
| IPv6 BETWEEN | 1, 2 |
| IPv4 IS NULL | 4 |

BETWEENは両端のアドレスを含みます。この例のIPv4範囲はCIDRの意味を自動適用するものではなく、
明示的に指定した2つのアドレス間の範囲です。
ネットワーク範囲への所属を判定する場合は、次の`CONTAINED`を使用してください。
NULLは`= NULL`ではなく`IS NULL`で検査します。

<a id="cidr-대역으로-판정합니다"></a>

## CIDRによる判定

アドレスが特定のネットワークに属するかを検査するには、`CONTAINED`を使用します。
範囲は必ず`アドレス/prefix`形式で指定します。IPv4とIPv6の両方で使用できます。

```sql
SELECT event_id FROM ch7_network
 WHERE src_ip CONTAINED '192.0.2.0/24'
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE dst_ip CONTAINED '2001:db8::/32'
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE src_ip NOT CONTAINED '192.0.2.0/24'
 ORDER BY event_id;
```

| 条件 | 選択されるevent_id |
|---|---|
| IPv4 `CONTAINED '192.0.2.0/24'` | 1, 2 |
| IPv6 `CONTAINED '2001:db8::/32'` | 1, 2, 3 |
| IPv4 `NOT CONTAINED '192.0.2.0/24'` | 3 |

向きを逆にした`'192.0.2.0/24' CONTAINS src_ip`も同じ意味です。
左辺にネットワーク、右辺にアドレスを指定する形式が`CONTAINS`で、その逆が`CONTAINED`です。

prefixを省略して`CONTAINED '192.0.2.0'`と書くと、ネットワークとして解釈できずエラーになります。
アドレスがNULLのイベント4はいずれの条件でも選択されません。
未収集のアドレスも数える場合は、`IS NULL`条件を別途指定してください。

<a id="혼합-주소와-원본-표기-정책을-먼저-정하세요"></a>

## アドレス形式と元の表記の保持

IPv4だけを入力する場合はIPV4、IPv6を入力する場合はIPV6でスキーマを定義します。
両方を扱う場合は、入力変換とカラム分離のポリシーを先に定め、実際のサンプルで検証してください。
暗黙の変換が常に意図どおりに元のアドレスを正規化するとは限りません。

出力文字列には注意が必要です。同じIPv6アドレスでも、元の圧縮表記と検索結果の表記が異なる場合があります。
原文を証跡として残す必要がある場合は、アドレス型カラムと原文カラムを分離すると明確です。

大量データでは、アドレス条件に加えて`_arrival_time`の範囲を制限し、実行計画を確認してください。
メッセージの正規表現検索は[テキスト検索](../text-search-keyword-index/#regex)と
[SQL関数リファレンス](/dbms/reference/sql/functions/)を参照してください。

```sql
DROP TABLE ch7_network;
```

アドレス検索の結果が予想と異なる場合は、元の文字列、入力型、範囲の両端を並べて比較してください。
文字列表現の違いか、実際のアドレス範囲の違いかを区別しやすくなります。
