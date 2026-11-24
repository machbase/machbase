---
type: docs
title: '12.12 로컬 URI와 원격 파일 읽기'
weight: 120
toc: true
---

파일을 DB에 적재하기 전에 `READ()`로 내용과 타입을 확인합니다. 파일의 **위치**는
경로나 URI로 지정하고 **데이터 형식**은 `format`으로 지정합니다. 예를 들어 CSV를
로컬 파일에서 읽다가 같은 CSV를 HTTPS로 제공하면 위치만 바꿔 같은 열을 조회할 수 있습니다.

| 읽을 위치 | 주소 예 | 다음 단계 |
|---|---|---|
| 로컬 파일 | `/data/events.csv`, `./data/events.csv`, `file:///data/events.csv` | [파일 URI와 HTTP(S)](./file-http/) |
| HTTP(S) 파일 | `https://files.example/data/events.parquet` | [파일 URI와 HTTP(S)](./file-http/) |
| FTP(S)·TFTP 파일 | `ftp://archive.example/events.csv`, `ftps://archive.example/events.csv`, `tftp://boot.example/events.csv` | [FTP·FTPS·TFTP](./ftp-tftp/) |
| AWS S3 또는 호환 저장소 | `s3://robot-data/episodes/part-001.parquet` | [S3와 호환 저장소](./s3/) |

이 기능은 Machbase DBMS 8.9 Standard Edition의 Linux x86-64·ARM64, macOS
x86-64·ARM64, Windows x86-64 배포에서 사용합니다. 위치를 읽을 수 있어도 해당
배포에 설치된 포맷 reader와 옵션을 확인합니다. 파일 접근과 네트워크 연결은 Machbase
**서버**가 수행합니다. 상대경로·인증 파일·환경변수와 `127.0.0.1`도 서버 기준입니다.

`READ('source=<경로 또는 URI>', 'format=csv')` 형태로 위치를 명시합니다. 첫 위치형
인자에는 주소를 직접 둘 수 있습니다. URL에 등호가 있는 query가 있으면 `source=`로
지정합니다. 형식을 자동 판별할 수 있으면 `format`을 생략할 수 있습니다.

## 같은 데이터로 실습하기

1. [전체 실습 자료](/assets/dbms-8.9/dfq/remote-read/samples.zip)를 내려받습니다.
2. 묶음의 [실행 안내](/assets/dbms-8.9/dfq/remote-read/README.md)에 따라 Machbase 서버와
   같은 호스트에서 전용 DBMS를 준비하고 아래 명령으로 실습 서비스를 시작합니다.
   `/tmp/dfq-read-lab`은 아직 존재하지 않는 경로여야 합니다.

   ```bash
   .venv/bin/python lab.py --example-ports /tmp/dfq-read-lab
   ```

3. 각 절의 SQL을 복사하거나 `/tmp/dfq-read-lab/sql/file.sql`과
   `/tmp/dfq-read-lab/sql/http.sql`을 `machsql -f`로 실행합니다. 본문의 경로와 포트는
   위 실습 명령 기준입니다.
4. 공통 CSV·Parquet에서 `ID`와 `V`가 모두 LONG인지 확인합니다. 첫 행은 (1, 10),
   마지막 행은 (100, 1000), 전체는 100행입니다. `V`의 합계는 50500입니다.

같은 조회를 일반 사용자로 실행할 때는 [디렉터리 또는 ENDPOINT 읽기 권한](../operations/#endpoint-read-permissions)을
먼저 받습니다. 오류 사례는 성공 조회와 분리해 실행합니다.

## 원격 입력의 단위와 전송

READ 호출 하나에 원격 **파일 또는 객체 하나**를 지정합니다. 원격 glob, 원격 주소 목록,
S3 prefix 열거와 원격 복합 dataset 탐색은 지원하지 않습니다. 디렉터리를 받아들이는
기존 로컬 reader에는 해당 포맷의 사용법을 적용합니다. 개별 READ 결과는 SQL에서
[JOIN 또는 적재](../analysis-load/)에 사용할 수 있습니다.

원격 Parquet도 원본 전체를 임시 파일로 받은 뒤 조회합니다. 응답 시간과 임시 디스크
공간을 잡을 때는 반환 행 수와 함께 입력 파일 크기를 확인합니다.
[전송과 임시 공간](../operations/#remote-read-spool)을 참고합니다.
