-- 없는 HTTP 파일
SELECT id, v
FROM READ(
    'source=${DFQ_HTTP}/missing.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;

-- 평문 HTTP에 TLS 파일 옵션
SELECT id, v
FROM READ(
    'source=${DFQ_HTTP}/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.tls.ca_file=${DFQ_CA}'
)
ORDER BY id;

-- 존재하지 않는 CA 파일
SELECT id, v
FROM READ(
    'source=${DFQ_HTTPS}/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.tls.ca_file=${DFQ_CA}.missing'
)
ORDER BY id;

-- 기대 SHA-256과 다른 원본
SELECT id, v
FROM READ(
    'source=${DFQ_HTTP}/measurements.parquet',
    'format=parquet',
    'source.expected_revision=sha256:0000000000000000000000000000000000000000000000000000000000000000'
)
ORDER BY id;

-- implicit FTPS에 평문 옵션 지정
SELECT id, v
FROM READ(
    'source=${DFQ_FTPS}/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.ftp.tls=none'
)
ORDER BY id;

-- TFTP에 FTP 옵션 지정
SELECT id, v
FROM READ(
    'source=${DFQ_TFTP}/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.ftp.tls=required'
)
ORDER BY id;

-- S3에 존재하지 않는 명시 프로필 사용
SELECT id, v
FROM READ(
    'source=s3://dfq-lab-data/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.s3.profile=dfq-missing',
    'source.s3.endpoint=${DFQ_S3}',
    'source.s3.region=us-east-1',
    'source.tls.ca_file=${DFQ_CA}'
)
ORDER BY id;

-- 완성된 S3 HTTPS URL에 주소 방식 지정
SELECT id, v
FROM READ(
    'source=${DFQ_S3}/dfq-lab-data/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.s3.profile=dfq-lab',
    'source.s3.addressing_style=path',
    'source.tls.ca_file=${DFQ_CA}'
)
ORDER BY id;

-- 사전 서명 URL에 별도 프로필 지정
SELECT id, v
FROM READ(
    'source=${DFQ_SIGNED}',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.s3.profile=dfq-lab',
    'source.tls.ca_file=${DFQ_CA}'
)
ORDER BY id;
