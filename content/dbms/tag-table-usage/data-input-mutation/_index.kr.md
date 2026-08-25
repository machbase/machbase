---
title: '5.4 데이터 입력과 변경'
weight: 40
toc: true
---
TAG 데이터는 SQL `INSERT`, Append API 또는 파일 적재 도구로 입력합니다. SQL 예제는 기능
확인과 소량 입력에 사용하고, 지속적인 수집은 Append API를 우선 검토합니다.

<a id="original-85-inserting-data"></a>

## SQL INSERT

다음 예제는 시간축과 거리축 TAG를 각각 만들고 데이터를 확인한 뒤 정리합니다.

```sql
CREATE TAG TABLE input_time_tag (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
);

INSERT INTO input_time_tag
VALUES ('TEMP_001', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 25.5);
INSERT INTO input_time_tag
VALUES ('TEMP_001', TO_DATE('2026-01-01 10:01:00', 'YYYY-MM-DD HH24:MI:SS'), 25.7);

CREATE TAG TABLE input_distance_tag (
    name     VARCHAR(32) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value    DOUBLE,
    quality  INTEGER
);

INSERT INTO input_distance_tag VALUES ('PIPE_A', 0.0, 10.1, 100);
INSERT INTO input_distance_tag VALUES ('PIPE_A', 500.5, 11.2, 100);

EXEC TABLE_FLUSH(input_time_tag);
EXEC TABLE_FLUSH(input_distance_tag);

SELECT name, time, value FROM input_time_tag ORDER BY time;
SELECT name, distance, value, quality
  FROM input_distance_tag
 ORDER BY distance;

DROP TABLE input_distance_tag;
DROP TABLE input_time_tag;
```

`TABLE_FLUSH`는 방금 입력한 데이터를 즉시 확인해야 하는 예제·검증 절차에 사용합니다. 일반
수집 루프에서 행마다 실행하지 마십시오.

## 메타데이터와 함께 입력

사용자 메타데이터 컬럼이 있는 TAG에서 새 태그를 만들 때는 데이터와 메타데이터 값을 함께
제공하거나, `INSERT ... METADATA`로 메타데이터를 먼저 등록합니다. 시스템 관리 컬럼은 입력
목록에 포함하지 않습니다.

메타데이터 값의 등록·갱신·삭제는 [TAG 메타데이터](../tag-metadata/)를 참고하십시오.

## 입력 경로 선택

| 경로 | 적합한 경우 | 확인할 사항 |
| --- | --- | --- |
| SQL `INSERT` | 기능 확인, 저빈도 입력 | 문장별 파싱·왕복 비용 |
| SDK Append | 지속적인 고처리량 입력 | 배치 크기, flush와 오류 처리 |
| `csvimport` / `machloader` | 클라이언트 파일 일괄 적재 | 컬럼 순서, 날짜 형식, bad 파일 |
| `LOAD DATA INFILE` | 서버가 접근할 수 있는 파일 | 서버 경로·권한, 오류 정책 |

SDK별 연결과 Append 예제는 [개발 도구 연동](/dbms/development-tools-integration/)을,
파일 형식과 명령은
[데이터 입력·적재·반출](/dbms/application-integration/data-input-load-export/)을
참고하십시오.

## 데이터 정정

TAG data UPDATE는 Standard Edition에서 태그 선택 조건과 BASETIME 범위를 함께 지정해
실행합니다. 태그명, 축과 메타데이터 컬럼은 일반 data UPDATE 대상으로 사용하지 않습니다.
정정 후 ROLLUP이 있다면 대상 범위를 재구성합니다.

자세한 절차는 [TAG 데이터 정정](../tag-data-update-correction/)을 참고하십시오.
