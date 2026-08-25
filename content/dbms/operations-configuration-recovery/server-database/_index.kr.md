---
type: docs
title: '14.1 서버와 데이터베이스 운영'
weight: 10
toc: true
---

`machadmin`은 server instance 시작·종료, physical database 생성·삭제, license 설치,
offline restore를 수행합니다. SQL `CREATE DATABASE`로 만드는 logical database와
`machadmin -c`의 physical instance database를 구분합니다.

## 주요 option 확인

```bash
"$MACHBASE_HOME/bin/machadmin" -h
```

설치된 release의 help를 기준으로 option과 영향을 확인합니다.

<a id="start-server"></a>

## Server 시작과 종료

상태 확인은 안전하게 실행할 수 있습니다.

```bash
"$MACHBASE_HOME/bin/machadmin" -e
```

start·shutdown은 service manager와 운영 runbook 중 한 경로로 통일합니다.

- 시작 전 config, license, data path, free space를 확인합니다.
- 시작 후 `machadmin -e`, 5656 connection, 가벼운 SQL, server log를 확인합니다.
- 정상 종료 전 새 connection·입력을 차단하고 진행 중 transaction·backup·Appender를
  확인합니다.
- 강제 종료는 정상 종료가 반복 실패하고 recovery 영향을 판단한 경우에만 사용합니다.
- recovery mode를 임의로 강제하지 말고 오류와 공식 복구 절차를 확인합니다.

명령 출력 예시는 release마다 달라질 수 있으므로 성공 문구 전체를 자동화 조건으로
사용하지 않습니다. process exit code와 실제 connection을 함께 확인합니다.

<a id="create-delete-database"></a>

## Physical instance database

`machadmin -c`와 `machadmin -d`는 `DBS_PATH`의 physical instance data를 생성·삭제합니다.
logical database 작업은 [다중 데이터베이스](../multi-database/)의 SQL을 사용합니다.

physical database 삭제·초기화는 instance 전체 data를 잃을 수 있는 파괴적 작업입니다.
일반 예제로 shutdown→destroy→create→startup 명령을 연속 제공하지 않습니다.

실행 전 확인:

1. 대상 `MACHBASE_HOME`과 `DBS_PATH`의 절대 경로
2. service·process가 완전히 종료됐는지
3. 최신 backup과 격리 restore 검증
4. 보존해야 할 config, license, log
5. rollback 가능 여부와 예상 recovery 시간
6. 두 명의 작업자가 instance·path를 교차 확인했는지

data directory 내부 file과 metadata를 수동으로 생성·이동·삭제하지 않습니다.

<a id="license"></a>

## License 설치와 확인

license file은 비밀정보로 취급하고 내용이나 실제 key를 문서·ticket·log에 복사하지
않습니다.

| 상태 | 방법 |
|------|------|
| server 종료 상태의 설치 | 현재 release의 `machadmin` license option |
| server 실행 중 설치 | `ALTER SYSTEM INSTALL LICENSE` |
| 적용 확인 | `machadmin` license info와 `V$LICENSE_INFO` |

```sql
SELECT *
FROM V$LICENSE_INFO;
```

설치 전 대상 instance, edition, 유효 기간, file permission을 확인합니다. online 설치
경로는 server process가 읽을 수 있어야 합니다. 갱신 후 새 connection과 필요한 edition
기능을 검증하고 원본 license file의 보관 정책을 적용합니다.

## 장애 시 자료

- `machadmin -e` 결과와 exit code
- release·edition과 `MACHBASE_HOME`
- 실제 config·data path
- server 시작·종료 시각
- 최초 오류 전후 server log
- filesystem free space와 permission
- 직전 config·license·storage 변경

server가 시작되지 않는다는 이유로 physical database를 삭제하거나 reset recovery를 먼저
실행하지 않습니다. backup을 보존한 채 원인을 진단합니다.
