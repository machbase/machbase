---
title: 'Tag 데이터 삽입'
type: docs
weight: 30
---

## 개요

Machbase는 Tag 데이터를 삽입하기 위한 여러 방법을 제공하며, 각 방법은 서로 다른 사용 사례에 최적화되어 있습니다. 데이터 볼륨과 애플리케이션 요구 사항에 가장 적합한 방법을 선택하십시오.

## 방법 1: INSERT 문

데이터를 삽입하는 가장 간단한 방법 - 소규모 데이터셋 및 테스트에 이상적입니다.

### 기본 INSERT 예제

```sql
Mach> create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized);
Executed successfully.

Mach> insert into tag metadata values ('TAG_0001');
1 row(s) inserted.

-- Insert single values
Mach> insert into tag values('TAG_0001', now, 0);
1 row(s) inserted.

Mach> insert into tag values('TAG_0001', now, 1);
1 row(s) inserted.

Mach> insert into tag values('TAG_0001', now, 2);
1 row(s) inserted.

Mach> select * from tag where name = 'TAG_0001';
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0001              2018-12-19 17:41:37 806:901:728 0
TAG_0001              2018-12-19 17:41:42 327:839:368 1
TAG_0001              2018-12-19 17:41:43 812:782:202 2
[3] row(s) selected.
```

> **사용 시기**: 테스트, 저용량 삽입, 대화형 데이터 입력

## 방법 2: CSV 파일 임포트

`csvimport` 도구를 사용하여 CSV 파일에서 대량의 데이터를 빠르게 로드합니다.

### CSV 파일 형식

태그 이름, 타임스탬프 및 값이 포함된 CSV 파일(`data.csv`)을 생성합니다:

```csv
TAG_0001, 2009-01-28 07:03:34 0:000:000, -41.98
TAG_0001, 2009-01-28 07:03:34 1:000:000, -46.50
TAG_0001, 2009-01-28 07:03:34 2:000:000, -36.16
```

### csvimport 사용

```bash
csvimport -t TAG -d data.csv -F "time YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn" -l error.log
```

**옵션 설명**:
- `-t TAG`: 대상 테이블 이름
- `-d data.csv`: 데이터 파일 경로
- `-F`: 시간 형식 지정
- `-l error.log`: 에러 로그 파일

> **사용 시기**: 대량 로딩, 데이터 마이그레이션, 배치 임포트

> **중요**: 데이터를 임포트하기 전에 태그 이름이 태그 메타데이터에 존재해야 합니다.

## 방법 3: RESTful API

HTTP 요청을 통해 데이터를 삽입합니다 - IoT 디바이스와 웹 애플리케이션에 완벽합니다.

### API 구문

```json
{
  "values": [
    [TAG_NAME, TAG_TIME, VALUE],
    [TAG_NAME, TAG_TIME, VALUE],
    ...
  ],
  "date_format": "YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn"
}
```

`date_format`이 생략되면 기본 형식 `YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn`이 사용됩니다.

### API 예제

```bash
curl -X POST http://localhost:5654/db/write/TAG \
  -H "Content-Type: application/json" \
  -d '{
    "values": [
      ["TAG_0001", "2024-01-01 10:00:00", 25.5],
      ["TAG_0001", "2024-01-01 10:01:00", 26.0],
      ["TAG_0002", "2024-01-01 10:00:00", 30.2]
    ]
  }'
```

> **사용 시기**: IoT 디바이스, 실시간 데이터 스트리밍, 웹 애플리케이션

## 방법 4: SDK 통합

애플리케이션에서 프로그래밍 방식의 데이터 삽입을 위해 Machbase SDK를 사용합니다.

### 지원 언어

- **[C/C++ 라이브러리](/dbms/sdk/cli-odbc)** - 고성능 네이티브 통합
- **[Java 라이브러리](/dbms/sdk/jdbc)** - 엔터프라이즈 Java 애플리케이션
- **[Python 라이브러리](/dbms/sdk/python)** - 데이터 과학 및 자동화
- **[C# 라이브러리](/dbms/sdk/dotnet)** - .NET 애플리케이션

### Python 예제

```python
import machbaseAPI as mach

# Connect to Machbase
conn = mach.connect(host='localhost', port=5656)

# Insert data
cursor = conn.cursor()
cursor.execute("""
    INSERT INTO tag VALUES (?, ?, ?)
""", ('TAG_0001', '2024-01-01 10:00:00', 25.5))

conn.commit()
conn.close()
```

> **사용 시기**: 애플리케이션 통합, 자동화된 데이터 수집, 사용자 정의 도구

## 적절한 방법 선택

| 방법 | 적합한 경우 | 장점 | 단점 |
|--------|----------|------|------|
| **INSERT** | 테스트, 소규모 데이터셋 | 간단합니다, 대화형 | 대용량 데이터에는 느림 |
| **CSV 임포트** | 대량 로딩, 마이그레이션 | 매우 빠름, 효율적 | 파일 준비 필요 |
| **RESTful API** | IoT, 웹 앱 | 유연합니다, 플랫폼 독립적 | 네트워크 오버헤드 |
| **SDK** | 애플리케이션 | 완전한 제어, 타입 안전성 | 개발 필요 |

## 추가 컬럼 사용

Tag 테이블에 추가 컬럼이 있는 경우 삽입 시 포함시킵니다:

```sql
-- Tag table with additional columns
CREATE TAG TABLE sensors (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    location VARCHAR(50),
    status SHORT
);

-- Insert with additional columns
INSERT INTO sensors VALUES (
    'TEMP_001',
    '2024-01-01 10:00:00',
    25.5,
    'Building A',
    1
);
```

## 모범 사례

1. **태그 먼저 등록**: 데이터를 삽입하기 전에 항상 태그 메타데이터를 삽입합니다
2. **배치 작업 사용**: 대규모 데이터셋의 경우 CSV 임포트 또는 배치 API 호출을 사용합니다
3. **에러 처리**: 항상 반환 값을 확인하고 에러를 로그에 기록합니다
4. **시간 정밀도**: 데이터 전체에서 타임스탬프 정밀도를 일관되게 유지합니다
5. **데이터 검증**: 에러를 방지하기 위해 삽입 전에 태그 이름이 존재하는지 확인합니다

## 성능 팁

- **CSV 임포트**: 대량 데이터(수백만 행)에 가장 빠름
- **배치 삽입**: 여러 INSERT 문을 트랜잭션으로 그룹화
- **병렬 로딩**: 병렬 수집을 위해 여러 csvimport 프로세스 사용
- **준비된 문**: SDK에서 더 나은 성능을 위해 파라미터화된 쿼리 사용

## 다음 단계

- [Tag 데이터 쿼리](../querying-data)에서 데이터 검색에 대해 학습합니다
- [Tag 인덱스](../tag-indexes)에서 쿼리 최적화를 탐색합니다
- [롤업 테이블](../rollup-tables)에서 시계열 집계를 이해합니다
