-- 기존 서버 경로로 CSV 읽기
SELECT id, v
FROM READ(
    'source=${DFQ_FILES}/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;

-- 파일 URI로 같은 CSV 읽기
SELECT id, v
FROM READ(
    'source=${DFQ_FILE_URI}/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;

-- URI에서 공백을 %20으로 나타내기
SELECT id, v
FROM READ(
    'source=${DFQ_FILE_URI}/a%20b.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;

-- 경로에서 %20을 그대로 사용하기
SELECT id, v
FROM READ(
    'source=${DFQ_FILES}/a%20b.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;
