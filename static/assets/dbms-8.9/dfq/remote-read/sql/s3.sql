-- S3 공유 파일의 명시 프로필로 읽기
SELECT id, v
FROM READ(
    'source=s3://dfq-lab-data/measurements.parquet',
    'format=parquet',
    'source.s3.profile=dfq-lab',
    'source.tls.ca_file=${DFQ_CA}'
)
ORDER BY id;

-- 별도 프로필 지정 없이 환경의 키로 읽기
SELECT id, v
FROM READ(
    'source=s3://dfq-lab-data/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.tls.ca_file=${DFQ_CA}'
)
ORDER BY id;

-- 명시 옵션으로 profile의 주소 방식을 덮어쓰기
SELECT id, v
FROM READ(
    'source=s3://dfq-lab-data/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.s3.profile=dfq-lab',
    'source.s3.endpoint=${DFQ_S3}',
    'source.s3.region=us-east-1',
    'source.s3.addressing_style=path',
    'source.tls.ca_file=${DFQ_CA}'
)
ORDER BY id;

-- 버킷을 호스트명에 넣어 읽기
SELECT id, v
FROM READ(
    'source=s3://dfq-lab-data/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.s3.profile=dfq-lab',
    'source.s3.addressing_style=virtual',
    'source.tls.ca_file=${DFQ_CA}'
)
ORDER BY id;

-- 직접 HTTPS 객체 주소에 SigV4 적용하기
SELECT id, v
FROM READ(
    'source=${DFQ_S3}/dfq-lab-data/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.s3.profile=dfq-lab',
    'source.s3.auth=sigv4',
    'source.tls.ca_file=${DFQ_CA}'
)
ORDER BY id;

-- 공개 S3 객체를 익명으로 읽기
SELECT id, v
FROM READ(
    'source=s3://dfq-lab-public/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.s3.endpoint=${DFQ_S3}',
    'source.s3.region=us-east-1',
    'source.s3.auth=anonymous',
    'source.tls.ca_file=${DFQ_CA}'
)
ORDER BY id;

-- 공개 객체의 직접 HTTPS 주소 사용하기
SELECT id, v
FROM READ(
    'source=${DFQ_S3}/dfq-lab-public/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.tls.ca_file=${DFQ_CA}'
)
ORDER BY id;

-- 객체 키의 공백을 인코딩해서 읽기
SELECT id, v
FROM READ(
    'source=s3://dfq-lab-data/a%20b.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.s3.profile=dfq-lab',
    'source.tls.ca_file=${DFQ_CA}'
)
ORDER BY id;

-- 발급된 사전 서명 HTTPS URL로 읽기
SELECT id, v
FROM READ(
    'source=${DFQ_SIGNED}',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.tls.ca_file=${DFQ_CA}'
)
ORDER BY id;

-- 사전 서명 URL의 결과 표시 확인하기
SELECT CASE WHEN _SOURCE LIKE '%X-Amz-Signature%' THEN 0 ELSE 1 END AS MASKED
FROM READ(
    'source=${DFQ_SIGNED}',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.tls.ca_file=${DFQ_CA}',
    'columns=envelope'
)
LIMIT 1;
