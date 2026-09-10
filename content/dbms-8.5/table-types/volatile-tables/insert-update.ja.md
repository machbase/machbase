---
title : Volatile データの挿入と更新
type : docs
weight: 30
toc: true
---

## データの挿入 {#data-insert}

Volatile テーブルには次のようにデータを挿入します。

```sql
Mach> create volatile table vtable (id integer, name varchar(20));
Created successfully.
Mach> insert into vtable values(1, 'west device');
1 row(s) inserted.
Mach> insert into vtable values(2, 'east device');
1 row(s) inserted.
Mach> insert into vtable values(3, 'north device');
1 row(s) inserted.
Mach> insert into vtable values(4, 'south device');
1 row(s) inserted.
```


## データの APPEND {#data-append}

Machbase が提供する、高速なリアルタイムデータ挿入 API です。
C、C++、C#、Java、Python、PHP、JavaScript から利用できます。

```sql
Mach> create volatile table vtable (id integer, value double);
```

```c
SQL_APPEND_PARAM sParam[2];
for(int i=0; i<10000; i++)
{
    sParam[0].mInteger  = i;
    sParam[1].mDouble   = i;
    if (SQLAppendDataV2(stmt, sParam) != SQL_SUCCESS)
    {
        break;
    }
}
```

Cluster Edition の APPEND は、Leader Broker を経由する必要があります。

詳細は [SDK と連携](../../../sdk-integration/)を参照してください。


## データの更新 {#data-update}

Volatile テーブルへの挿入時に主キーが重複した場合は、ON DUPLICATE KEY UPDATE 句で既存データを更新できます。

### 挿入する値で更新 {#update-data-value-to-be-inserted}

通常の INSERT では、既存データと主キーが重複すると挿入が失敗します。挿入の代わりに既存データを更新する場合は、ON DUPLICATE KEY UPDATE 句を追加します。

* 主キーが重複しない場合は、指定したデータをそのまま挿入します。
* 主キーが重複する場合は、挿入用に指定した値で既存データを更新します。

この機能には、次の制約があります。

* Volatile テーブルに主キーを定義する必要があります。
* 挿入するデータに主キーの値を含める必要があります。

```sql
Mach> create volatile table vtable (id integer primary key, direction varchar(10), refcnt integer);
Created successfully.
Mach> insert into vtable values(1, 'west', 0);
1 row(s) inserted.
Mach> insert into vtable values(2, 'east', 0);
1 row(s) inserted.
Mach> select * from vtable;
ID          DIRECTION   REFCNT     
----------------------------------------
1           west       0          
2           east        0          
[2] row(s) selected.
 
Mach> insert into vtable values(1, 'south', 0);
[ERR-01418 : The key already exists in the unique index.]
Mach> insert into vtable values(1, 'south', 0) on duplicate key update;
1 row(s) inserted.
 
Mach> select * from vtable;
ID          DIRECTION   REFCNT     
----------------------------------------
1           south        0          
2           east        0          
[2] row(s) selected.
```

### 更新する値を指定 {#specify-data-value-to-be-updated}

挿入用の値とは異なる列の値で更新するには、ON DUPLICATE KEY UPDATE SET 句を使用します。SET 句で更新値を指定します。

* 主キーが重複しない場合は、挿入用のデータをそのまま挿入します。
* 主キーが重複する場合は、SET 句で指定した値だけを使用して既存データを更新します。
* **主キーの値は更新対象に指定できません。**
* SET 句で指定していない列は更新されません。

```sql
Mach> create volatile table vtable (id integer primary key, direction varchar(10), refcnt integer);
Created successfully.
Mach> insert into vtable values(1, 'west', 0);
1 row(s) inserted.
Mach> insert into vtable values(2, 'east', 0);
1 row(s) inserted.
Mach> select * from vtable;
ID          DIRECTION   REFCNT     
----------------------------------------
1           west        0          
2           east        0          
[2] row(s) selected.
 
Mach> insert into vtable values(1, 'west', 0) on duplicate key update set refcnt = 1;
1 row(s) inserted.
 
Mach> select * from vtable;
ID          DIRECTION   REFCNT     
----------------------------------------
1           west        1          
2           east        0          
[2] row(s) selected.
```
