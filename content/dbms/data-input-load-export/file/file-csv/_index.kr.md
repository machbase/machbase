---
type: docs
title: 'CSV 파일 형식'
weight: 10
---

machloader, csvimport, LOAD DATA INFILE이 인식하는 CSV 파일 형식을 정리합니다.

## 기본 형식

- **구분자**: 콤마(`,`) — 기본값
- **필드 감싸기**: 쌍따옴표(`"`) — 선택사항
- **레코드 구분자**: 개행(`\n`)
- **인코딩**: UTF-8 — 기본값

```csv
TEMP-01,2024-01-15 10:00:00,25.3
TEMP-01,2024-01-15 10:01:00,25.7
TEMP-02,2024-01-15 10:00:00,22.1
```

## 헤더 행

첫 줄을 컬럼명 헤더로 사용할 수 있습니다. 도구에서 `-H` 옵션으로 지정합니다.

```csv
sensor_id,ts,value
TEMP-01,2024-01-15 10:00:00,25.3
TEMP-02,2024-01-15 10:00:00,22.1
```

## DATETIME 형식

DATETIME 컬럼의 값 형식은 machloader의 `-F` 옵션 또는 스키마 파일의 `DATEFORMAT`으로 지정합니다.

| 형식 | 설명 | 예시 |
|------|------|------|
| `YYYY-MM-DD HH24:MI:SS` | 표준 날짜시간 | `2024-01-15 10:00:00` |
| `YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn` | 나노초 포함 | `2024-01-15 10:00:00 000:000:000` |
| `unixtimestamp` | Unix 타임스탬프 (초 단위) | `1705312800` |
| `nanotimestamp` | 나노초 단위 Unix 타임스탬프 | `1705312800000000000` |

## NULL 표현

- 빈 필드는 NULL로 처리됩니다.
- `,,` 사이 빈 값은 NULL

```csv
TEMP-01,2024-01-15 10:00:00,
TEMP-02,,22.1
```

## 특수 구분자

탭, 파이프(`|`), 캐럿(`^`) 등 다른 구분자를 사용할 경우 machloader에서 `-D` 옵션으로 지정합니다.

```bash
# 탭 구분 파일
machloader -i -d data.tsv -t sensor_log -D '\t'

# 파이프 구분 파일
machloader -i -d data.pipe -t sensor_log -D '|'
```

## 지원 인코딩

`machloader`와 `csvimport`/`csvexport` 래퍼는 다음 인코딩을 사용할 수 있습니다.

| 코드 | 설명 |
|------|------|
| `UTF8` | UTF-8 (기본값) |
| `ASCII` | ASCII |
| `MS949` | Windows 한국어 |
| `KSC5601` | KS C 5601 |
| `EUCJP` | EUC-JP (일본어) |
| `SHIFTJIS` | Shift-JIS (일본어) |
| `BIG5` | Big5 (중국어 번체) |
| `GB231280` | GB2312 (중국어 간체) |
| `UTF16` | UTF-16 |

SQL `LOAD DATA INFILE`과 `SAVE DATA INTO`의 `ENCODED BY`는 `UTF8`, `MS949`, `KSC5601`,
`EUCJP`, `SHIFTJIS`, `BIG5`, `GB231280`을 지원합니다. SQL 구문에서는 `UTF16`을 지정하지 않습니다.
