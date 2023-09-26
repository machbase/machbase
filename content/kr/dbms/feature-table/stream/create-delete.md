---
title : '스트림 생성 및 삭제'
type: docs
weight: 10
---

## 스트림 생성

스트림 질의는 Insert... Select 의 형태로만 생성 가능하며, 스트림을 생성할 때, 질의문을 검사하여 정상 실행이 가능한 질의인지를 확인한다.

스트림을 생성하기 위해서 아래의 저장 프로시저를 이용한다.

```sql
EXEC STREAM_CREATE(stream_name, stream_query_string);
```

스트림을 성공적으로 생성하더라도 바로 실행이 시작되지 않는다. 관련 사항은 스트림 시작 및 종료를 참조하라.

스트림 질의는 Insert... Select문의 형태를 하고 있다. 기본적인 스트림 질의는 매 입력 데이터에 대해서 실행되는 것이 기본으로, 이 경우 SUM, AVG등의 통계 질의를 사용할 수 없다.

```sql
EXEC STREAM_CREATE(normal_query, 'INSERT INTO CEP_LOG_TABLE SELECT * FROM EVENT WHERE C1 = 0');
```

하지만 Insert select문의 마지막에 스트림 질의가 수행될 주기를 설정하면 일정 주기 마다 입력 데이터에 대한 통계 질의문을 이용할 수 있다.

```sql
EXEC STREAM_CREATE(aggr_1_sec, 'insert into aggr select sum(i1), i2 from base group by i2 BY 1 SECOND');
```

위 stream 질의는 매 1초마다 수행하여 group by 질의를 마지막 수행 이후에 입력된 최신 데이터에 대해 실행하고, 그 결과를 aggr 로그 테이블에 입력하게 된다.

만약 스트림 질의의 수행 시점을 사용자가 정의하여 수행하고 싶다면 실행 주기 설정 절에 아래와 같이 지정하면, 스트림 질의는 사용자의 명시적인 호출 이전에는 수행되지 않는다.

```sql
EXEC STREAM_CREATE(base_trig, 'insert into aggr select sum(i1), i2 from base group by i2 BY USER');
```

스트림 질의 실행조건절을 BY USER로 하면 STREAM_EXECUTE 프로시저를 이용하여 그 스트림 질의를 명시적으로 호출될 때 까지 실행되지 않는다. STREAM_EXECUTE로 호출된 STREAM은 이전에 읽어들인 부분을 제외하고 실행 기간 동안 추가된 증분 데이터에 대해서만 스트림 질의를 수행한다.

## 스트림 삭제
생성된 스트림의 목록은 V$STREAMS 메타 테이블을 이용하여 조회할 수 있다. 스트림을 삭제하려면, 스트림을 생성하였을 때 결정한 스트림의 이름을 매개변수로 다음의 저장 프로시저를 이용한다.

```sql
EXEC STREAM_DROP(stream_name);
```

실행중인 스트림은 삭제가 되지 않으며, 스트림을 삭제하기 전에 먼저 스트림의 실행을 종료시켜야 한다. 관련 사항은 스트림 시작 및 종료를 참조하라.

## V$STREAMS
DB서버에 등록된 스트림들의 현재 상태를 조회하기 위한 메타 테이블이다. 자세한 설명은 메뉴얼의 virtual table에 기술되어 있다.

