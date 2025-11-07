---
title: SQL
type: docs
weight: 22
---

"SQL"을 선택하면 새로운 SQL 에디터가 열립니다.

{{< figure src="/images/web-sql-pick.png" width="600" >}}

## SQL

### 테이블 생성

화면 왼쪽은 SQL 에디터, 오른쪽은 결과와 로그 패널입니다.

아래 DDL을 복사해 에디터에 붙여 넣습니다.

```sql
CREATE TAG TABLE IF NOT EXISTS example (
  name varchar(100) primary key,
  time datetime basetime,
  value double summarized
);
```

`Ctrl+Enter`를 누르거나 왼쪽 상단 ▶︎ 아이콘을 클릭해 실행합니다. 문장 끝의 세미콜론을 잊지 마십시오.

{{< figure src="/images/web-cretable.png" >}}

### 데이터 삽입

아래 문장을 실행해 레코드 한 건을 입력합니다.

```sql
INSERT INTO example VALUES('my-car', now, 1.2345);
```

{{< figure src="/images/web-insert.png" >}}

### 데이터 조회

아래 SELECT 문을 실행하면 오른쪽 표 형태 패널에 결과가 표시됩니다.

```sql
SELECT time, value FROM example WHERE name = 'my-car';
```

{{< figure src="/images/web-select.png" >}}

### 차트 그리기

INSERT 문을 반복 실행해 데이터를 더 입력합니다.

```sql
INSERT INTO example VALUES('my-car', now, 1.2345*1.1);
INSERT INTO example VALUES('my-car', now, 1.2345*1.2);
INSERT INTO example VALUES('my-car', now, 1.2345*1.3);
```

이후 저장된 `my-car` 레코드를 조회합니다.

```sql
SELECT time, value FROM example WHERE name = 'my-car';
```
{{< figure src="/images/web-select-multi.png" >}}

오른쪽 패널의 *CHART* 탭을 클릭하면 결과를 선 그래프로 확인할 수 있습니다.

{{< figure src="/images/web-select-chart.jpg" width="600" >}}

### CSV 파일 다운로드

쿼리 결과 전체를 CSV 파일로 다운로드할 수 있습니다.

{{< figure src="./img/web-select-download.png" >}}

### 테이블 삭제

*DELETE* 문으로 레코드를 삭제합니다.

```sql
DELETE FROM example WHERE name = 'my-car'
```

새로 만들고 싶다면 테이블을 삭제하세요.

```sql
DROP TABLE example;
```

## Non-SQL

### show tables

`M$SYS_TABLES`를 조회하는 단축 명령입니다.

```
show tables;
```

{{< figure src="./img/web-show-tables.png" >}}

### desc _table_name_

테이블의 컬럼과 인덱스 정보를 확인합니다.

```
desc example;
```

{{< figure src="./img/web-desc-table.png" >}}

### show tags _table_name_

```
show tags example;
```

TAG 테이블의 저장된 태그 목록을 확인합니다.

{{< figure src="./img/web-show-tags.png" >}}


## SQL 가이드

아래 절에서는 TAG 테이블의 핵심 개념과 기능을 간략히 소개합니다. 자세한 내용은 [DBMS 레퍼런스](https://docs.machbase.com/kr/dbms/)를 참고하십시오.

{{< children_toc />}}
