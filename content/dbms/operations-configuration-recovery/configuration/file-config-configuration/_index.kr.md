---
type: docs
title: '13.2.1 설정 파일 위치와 적용 절차'
weight: 10
---

## 설정 파일 위치

Machbase의 설정 파일은 다음 경로에 있습니다.

```
$MACHBASE_HOME/conf/machbase.conf
```

서버를 시작할 때 이 파일을 읽어 모든 파라미터를 초기화합니다. 파일이 없으면 내장된 기본값으로 동작합니다.

## 설정 파일 구조

`machbase.conf`는 `파라미터명 = 값` 형식으로 구성됩니다. `#`으로 시작하는 줄은 주석으로 처리됩니다.

```ini
# 네트워크 포트 설정
PORT_NO = 5656

# 최대 세션 수
MAX_SESSION_COUNT = 4096

# 프로세스 최대 메모리 (8GB)
PROCESS_MAX_SIZE = 8589934592

# 데이터 저장 경로 ('?'는 $MACHBASE_HOME을 의미)
DBS_PATH = ?/dbs

# 체크포인트 주기 (초)
DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC = 120
```

## 설정 변경 절차

설정을 변경하는 방법은 파라미터의 종류에 따라 다릅니다.

### 재시작이 필요한 설정

포트 번호, 데이터 경로, 일부 버퍼 크기처럼 서버 초기화 시에만 적용되는 설정은 파일을 수정한 뒤 서버를 재시작해야 합니다.

```bash
# 1. 설정 파일 수정
vi $MACHBASE_HOME/conf/machbase.conf

# 2. 서버 재시작
machadmin -s
machadmin -u
```

### 런타임 즉시 적용 설정

`MAX_SESSION_COUNT`, `PROCESS_MAX_SIZE`, `PVO_CACHE_ENABLE` 등 일부 파라미터는 `ALTER SYSTEM SET` 명령어로 서버를 재시작하지 않고 즉시 변경할 수 있습니다. Result Cache의 `RS_CACHE_*` 전역 기본값은 설정 파일을 수정하고 재시작하여 적용하며, 현재 세션의 Result Cache 동작은 `ALTER SESSION SET RS_CACHE_ENABLE = ...`처럼 세션 단위로 변경합니다. 자세한 내용은 [Runtime 변경 가능 설정](../alter-start-restart-configuration-runtime/)을 참고합니다.

## 설정 파일 백업

설정 파일을 변경하기 전에 현재 파일을 백업해 두는 것을 권장합니다.

```bash
cp $MACHBASE_HOME/conf/machbase.conf \
   $MACHBASE_HOME/conf/machbase.conf.bak.$(date +%Y%m%d)
```

운영 환경에서는 설정 변경 이력을 Git 등 버전 관리 시스템으로 관리하면 변경 추적과 롤백이 용이합니다.

## 현재 설정값 확인

서버 실행 중에는 `v$property` 뷰로 현재 적용된 설정값을 확인할 수 있습니다.

```sql
-- 전체 설정 조회
SELECT name, value FROM v$property ORDER BY name;

-- 특정 파라미터 조회
SELECT name, value FROM v$property WHERE name = 'PORT_NO';

-- 키워드로 검색
SELECT name, value FROM v$property WHERE name LIKE 'RS_CACHE%';
```
