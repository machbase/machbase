---
type: docs
title: 'R / RODBC'
weight: 70
---

## 개요

R 언어에서 ODBC 인터페이스를 통해 Machbase에 연결할 수 있습니다. `RODBC` 패키지를 사용하면 Machbase를 일반 ODBC 데이터 소스로 취급하여 SQL 쿼리를 실행하고 결과를 `data.frame`으로 받아볼 수 있습니다.

### 구성 요소

| 구성 요소 | 설명 |
|-----------|------|
| Machbase ODBC 드라이버 | `libmachbaseodbc.so` (Linux) / `machbaseodbc.dll` (Windows) |
| ODBC 관리자 | unixODBC (Linux) 또는 Windows ODBC 데이터 원본 관리자 |
| R 패키지 | `RODBC` |

## 사전 요구사항 {#prerequisites}

### 1. Machbase ODBC 드라이버 확인

Machbase 설치 경로의 `lib` 디렉터리에 ODBC 드라이버 파일이 있는지 확인합니다.

```sh
ls $MACHBASE_HOME/lib/libmachbaseodbc.so   # Linux
```

Windows의 경우 `%MACHBASE_HOME%\lib\machbaseodbc.dll`을 사용합니다.

### 2. unixODBC 설치 (Linux)

```sh
# Ubuntu / Debian
sudo apt-get install unixodbc unixodbc-dev

# RHEL / CentOS
sudo yum install unixODBC unixODBC-devel
```

### 3. R 및 RODBC 패키지 설치

```r
install.packages("RODBC")
```

## ODBC 드라이버 등록 {#odbc-config}

### Linux: `/etc/odbcinst.ini` 또는 `~/.odbcinst.ini`

Machbase ODBC 드라이버를 시스템에 등록합니다.

```ini
[MachbaseODBC]
Description = Machbase ODBC Driver
Driver      = /path/to/machbase/lib/libmachbaseodbc.so
Setup       = /path/to/machbase/lib/libmachbaseodbc.so
FileUsage   = 1
```

### DSN 설정 {#dsn-config}

#### Linux: `/etc/odbc.ini` (시스템 DSN) 또는 `~/.odbc.ini` (사용자 DSN)

```ini
[machbase_dsn]
Description = Machbase Database
Driver      = MachbaseODBC
SERVER      = 127.0.0.1
PORT        = 5656
UID         = SYS
PWD         = MANAGER
```

#### Windows: 시스템 DSN

1. **시작** → **ODBC 데이터 원본 관리자** (64비트) 실행
2. **시스템 DSN** 탭 → **추가**
3. 목록에서 `MachbaseODBC` 드라이버 선택
4. DSN 이름(`machbase_dsn`), 서버 주소, 포트, 사용자 정보 입력
5. **확인** 클릭

### DSN 설정 확인 (Linux)

```sh
isql -v machbase_dsn SYS MANAGER
```

접속에 성공하면 `SQL>` 프롬프트가 나타납니다.

## R에서 연결 {#r-connect}

```r
library(RODBC)

# DSN으로 연결
ch <- odbcConnect("machbase_dsn")

# 연결 성공 여부 확인
if (ch < 0) {
  stop("Machbase 연결 실패: ", odbcGetErrMsg(ch))
}

cat("Machbase에 연결되었습니다.\n")
```

### DSN 없이 직접 연결 (연결 문자열)

```r
library(RODBC)

ch <- odbcDriverConnect(
  "DRIVER=MachbaseODBC;SERVER=127.0.0.1;PORT=5656;UID=SYS;PWD=MANAGER"
)
```

## 데이터 조회 {#query}

### 테이블 조회

```r
library(RODBC)

ch <- odbcConnect("machbase_dsn")

# SQL 쿼리 실행 → data.frame 반환
result <- sqlQuery(ch, "SELECT name, time, value FROM sensor_data ORDER BY time DESC")

# 결과 확인
print(head(result, 10))
str(result)
summary(result)
```

### 조건부 조회

```r
# 특정 센서의 최근 1시간 데이터 조회
query <- "
  SELECT name, time, value
    FROM sensor_data
   WHERE name = 'sensor-1'
     AND time >= TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   ORDER BY time DESC
   LIMIT 1000
"

df <- sqlQuery(ch, query)
cat("조회된 행 수:", nrow(df), "\n")
```

### 집계 쿼리

```r
# 센서별 평균값 집계
agg <- sqlQuery(ch, "
  SELECT name,
         COUNT(*)  AS cnt,
         AVG(value) AS avg_value,
         MIN(value) AS min_value,
         MAX(value) AS max_value
    FROM sensor_data
   GROUP BY name
   ORDER BY name
")

print(agg)
```

## 데이터 삽입 {#insert}

### sqlQuery로 INSERT

```r
# 단건 삽입
sqlQuery(ch, "INSERT INTO sensor_data VALUES ('sensor-r', NOW, 3.14)")

# R 변수를 사용한 삽입 (sprintf로 SQL 조합)
name  <- "sensor-r"
value <- 2.71

sql <- sprintf(
  "INSERT INTO sensor_data VALUES ('%s', NOW, %f)",
  name, value
)
sqlQuery(ch, sql)
```

{{< callout type="warning" >}}
문자열 값을 직접 SQL에 삽입할 때는 SQL 인젝션에 주의하세요. 신뢰할 수 없는 입력값은 반드시 이스케이프 처리 후 사용하세요.
{{< /callout >}}

### sqlSave로 data.frame 일괄 삽입

`sqlSave()`를 사용하면 `data.frame`을 테이블에 일괄 삽입할 수 있습니다.

```r
# 삽입할 데이터 준비
new_data <- data.frame(
  name  = c("sensor-r", "sensor-r", "sensor-r"),
  time  = as.POSIXct(c("2024-01-01 00:00:00",
                        "2024-01-01 00:01:00",
                        "2024-01-01 00:02:00")),
  value = c(1.1, 2.2, 3.3)
)

# 테이블에 삽입 (append = TRUE: 기존 데이터 유지)
sqlSave(ch, new_data, tablename = "sensor_data", append = TRUE, rownames = FALSE)
```

## 시각화 예제 {#visualization}

Machbase에서 조회한 시계열 데이터를 R로 바로 시각화할 수 있습니다.

```r
library(RODBC)

ch <- odbcConnect("machbase_dsn")

# 데이터 조회
df <- sqlQuery(ch, "
  SELECT time, value
    FROM sensor_data
   WHERE name = 'sensor-1'
   ORDER BY time
   LIMIT 500
")

# time 컬럼을 POSIXct로 변환
df$time <- as.POSIXct(df$time)

# 시계열 플롯
plot(df$time, df$value,
     type  = "l",
     col   = "steelblue",
     xlab  = "시간",
     ylab  = "측정값",
     main  = "sensor-1 시계열 데이터")

odbcClose(ch)
```

## 연결 해제 {#disconnect}

```r
# 단일 연결 해제
odbcClose(ch)

# 열린 모든 ODBC 연결 해제
odbcCloseAll()
```

## 오류 처리 {#error-handling}

```r
library(RODBC)

ch <- odbcConnect("machbase_dsn")

tryCatch({
  result <- sqlQuery(ch, "SELECT * FROM sensor_data LIMIT 10", errors = TRUE)

  if (is.character(result)) {
    # sqlQuery는 오류 시 오류 메시지 문자열을 반환
    cat("오류 발생:", result, "\n")
  } else {
    print(result)
  }
}, finally = {
  odbcClose(ch)
})
```

## 주요 RODBC 함수 참고 {#rodbc-functions}

| 함수 | 설명 |
|------|------|
| `odbcConnect(dsn)` | DSN으로 연결 |
| `odbcDriverConnect(connStr)` | 연결 문자열로 연결 |
| `sqlQuery(ch, sql)` | SQL 실행 후 `data.frame` 반환 |
| `sqlFetch(ch, tableName)` | 테이블 전체를 `data.frame`으로 읽기 |
| `sqlSave(ch, df, tablename)` | `data.frame`을 테이블에 저장 |
| `sqlTables(ch)` | 사용 가능한 테이블 목록 조회 |
| `sqlColumns(ch, tableName)` | 테이블 컬럼 정보 조회 |
| `odbcGetErrMsg(ch)` | 오류 메시지 조회 |
| `odbcClose(ch)` | 연결 해제 |
| `odbcCloseAll()` | 모든 연결 해제 |

## 문제 해결 {#troubleshooting}

**드라이버를 찾을 수 없는 경우**

```sh
# 등록된 드라이버 목록 확인
odbcinst -q -d

# DSN 목록 확인
odbcinst -q -s
```

**연결 오류가 발생하는 경우**

- Machbase 서버가 실행 중인지 확인
- 방화벽에서 포트 5656이 열려 있는지 확인
- `isql -v machbase_dsn SYS MANAGER`로 ODBC 레벨에서 먼저 연결 테스트
- `LD_LIBRARY_PATH`에 `$MACHBASE_HOME/lib`가 포함되어 있는지 확인 (Linux)

```sh
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
```
