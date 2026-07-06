---
type: docs
title: '데이터 반출 작업 소유권'
weight: 10
---

데이터 반출 시 생성되는 파일의 소유권(ownership)에 대한 내용입니다.

## SAVE DATA INTO 파일 소유권

`SAVE DATA INTO` 구문으로 생성되는 파일은 **Machbase 서버 프로세스 계정**이 소유합니다. 일반적으로 `mach` 또는 Machbase를 실행한 시스템 사용자 계정입니다.

```sql
SAVE DATA INTO '/data/export/result.csv' AS SELECT * FROM sensor_log;
-- 파일 소유자: machbase 서버 프로세스 계정
```

파일을 다른 사용자가 읽어야 하는 경우, 서버 관리자가 적절한 파일 퍼미션을 설정해야 합니다.

## machloader / csvexport 파일 소유권

`machloader -o` 또는 `csvexport`는 클라이언트 프로세스가 파일을 생성합니다. 따라서 **클라이언트를 실행한 사용자**가 파일 소유권을 갖습니다.

```bash
# machloader를 실행한 OS 사용자가 파일 소유자
machloader -o -d /home/user/export.csv -t sensor_log
```

## 반출 디렉터리 권한 확인

`SAVE DATA INTO` 사용 시 대상 디렉터리에 Machbase 서버 프로세스가 쓰기 권한을 가져야 합니다.

```bash
# 반출 디렉터리 권한 확인
ls -la /data/export/

# 서버 프로세스 계정(예: mach)에 쓰기 권한 부여
chown mach:mach /data/export/
chmod 755 /data/export/
```

## 접근 권한 모범 사례

- 반출 디렉터리를 Machbase 서버 계정이 쓸 수 있는 전용 경로로 지정
- 민감한 데이터 반출 시 파일 퍼미션(600 또는 640)을 엄격하게 관리
- 정기 반출 작업의 경우 전용 서비스 계정을 사용하여 실행
