---
type: docs
title: '13.2.7.2 machsql -z'
weight: 20
---

`machsql`은 `-z` 옵션으로 세션 타임존을 지정할 수 있습니다. 이 옵션을 사용하면 해당 세션에서 조회하는 DATETIME 값이 지정된 타임존 기준으로 변환되어 표시됩니다.

## 사용법

```bash
machsql -z +-HHMM [기타 옵션]
```

### 예시

```bash
# KST(UTC+9)로 접속
machsql -u SYS -p MANAGER -z +0900

# UTC로 접속
machsql -u SYS -p MANAGER -z +0000

# EST(UTC-5)로 접속
machsql -u SYS -p MANAGER -z -0500
```

## 동작 방식

`-z` 옵션으로 지정한 타임존은 해당 `machsql` 세션에만 적용됩니다. 서버의 기본 타임존 설정은 변경되지 않습니다.

```
mach@localhost:~$ machsql -u SYS -p MANAGER -z +0900

Mach> show timezone;
Timezone : +0900

Mach> SELECT sysdate FROM v$tables LIMIT 1;
SYSDATE
----------------------------------
2026-07-07 10:30:00 000:000:000
```

같은 서버에 UTC로 접속하면 9시간 차이가 납니다.

```
mach@localhost:~$ machsql -u SYS -p MANAGER -z +0000

Mach> SELECT sysdate FROM v$tables LIMIT 1;
SYSDATE
----------------------------------
2026-07-07 01:30:00 000:000:000
```

## 세션 내 타임존 확인

접속 후 현재 세션의 타임존을 확인합니다.

```sql
SHOW TIMEZONE;
```

## 주의 사항

- `-z` 옵션을 지정하지 않으면 서버의 기본 타임존이 세션에 적용됩니다.
- 데이터가 저장될 때는 내부적으로 UTC로 변환되어 저장됩니다. `-z` 옵션은 표시와 입력 해석에만 영향을 미칩니다.
- INSERT 또는 Append로 데이터를 입력할 때 DATETIME 값도 세션 타임존을 기준으로 해석하여 UTC로 변환한 뒤 저장합니다.
