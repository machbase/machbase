---
type: docs
title: '12.9 애플리케이션에서 결과 받기'
weight: 90
toc: true
---

결과가 크면 클라이언트에 전체를 한 번에 쌓지 않고 순차 소비합니다.
기본 Python cursor의 전체 결과 수신과 선택적인 스트리밍을 구분합니다.

```python
import os
from machbaseAPI import connect
conn = connect(host=os.environ['DFQ_HOST'],port=int(os.environ['DFQ_PORT']),
               user=os.environ['DFQ_USER'],password=os.environ['DFQ_PASSWORD'])
cur = conn.cursor(stream=True, prepared=True)
try:
    cur.execute("SELECT id,v FROM READ('/srv/dfq/sensor.csv') ORDER BY id")
    while True:
        rows = cur.fetchmany(1000)
        if not rows:
            break
        print(rows)
finally:
    cur.close()
    conn.close()
```

スト리밍 rowcount는 EOF 전 -1이고 마지막 행 소비 후 소비 행 수로 바뀝니다.
fetchall은 남은 결과를 모두 수신하므로 메모리 사용에 주의합니다. 조기 close는 활성 statement를
해제합니다. 스트리밍 결과를 connection.result()의 전체 버퍼로 사용하지 않습니다.

## 메타데이터와 긴 값

READ는 일반 SELECT처럼 SQLPrepare/SQLDescribeCol 또는 JDBC ResultSetMetaData로
반환 타입을 확인합니다. reader의 mode=inspect/view=columns와 바깥 SELECT의 표현식
결과 타입은 다른 대상입니다.

SQLCLI/ODBC의 긴 TEXT/BINARY는 SQLGetData를 같은 컬럼에 반복 호출해 끝까지 읽습니다.
SQL_SUCCESS_WITH_INFO와 01004는 작은 버퍼에 따른 잘림을 뜻합니다. Indicator는 현재
호출 전의 잔여 길이이며 마지막 청크 뒤에는 SQL_NO_DATA입니다. 문자열 terminator 공간도
확보합니다. 행을 바꾸면 이전 행의 offset을 사용하지 않습니다.

빈 값의 indicator=0과 SQL_NULL_DATA를 구분합니다. BINARY의 CHAR 표시인 hex와
SQL_C_BINARY의 실제 바이트도 구분합니다. 큰 파일의 raw 청크는 부모별 offset으로 합칩니다.
기존 바인딩의 숫자·unsigned·LOB 지원 범위와 reader의 타입을 함께 확인합니다.
