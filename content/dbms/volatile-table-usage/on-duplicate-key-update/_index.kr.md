---
title: '10.13 ON DUPLICATE KEY UPDATE'
weight: 130
toc: true
---

<a id="on-duplicate-key-update"></a>

## 중복 키 갱신 선택

VOLATILE 테이블은 `PRIMARY KEY`가 중복될 때 새 행 대신 기존 행을 갱신할 수 있습니다.

| 목적 | 구문 |
|------|------|
| 입력값으로 기존 행 전체 갱신 | `ON DUPLICATE KEY UPDATE` |
| 지정한 컬럼만 갱신 | `ON DUPLICATE KEY UPDATE SET ...` |
| 존재하는 행을 명시적으로 변경 | `UPDATE ... WHERE primary_key = ...` |

`SET` 절에서는 `PRIMARY KEY`를 변경할 수 없습니다. 자동 증가 키를 사용하는 VOLATILE
테이블에는 이 구문을 사용할 수 없습니다.

완전한 생성·입력·조회·정리 예제는
[데이터 입력과 변경](/dbms/volatile-table-usage/data-input-mutation/)에 있습니다.

## 카운터를 갱신할 때

입력 측에서 계산한 최신 카운터 값을 저장하려면 `SET` 절을 사용합니다.

```sql
CREATE VOLATILE TABLE volatile_counter_demo (
    event_type VARCHAR(32) PRIMARY KEY,
    event_count LONG
);

INSERT INTO volatile_counter_demo VALUES ('LOGIN', 1)
ON DUPLICATE KEY UPDATE SET event_count = 1;

INSERT INTO volatile_counter_demo VALUES ('LOGIN', 2)
ON DUPLICATE KEY UPDATE SET event_count = 2;

SELECT * FROM volatile_counter_demo;
DROP TABLE volatile_counter_demo;
```

이 예제의 `SET` 값은 누적 연산이 아니라 입력 측에서 계산한 값입니다. 여러 클라이언트가
동시에 누적값을 계산해야 한다면 경합과 유실 갱신 가능성을 별도로 검증합니다.
