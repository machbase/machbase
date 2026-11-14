---
type: docs
title: '12.10 권한과 운영'
weight: 100
toc: true
---

파일 조회에는 DB 권한과 서버 OS 권한이 함께 필요합니다. 파일은 서버에서 열고
VIEW를 통해 읽어도 파일 권한은 VIEW 실행 사용자 기준으로 검사합니다.

## 디렉터리 권한

SYS가 기존 절대 디렉터리에 권한을 부여합니다. analyst는 이미 존재하는 사용자 예입니다.

```sql
GRANT READ ON DIRECTORY '/srv/dfq' TO analyst;
REVOKE READ ON DIRECTORY '/srv/dfq' FROM analyst;
```

해당 디렉터리와 하위 디렉터리의 일반 파일을 허용하며 명시 READ·인용 FROM·raw·inspect에
같은 경계를 적용합니다. OS 읽기 권한도 필요합니다. 여러 파일·glob는 각 파일을 검사합니다.
REVOKE는 다음 실행·새 open부터 적용하고 이미 열린 cursor는 기존 수명대로 끝납니다.

승인 경로에는 심볼릭 링크나 중간 부모 이동을 사용하지 않습니다. Windows는 drive가 있는
로컬 절대 경로를 사용하며 UNC·장치 경로·junction/reparse point 등 안전하게 승인할 수 없는
경로를 허용하지 않습니다. 상대 경로는 클라이언트가 아니라 서버의 작업 디렉터리 기준입니다.
파일 존재를 알아내기 위한 권한 없는 조회도 허용하지 않습니다.

## 파일 변경과 일관성

best_effort는 실행 중 파일 내용 전체를 불변 snapshot으로 보장하지 않습니다.
고정 내용이 필요하면 지원되는 source.consistency=strong을 사용합니다. 큰 source·다중
source는 복사·검사·임시 공간 비용이 있으므로 필요한 범위와 reader의 한도를 확인합니다.

원본 revision·mapping token과 구조 schema ID는 서로 다릅니다. 재조회에서
SOURCE_CHANGED·MAPPING_CHANGED가 나면 오래된 token을 다른 설정에 재사용하지 않고
다시 탐색합니다. SQL 입력에는 파일 snapshot 옵션을 붙이지 않습니다.

## 병렬·메모리·임시 디스크

CSV/TSV·JSON/JSONL의 parallel=auto/true/false와 threads 상한은 reader에 따라 적용됩니다.
CPU_COUNT와 실효 작업자 수를 확인하며 auto가 항상 빠르다고 가정하지 않습니다.
Parquet·NumPy·MCAP·HDF5·LeRobot의 동기 실행을 같은 병렬 계약으로 해석하지 않습니다.

MAX_QPX_MEM, SQL 결과의 타입 한도, reader별 레코드·해제·spool·metadata 예산을 함께 적용합니다.
메모리가 부족하면 지원 연산은 임시 디스크로 전환할 수 있지만 모든 decoder의 내부 heap에
동일한 hard cap을 보장하지는 않습니다. 오류·디스크 부족 시 잘린 결과를 성공으로 취급하지 않습니다.

## 취소와 측정

QUERY_TIMEOUT, SQLCancel 또는 관리 연결의 세션 취소를 사용하고 열린 cursor를 정리합니다.
취소된 요청의 일부 행을 완전한 결과로 사용하지 않습니다.
EXPLAIN FULL은 실제 쿼리를 실행하므로 부하가 생깁니다. prepare·추론·실행·전체 fetch와
디코딩·후처리 시간을 분리합니다. 단순 집계와 전체 원문 전송의 시간을 비교하지 않습니다.

LIMIT 성공은 파일 전체 검사의 성공이 아닙니다. 압축 chunk의 손상은 해당 chunk를 읽을 때
발견될 수 있습니다. LeRobot 미디어의 목록 조회는 실제 영상의 존재·내용·시간 정합성을
모두 확인한 것이 아닙니다.

## CSV/TSV 병렬 처리와 실행 통계

threads는 1~32의 동시 제출 작업 상한이고 기본은 min(4,CPU_COUNT)입니다.
CPU_COUNT 기본 1이면 auto도 순차이며 threads=1도 순차입니다. auto는 입력 크기·실측
압축률을 사용해 디코딩 입력이 8 MiB 이상으로 추정되거나 관측되면 병렬 처리를 시작합니다.
true는 작은 입력에서도 병렬 경로를 요청하지만 실제 작업자 사용을 보장하지 않습니다.

```sql
EXPLAIN FULL SELECT id,label FROM READ('/srv/dfq/sensor.csv',
 'parallel=auto','threads=4','type.label=TEXT') ORDER BY label LIMIT 3;
```

CSV_PARALLEL의 requested·effective·used·worker_rows·auto_decision을 확인합니다.
작은 샘플은 순차가 정상입니다. workers는 실행 중 사용한 고유 작업자 수여서 threads와
같지 않을 수 있습니다. decoded_bytes는 UTF-8 디코딩 후의 논리 바이트이며 물리 디스크 I/O가 아닙니다.

TEXT_TOPN은 K=LIMIT+OFFSET, seen·stored·peak_rows·peak_bytes·transitions를 표시합니다.
후보 메모리가 부족하면 임시 디스크 정렬로 전환하며, 작은 LIMIT이 모든 입력의 읽기와
표현식 검사를 없애지 않습니다. GROUP_CONCAT 결과의 32 KiB 한도는 유지합니다.
