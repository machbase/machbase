---
type: docs
title: 'machsql 로그'
weight: 30
---

`machsql`은 Machbase 서버에 직접 접속하는 대화형 SQL 클라이언트 도구입니다. machsql은 별도의 로그 파일을 생성하지 않지만, 실행한 SQL 명령의 이력은 히스토리 파일에 기록됩니다.

## SQL 실행 이력 (History)

machsql을 대화형 모드로 실행하면 입력한 모든 SQL 명령이 히스토리 파일에 저장됩니다.

**기본 위치**:
```
~/.machsql_history
```

이 파일은 현재 OS 사용자의 홈 디렉터리에 생성됩니다.

## 히스토리 파일 확인

```bash
# 최근 실행 이력 확인
cat ~/.machsql_history

# 최근 50개 이력만 확인
tail -50 ~/.machsql_history

# 특정 키워드를 포함한 이력 검색
grep -i 'sensor_log' ~/.machsql_history
```

## machsql 내에서 이력 조회

machsql 실행 중에 방향키(위/아래)를 눌러 이전 명령을 탐색할 수 있습니다.

```sql
-- machsql 실행
$ machsql -u sys -p manager -s 127.0.0.1

-- 접속 후 이력 활용 예시
Mach> SELECT * FROM sensor_log LIMIT 10;  -- 실행 후 히스토리에 저장됨
```

## machsql 실행 로그 (리다이렉션)

특정 SQL 스크립트 실행 결과를 파일로 저장하려면 셸 리다이렉션을 사용합니다.

```bash
# SQL 파일 실행 결과를 파일로 저장
machsql -u sys -p manager -s 127.0.0.1 -f query.sql > result.log 2>&1

# 인라인 SQL 실행 결과 저장
machsql -u sys -p manager -s 127.0.0.1 \
  -q "SELECT count(*) FROM sensor_log" > count.log
```

## 비대화형 모드에서의 오류 출력

스크립트 형태로 machsql을 실행할 때 발생하는 오류는 표준 오류(stderr)로 출력됩니다.

```bash
# 오류만 별도 파일로 저장
machsql -u sys -p manager -s 127.0.0.1 -f setup.sql \
  > /dev/null 2> setup.err

# 오류 발생 여부 확인
if [ -s setup.err ]; then
    echo "오류 발생:"
    cat setup.err
fi
```

## 주요 machsql 옵션

| 옵션 | 설명 |
|------|------|
| `-s <HOST>` | 서버 주소 |
| `-P <PORT>` | 서버 포트 (기본값: 5656) |
| `-u <USER>` | 사용자 이름 |
| `-p <PASS>` | 패스워드 |
| `-f <FILE>` | SQL 스크립트 파일 실행 |
| `-q <SQL>` | 단일 SQL 문 실행 후 종료 |
| `-o <FILE>` | 결과 출력 파일 지정 |

> **참고**: machsql 이력 파일(`~/.machsql_history`)은 접속 사용자의 홈 디렉터리에 생성되므로, 서버 로그 디렉터리(`$MACHBASE_HOME/trc/`)와는 위치가 다릅니다.
