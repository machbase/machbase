---
type: docs
title: '3.5 설치 검증 체크리스트'
weight: 50
toc: true
---

설치 또는 업그레이드 완료 후 아래 항목을 순서대로 확인합니다.

## Standard Edition 체크리스트

### 1. 서버 프로세스 확인

```bash
machadmin -e
# Machbase server is running with PID(<pid>).
```

또는 프로세스를 직접 확인합니다.

```bash
ps -ef | grep machbased | grep -v grep
```

### 2. 포트 리스닝 확인

```bash
ss -tlnp | grep 5656
# LISTEN 0 128 0.0.0.0:5656 ...
```

### 3. machsql 접속 테스트

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER
# MACHBASE_CONNECT_MODE=INET, PORT=5656 EDITION=STANDARD
# Mach>
```

### 4. 버전 확인

```sql
SELECT * FROM V$VERSION;
```

### 5. 라이선스 확인

```sql
SELECT ID, ISSUE_DATE, TYPE, VIOLATE_STATUS FROM V$LICENSE_INFO;
```

`VIOLATE_STATUS`가 0이면 정상입니다.

### 6. 기본 쿼리 테스트

```sql
CREATE TABLE check_test (id INTEGER, ts DATETIME);
INSERT INTO check_test VALUES (1, NOW);
SELECT * FROM check_test;
DROP TABLE check_test;
```

### 7. HTTP REST API 확인

```bash
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode "q=SELECT 1"
```

JSON 형식의 쿼리 결과가 반환되면 HTTP REST API가 응답하는 상태입니다.

---

## Cluster Edition 추가 체크리스트

### 8. 클러스터 노드 상태 확인

```bash
machcoordinatoradmin --cluster-status
# 모든 노드가 normal 상태인지 확인
```

### 9. Broker 접속 테스트

```bash
machsql -s <Broker IP> -u SYS -p MANAGER
Mach> SELECT * FROM V$NODE_STATUS;
```

### 10. 데이터 복제 확인

Warehouse 그룹 내 복제가 정상 동작하는지 간단한 INSERT로 확인합니다.

```sql
-- Broker를 통해 데이터 입력
CREATE TABLE cluster_check_test (id INTEGER, ts DATETIME);
INSERT INTO cluster_check_test VALUES (1, NOW);

-- 각 Warehouse 노드에 직접 접속하여 데이터 존재 여부 확인
SELECT COUNT(*) FROM cluster_check_test;
DROP TABLE cluster_check_test;
```

---

## 문제 발생 시

- 서버 로그: `$MACHBASE_HOME/trc/machbase.trc`
- [운영·장애 진단](/dbms/operations-configuration-recovery/diagnosis-observability/) 참고

---

**이 장의 내용을 모두 완료했습니다.**

다음으로 읽을 내용:
- [데이터 모델링 및 테이블 설계](/dbms/data-modeling-table-design/)
- [운영 및 구성](/dbms/operations-configuration-recovery/)
