---
type: docs
title: 'INSTALL LICENSE'
weight: 30
---

서버를 재시작하지 않고 라이선스 파일을 설치합니다.

## 구문

### 기본 경로 설치

```sql
ALTER SYSTEM INSTALL LICENSE;
```

`$MACHBASE_HOME/conf/license.dat` 경로에 있는 라이선스 파일을 설치합니다. 설치 전 라이선스의 유효성을 검증하며, 검증에 성공하면 즉시 적용됩니다.

### 지정 경로 설치

```sql
ALTER SYSTEM INSTALL LICENSE = '/경로/license.dat';
```

지정한 경로의 라이선스 파일을 설치합니다. 운영 절차에서는 현재 작업 디렉터리에 의존하지 않도록 절대 경로 사용을 권장하며, 설치 전 라이선스 유효성을 검증합니다.

**오류 상황**

- 지정한 경로에 파일이 없는 경우
- 라이선스 파일이 손상된 경우
- 현재 서버 환경에 맞지 않는 라이선스 파일인 경우

## 사용 예시

```sql
-- 기본 경로($MACHBASE_HOME/conf/license.dat)에서 설치
ALTER SYSTEM INSTALL LICENSE;

-- 지정 경로에서 설치
ALTER SYSTEM INSTALL LICENSE = '/tmp/new_license.dat';

-- 설치된 라이선스 정보 확인
SELECT * FROM v$license_info;
```

## 라이선스 정보 확인

```sql
SELECT * FROM v$license_info;
```

`v$license_info`에서 확인할 수 있는 주요 항목:

| 컬럼 | 설명 |
|---|---|
| `EDITION` | 에디션 (Standard, Cluster 등) |
| `EXPIRY_DATE` | 라이선스 만료일 |
| `MAX_NODE` | 최대 허용 노드 수 |
| `MAX_SENSORS` | 최대 허용 센서(태그) 수 |
| `MAX_STORAGE_SIZE` | 최대 스토리지 크기 |

## 참고

- 라이선스 파일은 Machbase 공식 채널을 통해 발급받습니다.
- 라이선스 만료 전 갱신을 권장합니다.
- 서버 시작 시 라이선스를 확인하며, 라이선스가 없거나 만료된 경우 제한된 모드로 동작할 수 있습니다.
- 라이선스 관련 상세 내용은 [라이선스 관리](../../server-database/license/)를 참고하십시오.
