---
type: docs
title: '18.6.3 /machiot TAG/Datapoints API'
weight: 30
toc: true
---

`/machiot` 엔드포인트는 TAG 테이블의 태그 메타데이터, 시간 범위, 집계 통계,
raw/calculated datapoint 조회와 raw datapoint append/delete를 제공합니다. `/machiot-rest-api`는 같은 handler로
등록된 호환 alias입니다.

## TAG 테이블 준비

```bash
# TAG 테이블 생성
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=CREATE TAG TABLE tag (name VARCHAR(64) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED)"

# 데이터 입력 (Append API 사용)
curl -X POST "http://127.0.0.1:5657/machbase" \
  -H "Content-Type: application/json" \
  -d '{"name":"tag","date_format":"YYYY-MM-DD HH24:MI:SS","values":[["tag-1","2001-09-09 00:00:00",1],["tag-1","2001-09-09 00:01:00",2]]}'
```

## TAG 목록 조회

경로 파라미터 또는 query string을 사용할 수 있습니다.

```bash
curl "http://127.0.0.1:5657/machiot/tags/list/tag"
curl "http://127.0.0.1:5657/machiot/tags/list?Table=tag"
curl "http://127.0.0.1:5657/machiot/tags/list/tag/tag-1"
curl "http://127.0.0.1:5657/machiot/tags/list?Table=tag&TagNames=tag-1"
```

## TAG 메타데이터 쓰기

`/machiot/tags/list` 계열은 조회뿐 아니라 TAG 메타데이터 insert/update/delete에도 사용합니다.

| 메서드 | 동작 |
|--------|------|
| `POST` | TAG 메타데이터 삽입 |
| `PUT` / `PATCH` | TAG 메타데이터 갱신 |
| `DELETE` | TAG 메타데이터 삭제 |

요청 본문은 대상 TAG 테이블의 메타데이터 컬럼 구조에 맞는 JSON 객체 또는 배열을 사용합니다.

```bash
curl -X POST "http://127.0.0.1:5657/machiot/tags/list/tag" \
  -H "Content-Type: application/json" \
  -d '{"values":[{"name":"tag-2"}]}'

curl -X DELETE "http://127.0.0.1:5657/machiot/tags/list/tag/tag-2"
```

## TAG 시간 범위 조회

```bash
curl "http://127.0.0.1:5657/machiot/tags/range/tag"
curl "http://127.0.0.1:5657/machiot/tags/range/tag/tag-1"
curl "http://127.0.0.1:5657/machiot/tags/range?Table=tag&TagNames=tag-1"
```

## TAG 통계 조회

`min`, `max`, `count`(`cnt` alias)를 사용할 수 있습니다.

```bash
curl "http://127.0.0.1:5657/machiot/tags/min/tag/tag-1"
curl "http://127.0.0.1:5657/machiot/tags/max?Table=tag&TagNames=tag-1"
curl "http://127.0.0.1:5657/machiot/tags/count/tag/tag-1"
curl "http://127.0.0.1:5657/machiot/tags/cnt?Table=tag&TagNames=tag-1"
```

## Raw datapoints 조회

경로 형식:

```text
/machiot/v1/datapoints/raw/<table>/<tag_names>/<start>/<end>/<direction>/<count>/<offset>
```

Query string 형식:

```text
/machiot/v1/datapoints/raw?Table=<table>&TagNames=<tags>&Start=<start>&End=<end>&Direction=<direction>&Count=<count>&Offset=<offset>
```

예시:

```bash
curl "http://127.0.0.1:5657/machiot/v1/datapoints/raw/tag/tag-1/2001-09-09T00:00:00,000/2001-09-09T01:20:00,000/0/5/0"
curl "http://127.0.0.1:5657/machiot/v1/datapoints/raw?Table=tag&TagNames=tag-1&Start=2001-09-09T00:00:00,000&End=2001-09-09T01:20:00,000&Direction=2&Count=1&Offset=1"
```

`DELETE /machiot/v1/datapoints/raw/...` 형식으로 raw datapoint 삭제도 지원합니다.

## Raw datapoints Append

`POST /machiot/v1/datapoints/raw/<table>` 형식으로 TAG raw datapoint를 append할 수 있습니다.

```bash
curl -X POST "http://127.0.0.1:5657/machiot/v1/datapoints/raw/tag" \
  -H "Content-Type: application/json" \
  -d '{"values":[["tag-1","2001-09-09 00:02:00",3],["tag-1","2001-09-09 00:03:00",4]]}'
```

## Calculated datapoints 조회

경로 형식:

```text
/machiot/v1/datapoints/calculated/<table>/<tag_names>/<start>/<end>/<calculation_mode>/<count>/<interval_type>/<interval_value>
```

Query string 형식:

```text
/machiot/v1/datapoints/calculated?Table=<table>&TagNames=<tags>&Start=<start>&End=<end>&Count=<count>&CalculationMode=<mode>&IntervalType=<unit>&IntervalValue=<n>
```

예시:

```bash
curl "http://127.0.0.1:5657/machiot/v1/datapoints/calculated/tag/tag-1/2001-09-09T00:00:00,000/2001-09-09T01:20:00,000/avg/5/min/5"
curl "http://127.0.0.1:5657/machiot/v1/datapoints/calculated?Table=tag&TagNames=tag-1&Start=2001-09-09 00:00:00,000&End=2001-09-09 23:20:00,000&Count=5&CalculationMode=sum&IntervalType=min&IntervalValue=5"
```

## SQL API로 대체 조회

복잡한 조건이나 조인이 필요하면 `/machbase` SQL API를 사용합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT name, time, value FROM TAG TABLE tag WHERE name = 'tag-1' ORDER BY time DESC LIMIT 10"
```
