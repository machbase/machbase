---
layout : post
title : メタテーブル
type : docs
toc: true
weight: 0
---

## 目次 {#index}

- [目次](#index)
- [ユーザーオブジェクト](#user-objects)
  - [M$SYS_TABLES](#msys_tables)
  - [M$SYS_TABLE_PROPERTY](#msys_table_property)
  - [M$SYS_COLUMNS](#msys_columns)
  - [M$SYS_INDEXES](#msys_indexes)
  - [M$SYS_INDEX_COLUMNS](#msys_index_columns)
  - [M$SYS_TABLESPACES](#msys_tablespaces)
  - [M$SYS_TABLESPACE_DISKS](#msys_tablespace_disks)
  - [M$SYS_USERS](#msys_users)
  - [M$SYS_VIEWS](#msys_views)
  - [M$SYS_USER_ACCESS](#msys_user_access)
  - [M$RETENTION](#mretention)
- [その他](#others)
  - [M$TABLES](#mtables)
  - [M$COLUMNS](#mcolumns)


メタテーブルは Machbase のスキーマ情報を表示するテーブルです。名前は M$ で始まります。

テーブル名、列、インデックスなどの情報を保持し、DDL による作成、変更、削除を反映します。
ユーザーがメタテーブルのデータを追加、削除、変更することはできません。


## ユーザーオブジェクト {#user-objects}

### M$SYS_TABLES {#msys_tables}
---

ユーザーが作成したテーブルを表示します。

| 列名 | 説明 |
|--|--|
|NAME|テーブル名|
|TYPE|テーブル型<br> - 0：Log<br> - 1：Fixed<br> - 3：Volatile<br> - 4：Lookup<br> - 5：Key Value<br> - 6：Tag|
|DATABASE_ID|データベース識別子|
|ID|テーブル識別子|
|USER_ID|テーブルを作成したユーザー|
|COLCOUNT|列数|
|FLAG|テーブルの分類<br> - 1：Tag データテーブル<br> - 2：ロールアップテーブル<br> - 4：Tag メタテーブル<br> - 8：Tag 統計テーブル|

### M$SYS_TABLE_PROPERTY {#msys_table_property}
---

各テーブルに適用されたプロパティを表示します。

| 列名 | 説明 |
|--|--|
|ID|テーブル識別子|
|NAME|プロパティ名|
|VALUE|プロパティ値|


### M$SYS_COLUMNS {#msys_columns}
---

M$SYS_TABLES に表示されるユーザーテーブルの列情報です。

| 列名 | 説明 |
|--|--|
|NAME|列名|
|TYPE|列の型|
|DATABASE_ID|データベース識別子|
|ID|列識別子|
|LENGTH|列の長さ|
|TABLE_ID|列が属するテーブルの識別子|
|FLAG|サーバー内部用の情報|
|PART_PAGE_COUNT|パーティションあたりのページ数|
|PAGE_VALUE_COUNT|ページあたりのデータ数|
|MINMAX_CACHE_SIZE|MIN-MAX キャッシュのサイズ|
|MAX_CACHE_PART_COUNT|パーティションキャッシュの最大数|
|NEXTVAL|シーケンスメタデータを使用する列の次のシーケンス値|


### M$SYS_INDEXES {#msys_indexes}
---

ユーザーが作成したインデックスを表示します。

| 列名 | 説明 |
|--|--|
|NAME|インデックス名|
|TYPE|インデックスの型|
|DATABASE_ID|データベース識別子|
|ID|インデックス識別子|
|TABLE_ID|インデックスが属するテーブルの識別子|
|COLCOUNT|インデックスの列数|
|PART_VALUE_COUNT|インデックステーブルのパーティションあたりのデータ数|
|KEY_COMPRESS|キー値の圧縮設定|
|MAX_LEVEL|インデックスの最大レベル（LSM のみ）|
|PAGE_SIZE|ページサイズ|
|MAX_KEYWORD_SIZE|キーワードの最大長（KEYWORD のみ）|
|BITMAP_ENCODE|ビットマップのエンコード方式（RANGE / EQUAL）|


### M$SYS_INDEX_COLUMNS {#msys_index_columns}
---

M$SYS_INDEXES に表示されるユーザーインデックスの列情報です。

| 列名 | 説明 |
|--|--|
|INDEX_ID|インデックス識別子|
|INDEX_TYPE|インデックスの型|
|NAME|列名|
|COL_ID|列識別子|
|DATABASE_ID|データベース識別子|
|TABLE_ID|テーブル識別子|
|TYPE|列のデータ型|


### M$SYS_TABLESPACES {#msys_tablespaces}
---

ユーザーが作成したテーブルスペースを表示します。

| 列名 | 説明 |
|--|--|
|NAME|テーブルスペース名|
|ID|テーブルスペース識別子|
|DISK_COUNT|テーブルスペースのディスク数|


### M$SYS_TABLESPACE_DISKS {#msys_tablespace_disks}
---

テーブルスペースが使用するディスク情報です。

| 列名 | 説明 |
|--|--|
|NAME|ディスク名|
|ID|ディスク識別子|
|TABLESPACE_ID|ディスクが属するテーブルスペースの識別子|
|PATH|ディスクのパス|
|IO_THREAD_COUNT|ディスクに割り当てた I/O スレッド数|
|VIRTUAL_DISK_COUNT|ディスクに割り当てた仮想ディスク数|


### M$SYS_USERS {#msys_users}
---

Machbase に登録されたユーザー情報です。

| 列名 | 説明 |
|--|--|
|USER_ID|ユーザー識別子|
|NAME|ユーザー名|
|PWD_POLICY_LEVEL|パスワードポリシーレベル|
|VALID_BEFORE|パスワードの有効期限|

### M$SYS_VIEWS {#msys_views}
---

ビューの定義を表示します。

| 列名 | 説明 |
|--|--|
|USER_NAME|所有者のユーザー名|
|DB_NAME|データベース名|
|VIEW_NAME|ビュー名|
|VIEW_SQL|ビューを定義する SQL テキスト|

### M$SYS_USER_ACCESS {#msys_user_access}
---

テーブルに対して付与されたユーザー権限を表示します。

| 列名 | 説明 |
|--|--|
|USER_NAME|ユーザー名|
|TABLE_NAME|テーブル名|
|PRIV|権限名|

### M$RETENTION {#mretention}
---

保持ポリシーの情報を表示します。

| 列名 | 説明 |
|-------------|----------------|
| USER_ID | ユーザー ID |
| POLICY_NAME | ポリシー名 |
| DURATION | 保持期間（秒） |
| INTERVAL | 更新間隔（秒） |

## その他 {#others}

### M$TABLES {#mtables}
---

M$ で始まるすべてのメタテーブルを表示します。

| 列名 | 説明 |
|--|--|
|NAME|メタテーブル名|
|TYPE|テーブル型|
|DATABASE_ID|データベース識別子|
|ID|メタテーブル識別子|
|USER_ID|テーブルのユーザー（SYS）|
|COLCOUNT|列数|


### M$COLUMNS {#mcolumns}
---

M$TABLES に表示されるメタテーブルの列情報です。

| 列名 | 説明 |
|--|--|
|NAME|列名|
|TYPE|列の型|
|DATABASE_ID|データベース識別子|
|ID|列識別子|
|LENGTH|列の長さ|
|TABLE_ID|列が属するテーブルの識別子|
|FLAG|サーバー内部用の情報|
|PART_PAGE_COUNT|パーティションあたりのページ数|
|PAGE_VALUE_COUNT|ページあたりのデータ数|
|MINMAX_CACHE_SIZE|MIN-MAX キャッシュのサイズ|
|MAX_CACHE_PART_COUNT|パーティションキャッシュの最大数|
