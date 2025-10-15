---
type: docs
title: '설정'
weight: 100
---

Machbase의 서버 설정 및 튜닝 가이드입니다. 워크로드와 하드웨어에 맞게 서버 설정을 최적화하는 방법을 알아봅니다.

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

## 주요 설정 파라미터

### 네트워크 설정

```properties
# 서버 포트
PORT_NO = 5656

# 바인드 IP 주소 (모든 인터페이스는 0.0.0.0)
BIND_IP_ADDRESS = 0.0.0.0

# 최대 연결 수
MAX_CONNECTION = 100
```

### 메모리 설정

```properties
# 공유 버퍼 풀 (권장: 사용 가능한 RAM의 50-70%)
BUFFER_POOL_SIZE = 2G

# Volatile 테이블 메모리
VOLATILE_TABLESPACE_SIZE = 1G

# 쿼리당 메모리 제한
MAX_QPX_MEM = 512M

# 로그 버퍼 크기
LOG_BUFFER_SIZE = 64M
```

### 성능 설정

```properties
# 체크포인트 간격 (초)
CHECKPOINT_INTERVAL_SEC = 600

# 쿼리 타임아웃 (초)
QUERY_TIMEOUT = 60

# 최대 병렬 쿼리 수
MAX_PARALLEL_QUERY = 4
```

### 스토리지 설정

```properties
# 데이터베이스 디렉토리
DB_DIR = $MACHBASE_HOME/dbs

# 로그 디렉토리
LOG_DIR = $MACHBASE_HOME/dbs

# 트레이스 로그 디렉토리
TRC_LOG_DIR = $MACHBASE_HOME/trc
```

### 백업 설정

```properties
# 백업 압축
BACKUP_COMPRESSION = 1

# 백업 스레드 수
BACKUP_THREAD_COUNT = 4
```

## 워크로드별 튜닝

### 쓰기 집약적 워크로드

```properties
# 버퍼 증가
BUFFER_POOL_SIZE = 4G
LOG_BUFFER_SIZE = 128M

# 체크포인트 빈도 감소
CHECKPOINT_INTERVAL_SEC = 900

# 연결 수 증가
MAX_CONNECTION = 200
```

### 읽기 집약적 워크로드

```properties
# 버퍼 풀 증가
BUFFER_POOL_SIZE = 8G

# 쿼리 메모리 증가
MAX_QPX_MEM = 1G

# 병렬 쿼리 활성화
MAX_PARALLEL_QUERY = 8
```

### 혼합 워크로드

```properties
# 균형 잡힌 설정
BUFFER_POOL_SIZE = 4G
LOG_BUFFER_SIZE = 64M
MAX_QPX_MEM = 512M
CHECKPOINT_INTERVAL_SEC = 600
MAX_PARALLEL_QUERY = 4
```

## 설정 모니터링

### 시스템 테이블

```sql
-- 설정 확인
SELECT * FROM SYSTEM_.SYS_PROPERTIES_;

-- 메모리 사용량 확인
SHOW STORAGE;
```

### 로그 설정

```properties
# 트레이스 로그 활성화
TRC_LOG_LEVEL = 1

# 로그 파일 크기
TRC_LOG_FILE_SIZE = 10M

# 로그 파일 수
TRC_LOG_FILE_COUNT = 10
```

## 보안 설정

### 접근 제어

```properties
# 네트워크 접근 제한
BIND_IP_ADDRESS = 192.168.1.100

# 최대 연결 수 감소
MAX_CONNECTION = 50
```

### SSL/TLS

```properties
# SSL 활성화
SSL_ENABLE = 1
SSL_CERT = /path/to/cert.pem
SSL_KEY = /path/to/key.pem
```

## 클러스터 설정

클러스터 배포의 경우 추가 설정이 필요합니다:

```properties
# 클러스터 모드
CLUSTER_ENABLE = 1

# 클러스터 ID
CLUSTER_ID = cluster01

# 코디네이터 주소
COORDINATOR_HOST = 192.168.1.10
COORDINATOR_PORT = 6656
```

전체 클러스터 설정은 [클러스터 설치](../../dbms/install/cluster/)를 참조하세요.

## 설정 모범 사례

1. **변경 전 설정 백업** - 원본 설정 저장
2. **스테이징 환경에서 테스트** - 프로덕션 적용 전 검증
3. **변경 후 모니터링** - 로그 및 성능 확인
4. **변경 사항 문서화** - 변경 이력 유지
5. **적절한 값 사용** - 하드웨어 및 워크로드에 맞춤

## 일반적인 설정 문제

### 메모리 부족

**증상**: 서버 크래시 또는 느린 성능

**해결책**:
```properties
# 메모리 사용량 감소
BUFFER_POOL_SIZE = 1G  # 버퍼 풀 감소
MAX_QPX_MEM = 256M     # 쿼리 메모리 감소
```

### 연결 수 초과

**증상**: "Max connections exceeded" 오류

**해결책**:
```properties
# 연결 제한 증가
MAX_CONNECTION = 200
```

### 느린 쿼리

**증상**: 쿼리 타임아웃

**해결책**:
```properties
# 쿼리 타임아웃 증가
QUERY_TIMEOUT = 120

# 쿼리 메모리 증가
MAX_QPX_MEM = 1G

# 병렬 쿼리 활성화
MAX_PARALLEL_QUERY = 8
```

## 전체 설정 참조

자세한 설정 문서는 다음을 참조하세요:
- [설정 속성](../../dbms/config-monitor/property/) - 전체 파라미터 참조
- [시스템 테이블](../../dbms/config-monitor/meta-table/) - 시스템 메타데이터
- [가상 테이블](../../dbms/config-monitor/virtual-table/) - 모니터링 테이블

## 설정 템플릿

```properties
# machbase.conf - 프로덕션 설정 템플릿

# 네트워크
PORT_NO = 5656
BIND_IP_ADDRESS = 0.0.0.0
MAX_CONNECTION = 100

# 메모리 (사용 가능한 RAM에 따라 조정)
BUFFER_POOL_SIZE = 4G
VOLATILE_TABLESPACE_SIZE = 1G
MAX_QPX_MEM = 512M
LOG_BUFFER_SIZE = 64M

# 성능
CHECKPOINT_INTERVAL_SEC = 600
QUERY_TIMEOUT = 60
MAX_PARALLEL_QUERY = 4

# 스토리지
DB_DIR = $MACHBASE_HOME/dbs
LOG_DIR = $MACHBASE_HOME/dbs
TRC_LOG_DIR = $MACHBASE_HOME/trc

# 로깅
TRC_LOG_LEVEL = 1
TRC_LOG_FILE_SIZE = 10M
TRC_LOG_FILE_COUNT = 10
```

## 다음 단계

- **설정 적용**: [도구 참조](../tools-reference/) - machadmin 사용법
- **성능 모니터링**: [문제 해결](../troubleshooting/) - 성능 튜닝
- **고급 설정**: [고급 기능](../advanced-features/) - 클러스터 설정
