---
type: docs
title: '16.4 입력과 적재 문제'
weight: 40
toc: true
---

<a id="failure"></a>

## 입력이 실패할 때

클라이언트가 보고한 전체 오류, 대상 database·테이블, 입력 방식, 마지막 성공 행을 먼저
기록합니다. 오류 코드 의미는 [오류 코드 사전](/dbms/reference/error-dictionary-codes/)에서
확인하고 이 페이지의 고정 코드 표에 의존하지 않습니다.

```sql
DESC target_table;
SELECT NAME, TYPE, COLCOUNT
  FROM M$SYS_TABLES
 WHERE NAME = 'TARGET_TABLE';
```

다음을 확인합니다.

- 입력 열 수·순서·타입과 NULL 허용 여부
- 현재 database와 테이블 소유자
- 사용자 `CONNECT`와 테이블 `INSERT` 권한
- 시간 문자열 형식과 연결 시간대
- 파일 시스템 공간과 `V$STORAGE_USAGE`
- Append API의 반환값, 실패 행과 flush 결과

시간 역순 입력 가능 여부나 UPDATE/DELETE 조건은 테이블 타입에 따라 다르므로 해당 활용 장의
제약 문서를 확인합니다.

<a id="failure-csv-import"></a>

## CSV import가 실패할 때

현재 배포본의 옵션은 `machloader -h`로 확인합니다.

```bash
machloader -h
machloader -s 127.0.0.1 -P 5656 -u app_user \
  -t target_table -i /data/input.csv \
  -b /data/input.bad -l /data/input.log
```

실패 시 다음 순서로 작은 파일부터 재현합니다.

1. 절대 경로와 서버가 아닌 loader 실행 호스트의 파일 권한을 확인합니다.
2. CSV 한 행의 열 수와 `DESC target_table` 결과를 비교합니다.
3. 인코딩 이름을 현재 도움말과 대조합니다. 배포본에서 확인되는 이름에는 `UTF8`, `MS949`,
   `KSC5601`, `EUCJP` 등이 있습니다.
4. 구분자와 enclosure 옵션을 실제 파일과 맞춥니다.
5. 날짜 형식 옵션에는 대상 열 이름과 형식을 함께 지정합니다.
6. bad 파일의 첫 실패 행을 고친 뒤 별도 검증 테이블에 다시 적재합니다.

`-F` 구문의 정확한 형식과 loader 옵션은
[machloader 명령/옵션 사전](/dbms/reference/command-line-tools/dictionary-machloader/)을
사용하십시오. 일부 성공 뒤 재시도할 때는 이미 입력된 범위를 확인해 중복을 방지합니다.

<a id="failure-ingestion-collector"></a>

## Collector 수집이 실패할 때

```bash
machadmin -e
machcollectoradmin --status-collector=my_collector
```

Collector 로그에서 최초 오류와 마지막 성공 파일을 찾고, FILE 경로·권한 또는 SFTP 연결,
템플릿의 열 매핑, 대상 테이블과 권한을 확인합니다. 원인을 제거한 뒤 해당 Collector만
재시작하고 처리 건수와 대상 데이터가 증가하는지 검증합니다.

이미 처리한 파일을 원본 위치에 되돌리기 전에 재개 offset과 중복 정책을 확인하십시오. 자세한
절차는 [Collector 운영](/dbms/operations-configuration-recovery/collector/)을 따릅니다.
