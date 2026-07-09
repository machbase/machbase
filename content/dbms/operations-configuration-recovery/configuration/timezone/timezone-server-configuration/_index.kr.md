---
type: docs
title: '13.2.7.1 서버 타임존 설정'
weight: 10
---

서버 타임존은 모든 클라이언트 세션의 기본 타임존이 됩니다. 클라이언트가 연결 시 타임존을 별도로 지정하지 않으면 서버 타임존이 세션에 자동으로 적용됩니다.

## TIMEZONE 프로퍼티

`machbase.conf`의 `TIMEZONE` 프로퍼티로 서버 기본 타임존을 설정합니다.

```ini
# machbase.conf
TIMEZONE = +0900   # 한국 표준시 (KST)
```

| 항목 | 값 |
|------|----|
| 기본값 | 설정하지 않으면 OS의 타임존을 사용 |
| 형식 | `+HHMM` 또는 `-HHMM` (5자리 오프셋) |
| 재시작 필요 | 예 |

`TIMEZONE`을 `machbase.conf`에 명시하지 않으면 서버가 운영 체제의 기본 타임존을 읽어 사용합니다. 예측 가능한 동작을 위해 운영 환경에서는 명시적으로 설정하는 것을 권장합니다.

## 변경 방법

1. `machbase.conf`를 편집합니다.

```bash
vi $MACHBASE_HOME/conf/machbase.conf
```

2. `TIMEZONE` 값을 원하는 오프셋으로 설정합니다.

```ini
TIMEZONE = +0000   # UTC로 변경
```

3. 서버를 재시작합니다.

```bash
machadmin -s
machadmin -u
```

## 현재 서버 타임존 확인

서버가 실행 중일 때 `machsql`에서 다음 명령어로 현재 타임존을 확인합니다.

```sql
SHOW TIMEZONE;
```

```
Mach> show timezone;
Timezone : +0900
```

`v$property` 뷰로도 확인할 수 있습니다.

```sql
SELECT name, value FROM v$property WHERE name = 'TIMEZONE';
```

## 주의 사항

- 서버 타임존을 변경하면 이후 연결되는 모든 세션의 기본 타임존이 바뀝니다. 기존 데이터는 UTC로 저장되어 있으므로 데이터 자체는 변경되지 않고, 표시되는 시각만 달라집니다.
- 클러스터 환경에서는 모든 노드의 타임존을 동일하게 설정해야 합니다.
- 타임존이 다른 클라이언트가 혼재하는 환경에서는 서버를 UTC(`+0000`)로 설정하고 각 클라이언트에서 세션 타임존을 지정하는 방식이 혼선을 줄이는 데 효과적입니다.
