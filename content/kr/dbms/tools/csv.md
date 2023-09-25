---
title : 'csvimport / csvexport'
type : docs
weight: 10
---

'csvimport'와 'csvexport' 는 CSV 파일을 마크베이스 서버에 import/export 하기 위해 사용되는 도구이다.

CSV 파일에 대해서 machloader 를 이용하여 보다 간단하게 사용할 수 있도록 옵션을 단순화하였다.

아래 기술된 Option이외에도 machloader에서 사용할 수 있는 옵션을 모두 사용 가능하다.

## csvimport

csvimport를 이용하면 쉽게 CSV 파일을 서버에 입력할 수 있다.

### 기본 사용법

테이블 명과 데이터 파일명을 다음의 옵션에 따라 입력하여 수행한다.

**Option:**
```
-t: 테이블명 지정 옵션
-d: 데이터 파일명 지정 옵션
* 옵션을 지정하지 않고 테이블명과 데이터 파일명만으로도 수행할 수 있다.
```

**Example:**
```
csvimport -t table_name -d table_name.csv
csvimport table_name file_path
csvimport file_path table_name
```

### CSV 헤더 제외

입력시에 CSV 파일의 헤더를 제외하고 입력하려면 다음의 옵션을 사용한다.

**Option:**
```
-H: csv 파일의 첫번째 라인을 헤더로 인식하고 입력하지 않는다.
```

**Example:**
```
csvimport -t table_name -d table_name.csv -H
```

### 테이블 자동 생성

입력시 입력할 테이블을 생성하지 않은 경우, 다음 옵션을 통해서 테이블 생성도 동시에 수행할 수 있다.

**Option:**
```
-C: import할 때 테이블을 자동 생성한다. 칼럼명은 c0, c1, ... 자동으로 생성된다. 생성되는 칼럼은 varchar(32767) 타입이다.
-H: import할 때 csv 헤더명으로 칼럼명을 생성한다.
```

**Example:**
```
csvimport -t table_name -d table_name.csv -C
csvimport -t table_name -d table_name.csv -C -H
```

## csvexport

'csvexport'로 데이터베이스 테이블 데이터를 CSV 파일로 쉽게 export할 수 있다.

### 기본 사용법

**Option:**
```
-t: 테이블명 지정 옵션
-d: 데이터 파일명 지정 옵션
* 옵션을 지정하지 않고 테이블명과 데이터 파일명만으로도 수행할 수 있다.
```

**Example:**
```
csvexport -t table_name -d table_name.csv
csvexport table_name file_path
csvexport file_path table_name
```

### CSV 헤더 사용

다음의 옵션을 이용하면, export할 CSV 파일에 칼럼명으로 헤더를 추가할 수 있다.

**Option:**
```
-H: 테이블 칼럼명으로 csv 파일의 헤더를 생성한다.
```

**Example:**
```
csvexport -t table_name -d table_name.csv -H
```
