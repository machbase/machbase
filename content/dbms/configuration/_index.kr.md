---
type: docs
title: '설정'
weight: 100
toc: true
---

Machbase 서버 프로퍼티는 서버 시작 시 `machbase.conf`에서 읽는 키-값 쌍입니다. 이
페이지는 자주 변경하는 프로퍼티 예시를 보여 주며, 정확한 범위는 전체 프로퍼티
레퍼런스를 기준으로 확인합니다.

## 설정 파일

### 위치

```bash
$MACHBASE_HOME/conf/machbase.conf
```

### 설정 편집

```bash
# 편집 전 서버 종료
machadmin -s

# 설정 파일 편집
vi $MACHBASE_HOME/conf/machbase.conf

# 새 설정으로 서버 시작
machadmin -u
```

대부분의 프로퍼티는 시작 시 적용됩니다. 프로퍼티 레퍼런스에 런타임 변경 가능 여부가
명시되어 있지 않다면 서버를 중지한 상태에서 변경합니다.

## 주요 설정 파라미터

### 네트워크와 세션

```properties
# 서버 포트
PORT_NO = 5656

# 바인드 IP 주소. 모든 인터페이스에서 수신하려면 0.0.0.0을 사용합니다.
BIND_IP_ADDRESS = 0.0.0.0

# 최대 동시 세션 수
MAX_SESSION_COUNT = 4096

# 세션 유휴/쿼리 타임아웃(초). 0이면 사용하지 않습니다.
SESSION_IDLE_TIMEOUT_SEC = 0
SESSION_QUERY_TIMEOUT_SEC = 0
```

### 메모리

```properties
# machbased 프로세스 최대 메모리
PROCESS_MAX_SIZE = 8589934592 # 8GB

# 디스크 컬럼 테이블스페이스 메모리 제한
DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE = 8589934592 # 8GB

# Volatile 테이블스페이스 메모리 제한
VOLATILE_TABLESPACE_MEMORY_MAX_SIZE = 2147483648 # 2GB

# 쿼리당 질의 처리기 메모리 제한
MAX_QPX_MEM = 1073741824 # 1GB
```

### 스토리지와 체크포인트

```properties
# 데이터베이스 디렉터리. ?는 $MACHBASE_HOME으로 확장됩니다.
DBS_PATH = ?/dbs

# 테이블/인덱스 체크포인트 간격(초)
DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC = 120
DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC = 120
```

### 질의 처리

```properties
# 병렬 질의 계수. Standard 빌드 기본값은 0, Cluster 빌드 기본값은 4입니다.
QUERY_PARALLEL_FACTOR = 0

# Tag 테이블 스캔 방향: -1 역방향, 0 엔진 결정, 1 정방향
TABLE_SCAN_DIRECTION = 0
```

### 트레이스 로그

```properties
# 트레이스 로그 디렉터리. ?는 $MACHBASE_HOME으로 확장됩니다.
TRACE_LOGFILE_PATH = ?/trc

# 트레이스 로그 파일 크기와 보관 개수
TRACE_LOGFILE_SIZE = 10485760 # 10MB
TRACE_LOGFILE_COUNT = 1000

# 트레이스 로그 레벨
TRACE_LOG_LEVEL = 277
```

## 튜닝 예시

### 메모리 예산 확대

```properties
PROCESS_MAX_SIZE = 17179869184 # 16GB
DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE = 12884901888 # 12GB
MAX_QPX_MEM = 2147483648 # 2GB
```

### 동시 접속 확대

```properties
MAX_SESSION_COUNT = 8192
MAX_STMT_COUNT_PER_SESSION = 2048
```

### 장시간 쿼리 허용

```properties
# 쿼리 타임아웃 비활성화
SESSION_QUERY_TIMEOUT_SEC = 0

# 또는 2분 타임아웃 설정
SESSION_QUERY_TIMEOUT_SEC = 120
```

## 설정 모니터링

```sql
-- 현재 프로퍼티 값 확인
SELECT * FROM V$PROPERTY;

-- 스토리지 사용량 확인
SELECT * FROM V$STORAGE;
```

## 보안 설정

```properties
# 특정 인터페이스에서만 수신
BIND_IP_ADDRESS = 192.168.1.100

# 원격 접근을 차단하고 리스너를 loopback에 바인드
GRANT_REMOTE_ACCESS = 0
```

## 클러스터 설정

Cluster Edition에는 추가 프로퍼티가 있습니다. 자주 확인하는 예시는 다음과 같습니다.

```properties
# 클러스터 링크 엔드포인트
CLUSTER_LINK_HOST = localhost
CLUSTER_LINK_PORT_NO = 3868

# 코디네이터 스토리지 경로
COORDINATOR_DBS_PATH = ?/dbs

# 코디네이터 HTTP 관리 포트
HTTP_ADMIN_PORT = 5779
```

전체 클러스터 설정은 [클러스터 설치](../installation/cluster/)를 참조하세요.

## 설정 모범 사례

1. 변경 전 `machbase.conf`를 백업합니다.
2. 한 번에 하나의 튜닝 영역만 변경합니다.
3. 운영 반영 전 프로퍼티 레퍼런스에서 값의 범위를 확인합니다.
4. 시작 시 적용되는 프로퍼티를 변경한 뒤 서버를 재시작합니다.
5. 변경 후 `V$PROPERTY`, 트레이스 로그, 워크로드 동작을 모니터링합니다.

## 전체 설정 참조

- [설정 프로퍼티](./property/) - Standard 서버 프로퍼티 레퍼런스
- [클러스터 설정 프로퍼티](./property-cl/) - Cluster Edition 프로퍼티 레퍼런스
- [메타 테이블](./meta-table/) - 시스템 메타데이터 테이블
- [가상 테이블](./virtual-table/) - 런타임 모니터링 테이블
