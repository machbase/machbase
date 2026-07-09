---
type: docs
title: '라이선스 설치'
weight: 30
toc: true
---

라이선스 설치는 Machbase 설치 완료 후 수행합니다. 라이선스 파일이 없어도 서버는 구동되지만 기능 제한이 있습니다.

## 라이선스 없이 동작하는 경우의 제한사항

라이선스가 설치되지 않으면 다음 제한이 적용됩니다.

1. **Append 입력 제한**: 한 세션에서 1억 건 이상 Append 입력 시 경고 메시지와 함께 입력이 중단됩니다. 제한은 서버 재시작 시에만 해제됩니다.
2. **다중 디스크 테이블스페이스 불가**: 테이블스페이스에 두 개 이상의 디스크 경로를 지정할 수 없습니다. 병렬 I/O를 사용하는 고성능 구성에 영향을 줍니다.

## 라이선스 파일 구조

발급받은 라이선스는 `license.dat` 텍스트 파일 형식입니다.

```
#License ID: 00000001
#Issue DATE: 20991231
#License Type(Version 3): FOGUNLIMITED
#Company: MACHBASE
#Project(Product): NONE
#Country Code: KR
dXlIm7cdJjV1eUibtx0mNQ...
```

## 설치 방법

### 방법 1: 파일 복사 (서버 시작 전)

`license.dat` 파일을 `$MACHBASE_HOME/conf/`에 복사합니다. 서버가 시작될 때 자동으로 인식합니다.

```bash
cp license.dat $MACHBASE_HOME/conf/license.dat
```

### 방법 2: machadmin 명령

`machadmin`으로 라이선스 파일을 검증하고 설치합니다. 서버가 실행 중이면 라이선스 reload 요청을
함께 보냅니다.

```bash
machadmin -t /path/to/license.dat
```

### 방법 3: SQL 쿼리 (서버 실행 중)

서버가 이미 실행 중인 경우 machsql에서 쿼리로 설치할 수 있습니다.

```sql
ALTER SYSTEM INSTALL LICENSE = '/path/to/license.dat';
```

## 설치 확인

### 서버 로그 확인

서버 시작 후 `$MACHBASE_HOME/trc/machbase.trc`에서 라이선스 정보가 출력되면 정상 설치된 것입니다.

```
[INFO] LICENSE [License ID] [00000001]
[INFO] LICENSE [Issue DATE] [20991231]
[INFO] LICENSE [License Type(Version 3)] [FOGUNLIMITED]
[INFO] LICENSE [Company] [MACHBASE]
```

### machadmin 확인

```bash
machadmin -f
```

### V$LICENSE_INFO 뷰 조회

```sql
SELECT ID, ISSUE_DATE, TYPE, CUSTOMER, VIOLATE_STATUS, VIOLATE_MSG
FROM V$LICENSE_INFO;
```

`VIOLATE_STATUS`가 0이면 정상입니다.

machsql에서는 다음 명령으로도 라이선스 정보를 확인할 수 있습니다.

```sql
SHOW LICENSE;
```

---

**다음 읽을 내용**
- [Standard Edition 설치](/dbms/installation-deployment-upgrade/standard-edition/)
- [Cluster Edition 설치](/dbms/installation-deployment-upgrade/cluster-edition/)
