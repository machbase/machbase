---
type: docs
title: '문제 해결'
weight: 110
---

Machbase의 일반적인 문제, 에러 코드 및 성능 최적화 가이드에 대한 해결 방법을 제공합니다.

## 일반적인 문제

### 서버 문제

#### 서버가 시작되지 않음

**증상**:
- `machadmin -u` 실패
- "Address already in use" 에러
- 서버 프로세스가 실행되지 않음

**해결 방법**:
```bash
# 포트가 사용 중인지 확인
netstat -an | grep 5656
lsof -i :5656

# 기존 프로세스 종료
kill $(lsof -t -i:5656)

# 데이터베이스 디렉토리 확인
ls -la $MACHBASE_HOME/dbs/

# 로그 확인
tail -50 $MACHBASE_HOME/trc/machbase.log

# 다시 시작 시도
machadmin -u
```

#### 서버 크래시

**증상**:
- 서버가 예기치 않게 중단됨
- 코어 덤프 파일 생성
- "Segmentation fault" 에러

**해결 방법**:
```bash
# 로그 확인
tail -100 $MACHBASE_HOME/trc/machbase.log

# 시스템 리소스 확인
free -h
df -h

# 메모리 사용량 줄이기 (machbase.conf에서)
BUFFER_POOL_SIZE = 1G

# 디스크 공간 확인
du -sh $MACHBASE_HOME/dbs/
```

### 연결 문제

#### 서버에 연결할 수 없음

**증상**:
- "Connection refused" 에러
- "Connection timeout"
- machsql 연결 실패

**해결 방법**:
```bash
# 서버가 실행 중인지 확인
machadmin -e

# 네트워크 연결 확인
ping server-address
telnet server-address 5656

# 방화벽 확인
sudo iptables -L | grep 5656

# 인증 정보 확인
machsql -s localhost -u SYS -p MANAGER
```

#### 연결 수 초과

**증상**:
- "Max connections exceeded" 에러
- 새로운 연결 거부됨

**해결 방법**:
```sql
-- 활성 연결 확인
SHOW STATEMENTS;

-- machbase.conf에서 MAX_CONNECTION 증가
-- MAX_CONNECTION = 200

-- 필요시 유휴 연결 종료
```

### 쿼리 문제

#### 느린 쿼리

**증상**:
- 쿼리 실행 시간이 너무 오래 걸림
- 타임아웃 에러
- 높은 CPU 사용률

**해결 방법**:
```sql
-- 시간 필터 추가
SELECT * FROM table DURATION 1 HOUR;  -- 이것을 추가하세요!

-- LIMIT 사용
SELECT * FROM table LIMIT 1000;

-- 원시 데이터 대신 롤업 조회
SELECT * FROM sensors WHERE rollup = hour;

-- 인덱스 생성
CREATE INDEX idx_column ON table(column);

-- 쿼리 플랜 확인
EXPLAIN SELECT ...;
```

#### 메모리 부족

**증상**:
- "Out of memory" 에러
- 쿼리가 중간에 실패함
- 서버가 응답하지 않음

**해결 방법**:
```sql
-- 결과 집합 축소
SELECT * FROM table DURATION 1 HOUR LIMIT 1000;

-- 적은 컬럼 선택
SELECT col1, col2 FROM table;  -- SELECT * 대신

-- machbase.conf에서 MAX_QPX_MEM 증가
-- MAX_QPX_MEM = 1G
```

### 데이터 문제

#### 데이터 임포트 실패

**증상**:
- machloader 에러
- CSV 임포트 실패
- 데이터 타입 불일치

**해결 방법**:
```bash
# CSV 형식 확인
head -10 data.csv

# 테이블 스키마 검증
machsql -f - <<EOF
SHOW TABLE tablename;
EOF

# 에러 로그 확인
cat $MACHBASE_HOME/trc/machloader.log

# 데이터 타입 검증
# CSV 컬럼이 테이블 스키마와 일치하는지 확인

# 먼저 작은 배치로 시도
head -100 data.csv > test.csv
machloader -t table -d csv -i test.csv
```

#### 데이터 누락

**증상**:
- 예상되는 데이터를 찾을 수 없음
- 카운트 불일치
- 시간 간격 존재

**해결 방법**:
```sql
-- 시간 범위 확인
SELECT MIN(_arrival_time), MAX(_arrival_time) FROM table;

-- 전체 카운트 확인
SELECT COUNT(*) FROM table;

-- NULL 값 확인
SELECT COUNT(*) FROM table WHERE column IS NULL;

-- 임포트 완료 확인
-- machloader 로그 확인
```

## 에러 코드

### 일반적인 에러 메시지

| 에러 코드 | 메시지 | 해결 방법 |
|-----------|---------|----------|
| -20000 | Connection failed | 서버 상태, 네트워크 확인 |
| -20001 | Authentication failed | 사용자명/비밀번호 확인 |
| -20100 | Table not found | 테이블명 확인, SHOW TABLES 사용 |
| -20101 | Column not found | 컬럼명 확인, SHOW TABLE 사용 |
| -20200 | Duplicate key | PRIMARY KEY 제약 조건 확인 |
| -20300 | Data type mismatch | 데이터 타입 검증 |
| -30000 | Out of memory | 쿼리 크기 축소, 메모리 증가 |
| -30100 | Timeout | 시간 필터 추가, 타임아웃 증가 |

전체 에러 코드 참조는 [에러 코드](../../dbms/faq/error-code/)를 참조하세요.

## 성능 최적화

### 쿼리 최적화

1. **항상 시간 필터 사용**
```sql
-- 나쁨
SELECT * FROM sensors WHERE sensor_id = 'sensor01';

-- 좋음
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
DURATION 1 HOUR;
```

2. **분석용 롤업 사용**
```sql
-- 느림
SELECT AVG(value) FROM sensors DURATION 7 DAY;

-- 빠름
SELECT AVG(avg_value) FROM sensors
WHERE rollup = hour
DURATION 7 DAY;
```

3. **인덱스 생성**
```sql
CREATE INDEX idx_level ON logs(level);
```

4. **결과 제한**
```sql
SELECT * FROM logs DURATION 1 DAY LIMIT 1000;
```

### 서버 튜닝

```properties
# 메모리 최적화
BUFFER_POOL_SIZE = 4G       # RAM의 50-70%
MAX_QPX_MEM = 1G            # 쿼리당 메모리
LOG_BUFFER_SIZE = 128M      # 쓰기 버퍼

# 성능 튜닝
CHECKPOINT_INTERVAL_SEC = 900
MAX_PARALLEL_QUERY = 8
```

### 데이터 관리

1. **보존 정책 구현**
```sql
DELETE FROM logs EXCEPT 30 DAYS;
```

2. **배치 쓰기**
```python
# 대량 삽입을 위해 APPEND API 사용
appender = conn.create_appender('table')
for row in data:
    appender.append(row)
appender.close()
```

3. **저장소 모니터링**
```sql
SHOW STORAGE;
```

## 진단 명령어

### 서버 상태 확인

```bash
# 서버가 실행 중인가?
machadmin -e

# 활성 쿼리 보기
machsql -f - <<EOF
SHOW STATEMENTS;
EOF

# 저장소 확인
machsql -f - <<EOF
SHOW STORAGE;
EOF
```

### 로그 확인

```bash
# 서버 로그
tail -50 $MACHBASE_HOME/trc/machbase.log

# 에러 로그
grep -i error $MACHBASE_HOME/trc/machbase.log

# 최근 활동
tail -100 $MACHBASE_HOME/trc/machbase.log
```

### 시스템 정보

```sql
-- 테이블
SHOW TABLES;

-- 테이블 상세 정보
SHOW TABLE tablename;

-- 사용자
SHOW USERS;

-- 인덱스
SHOW INDEXES;

-- 라이선스
SHOW LICENSE;
```

## 도움 받기

### 수집해야 할 정보

문제를 보고할 때 다음 정보를 수집하세요:

1. **에러 메시지** (정확한 텍스트)
2. **서버 로그** ($MACHBASE_HOME/trc/machbase.log)
3. **Machbase 버전** (`machadmin -v`)
4. **운영 체제** (`uname -a`)
5. **재현 단계**

### 지원 리소스

- **문서**: 이 가이드와 [FAQ](../../dbms/faq/)를 검토하세요
- **에러 코드**: [에러 코드 참조](../../dbms/faq/error-code/)를 확인하세요
- **메모리 문제**: [메모리 에러 가이드](../../dbms/faq/memory-error/)를 참조하세요

## 문제를 피하기 위한 모범 사례

1. **쿼리에 항상 시간 필터 사용**
2. **데이터 보존 정책 구현**
3. **정기적으로 서버 리소스 모니터링**
4. **정기 백업** (일일)
5. **먼저 작은 데이터셋에서 쿼리 테스트**
6. **데이터에 적합한 테이블 타입 사용**
7. **Machbase를 최신 버전으로 유지**

## 빠른 해결 방법

```bash
# 서버 재시작
machadmin -s && sleep 5 && machadmin -u

# 디스크 공간 확인
df -h

# 메모리 확인
free -h

# 최근 에러 보기
grep -i error $MACHBASE_HOME/trc/machbase.log | tail -20

# 연결 테스트
machsql -s localhost -u SYS -p MANAGER -f - <<EOF
SELECT SYSDATE;
EOF
```

## 관련 문서

- [구성](../configuration/) - 서버 구성
- [도구 참조](../tools-reference/) - 명령줄 도구
- [FAQ](../../dbms/faq/) - 자주 묻는 질문
