-- 공개 Vega 데이터의 JSON 행 수
SELECT COUNT(*) AS N
FROM READ('source=https://raw.githubusercontent.com/vega/vega-datasets/main/data/barley.json',
          'format=json');

-- NOAA GHCN 공개 S3 객체에서 헤더 없는 gzip CSV 읽기
SELECT COUNT(*) AS N
FROM READ('source=s3://noaa-ghcn-pds/csv.gz/1763.csv.gz',
          'source.s3.auth=anonymous', 'source.s3.region=us-east-1',
          'source.s3.endpoint=https://s3.us-east-1.amazonaws.com',
          'source.s3.addressing_style=virtual',
          'format=csv', 'compression=gzip', 'header=false', 'auto_detect=false');
