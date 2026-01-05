---
title : 'csvimport / csvexport'
type : docs
weight: 10
---

'csvimport'와 'csvexport'는 Machbase 서버로 CSV 파일을 가져오거나 내보내기 위해 사용되는 도구입니다.

machloader를 사용한 CSV 파일의 간편한 사용을 위해 옵션이 단순화되었습니다.

아래 설명된 옵션 외에도 machloader에서 사용 가능한 모든 옵션을 사용할 수 있습니다.

지원하는 날짜/시간 포맷 토큰은 [TO_CHAR (DATETIME)](../../sql-reference/functions/#to_char-datetime-type)을 참고하세요.

## csvimport

csvimport를 사용하여 CSV 파일을 서버에 쉽게 입력할 수 있습니다.

### 기본 사용법

다음 옵션에 따라 테이블 이름과 데이터 파일 이름을 입력합니다.

옵션:

```
-t: 테이블 이름 지정 옵션
-d: 데이터 파일 이름 지정 옵션
* 옵션을 지정하지 않고 테이블 이름과 데이터 파일 이름만으로 실행할 수 있습니다.
```

예제:

```
csvimport -t table_name -d table_name.csv
csvimport table_name file_path
csvimport file_path table_name
```

### CSV 헤더 제외

입력 시 헤더를 제외하고 CSV 파일을 입력하려면 다음 옵션을 사용합니다.

옵션:

```
-H: csv 파일의 첫 번째 라인을 헤더로 인식하지 않습니다.
```

예제:

```
csvimport -t table_name -d table_name.csv -H
```

### 자동 테이블 생성

입력 시 테이블이 생성되지 않은 경우, 다음 옵션을 통해 테이블을 동시에 생성할 수 있습니다.

옵션

```
-C: 가져오기 중 자동으로 테이블을 생성합니다. 컬럼 이름은 c0, c1, .... 으로 자동 생성됩니다. 생성된 컬럼은 varchar(32767) 타입입니다.
-H: 가져오기 중 csv 헤더 이름으로 컬럼 이름을 생성합니다.
```

예제:

```
csvimport -t table_name -d table_name.csv -C
csvimport -t table_name -d table_name.csv -C -H
```


## csvexport

'csvexport'를 사용하여 데이터베이스 테이블 데이터를 CSV 파일로 쉽게 내보낼 수 있습니다.

### 기본 사용법

옵션:

```
-t: 테이블 이름 지정 옵션
-d: 데이터 파일 이름 지정 옵션
* 옵션을 지정하지 않고 테이블 이름과 데이터 파일 이름만으로 실행할 수 있습니다.
```

예제:

```
csvexport -t table_name -d table_name.csv
csvexport table_name file_path
csvexport file_path table_name
```

### CSV 헤더 사용

다음 옵션을 사용하면 내보낼 CSV 파일에 컬럼 이름으로 헤더를 추가할 수 있습니다.

옵션:

```
-H: 테이블 컬럼 이름으로 csv 파일의 헤더를 생성합니다.
```

예제:

```
csvexport -t table_name -d table_name.csv -H
```
