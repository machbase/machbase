# DBMS 8.9 READ 로컬 URI·원격 파일 실습

DBMS 8.9 Standard Edition의 전용 실습 설치와 DB를 준비합니다. 같은 설치를 사용하는
다른 서비스가 없는 상태에서 진행합니다. 파일의 주소는 Machbase 서버 기준이므로 이 자료의
실습 서비스는 **Machbase 서버와 같은 호스트**에서 실행합니다. Linux 실습에는 Python 3.10
이상, OpenSSL 명령이 필요합니다. Python과 패키지는 실습 서버를 구동하는 데 사용합니다.

## 1. 실습 서비스를 실행합니다

압축을 푼 디렉터리에서 먼저 패키지를 설치합니다. 별도 환경을 사용합니다.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python lab.py --example-ports /tmp/dfq-read-lab
```

`/tmp/dfq-read-lab`은 아직 존재하지 않는 디렉터리여야 합니다. `DFQ lab ready`가 출력될 때까지
기다린 뒤 이 터미널을 유지합니다. 스크립트는 루프백 주소에서만 서비스를 엽니다. CSV,
Parquet와 보조 입력은 `/tmp/dfq-read-lab/files`, 생성한 인증 자료는 `/tmp/dfq-read-lab` 아래에 둡니다.
`/tmp/dfq-read-lab/sql`에는 실제 포트·서버 경로를 채운 실행용 SQL이 있습니다. 원본 `sql/`에는
같은 코드를 템플릿으로 보관합니다. 사전 서명 URL은 실습 서비스가 시작될 때 발급되며
30분 이내에 사용합니다.

본문의 경로와 주소를 그대로 사용하려면 위 디렉터리와 `--example-ports`를 사용합니다.
실습 포트 18069, 18080~18081, 18210~18211, 18443, 18990, 19000을 이미 사용 중이면
`--example-ports`를 생략해 빈 포트를 자동 배정합니다. 이 경우 본문 대신 실행용
`/tmp/dfq-read-lab/sql/` 파일을 사용합니다.

## 2. 전용 DBMS 서버를 설정합니다

다른 터미널에서 전용 DBMS 설치를 선택합니다. 설치의 conf/machbase.conf에 다음 두 줄의
값을 실제 실습 디렉터리 경로로 지정합니다. 기존에 같은 키가 있으면 값을 바꿉니다.

```ini
READ_REMOTE_CA_FILE = /tmp/dfq-read-lab/ca.pem
READ_REMOTE_NETRC_FILE = /tmp/dfq-read-lab/ftp.netrc
```

전용 서버를 시작할 터미널에서 다음을 실행합니다. 해당 설치의 바이너리와 설정을
사용하도록 MACHBASE_HOME과 PATH를 먼저 지정합니다. 서버의 포트는 전용 설치에서 정한
값으로 접속합니다.

```bash
source /tmp/dfq-read-lab/server.env
machadmin -u
```

server.env에는 시뮬레이터 전용 AWS 파일 경로와 테스트 키가 담깁니다. 파일은 이 실습
설치에만 사용합니다. 실습 SQL의 일반 계정도 전용 DB에서만 사용합니다. 실제 AWS
계정이나 원격 저장소는 필요하지 않습니다. 실습은 기본 데이터베이스에서 진행합니다.

## 3. SQL을 실행하고 결과를 읽습니다

다음 예시는 포트 5656의 전용 서버에 접속합니다. 다른 포트나 계정이면 바꿉니다.
실습 SYS 비밀번호는 아래 프롬프트에서 입력합니다.

```bash
read -rsp '실습 SYS 비밀번호: ' DFQ_SYS_PASSWORD
printf '\n'
DFQ_PORT=5656
for topic in file http ftp s3; do
  machsql -s 127.0.0.1 -P "$DFQ_PORT" -u SYS -p "$DFQ_SYS_PASSWORD" \
    -f "/tmp/dfq-read-lab/sql/$topic.sql"
done
```

기본 CSV·Parquet의 두 컬럼은 LONG입니다. 첫 행은 (1,10), 마지막 행은 (100,1000),
합계는 50500입니다. JSONL은 2행, LIMIT은 1행입니다. RAW의 TOTAL_BYTES는
measurements.parquet의 실제 바이트 길이와 같습니다. 빈 헤더 예제는 id,c2,unit,c4를,
충돌 TSV는 id,c2_2,c2를 사용합니다. 사전 서명 결과 표시의 MASKED는 1입니다.
오류 사례는 별도 errors.sql에 있으며 성공 조회가 끝난 뒤 개별 문장으로 실행합니다.
인터넷 접속과 플랫폼 기본 CA 또는 해당 공개 CA가 설정된 서버에서는 public.sql로 Vega Barley JSON과 NOAA 공개 S3 객체도
읽을 수 있습니다. 각각 120행과 730행입니다.

## 4. 일반 사용자 권한을 확인합니다

SYS로 `grant.sql`을 실행해 고유한 DFQ_REMOTE_LAB 사용자와 VIEW를 만듭니다.
이름이 이미 사용 중인 DB는 피하십시오. 일반 사용자로 `analyst.sql`을 실행하면 각각
동일한 100행을 조회합니다. SYS로 `revoke-http.sql`을 실행한 뒤 같은 VIEW에서 읽으면
ACCESS_DENIED가 발생합니다. `cleanup.sql`로 실습 VIEW와 계정을 정리합니다.

```bash
machsql -s 127.0.0.1 -P "$DFQ_PORT" -u SYS -p "$DFQ_SYS_PASSWORD" \
  -f /tmp/dfq-read-lab/sql/grant.sql
machsql -s 127.0.0.1 -P "$DFQ_PORT" -u DFQ_REMOTE_LAB -p dfq_loopback_lab_only \
  -f /tmp/dfq-read-lab/sql/analyst.sql
machsql -s 127.0.0.1 -P "$DFQ_PORT" -u SYS -p "$DFQ_SYS_PASSWORD" \
  -f /tmp/dfq-read-lab/sql/revoke-http.sql
machsql -s 127.0.0.1 -P "$DFQ_PORT" -u SYS -p "$DFQ_SYS_PASSWORD" \
  -f /tmp/dfq-read-lab/sql/cleanup.sql
unset DFQ_SYS_PASSWORD
```

전용 Machbase 서버를 정상 종료한 뒤 실습 서버 터미널에서 Ctrl+C로 서비스를 종료합니다.
`/tmp/dfq-read-lab`에는 입력·요청 경로 기록·실습 전용 인증 자료가 남습니다. 해당 디렉터리를 다른
사람과 공유하지 말고 실습이 끝나면 정리합니다.
