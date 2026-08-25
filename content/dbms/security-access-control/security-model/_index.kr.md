---
type: docs
title: '15.1 보안 모델 개요'
weight: 10
toc: true
---

Machbase의 보안 모델은 **사용자 계정**, **권한(GRANT/REVOKE)**, **접속 제어(IP/인증)** 세 요소가 계층적으로 결합된 구조입니다.

## Machbase 보안 구조

```
클라이언트 연결 요청
        │
        ▼
┌─────────────────────┐
│   접속 제어          │  BIND_IP_ADDRESS, GRANT_REMOTE_ACCESS
│   (네트워크 레이어)   │
└────────┬────────────┘
         │ 허용된 경우
         ▼
┌─────────────────────┐
│   인증               │  비밀번호 인증 또는 AUTH KEY (공개키) 인증
│   (사용자 식별)       │
└────────┬────────────┘
         │ 인증 성공
         ▼
┌─────────────────────┐
│   권한 검사          │  GRANT/REVOKE로 부여된 권한 확인
│   (작업 허용 여부)    │  테이블 권한 + 데이터베이스 권한
└─────────────────────┘
```

연결 요청은 먼저 네트워크 접속 제어를 통과해야 하고, 이후 사용자 인증을 거쳐, 마지막으로 해당 작업에 필요한 권한이 부여되어 있는지 확인하는 순서로 진행됩니다.

## 기본 계정: SYS

Machbase를 설치하면 `SYS` 계정이 자동으로 생성됩니다. SYS는 슈퍼유저로서 모든 데이터베이스 작업을 수행할 수 있고, 다른 사용자를 생성하고 권한을 부여합니다.

| 항목 | 내용 |
|------|------|
| 계정명 | `SYS` |
| 기본 비밀번호 | `MANAGER` |
| 권한 | 모든 권한 보유 (슈퍼유저) |
| 삭제 가능 여부 | 불가 |

> **운영 환경 필수 조치**: SYS 계정의 기본 비밀번호(`MANAGER`)는 설치 후 즉시 변경해야 합니다.
>
> ```sql
> ALTER USER SYS IDENTIFIED BY '새_비밀번호';
> ```

## 권한 종류

Machbase의 권한은 **테이블 권한**과 **데이터베이스 권한** 두 가지로 나뉩니다.

### 테이블 권한

특정 테이블에 대한 DML 작업을 허용합니다.

| 권한 | 설명 |
|------|------|
| `SELECT` | 테이블 조회 |
| `INSERT` | 데이터 입력 |
| `DELETE` | 데이터 삭제 |
| `UPDATE` | 데이터 수정 (LOG는 미지원, TAG data UPDATE는 Standard Edition에서 태그/축 조건 필요) |
| `ALL` | 위 모든 DML 권한 |

```sql
GRANT SELECT ON sensor_log TO reader_user;
GRANT SELECT, INSERT ON sys.sensor_log TO writer_user;
```

### 데이터베이스 권한

지정한 active database에 영향을 미치는 DDL 및 운영 작업을 허용합니다. 기본
`MACHBASEDB` 외에도 8.7.0 Standard Edition의 각 logical database를 대상으로 지정할
수 있습니다.

| 권한 | 허용 작업 |
|------|-----------|
| `CONNECT` | active database 연결, `USE`, 객체 탐색 |
| `CREATE` | CREATE TABLE/VIEW/INDEX/ROLLUP 등 |
| `DROP` | DROP TABLE/VIEW/INDEX/ROLLUP 등 |
| `DDL` | CREATE + DROP 묶음 |
| `ALTER` | ALTER SYSTEM |
| `BACKUP` | BACKUP DATABASE |
| `MOUNT` | MOUNT/UMOUNT DATABASE |
| `USAGE` | mounted database 탐색. table SELECT는 별도 필요 |
| `ALL` | 위 모든 데이터베이스 권한 |

```sql
GRANT DDL ON DATABASE factory_a TO deploy_user;
GRANT BACKUP ON DATABASE factory_a TO backup_user;
GRANT MOUNT ON DATABASE MACHBASEDB TO mount_user;
```

### 사용자 생성 시 기본 권한

사용자를 생성하면 다음 권한이 자동으로 부여됩니다.

- `SELECT`, `INSERT`, `DELETE`, `UPDATE`, `CREATE`, `DROP`

다음 권한은 포함되지 않으므로 필요할 때 명시적으로 부여해야 합니다.

- `ALTER`, `MOUNT`, `BACKUP`

## AUTH KEY 인증

비밀번호 인증 외에 공개키 기반의 AUTH KEY 인증을 사용할 수 있습니다. 클라이언트가 보유한 개인키로 서명하고, 서버에 등록된 공개키로 서명을 검증하는 challenge 방식입니다.

지원 알고리즘:

| 알고리즘 | 지원 파라미터 |
|----------|--------------|
| ECDSA | P-256, P-384, P-521 |
| RSA | 2048, 3072, 4096 bits |

AUTH KEY를 사용하면 비밀번호 유출 위험 없이 서비스 계정을 운영할 수 있습니다. 설정 방법은 [AUTH KEY 인증](../authentication-auth-key/)을 참고하십시오.

## 최소 권한 원칙

운영 환경에서는 다음 원칙을 적용하십시오.

- **SYS는 관리 작업 전용**: 일상적인 데이터 조회나 입력에는 SYS 계정을 사용하지 않습니다.
- **용도별 계정 분리**: 읽기 전용 계정, 데이터 입력 계정, 배포(DDL) 계정, 백업 계정을 분리합니다.
- **테이블 단위 권한 제한**: 계정이 접근해야 하는 테이블에만 필요한 DML 권한을 부여합니다.
- **정기 점검**: 불필요한 계정을 제거하고 권한이 과도하게 부여된 계정을 확인합니다.

```sql
-- 읽기 전용 계정
CREATE USER reader IDENTIFIED BY 'Reader#Strong123';
GRANT SELECT ON sys.sensor_log TO reader;

-- 데이터 입력 전용 계정
CREATE USER writer IDENTIFIED BY 'Writer#Strong123';
GRANT SELECT, INSERT ON sys.sensor_log TO writer;

-- DDL 전용 계정 (테이블 생성/삭제)
CREATE USER deploy IDENTIFIED BY 'Deploy#Strong123';
GRANT DDL ON DATABASE factory_a TO deploy;
```
