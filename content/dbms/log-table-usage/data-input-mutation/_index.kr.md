---
title: '7.4 데이터 입력'
weight: 40
toc: true
---
LOG 데이터는 SQL `INSERT`, Append API 또는 파일 적재 도구로 입력합니다. 입력 경로는 데이터
발생 방식과 처리량, 파일 위치를 기준으로 선택합니다.

<a id="original-85-inserting-data"></a>

## SQL INSERT

SQL은 소량 입력과 기능 확인에 적합합니다. `_arrival_time`을 컬럼 목록에서 생략하면 서버가
수신 시각을 기록합니다.

```sql
CREATE LOG TABLE input_log (
    event_time DATETIME,
    device     VARCHAR(32),
    message    VARCHAR(128),
    value      DOUBLE
);

INSERT INTO input_log(event_time, device, message, value)
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        'DEV-01', 'temperature warning', 82.5);

SELECT _arrival_time, event_time, device, message, value
  FROM input_log
  DURATION 1 HOUR;

DROP TABLE input_log;
```

데이터 이관이나 재현 테스트에서 `_arrival_time`을 명시해야 하면 입력 시각의 순서와 해당
입력 도구의 제약을 확인합니다. 일반 수집 애플리케이션의 실제 이벤트 시각은 별도
`DATETIME` 컬럼에 저장하십시오.

## Append API

지속적인 대량 입력은 SDK의 Append API를 사용해 여러 행을 배치로 전송합니다. 다음 항목을
반드시 처리합니다.

- 연결과 Appender 종료 시 남은 버퍼 flush
- 행별 타입·NULL 처리와 Append 반환 오류
- 재연결 시 중복 전송 가능성
- 배치 크기별 지연 시간과 메모리 사용량

언어별 실행 예제는 [개발 도구 연동](/dbms/development-tools-integration/)을 참고하십시오.

## 파일 적재

| 입력 파일 위치 | 선택 |
| --- | --- |
| 클라이언트가 접근하는 CSV | `csvimport` 또는 `machloader` |
| 서버가 접근할 수 있는 파일 | `LOAD DATA INFILE` |
| 지속적으로 생성되는 로컬·SFTP 파일 | Collector 검토 |

파일 적재 전에는 컬럼 순서, 구분자, 날짜 형식과 인코딩을 소량 샘플로 검증하고 bad 파일과
로그를 보존합니다. 전체 명령과 재현 예제는
[데이터 입력·적재·반출](/dbms/development-tools-integration/data-input-load-export/)을
기준으로 사용하십시오.

## 입력 경로 비교

| 경로 | 장점 | 주의점 |
| --- | --- | --- |
| SQL `INSERT` | 간단하고 모든 SQL 클라이언트에서 사용 | 문장별 파싱·왕복 비용 |
| Append API | 배치 기반 지속 입력 | SDK 통합과 오류·재시도 처리 필요 |
| 파일 적재 | 대량 초기·배치 데이터에 적합 | 파일 형식과 실패 행 관리 필요 |
| Collector | 지원 파일 소스를 설정으로 수집 | 현재 지원 source type 확인 필요 |

LOG는 입력된 행의 일반 `UPDATE`를 지원하지 않습니다. 잘못 입력한 데이터의 보정과 삭제는
[운영과 데이터 생명주기](../operations-lifecycle/)를 참고하십시오.
