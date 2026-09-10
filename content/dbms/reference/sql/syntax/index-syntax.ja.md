---
type: docs
title: 'INDEX'
weight: 150
toc: true
---

インデックス構文とテーブルタイプ別のサポート範囲を説明します。
インデックスは検索コストを減らす一方、入力・変更時の維持コストが発生するため、実際の条件と実行計画を確認してから追加してください。

<a id="create-index"></a>

## CREATE INDEX

<span class="badge-since">Machbase 8.7.0からサポートする機能</span>

```sql
create_index_stmt ::=
    'CREATE' index_modifier? 'INDEX' [ 'IF NOT EXISTS' ] index_name
    'ON' index_target '(' index_column_list ')'
    [ 'INDEX_TYPE' ( 'LSM' | 'KEYWORD' | 'BITMAP' | 'REDBLACK' | 'TAG' ) ]
    [ 'TABLESPACE' tablespace_name ]
    [ index_property_list ]

index_modifier ::= 'UNIQUE' | 'PRIMARY KEY'

index_target ::= table_name | table_name 'METADATA'

index_column_list ::=
    column_name ( ',' column_name )*
  | column_name json_path

index_property_list ::=
    ( 'MAX_LEVEL'        '=' number
    | 'PAGE_SIZE'        '=' number
    | 'BITMAP_ENCODE'    '=' ( 'EQUAL' | 'RANGE' )
    | 'PART_VALUE_COUNT' '=' number )
    ( ',' index_property_list )*
```

<a id="create-index-if-not-exists"></a>

### IF NOT EXISTS

`IF NOT EXISTS`を指定すると、同じデータベースと所有者に同名のインデックスがある場合、エラーなしで成功し、既存のインデックスを保持します。

- 同名のインデックスがなければ、テーブル、列、インデックスタイプ、プロパティ、権限を通常のCREATE INDEXと同様に検証して作成します。
- 同名のインデックスがあれば、テーブル、列、インデックスタイプ、JSONパス、プロパティを比較・変更しません。
- 重複判定の名前空間は`database + owner + index name`です。別のデータベースや所有者の同名インデックスは別物です。
- オプションを省略したCREATE INDEXは、従来の名前重複エラーを返します。

{{< callout type="warning" >}}
`IF NOT EXISTS`はインデックス定義を一致させる機能ではありません。
同名のインデックスがあれば、文の対象テーブルや列が存在しない場合や定義が異なる場合も、no-opとして成功します。
繰り返しデプロイした後は、`SHOW INDEX`またはシステムカタログで実際のテーブル、列、タイプ、プロパティを確認してください。
{{< /callout >}}

```sql
CREATE LOG TABLE sensor_log_ifne (
    sensor_id INTEGER,
    value     DOUBLE
);

CREATE INDEX IF NOT EXISTS sensor_log_ifne_idx
    ON sensor_log_ifne(sensor_id);

-- 同名のインデックスがあるため成功し、既存のSENSOR_IDマッピングを保持します。
CREATE INDEX IF NOT EXISTS sensor_log_ifne_idx
    ON sensor_log_ifne(value);

SHOW INDEX sensor_log_ifne_idx;

DROP TABLE sensor_log_ifne;
```

### 条件付き作成に対応する形式

| 形式 | サポート範囲 |
|---|---|
| 一般の`CREATE INDEX IF NOT EXISTS` | 対象テーブルタイプがサポートする一般インデックス |
| `CREATE UNIQUE INDEX IF NOT EXISTS` | Standard EditionのTRANSACTIONテーブル |
| `CREATE PRIMARY KEY INDEX IF NOT EXISTS` | Standard EditionのTRANSACTIONテーブル |
| TAG DATAのJSONパス / TAG METADATAインデックス | Standard Edition、Cluster Edition |
| 一般構文の`INDEX_TYPE`句 | 対象テーブルタイプとインデックスタイプの既存サポート範囲 |

非推奨の専用構文`CREATE BITMAP INDEX`、`CREATE KEYWORD INDEX`、`CREATE REDBLACK INDEX`では、`IF NOT EXISTS`を使用できません。
一般構文を使用してください。

```sql
CREATE INDEX IF NOT EXISTS idx_message
    ON app_log(message) INDEX_TYPE KEYWORD;
```

## テーブルタイプ別のサポート範囲

| テーブルタイプ | インデックス | 主な用途 |
|------------|--------|-----------|
| LOG | LSM、KEYWORD、BITMAP | 範囲検索、テキスト検索、分析条件 |
| TAG | TAG/KVセカンダリ、JSONパス | 値列とJSONメンバーの条件 |
| TAG METADATA | 自動列インデックス、JSONパス | タグ属性の条件 |
| TRANSACTION | PRIMARY KEY、UNIQUE、一般BTREE | リレーショナルキーと複合条件 |
| VOLATILE | REDBLACK | メモリテーブルのキー・条件検索 |
| LOOKUP | REDBLACK | メモリテーブルのキー・条件検索 |

タイプを省略した場合の内部インデックスは、テーブルタイプによって異なります。
他のテーブルタイプのインデックス名を指定しても、同じ構造が作成されるとは考えないでください。

## LOGのインデックス

```sql
CREATE INDEX idx_ts ON sensor_log (ts);
CREATE INDEX idx_msg ON app_log (message) INDEX_TYPE KEYWORD;
CREATE INDEX idx_status ON sensor_log (status)
    INDEX_TYPE BITMAP BITMAP_ENCODE = RANGE;
```

| タイプ | 対象と特性 |
|------|-------------|
| LSM | LOGの標準の範囲インデックス |
| KEYWORD | VARCHAR/TEXTの`SEARCH`、`ESEARCH` |
| BITMAP | 繰り返し値の分析。VARCHAR、TEXT、BINARYには使用しない |

LSMの`MAX_LEVEL`、`PAGE_SIZE`、BITMAPの`BITMAP_ENCODE`などの属性は、データ分布とクエリ条件に基づいて測定し、決定してください。

## TAGのインデックス

タグ名と時間軸の基本アクセス構造は自動管理されます。
値列を単独条件として頻繁に使用する場合は、TAG/KVセカンダリインデックスを検討します。

```sql
CREATE INDEX idx_value ON sensor_tag (value) INDEX_TYPE TAG;
```

JSON値列は、パスごとのインデックスを作成できます。

```sql
CREATE INDEX idx_sensor ON tag_json (value.sensor.name);
CREATE INDEX idx_metric ON tag_json (value->'$.metric');
CREATE INDEX idx_item ON tag_json (value.items[0]."product-id");
```

TAG METADATAの一般列にはインデックスが自動作成されます。
METADATAのJSON列のパスを追加する場合は、次の形式を使用します。

```sql
CREATE INDEX idx_ship_owner
ON ships METADATA (info->'$.owner');
```

サポート範囲と実行計画の例は、[TAGのインデックスとパフォーマンス](/dbms/tag-table-usage/index-performance/)を参照してください。

## TRANSACTIONのインデックス

TRANSACTIONは、PRIMARY KEY、UNIQUE INDEX、一般の単一・複合インデックスをサポートします。

```sql
CREATE PRIMARY KEY INDEX idx_pk_order ON orders (order_id);
CREATE UNIQUE INDEX uidx_account_email ON account (email);
CREATE UNIQUE INDEX uidx_tenant_login ON account (tenant_id, login_name);
CREATE INDEX idx_category_name ON product (category, product_name);
```

PRIMARY KEYはテーブルごとに1つで、単一列です。
`CREATE UNIQUE INDEX`は複合列をサポートし、NULLを含むキーは他のNULLを含むキーと重複とは判定しません。
詳細な動作は、[TRANSACTIONのインデックスとパフォーマンス](/dbms/rdb-table-usage/index-performance/)を参照してください。

## VOLATILEとLOOKUPのインデックス

VOLATILEとLOOKUPはREDBLACKメモリインデックスを使用します。

```sql
CREATE INDEX idx_status ON device_status (status) INDEX_TYPE REDBLACK;
```

タイプ別の主キーと追加インデックスの設計は、次を参照してください。

- [VOLATILEのインデックスとパフォーマンス](/dbms/volatile-table-usage/index-performance/)
- [LOOKUPのインデックスとパフォーマンス](/dbms/lookup-table-usage/index-performance/)

<a id="drop-index"></a>

## DROP INDEX

```sql
drop_index_stmt ::= 'DROP INDEX' index_name
```

```sql
DROP INDEX idx_status;
```

対象インデックスを使用するセッションがある場合は、削除に失敗することがあります。
削除前に実行計画と、そのインデックスを使用する本番クエリを確認してください。

## 関連文書

- [SEARCH / ESEARCH / REGEXP](../search-esearch-regexp-syntax/)
- [クエリのパフォーマンスチューニング](/dbms/performance-tuning/performance-query-tuning/)
