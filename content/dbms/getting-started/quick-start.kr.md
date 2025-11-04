---
type: docs
title: '빠른 시작'
weight: 10
---

5분 안에 Machbase를 시작하고 실행하세요! 이 가이드는 설치, 첫 번째 테이블 생성 및 첫 번째 쿼리 실행을 안내합니다.

## 전제 조건

- Linux 또는 Windows 운영 체제
- 100MB 여유 디스크 공간
- 터미널 액세스

## 1단계: Machbase 설치

### Linux

Machbase 다운로드 및 압축 해제:

```bash
# 패키지 다운로드 (x.x.x를 실제 버전으로 바꾸세요)
wget http://machbase.com/dist/machbase-fog-x.x.x.official-LINUX-X86-64-release.tgz

# 디렉토리 생성 및 압축 해제
mkdir machbase_home
tar zxf machbase-fog-x.x.x.official-LINUX-X86-64-release.tgz -C machbase_home

# 환경 변수 설정
export MACHBASE_HOME=$(pwd)/machbase_home
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
```

### Windows

1. Windows 설치 프로그램(.msi 파일) 다운로드
2. 설치 프로그램을 실행하고 마법사를 따릅니다
3. 설치 프로그램이 자동으로 환경 변수를 설정합니다

## 2단계: 데이터베이스 생성 및 시작

```bash
# 데이터베이스 생성
machadmin -c

# 서버 시작
machadmin -u
```

다음과 같이 표시됩니다:
```
Database created successfully.
Machbase server started successfully.
```

## 3단계: Machbase에 연결

대화형 SQL 클라이언트 실행:

```bash
machsql
```

프롬프트가 표시되면:
- **Server address**: Enter 키 누름 (기본값 127.0.0.1 사용)
- **User ID**: Enter 키 누름 (기본값 SYS 사용)
- **Password**: `MANAGER`를 입력하고 Enter 키 누름

명령을 입력할 수 있는 `Mach>` 프롬프트가 표시됩니다!

## 4단계: 첫 번째 테이블 생성

센서 온도 데이터를 저장할 테이블을 생성해 보겠습니다:

```sql
CREATE TABLE sensor_data (
    sensor_id VARCHAR(20),
    temperature DOUBLE,
    humidity DOUBLE
);
```

## 5단계: 데이터 삽입

샘플 센서 판독값을 추가합니다:

```sql
INSERT INTO sensor_data VALUES ('sensor01', 25.3, 65.2);
INSERT INTO sensor_data VALUES ('sensor01', 25.5, 64.8);
INSERT INTO sensor_data VALUES ('sensor02', 22.1, 70.5);
```

## 6단계: 데이터 조회

데이터를 검색합니다:

```sql
-- 모든 레코드 가져오기
SELECT * FROM sensor_data;

-- 타임스탬프가 포함된 레코드 가져오기
SELECT _arrival_time, * FROM sensor_data;

-- 평균 온도 가져오기
SELECT AVG(temperature) FROM sensor_data;

-- 최근 10분간의 데이터 가져오기
SELECT * FROM sensor_data DURATION 10 MINUTE;
```

**참고**: `_arrival_time` 컬럼은 나노초 정밀도로 모든 레코드에 자동으로 추가됩니다!

## 결과 이해

`SELECT * FROM sensor_data`를 실행하면 다음을 확인할 수 있습니다:

1. **최신 데이터 우선** - Machbase는 결과를 자동으로 최신 순으로 정렬합니다
2. **자동 타임스탬프** - 모든 레코드에 `_arrival_time` 컬럼이 있습니다
3. **높은 정밀도** - 타임스탬프는 나노초까지 정확합니다

출력 예시:
```
SENSOR_ID            TEMPERATURE  HUMIDITY
------------------------------------------------
sensor02             22.1         70.5
sensor01             25.5         64.8
sensor01             25.3         65.2
[3] row(s) selected.
```

## 무슨 일이 일어났나요?

축하합니다! 방금 다음을 수행했습니다:

✓ Machbase 설치
✓ 데이터베이스 생성 및 시작
✓ machsql을 사용하여 연결
✓ 테이블 생성
✓ 시계열 데이터 삽입
✓ 자동 타임스탬프로 데이터 조회

## 다음 단계

이제 Machbase가 실행되고 있습니다:

1. [**첫 단계**](../first-steps/) - machsql 명령어 더 배우기
2. [**기본 개념**](../concepts/) - 테이블 타입과 사용 시기 이해
3. [**튜토리얼**](../../tutorials/) - 실제 시나리오를 위한 실습 튜토리얼 따라하기

## 일반 명령어

다음 명령어를 편리하게 사용하세요:

```bash
# Machbase 시작
machadmin -u

# Machbase 중지
machadmin -s

# 실행 중인지 확인
machadmin -e

# 데이터베이스에 연결
machsql
```

## 문제 해결

**서버가 시작되지 않나요?**
- 포트 5656이 사용 가능한지 확인: `netstat -an | grep 5656`
- `$MACHBASE_HOME/trc/` 디렉토리의 로그 확인

**연결할 수 없나요?**
- 서버가 실행 중인지 확인: `machadmin -e`
- 기본 자격 증명 확인: 사용자 이름 `SYS`, 비밀번호 `MANAGER`

**도움이 필요하신가요?**
- [문제 해결 가이드](../../troubleshooting/) 참조
- [에러 코드](../../troubleshooting/error-codes/) 확인

---

**더 깊이 파고들 준비가 되셨나요?** [첫 단계](../first-steps/)로 계속하여 machsql 명령줄 인터페이스를 마스터하세요!
