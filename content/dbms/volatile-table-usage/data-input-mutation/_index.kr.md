---
title: '10.4 데이터 입력과 변경'
weight: 40
toc: true
---

VOLATILE 테이블의 `INSERT`, 중복 키 갱신, `DELETE`를 실행 가능한 예제로 설명합니다.

<a id="original-85-insert-update"></a>

## 데이터 입력과 갱신

다음 예제는 마지막 정리 구문까지 순서대로 실행할 수 있습니다. 최신 상태처럼 같은 키의 값을
계속 바꿔야 한다면 `PRIMARY KEY`를 정의하고 `ON DUPLICATE KEY UPDATE`를 사용합니다.

```sql
CREATE VOLATILE TABLE volatile_mutation_demo (
    id         INTEGER PRIMARY KEY,
    direction  VARCHAR(10),
    refcnt     INTEGER
);

INSERT INTO volatile_mutation_demo VALUES (1, 'west', 0);
INSERT INTO volatile_mutation_demo VALUES (2, 'east', 0);

INSERT INTO volatile_mutation_demo VALUES (1, 'south', 0)
ON DUPLICATE KEY UPDATE;

INSERT INTO volatile_mutation_demo VALUES (1, 'south', 0)
ON DUPLICATE KEY UPDATE SET refcnt = 1;

SELECT * FROM volatile_mutation_demo ORDER BY id;
```

중복 키가 없으면 새 행이 입력됩니다. 중복 키가 있으면 `SET` 절이 없는 구문은 입력값으로
행 전체를 갱신하고, `SET` 절이 있는 구문은 지정한 컬럼만 갱신합니다. `PRIMARY KEY` 자체는
갱신 대상으로 지정할 수 없습니다.

대량 입력 API는 언어와 드라이버에 따라 초기화·바인딩·오류 처리가 다릅니다. 불완전한 코드
조각을 복사하지 말고 [SDK 및 통합](/dbms/application-integration/)의 해당 드라이버 예제를
사용합니다.

<a id="original-85-deleting-data"></a>

## 데이터 삭제

조건부 삭제는 `PRIMARY KEY = 값` 형태만 지원합니다. 다른 컬럼 조건이나 복합 조건은 사용할 수
없습니다.

```sql
DELETE FROM volatile_mutation_demo WHERE id = 2;
SELECT * FROM volatile_mutation_demo ORDER BY id;
DROP TABLE volatile_mutation_demo;
```

모든 행을 비워야 하면 테이블을 삭제한 뒤 초기화 스크립트로 다시 생성하는 방식을 사용할 수
있습니다. 서버 재시작 때 테이블과 데이터가 모두 사라진다는 점도 함께 고려합니다.
