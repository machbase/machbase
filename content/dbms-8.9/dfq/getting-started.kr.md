---
type: docs
title: '12.1 시작하기'
weight: 10
toc: true
---

DFQ(Direct File Query)는 파일을 DB에 적재하지 않고 SQL로 조회하는 기능입니다.
DBMS 8.9 Standard Edition에서 `READ()`를 사용합니다. 파일 경로는 클라이언트가 아니라
**DB 서버**에서 해석합니다. 데이터셋 다운로드와 미디어 디코딩은 클라이언트의 역할입니다.

## 1. 실습 파일 준비

[샘플 묶음](/assets/dbms-8.9/dfq/samples.zip)을 DB 서버에 내려받습니다.
서버 관리자가 읽을 수 있는 전용 디렉터리에 풉니다. 다음 /srv/dfq는 예제 경로입니다.

```bash
mkdir -p /srv/dfq
unzip samples.zip -d /srv/dfq
```

같은 이름의 기존 파일이 없는 전용 디렉터리를 사용합니다. 권한이 없으면 관리자가 준비한
다른 경로를 사용하고 SQL의 /srv/dfq를 모두 바꿉니다. ZIP에는 작은 센서 파일과
별도의 LeRobot 학습용 데이터셋이 들어 있습니다. 손상 입력 bad.*는 오류 예제용입니다.

| 센서 입력 | 값 |
|---|---|
| id | 1~5 |
| v | id×10 |
| label | sensor-1~sensor-5 |
| day | 2026-11-01 |
| pose.x / items | JSON·Parquet의 중첩 구조 |

[센서 파일 생성 코드](/assets/dbms-8.9/dfq/generate_samples.py)도 제공합니다.
생성 코드를 실행하려면 NumPy·PyArrow·h5py·mcap이 필요합니다. **제공된 파일을 READ로
조회하는 서버에는 이 Python 패키지가 필요하지 않습니다.** LeRobot 데이터셋은 ZIP에
별도로 포함되어 있으며 이 생성 코드의 출력이 아닙니다.

## 2. 접속과 권한

```bash
export DFQ_HOST=127.0.0.1 DFQ_PORT=5656 DFQ_USER=SYS
read -rsp 'DB 비밀번호: ' DFQ_PASSWORD
export DFQ_PASSWORD
printf '\n'
machsql -s "$DFQ_HOST" -P "$DFQ_PORT" -u "$DFQ_USER" -p "$DFQ_PASSWORD"
```

일반 사용자는 SYS에게 디렉터리 READ 권한을 받아야 합니다. 서버 프로세스의 OS 읽기
권한도 필요합니다. [권한과 운영](../operations/)을 참고합니다.

## 3. 파일 조회

```sql
SELECT id,v FROM READ('/srv/dfq/sensor.csv') ORDER BY id;
SELECT COUNT(*) AS N,SUM(v) AS TOTAL FROM READ('/srv/dfq/sensor.csv');
```

첫 결과는 (1,10)부터 (5,50)까지 5행입니다. 집계는 N=5, TOTAL=150입니다.

```sql
SELECT * FROM '/srv/dfq/sensor.csv' LIMIT 3;
DESC '/srv/dfq/sensor.csv';
```

인용 파일명은 같은 이름의 테이블·뷰가 없을 때 파일로 해석합니다. 기존 관계의 SELECT
권한 오류를 파일 읽기로 우회하지 않습니다. 옵션을 지정하거나 파일을 명시적으로
선택하려면 READ를 사용합니다. 인용되지 않은 이름은 기존 관계 이름입니다.

## 4. 다음 단계

- 입력 구조를 모르면 [DESC와 탐색](../inspect/)부터 확인합니다.
- [포맷별 상세 사용법](../formats/)에서 작업과 옵션 조합을 찾습니다.
- SQL 파일은 `machsql ... -f csv.sql`로 실행합니다. 오류 예제는 정상 SQL과 분리합니다.
- 실습은 DB 테이블을 만들지 않습니다. 제공 파일은 필요한 동안 보존하고 전용 실습 파일만 정리합니다.
