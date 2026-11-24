-- 로컬 파일 URI와 디렉터리 권한
SELECT id, v
FROM READ(
    'source=${DFQ_FILE_URI}/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;

-- 서버 자격증명 없는 요청
SELECT id, v
FROM READ(
    'source=${DFQ_HTTP}/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;

-- 프로필 권한으로 S3 읽기
SELECT id, v
FROM READ(
    'source=s3://dfq-lab-data/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.s3.profile=dfq-lab'
)
ORDER BY id;

-- 환경변수 권한으로 S3 읽기
SELECT id, v
FROM READ(
    'source=s3://dfq-lab-data/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;

-- NETRC 권한으로 FTPS 읽기
SELECT id, v
FROM READ(
    'source=${DFQ_FTPS}/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;

-- VIEW 실행자의 주소 권한
SELECT id, v FROM SYS.DFQ_REMOTE_LAB_VIEW ORDER BY id;
