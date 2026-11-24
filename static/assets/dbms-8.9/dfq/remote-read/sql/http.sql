-- HTTP에서 CSV 읽기
SELECT id, v
FROM READ(
    'source=${DFQ_HTTP}/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;

-- HTTPS에서 Parquet 읽기
SELECT id, v
FROM READ(
    'source=${DFQ_HTTPS}/measurements.parquet',
    'format=parquet',
    'source.tls.ca_file=${DFQ_CA}'
)
ORDER BY id;

-- HTTP Parquet에서 한 행 반환하기
SELECT id, v
FROM READ(
    'source=${DFQ_HTTP}/measurements.parquet',
    'format=parquet'
)
LIMIT 1;

-- 로컬 파일과 원격 Parquet의 기준값 비교
SELECT COUNT(*) AS N, SUM(v) AS TOTAL
FROM READ(
    'source=${DFQ_HTTP}/measurements.parquet',
    'format=parquet'
);

-- HTTP 원본을 SHA-256으로 확인하기
SELECT id, v
FROM READ(
    'source=${DFQ_HTTP}/measurements.parquet',
    'format=parquet',
    'source.consistency=strong',
    'source.expected_revision=sha256:${DFQ_PARQUET_SHA}'
)
ORDER BY id;

-- 원격 JSONL을 행으로 읽기
SELECT id, v
FROM READ(
    'source=${DFQ_HTTP}/measurements.jsonl',
    'format=jsonl',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;

-- CSV 빈 헤더를 열 이름으로 사용하기
SELECT id, c2, unit, c4
FROM READ('source=${DFQ_HTTP}/blank-header.csv',
          'format=csv', 'header=true', 'type.id=LONG', 'type.c2=LONG');

-- TSV 빈 헤더와 기존 이름 충돌 확인하기
SELECT id, c2_2, c2
FROM READ('source=${DFQ_HTTP}/colliding-header.tsv', 'format=tsv',
          'header=true', 'type.id=LONG', 'type.c2_2=LONG', 'type.c2=LONG');

-- HTTP 응답이 가리키는 허용된 다른 주소 읽기
SELECT id, v
FROM READ(
    'source=${DFQ_HTTP}/redirect.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;

-- RAW에서 원본 Parquet 크기 확인하기
SELECT _TOTAL_SIZE AS TOTAL_BYTES
FROM READ('source=${DFQ_HTTP}/measurements.parquet', 'mode=raw')
LIMIT 1;
