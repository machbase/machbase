---
title : '참조 데이터의 입력'
type: docs
weight: 20
---

휘발성 테이블의 입력 및 갱신 방법과 대부분 동일하다.

한가지 차이점이 있다면 참조 테이블에 Append를 통해 데이터를 입력할 경우 'LOOKUP_APPEND_UPDATE_ON_DUPKEY ' Property 를 설정해 Primary Key가 중복일 경우에 해당 Row를 Update 하도록 설정 가능하다.

'LOOKUP_APPEND_UPDATE_ON_DUPKEY'에 대한 세부 내용은 [Property](/kr/setting-monitoring/property.md) 가이드를 참고한다.

## 참조 테이블 재로딩

마크베이스 6.7 부터 참조 테이블 데이터를 룩업 노드가 관리하도록 수정되었다.

룩업 노드로부터 참조 테이블 데이터를 다시 불러오고 싶다면

EXEC TABLE_REFRESH 명령어를 사용하면된다.

```sql
EXEC TABLE_REFRESH(lktable);
```
