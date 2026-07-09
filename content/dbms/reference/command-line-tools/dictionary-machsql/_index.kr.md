---
type: docs
title: '17.4.2 machsql 명령/옵션 사전'
weight: 20
---

`machsql`은 터미널에서 SQL 쿼리를 대화형으로 실행하는 클라이언트 도구입니다. SQL 스크립트 파일 실행, 결과 파일 저장, 공개키 인증도 지원합니다.

## 옵션 목록

```bash
machsql -h
```

| 짧은 옵션 | 긴 옵션 | 기본값 | 설명 |
|----------|---------|--------|------|
| `-s` | `--server` | 127.0.0.1 | 접속할 서버 IP 주소 |
| `-P` | `--port` | 5656 | 서버 포트 번호 |
| `-u` | `--user` | SYS | 사용자 이름 |
| `-p` | `--password` | MANAGER | 사용자 비밀번호 |
| `-K` | `--auth-key-file` | - | 공개키 인증용 개인키 파일 경로 (8.5 이상) |
| | `--auth-sig-scheme` | - | 인증 서명 스킴. `ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS` (8.5 이상) |
| `-f` | `--script` | - | 실행할 SQL 스크립트 파일 |
| `-o` | `--output` | - | 쿼리 결과를 저장할 파일 이름 |
| `-r` | `--format` | csv | 출력 파일 포맷 (`csv`, `json` 등) |
| `-z` | `--timezone` | - | 타임존 설정. 예: `+0900`, `-1230` |
| `-n` | `--nls` | - | NLS 설정 |
| `-c` | `--connstr` | - | 추가 연결 매개변수 문자열 (6.1 이상) |
| `-i` | `--silent` | - | 저작권 배너 없이 실행 |
| `-v` | `--verbose` | - | 상세 출력 |
| `-x` | `--testing` | - | 테스트 모드로 실행 |
| `-h` | `--help` | - | 옵션 목록 출력 |

## 접속 예시

기본 접속:

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER
machsql --server=localhost --user=SYS --password=MANAGER
```

포트 지정:

```bash
machsql -s 192.168.1.10 -P 5656 -u SYS -p MANAGER
```

SQL 스크립트 실행:

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -f create_tables.sql
```

타임존 지정:

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -z +0900
machsql -s 127.0.0.1 -u SYS -p MANAGER -z -1230
```

결과를 파일로 저장:

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -o result.csv -f query.sql
```

## 공개키 인증 (Machbase 8.5 이상)

비밀번호 대신 공개키 기반 challenge 인증을 사용할 수 있습니다.

ECDSA 키로 접속:

```bash
machsql -s 127.0.0.1 -u app_user \
    -K /opt/machbase/keys/app_user_ecdsa.pem \
    --auth-sig-scheme=ECDSA
```

RSA-PSS 키로 접속:

```bash
machsql -s 127.0.0.1 -u app_user \
    -K /opt/machbase/keys/app_user_rsa.pem \
    --auth-sig-scheme=RSA_PSS
```

지원 키 알고리즘:

| 알고리즘 | 키 파라미터 | 기본 서명 스킴 |
|---------|-----------|--------------|
| ECDSA | P-256, P-384, P-521 | `ECDSA` |
| RSA | 2048, 3072, 4096 bits | `RSA_PKCS1_V15` |

## 추가 연결 매개변수 (6.1 이상)

`-c` 옵션으로 추가 연결 파라미터를 지정합니다.

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -P 5656 \
    -c ALTERNATIVE_SERVERS=192.168.0.147:9209;CONNECTION_TIMEOUT=10
```

환경변수로도 설정할 수 있습니다.

```bash
export MACHBASE_CONNECTION_STRING="ALTERNATIVE_SERVERS=192.168.0.148:8888;CONNECTION_TIMEOUT=3"
machsql -s 127.0.0.1 -u SYS -p MANAGER
```

`-c` 옵션이 환경변수보다 우선 적용됩니다.

## machsql 내장 명령

machsql 프롬프트(`Mach>`)에서 사용할 수 있는 내장 명령입니다.

| 명령 | 설명 |
|------|------|
| `SHOW TABLES` | 전체 테이블 목록 출력 |
| `SHOW TABLE table_name` | 특정 테이블의 컬럼 및 인덱스 정보 출력 |
| `SHOW INDEXES` | 전체 인덱스 목록 출력 |
| `SHOW INDEX index_name` | 특정 인덱스 정보 출력 |
| `SHOW INDEXGAP` | 인덱스 생성 GAP 정보 출력 |
| `SHOW LSM` | LSM 인덱스 생성 정보 출력 |
| `SHOW TABLESPACES` | 전체 테이블스페이스 목록 출력 |
| `SHOW TABLESPACE name` | 특정 테이블스페이스 정보 출력 |
| `SHOW STORAGE` | 테이블별 디스크 사용량 출력 |
| `SHOW STATEMENTS` | 서버에 등록된 쿼리 목록 출력 |
| `SHOW USERS` | 사용자 목록 출력 |
| `SHOW LICENSE` | 라이선스 정보 출력 |

## 사용 예시

```bash
# 대화형 모드로 접속
machsql -s 127.0.0.1 -u SYS -p MANAGER

# 접속 후 테이블 확인
Mach> SHOW TABLES;

# 테이블 구조 확인
Mach> SHOW TABLE sensor_data;

# SQL 스크립트를 실행하고 결과를 CSV로 저장
machsql -s 127.0.0.1 -u SYS -p MANAGER \
    -f report.sql -o report_output.csv -i
```
