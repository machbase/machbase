---
title : Volatile インデックスの作成と管理
type : docs
weight: 50
toc: true
---

##  インデックスの作成と使用 {#create-and-use-index}

Volatile テーブルは、リアルタイム検索に最適化された RED-BLACK ツリーを提供します。すべてのデータ型にインデックスを設定できます。ただし、1 列につき作成できるインデックスは 1 つで、複合インデックスはサポートしません。

```sql
Mach> create volatile table vtable (id integer, name varchar(10));
Created successfully.
Mach> create index idx_vrb on vtable (name) index_type redblack;
Created successfully.
Mach> desc vtable;
----------------------------------------------------------------
NAME                          TYPE                LENGTH       
----------------------------------------------------------------
ID                            integer             11             
NAME                          varchar             10                 
 
[ INDEX ]                             
----------------------------------------------------------------
NAME                          TYPE                COLUMN
----------------------------------------------------------------
IDX_VRB                       REDBLACK            NAME               
Mach>
```


##  主キーインデックス {#primary-key-index}

Volatile テーブルの列に主キーを指定すると、RED-BLACK ツリーインデックスが自動的に作成されます。このインデックスは一意性を保証し、重複する値を許可しません。

```sql
Mach> create volatile table vtable (id integer primary key, name varchar(20));
Created successfully.
Mach> desc vtable;
----------------------------------------------------------------
NAME                          TYPE                LENGTH       
----------------------------------------------------------------
ID                            integer             11             
NAME                          varchar             20                 
 
[ INDEX ]                             
----------------------------------------------------------------
NAME                          TYPE                COLUMN
----------------------------------------------------------------
__PK_IDX_VTABLE               REDBLACK            ID  
 
Mach>
```


##  その他のインデックスの種類 {#other-index-types}

Log テーブルで使用するビットマップインデックスとキーワードインデックスは、Volatile テーブルでは使用できません。

```sql
Mach> create bitmap   index idx_1237 on vtable(id);
[ERR-02069: BITMAP index can only be created for LOG table.]
Mach> create keyword  index idx_1238 on vtable(name);
[ERR-02069: KEYWORD index can only be created for LOG table.]
```
