---
layout : post
title : '스트림 실행 및 종료'
type: docs
weight: 20
---

## 스트림 실행

저장 프로시저를 이용하여 등록된 스트림을 실행한다. 한번 실행한 스트림은 지속적으로 실행되며 서버를 재시작하더라도 마지막으로 실행한 시점 이후에 입력된 데이터에 대해서 계속 스트림 질의를 실행한다.

```sql
EXEC STREAM_START(stream_name);
```

## 스트림 종료

실행중인 스트림을 종료시키기 위해서 아래의 저장 프로시저를 이용한다.

```sql
EXEC STREAM_STOP(stream_name);
```

## 스트림의 직접 실행

스트림 실행 조건을 BY USER로 설정한 경우, 사용자에 의한 명시적 호출 없이는 해당 질의가 수행되지 않는다. 이 스트림 질의를 실행하기 위해 다음의 저장프로시저를 이용한다.

```sql
EXEC STREAM_EXECUTE(stream_name);
```

호출할 스트림 질의를 생성할 때, BY USER조건으로 생성하지 않았거나, STREAM_START로 실행 상태로 전환하지 않은 경우, 오류가 발생한다.

