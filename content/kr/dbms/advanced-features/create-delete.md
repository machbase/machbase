---
title : STREAM 생성과 삭제
type: docs
weight: 10
---

##  STREAM 생성

STREAM 쿼리는 Insert... Select 형태로만 생성할 수 있습니다. STREAM을 생성할 때 쿼리가 정상적으로 실행될 수 있는지 검사됩니다.
다음 저장 프로시저를 사용하여 STREAM을 생성합니다.

STREAM이 성공적으로 생성되어도 실행은 즉시 시작되지 않습니다. 자세한 내용은 STREAM 시작과 종료를 참조하십시오.

```sql
EXEC STREAM_CREATE(stream_name, stream_query_string);
```

기본 STREAM 쿼리는 입력되는 모든 데이터에 대해 실행됩니다. 이 경우 SUM 및 AVG와 같은 통계 쿼리는 사용할 수 없습니다.

```sql
EXEC STREAM_CREATE(normal_query, 'INSERT INTO CEP_LOG_TABLE SELECT * FROM EVENT WHERE C1 = 0');
```

그러나 insert select 문의 끝에 STREAM 쿼리를 실행할 주기를 설정하면 입력 데이터에 대한 통계 쿼리를 정기적으로 사용할 수 있습니다.

```sql
EXEC STREAM_CREATE(aggr_1_sec, 'insert into aggr select sum(i1), i2 from base group by i2 BY 1 SECOND');
```

위의 STREAM 쿼리는 매초마다 마지막 실행 이후 입력된 최신 데이터에 대해 group by 쿼리를 실행하고 그 결과를 "aggr" 로그 테이블에 입력합니다.

사용자가 STREAM 쿼리의 실행 시간을 정의하고 싶으면 실행 주기 설정 부분에 다음과 같이 지정합니다.

STREAM 쿼리는 사용자의 명시적인 호출 전에는 실행되지 않습니다.

```sql
EXEC STREAM_CREATE(base_trig, 'insert into aggr select sum(i1), i2 from base group by i2 BY USER');
```

STREAM 쿼리를 실행하는 조건이 BY USER이면 STREAM_EXECUTE 프로시저를 사용하여 STREAM 쿼리를 명시적으로 호출할 때까지 실행되지 않습니다.

이는 STREAM_EXECUTE로 호출되면 이전에 읽은 데이터를 제외하고 실행 중에 추가된 증분 데이터에 대해서만 STREAM 쿼리를 실행합니다.

##  STREAM 삭제

생성된 STREAM 목록은 V$STREAMS 메타 테이블을 사용하여 조회할 수 있습니다. STREAM을 삭제하려면 STREAM을 생성할 때 결정한 STREAM 이름을 매개변수로 하여 다음 저장 프로시저를 사용합니다.

```sql
EXEC STREAM_DROP(stream_name);
```

실행 중인 STREAM은 삭제할 수 없습니다. STREAM을 삭제하기 전에 먼저 STREAM을 종료해야 합니다. 자세한 내용은 STREAM 시작과 종료를 참조하십시오.


## V$STREAMS

DB 서버에 등록된 STREAM의 현재 상태를 확인하는 메타 테이블입니다. 자세한 설명은 매뉴얼의 가상 테이블 섹션에 제공됩니다.
