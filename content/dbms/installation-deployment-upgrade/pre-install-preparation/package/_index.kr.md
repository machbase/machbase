---
type: docs
title: '3.1.2 패키지 구성 이해'
weight: 20
toc: true
---

## 패키지 파일 명명 규칙

Machbase 패키지 파일 이름은 에디션에 따라 다음 형식을 따릅니다.

```
machbase-EDITION-VERSION-OS-CPU-BIT-MODE.EXT
```

| 항목 | 설명 | 예시 |
|------|------|------|
| EDITION | 에디션 구분 | `SDK`, `cluster` |
| VERSION | 버전 (Major.Minor.Fix.AUX) | `8.6.0.official` |
| OS | 운영체제 | `LINUX`, `WINDOWS` |
| CPU | CPU 아키텍처 | `X86` |
| BIT | 아키텍처 비트 수 | `64` |
| MODE | 빌드 모드 | `release` |
| EXT | 확장자 | `tgz` (Linux), `zip` 또는 설치 실행 파일 (Windows) |

Standard Edition Linux tarball은 `machbase-SDK-...tgz` 이름으로 생성됩니다.

예시:
- Standard Edition: `machbase-SDK-8.6.0.official-LINUX-X86-64-release.tgz`
- Cluster Edition: `machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz`

버전에서 Minor 버전이 다른 경우 DB 파일 및 프로토콜 호환이 보장되지 않습니다. Fix 버전 변경은 호환성이 유지됩니다.

## 설치 디렉터리 구조

tarball 압축을 해제하면 `$MACHBASE_HOME` 아래에 다음 구조가 생성됩니다.

```
$MACHBASE_HOME/
├── bin/        실행 파일
├── conf/       설정 파일 (machbase.conf 등)
├── dbs/        데이터 저장 공간
├── doc/        라이선스 문서
├── http/       HTTP REST API 및 웹 리소스
├── include/    C/C++ 헤더 파일
├── install/    Makefile용 mk 파일
├── lib/        공유 라이브러리
├── package/    Cluster Edition 추가 패키지 경로
├── sample/     예제 파일
├── trc/        서버 로그 및 트레이스 파일
├── tutorials/  튜토리얼
├── utility/    유틸리티 파일
└── 3rd-party/  Grafana 플러그인 등
```

## 주요 실행 파일

| 실행 파일 | 설명 |
|-----------|------|
| `machbased` | 서버 데몬 |
| `machadmin` | 서버 관리 (시작·종료·DB 생성) |
| `machsql` | CLI 쿼리 도구 |
| `machloader` | 대용량 파일 적재·추출 도구 |
| `csvimport` | CSV 파일 가져오기 |
| `csvexport` | CSV 파일 내보내기 |
| `tagmetaimport` | TAG 메타 데이터 일괄 등록 |

Cluster Edition 패키지에는 `machcoordinatoradmin`, `machdeployeradmin` 등의 관리 도구가 추가됩니다.
`machclusterctl`은 해당 도구를 포함하도록 빌드된 패키지에서 사용할 수 있습니다.

## 설정 파일

`$MACHBASE_HOME/conf/` 아래에 에디션별 샘플 설정 파일이 있습니다.

```bash
ls $MACHBASE_HOME/conf/
# machbase.conf
# machbase.conf.sample.standard
# machbase.conf.sample.edge
# machloader.conf.sample
```

실제 사용 파일은 `machbase.conf`입니다. Standard full 패키지는 빌드 과정에서
`machbase.conf.sample.standard`를 복사해 `machbase.conf`를 포함합니다. 실제 파일이 없는
패키지에서는 에디션에 맞는 샘플 파일을 복사하여 수정합니다.

RDB 테이블 기능이 포함된 빌드의 Standard/Edge 샘플에는 RDB 테이블 sidecar 파일 동작을 제어하는
`RDB_BUSY_TIMEOUT_MS`, `RDB_SYNCHRONOUS`, `RDB_JOURNAL_MODE` 설정이 포함될 수 있습니다. 해당
항목이 없는 패키지에서는 추가하지 말고, RDB 테이블을 사용하는 환경에서만 기본값과 운영 중 busy
timeout 또는 SQLite 동기화 정책 조정 필요성을 검토합니다.

---

**다음 읽을 내용**
- [라이선스 설치](/kr/dbms/installation-deployment-upgrade/pre-install-preparation/license/)
