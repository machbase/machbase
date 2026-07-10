---
title: '9.4 데이터 입력과 변경'
weight: 40
toc: true
---
LOOKUP 테이블의 데이터 입력, 갱신, 삭제 방법을 다룬다.


<a id="original-85-inserting-data"></a>

## Lookup 데이터 입력


입력 및 업데이트 방법은 대부분 Volatile 테이블과 동일하다.

차이점은 APPEND로 데이터를 삽입할 때 primary key가 중복되면 'LOOKUP_APPEND_UPDATE_ON_DUPKEY' 속성을 설정해 해당 행을 업데이트할 수 있다는 점이다.

자세한 내용은 [Property](../../../configuration/property/#lookup_append_update_on_dupkey) 가이드를 참고한다.


### Lookup 테이블 리로드

Machbase 6.7부터 Lookup Node가 Lookup 테이블 데이터를 관리한다.

Lookup 노드에서 데이터를 리로드하려면 EXEC TABLE_REFRESH 명령을 사용한다.

```sql
EXEC TABLE_REFRESH(lktable);
```

<a id="original-85-deleting-data"></a>

## Lookup 데이터 삭제


Volatile 테이블과 동일하다.
