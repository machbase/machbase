---
title: SQL
type: docs
weight: 22
---

새 탭 화면에서 `SQL` 카드를 선택하면 새 SQL 에디터가 열립니다.

{{< figure src="/images/web-sql-pick.png" width="600px" >}}

## SQL

### 테이블 생성

화면 왼쪽은 SQL 에디터, 오른쪽은 결과 패널(`RESULT`·`CHART`)입니다. 실행 로그는 아래쪽 콘솔에 표시됩니다.

아래 DDL을 복사해 에디터에 붙여 넣습니다.

```sql
CREATE TAG TABLE IF NOT EXISTS example (
  name varchar(100) primary key,
  time datetime basetime,
  value double summarized
);
```

에디터 칸 왼쪽 위의 <img src="/neo/sql/img/sql_run_icon.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 을 클릭하거나 `Ctrl+Enter`(macOS 는 `Cmd+Enter`)를 눌러 실행합니다. 문장 끝의 세미콜론을 잊지 마십시오.

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

### Named Args 사용

SQL 에디터에서는 `:name`, `:value`와 같은 named args를 사용할 수 있습니다.
named args 값은 SQL 문 앞에 `-- env:` 주석으로 지정합니다.
같은 값을 여러 SQL 문에서 반복해서 사용하거나, 테스트 값을 빠르게 바꿔 실행할 때 유용합니다.

```sql
-- env: named.name='my-car' named.value=1.5432
INSERT INTO example VALUES(:name, now, :value);

SELECT * FROM example WHERE name = :name;
-- env: reset
```

위 예시는 `name` 인자에 `'my-car'`, `value` 인자에 `1.5432`를 설정한 뒤,
INSERT와 SELECT 문에서 각각 `:name`, `:value`로 참조합니다.
`-- env: reset`을 실행하면 SQL 에디터에 설정된 named args가 초기화됩니다.

`-- env:`로 설정한 내용은 `-- env: reset`을 실행할 때까지 누적됩니다.

```sql
--env: named.name=my-car
--env: named.time='2026-09-10 12:28:26.197719833'
--env: named.layout='YYYY-MM-DD HH24:MI:SS.mmmuuunnn'
SELECT * FROM example
  WHERE name = :name AND time=to_date(:time, :layout);

--env: named.new_value=9.876
UPDATE example SET value = :new_value
  WHERE name = :name AND time=to_date(:time, :layout);
--env: reset
```

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

오른쪽 패널의 `CHART` 탭을 클릭하면 결과를 선 그래프로 확인할 수 있습니다. 첫 번째 열이 X 축, 두 번째 열이 Y 축으로 잡히며, `X Axis`·`Y Axis`에서 열을 바꾼 뒤 옆의 ▶ 버튼을 누르면 다시 그립니다.

{{< figure src="/images/web-select-chart.jpg" width="560px" >}}

### CSV 파일 다운로드

결과 패널 오른쪽 위의 <img src="/neo/sql/img/sql_download_icon.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 을 클릭하면 쿼리 결과를 CSV 파일로 내려받습니다. 결과 표는 50행씩 나눠 보여 주지만 CSV 파일에는 쿼리가 반환하는 모든 행이 머리행과 함께 저장되며, 시간 값은 에디터의 시간 형식·시간대 설정을 따릅니다.

{{< figure src="/neo/sql/img/web-select-download.png" width="570px" >}}

### 테이블 삭제

*DELETE* 문으로 레코드를 삭제합니다.

```sql
DELETE FROM example WHERE name = 'my-car';
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

{{< figure src="/neo/sql/img/web-show-tables.png" >}}

### desc _table_name_

테이블의 컬럼과 인덱스 정보를 확인합니다.

```
desc example;
```

{{< figure src="/neo/sql/img/web-desc-table.png" >}}

### show tags _table_name_

```
show tags example;
```

TAG 테이블의 저장된 태그 목록을 확인합니다.

{{< figure src="/neo/sql/img/web-show-tags.png" >}}


## SQL 가이드

아래 절에서는 TAG 테이블의 핵심 개념과 기능을 간략히 소개합니다. 자세한 내용은 [DBMS 레퍼런스](https://docs.machbase.com/kr/dbms/)를 참고하십시오.

{{< children_toc />}}
