---
type: docs
title: '16.4 대량 적재 파이프라인'
weight: 40
toc: true
---

대량 적재는 입력 파일, 대상 테이블, 실패 처리, 재시도와 검증을 하나의 파이프라인으로
설계해야 합니다. 명령 옵션의 정본은
[데이터 입력·적재·내보내기](/dbms/application-integration/data-input-load-export/)와
[machloader 사전](/dbms/reference/command-line-tools/dictionary-machloader/)에서 확인합니다.

## 1단계: 적재 계약 정의

다음을 배치 실행 전에 고정합니다.

- 대상 database, 테이블과 열 순서
- 파일 인코딩, 구분자, 따옴표, 줄바꿈과 시간 형식
- 중복 행을 구분할 키 또는 시간 범위
- 허용할 실패 행과 전체 배치 실패 기준
- 원본, 처리 완료, 실패 파일의 보관 위치

LOG 테이블에는 `_ARRIVAL_TIME`이 자동으로 제공되므로 사용자 열로 다시 선언하지 않습니다.

```sql
CREATE LOG TABLE sc16_bulk_log (
    source_time DATETIME,
    sensor_id   VARCHAR(64),
    value       DOUBLE,
    quality     INTEGER
);
```

## 2단계: 입력 방식 선택

| 조건 | 시작점 |
|---|---|
| 정형 CSV 파일 | `machloader` |
| 애플리케이션에서 연속 배치 입력 | 해당 SDK의 Append API |
| 일회성 소량 검증 | prepared INSERT |

`machloader -h`로 현재 배포본의 옵션 의미를 확인한 뒤 사용합니다. 예를 들어 오류 행 파일은
`-b`, 실행 로그는 `-l`로 지정합니다. `-e`와 `-n`을 오류 수 옵션으로 사용하지 마십시오.

```bash
machloader -h
machloader -s 127.0.0.1 -P 5656 -u app_user \
  -t sc16_bulk_log -i /data/input.csv \
  -b /data/input.bad -l /data/input.log
```

비밀번호는 명령행에 고정하지 말고 배포 환경의 안전한 입력 수단을 사용합니다.

## 3단계: Append 구현

언어별 Append 호출, 반환값과 오류 처리는 [개발 도구 연동](/dbms/development-tools-integration/)의
현재 quickstart를 사용합니다. 예외만 기다리지 말고 SDK가 반환하는 성공·실패 값도 확인합니다.
실패한 행을 문자열 결합 INSERT로 자동 재실행하지 마십시오. 바인드 구문을 사용하고, 실패가
일시적인지 데이터 오류인지 구분한 뒤 재처리합니다.

## 4단계: 완료 검증

적재 시작 전에 기준 행 수와 시간 범위를 기록하고, 완료 후 같은 쿼리로 비교합니다.

```sql
SELECT COUNT(*) AS row_count,
       MIN(source_time) AS min_source_time,
       MAX(source_time) AS max_source_time
  FROM sc16_bulk_log;
```

검증에는 loader 또는 SDK의 성공 건수, 실패 파일의 행 수, 대상 테이블 행 수를 모두 사용합니다.
checkpoint는 DB 입력 성공과 검증이 끝난 뒤에만 전진시킵니다.

## 5단계: 정리

검증용 객체가 더 필요하지 않으면 제거합니다.

```sql
DROP TABLE sc16_bulk_log;
```

스레드 수, 배치 크기, 재시도 간격은 고정 권장값이 아니라 테스트 환경의 처리량, 지연, 메모리와
서버 부하를 함께 측정해 결정합니다.
