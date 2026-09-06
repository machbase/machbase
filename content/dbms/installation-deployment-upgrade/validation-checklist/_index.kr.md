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
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER
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
CREATE LOG TABLE check_test (id INTEGER, ts DATETIME);
INSERT INTO check_test VALUES (1, NOW);
SELECT * FROM check_test;
DROP TABLE check_test;
```

## Cluster Edition 추가 체크리스트

### 7. 클러스터 노드 상태 확인

```bash
machcoordinatoradmin --cluster-status
# 모든 노드가 normal 상태인지 확인
```

### 8. Broker 접속 테스트

```bash
machsql -s <Broker IP> -P 5656 -u SYS -p MANAGER
```

```sql
SELECT * FROM V$NODE_STATUS;
```

### 9. 데이터 복제 확인

Warehouse 그룹 내 복제가 정상 동작하는지 간단한 INSERT로 확인합니다.

```sql
-- Broker를 통해 데이터 입력
CREATE LOG TABLE cluster_check_test (id INTEGER, ts DATETIME);
INSERT INTO cluster_check_test VALUES (1, NOW);

-- Broker에서 입력 결과 확인
SELECT COUNT(*) FROM cluster_check_test;
```

Warehouse 직접 SQL 접속은 일반 애플리케이션 경로가 아니라 복제 진단용 관리 절차입니다.
`machcoordinatoradmin --cluster-status`에서 같은 복제 그룹의 active·standby peer를
확인한 뒤, 필요한 경우에만 각 peer의 네이티브 포트에 관리 계정으로 접속해 동일한 조회 결과를
비교합니다. 서로 다른 Warehouse 그룹의 모든 노드가 같은 행을 가진다고 가정하지 마십시오.

검증이 끝나면 Broker 연결에서 테이블을 정리합니다.

```sql
DROP TABLE cluster_check_test;
```

---

## 문제 발생 시

- 서버 로그: `$MACHBASE_HOME/trc/machbase.trc`
- [운영·장애 진단](/dbms/operations-configuration-recovery/diagnosis-observability/) 참고
