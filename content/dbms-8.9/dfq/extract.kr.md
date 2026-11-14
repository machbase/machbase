---
type: docs
title: '12.5 구조화된 값과 원문 추출'
weight: 50
toc: true
---

출력 컬럼을 구성하는 것과 원래 구조·바이트를 보존하는 것은 별도의 작업입니다.

| 선택 방법 | 결과 |
|---|---|
| columns=native | SQL 타입의 일반 컬럼 |
| columns=envelope | _ROW·DATA·_META·_REFS 등 구조와 참조 |
| project.key=id | 원래 id를 key로 선택해 본문 출력 구성 |
| column.copy=data.id | 기존 출력 뒤에 원래 id 추가 |
| column.pos=meta.row | 원래 부모 행 순번 추가 |

```sql
SELECT key,x FROM READ('/srv/dfq/sensor.json',
 'project.key=id','project.x=pose.x','type.key=LONG');
SELECT key,pos FROM READ('/srv/dfq/sensor.json',
 'project.key=id','column.pos=meta.row');
SELECT DATA FROM READ('/srv/dfq/sensor.json','columns=envelope',
 'target=rows','row=0','field=pose');
SELECT * FROM READ('/srv/dfq/sensor.json','mode=elements',
 'target=rows','row=0','field=items');
```

project와 column은 원래 논리 행의 경로를 사용합니다. column이 다른 project 별칭을
다시 참조하는 것으로 해석하지 않습니다. metadata 컬럼의 타입은 고정되므로 바꾸려면
바깥 SELECT에서 CAST합니다. meta.source·meta.row·meta.csv.start_line과 MCAP의
기록·발행 시각은 해당 reader에서 지원하는지 확인합니다.

## 원문 표현 선택

| 표현 | 반환하는 바이트 |
|---|---|
| stored | 저장 파일의 원래 바이트. 외부 압축 해제 전 |
| canonical_json | 선택한 논리값의 정규 JSON UTF-8 |
| utf8_text | 지원되는 문자열의 디코딩된 UTF-8 |
| numpy_bytes | 지원되는 NumPy 선택값의 원본 배열 표현 |
| hdf5_bytes | 지원되는 HDF5 선택값의 바이트 |
| message_bytes | MCAP 선택 메시지의 직렬화 payload |
| payload_bytes | MCAP 스키마·첨부 등의 원 data |

표현이 모든 target·field에 적용되는 것은 아닙니다. 포맷별 capability와 예제를 확인합니다.

```sql
SELECT _OFFSET,_LENGTH,_LAST,_CONTENT
FROM READ('/srv/dfq/sensor.csv','mode=raw','raw.chunk_bytes=16')
ORDER BY _OFFSET;
SELECT _OFFSET,_LENGTH,_LAST,_CONTENT
FROM READ('/srv/dfq/sensor.mcap','target=messages','row=0','mode=raw',
 'raw.representation=message_bytes','raw.chunk_bytes=16') ORDER BY _OFFSET;
```

_CONTENT는 BINARY이며 화면의 hex 표시와 원래 바이트를 구분합니다. source·target·snapshot·
mapping과 _META.identity.parent_key별로 나눈 뒤 _OFFSET 순으로 합칩니다. 서로 다른 부모의
청크를 섞지 않습니다. _OFFSET은 반환 바이트열의 위치이며 원본 파일의 물리 offset과 같다고
가정하지 않습니다. 청크 경계가 바뀌어도 부모 key와 청크 위치의 역할은 구분합니다.

## 참조와 큰 metadata 재조회

큰 값의 _REFS와 inspect의 references/ref_operations/ref_arguments를 확인해 제공되는
재조회 인자나 SQL을 사용합니다. 임의로 token을 구성하거나 다른 파일·사용자에게 재사용하지
않습니다. read-context 주소는 다운로드 URL이 아니며 서버·DB·원본에 종속됩니다.
참조 재조회에는 원본 revision·mapping 검사가 적용될 수 있으며 SYS 전용 경계를 유지합니다.

native의 NULL·실제 빈 값·MISSING·REFERENCE는 원래 의미가 다릅니다. DATA와 값 노드·타입
metadata를 함께 확인합니다. 정규 JSON으로 변환한 값은 파일의 원래 인용·공백·배열 padding이나
수치 bit 표현과 같지 않으므로 바이트 보존에는 지원되는 원문 표현을 사용합니다.
