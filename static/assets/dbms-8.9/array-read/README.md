# DBMS 8.9 숫자 ARRAY와 READ JOIN 실습

Standard Edition의 전용 실습 DB에서 실행합니다.

1. anchors.csv, payload.jsonl, bad-payload.jsonl과 ticks.csv를 서버의 /srv/dfq/array-read/에 둡니다.
   다른 경로에서는 SQL 파일의 경로를 바꿉니다. 실행 계정에 서버 디렉터리 READ 권한이 필요합니다.
2. 실습 DB에 M89_ARRAY_LAB, M89_READ_HISTORY, M89_READ_TAG, M89_READ_TICKS, M89_ARRAY_PY가 없는지 확인합니다.
   각각의 예제는 자신이 만든 테이블을 마지막에 삭제합니다.
3. `machsql -f array.sql`과 `machsql -f read-join.sql`을 실행합니다. 서버·계정과
   포트는 -s, -u, -P 옵션으로 지정합니다.

array.sql의 (ID, 길이, 마스크)는 (1, 3, 05), (2, 0, 빈 BINARY), (3, NULL, NULL),
(4, 1, 00)입니다. CAST 길이는 2입니다. 희소 배열의 마지막 값은 -3이며 길이는
65,536입니다. stride 2 슬라이스의 두 번째 값은 30입니다.

read-join.sql의 두 JOIN 결과는 (관측 ID, 저장 ID, 길이) 순으로 (1, 1, 3), (2, 2, 0),
(3, NULL, NULL)입니다. ASOF에는 출처 JSON 열도 있습니다. JSONL 길이는 3, 0, NULL입니다.

relative-join.sql은 VIEW에서 정수 tick을 나노초로 변환하고 TAG의 시각과 결합합니다.
두 결과의 TARGET_NS는 1700000000000000001이고 저장 ID는 101과 NULL입니다.

array-errors.sql은 의도적 오류만 모았습니다. 각 문장을 개별 실행하고 선언 상한, 인덱스,
stride, READ 목록 길이, READ 원소 변환 오류를 확인합니다.

배열 확장을 협상하는 Machbase Python SDK를 설치한 환경에서 다음을 실행하면 길이
0, 1, 1,024, 1,025, 65,536과 NULL ARRAY의 bind·fetch 왕복을 확인할 수 있습니다.

```bash
export M89_HOST=127.0.0.1 M89_PORT=5656 M89_USER=SYS
read -rsp '실습 DB 비밀번호: ' M89_PASSWORD
export M89_PASSWORD
python3 python-array.py
unset M89_PASSWORD
```
