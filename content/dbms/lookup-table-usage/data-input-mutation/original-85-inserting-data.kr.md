---
title: '9.4.1 Lookup 데이터 입력'
type: docs
weight: 20
---

> **8.5 원문 보강 자료**: 이 문서는 기존 8.5 매뉴얼의 내용을 새 장 구조에 맞춰 보존한 것입니다. Machbase 8.6 기준과 표현이 다른 부분은 같은 절의 최신 리뉴얼 문서를 우선합니다.

대부분의 사항은 Volatile 테이블의 입력 및 업데이트 방법과 동일합니다.

한 가지 차이점은 APPEND를 통해 Lookup 테이블에 데이터가 삽입될 때, primary key가 중복되는 경우 'LOOKUP_APPEND_UPDATE_ON_DUPKEY' 속성을 설정하여 해당 행을 업데이트할 수 있다는 것입니다.

'LOOKUP_APPEND_UPDATE_ON_DUPKEY'에 대한 자세한 내용은 [Property](../../../configuration/property/#lookup_append_update_on_dupkey) 가이드를 참조하시기 바랍니다.


## Lookup 테이블 리로드

Machbase 6.7부터 Lookup Node가 Lookup 테이블 데이터를 관리합니다.

Lookup 노드에서 Lookup 테이블 데이터를 리로드하려면 EXEC TABLE_REFRESH 명령을 사용하면 됩니다.

```sql
EXEC TABLE_REFRESH(lktable);
```
