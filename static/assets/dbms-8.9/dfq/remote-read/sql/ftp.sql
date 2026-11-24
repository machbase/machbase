-- 익명 FTP로 CSV 읽기
SELECT id, v
FROM READ(
    'source=${DFQ_FTP_ANON}/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;

-- FTP에서 .netrc 계정으로 읽기
SELECT id, v
FROM READ(
    'source=${DFQ_FTP}/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.ftp.netrc_file=${DFQ_NETRC}'
)
ORDER BY id;

-- 명시적 FTP TLS로 CSV 읽기
SELECT id, v
FROM READ(
    'source=${DFQ_EXPLICIT}/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.ftp.tls=required',
    'source.tls.ca_file=${DFQ_CA}',
    'source.ftp.netrc_file=${DFQ_NETRC}'
)
ORDER BY id;

-- 연결 시작부터 TLS를 사용하는 FTPS
SELECT id, v
FROM READ(
    'source=${DFQ_FTPS}/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.tls.ca_file=${DFQ_CA}',
    'source.ftp.netrc_file=${DFQ_NETRC}'
)
ORDER BY id;

-- FTPS에서 Parquet 읽기
SELECT id, v
FROM READ(
    'source=${DFQ_FTPS}/measurements.parquet',
    'format=parquet',
    'source.tls.ca_file=${DFQ_CA}',
    'source.ftp.netrc_file=${DFQ_NETRC}'
)
ORDER BY id;

-- TFTP에서 작은 CSV 읽기
SELECT id, v
FROM READ(
    'source=${DFQ_TFTP}/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;
