---
type: docs
title: 'Standard Edition 업그레이드'
weight: 10
toc: true
---

Standard Edition 업그레이드는 서버를 종료하고 패키지를 교체한 후 재시작하는 방식입니다.

## 업그레이드 전 준비

1. **백업 수행**: 데이터 디렉터리(`$MACHBASE_HOME/dbs/`)를 백업합니다.

2. **클라이언트 연결 종료**: 진행 중인 Append 또는 INSERT 작업을 모두 완료합니다.

3. **현재 버전 확인**:
   ```bash
   machbased -v
   ```

## 업그레이드 절차

### 1. 서버 종료

```bash
machadmin -s
# Machbase server shut down successfully.
```

### 2. 기존 패키지 백업 (선택)

실행 파일과 라이브러리를 백업합니다.

```bash
cp -a $MACHBASE_HOME/bin $MACHBASE_HOME/bin.bak
cp -a $MACHBASE_HOME/lib $MACHBASE_HOME/lib.bak
```

**데이터 디렉터리(`dbs/`)는 삭제하지 마십시오.** 기존 데이터가 보존됩니다.

### 3. 새 패키지 압축 해제

```bash
tar zxf machbase-SDK-8.6.0.official-LINUX-X86-64-release.tgz -C $MACHBASE_HOME
```

압축 해제 시 `bin/`, `lib/`, `include/` 등이 덮어씌워지고 `dbs/`는 변경되지 않습니다.

### 4. 서버 시작

```bash
machadmin -u
# Machbase server started successfully.
```

### 5. 버전 확인

```bash
machbased -v

# machsql에서 확인
machsql -u SYS -p MANAGER
Mach> SELECT VERSION FROM V$VERSION;
```

## 주의사항

- `dbs/` 디렉터리를 절대 삭제하거나 초기화(`machadmin -d`)하지 마십시오.
- Minor 버전 간 업그레이드는 DB 파일 마이그레이션이 필요할 수 있습니다. 릴리스 노트를 반드시 확인하십시오.
- Windows 환경에서는 MSI 설치 관리자를 실행하기 전에 Machbase 서비스를 중지합니다.

---

**다음 읽을 내용**
- [설치 검증 체크리스트](/kr/dbms/installation-deployment-upgrade/validation-checklist/)
