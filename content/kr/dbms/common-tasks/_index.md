---
type: docs
title: '일반 작업'
weight: 50
---

Machbase의 일상적인 운영을 위한 실용적인 how-to 가이드입니다. 각 가이드는 실제 예제와 함께 단계별 지침을 제공합니다.

## 빠른 링크

| 작업 | 학습 내용 | 소요 시간 |
|------|------------------|------|
| [연결하기](./connecting/) | machsql, ODBC, JDBC, REST API를 통한 연결 | 10분 |
| [데이터 가져오기](./importing-data/) | CSV 가져오기, 대량 로딩, APPEND 프로토콜 | 15분 |
| [데이터 조회하기](./querying/) | 일반적인 쿼리 패턴과 최적화 | 20분 |
| [사용자 관리](./user-management/) | 사용자 생성, 권한 부여, 보안 | 15분 |
| [백업 및 복구](./backup-recovery/) | 백업 전략, 복구 절차 | 15분 |

## 섹션 내용

### [Machbase 연결하기](./connecting/)

Machbase에 연결하는 모든 방법을 학습합니다:
- machsql 명령줄 클라이언트
- ODBC/CLI 연결
- Java 애플리케이션을 위한 JDBC
- HTTP 접근을 위한 REST API
- Python, .NET 및 기타 SDK
- 커넥션 풀링과 모범 사례

### [데이터 가져오기](./importing-data/)

데이터 가져오기 기법을 마스터합니다:
- machloader를 이용한 CSV 파일 가져오기
- APPEND 프로토콜을 이용한 대량 로딩
- 실시간 데이터 수집
- 대용량 데이터셋 처리
- 오류 처리 및 검증
- 성능 최적화

### [데이터 조회하기](./querying/)

일반적인 쿼리 패턴:
- DURATION을 사용한 시간 기반 쿼리
- 집계 및 GROUP BY
- SEARCH 키워드를 이용한 텍스트 검색
- JOIN 연산
- 서브쿼리와 CTE
- 쿼리 최적화 팁

### [사용자 관리](./user-management/)

데이터베이스 사용자와 보안 관리:
- 사용자 생성 및 삭제
- 권한 부여 및 취소
- 역할 기반 접근 제어
- 비밀번호 관리
- 사용자 활동 감사
- 보안 모범 사례

### [백업 및 복구](./backup-recovery/)

데이터 보호:
- 전체 데이터베이스 백업
- 증분 백업
- 온라인 vs 오프라인 백업
- 복구 절차
- 재해 복구 계획
- 백업 자동화

## 대상 독자

이 가이드는 다음 사용자를 위한 것입니다:
- **데이터베이스 관리자** - Machbase 설치를 관리하는 관리자
- **개발자** - Machbase로 애플리케이션을 구축하는 개발자
- **데이터 엔지니어** - 데이터 파이프라인을 구축하는 엔지니어
- **DevOps** - 데이터베이스 운영을 자동화하는 DevOps 담당자

## 사전 요구사항

이 가이드를 따르기 전에:
- Machbase가 설치되고 실행 중이어야 합니다
- [시작하기](../getting-started/) 섹션을 완료해야 합니다
- 기본적인 SQL 지식이 필요합니다
- 명령줄에 익숙해야 합니다

## 빠른 참조

### 일상 운영

```sql
-- 연결
machsql -s localhost -u SYS -p MANAGER

-- CSV 가져오기
machloader -t sensor_data -d csv -i data.csv

-- 최근 데이터 조회
SELECT * FROM logs DURATION 1 HOUR;

-- 사용자 생성
CREATE USER analyst IDENTIFIED BY 'password';

-- 백업
machadmin -b /backup/machbase_backup
```

### 일반 명령어

| 작업 | 명령어 |
|------|---------|
| 서버 시작 | `machadmin -u` |
| 서버 중지 | `machadmin -s` |
| 상태 확인 | `machadmin -e` |
| 연결 | `machsql` |
| CSV 가져오기 | `machloader -t TABLE -d csv -i file.csv` |
| 백업 | `machadmin -b /path/to/backup` |
| 복구 | `machadmin -r /path/to/backup` |

### 주요 SQL 연산

```sql
-- 사용자 관리
CREATE USER username IDENTIFIED BY 'password';
GRANT SELECT ON table TO username;
ALTER USER username IDENTIFIED BY 'newpass';
DROP USER username;

-- 데이터 가져오기
-- (machloader 또는 APPEND API 사용)

-- 조회
SELECT * FROM table DURATION 1 HOUR;
SELECT * FROM table WHERE column = 'value';
SELECT AVG(value) FROM table GROUP BY sensor_id;

-- 백업
-- (machadmin 명령줄 도구 사용)
```

## 모범 사례

### 연결 관리

1. **커넥션 풀링 사용** - 애플리케이션에서 커넥션 풀링 사용
2. **연결 종료** - 사용 완료 후 연결 종료
3. **연결 오류 처리** - 연결 오류를 우아하게 처리
4. **동시 연결 제한** - 동시 연결 수 제한 (일반적으로 10-20개)

### 데이터 가져오기

1. **APPEND 프로토콜 사용** - 대용량 데이터에 대해 APPEND 프로토콜 사용
2. **배치 삽입** - 배치당 1000-10000행 단위로 삽입
3. **데이터 검증** - 가져오기 전 데이터 검증
4. **진행 상황 모니터링** - 가져오기 진행 상황 및 오류 모니터링
5. **적절한 방법 선택** - 일회성 가져오기는 CSV, 지속적 데이터는 API 사용

### 조회

1. **항상 시간 필터 사용** - DURATION 사용
2. **결과셋 제한** - LIMIT 절 사용
3. **롤업 조회** - 분석 시 롤업 조회 (Tag 테이블)
4. **인덱스 생성** - 자주 조회하는 컬럼에 인덱스 생성
5. **SELECT * 피하기** - 대용량 테이블에서 SELECT * 피하기

### 사용자 관리

1. **강력한 비밀번호 사용** - 최소 8자 이상
2. **최소 권한 부여** - 최소 권한 원칙 적용
3. **정기적인 비밀번호 변경** - 분기별 비밀번호 변경
4. **사용자 활동 감사** - 로그 확인
5. **비활성 사용자 제거** - 신속하게 비활성 사용자 제거

### 백업 및 복구

1. **일일 자동 백업** - cron 작업으로 자동화
2. **정기적인 복구 테스트** - 월별 복구 테스트
3. **여러 백업 사본 유지** - 3-2-1 규칙 적용
4. **오프사이트 저장** - 재해 복구를 위한 원격 저장
5. **절차 문서화** - 런북 작성

## 문제 해결 빠른 수정

### 연결 문제

```bash
# 서버 실행 확인
machadmin -e

# 포트 사용 가능 여부 확인
netstat -an | grep 5656

# 자격 증명 확인
machsql -s localhost -u SYS -p MANAGER
```

### 가져오기 문제

```bash
# CSV 형식 확인
head -10 data.csv

# 데이터 타입 검증
SHOW TABLE tablename;

# 오류 로그 확인
cat $MACHBASE_HOME/trc/machloader.log
```

### 쿼리 성능

```sql
-- 시간 필터 추가
SELECT * FROM table DURATION 1 HOUR;

-- LIMIT 사용
SELECT * FROM table LIMIT 1000;

-- 활성 쿼리 확인
SHOW STATEMENTS;
```

### 사용자 권한 문제

```sql
-- 사용자 권한 확인
SHOW USERS;

-- 필요한 권한 부여
GRANT SELECT ON tablename TO username;
```

### 백업 문제

```bash
# 디스크 공간 확인
df -h

# 백업 디렉토리 권한 확인
ls -la /backup/

# 백업 로그 확인
cat $MACHBASE_HOME/trc/machadmin.log
```

## 추가 자료

### 관련 문서

- [시작하기](../getting-started/) - 기본 Machbase 사용법
- [핵심 개념](../core-concepts/) - Machbase 아키텍처 이해
- [튜토리얼](../tutorials/) - 실습 학습
- [SQL 레퍼런스](../sql-reference/) - 완전한 SQL 구문
- [도구 레퍼런스](../tools-reference/) - 명령줄 도구
- [문제 해결](../troubleshooting/) - 상세한 문제 해결

### 외부 자료

- [ODBC 문서](../../sdk/cli-odbc/) - ODBC 드라이버 세부 정보
- [JDBC 문서](../../sdk/jdbc/) - JDBC 드라이버 세부 정보
- [REST API](../../sdk/restful_api/) - HTTP API 레퍼런스
- [Python SDK](../../sdk/python/) - Python 통합

## 다음 단계

필요에 따라 작업을 선택하세요:

1. **Machbase가 처음이신가요?** [연결하기](./connecting/)부터 시작하세요
2. **데이터를 로드해야 하나요?** [데이터 가져오기](./importing-data/)로 이동하세요
3. **쿼리를 작성하시나요?** [데이터 조회하기](./querying/)를 확인하세요
4. **접근 권한을 관리하시나요?** [사용자 관리](./user-management/)를 참조하세요
5. **데이터를 보호하시나요?** [백업 및 복구](./backup-recovery/)를 읽어보세요

---

이 가이드는 일상적인 Machbase 작업에 대한 실용적인 솔루션을 제공합니다. 필요한 작업을 선택하고 단계별 지침을 따라하세요!
