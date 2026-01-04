---
type: docs
title: '도구 레퍼런스'
weight: 90
---

Machbase 명령줄 도구 및 유틸리티에 대한 완전한 레퍼런스입니다. 이 섹션에서는 데이터베이스 관리, 데이터 가져오기/내보내기, 시스템 관리를 위한 모든 도구를 다룹니다.

## 명령줄 도구

### machadmin

데이터베이스 서버 관리:
- 서버 시작/중지
- 데이터베이스 생성/삭제
- 백업/복구
- 서버 상태

```bash
machadmin -u          # 서버 시작
machadmin -s          # 서버 중지
machadmin -c          # 데이터베이스 생성
machadmin -b path     # 백업
machadmin -r path     # 복구
```

[전체 레퍼런스](./machadmin/)

### machsql

대화형 SQL 클라이언트:
- 쿼리 실행
- SQL 스크립트 실행
- 결과 내보내기
- 데이터베이스 관리

```bash
machsql                           # 대화형 모드
machsql -f script.sql            # 스크립트 실행
machsql -o output.csv -r csv     # CSV로 내보내기
```

[전체 레퍼런스](./machsql/)

### machloader

대량 데이터 가져오기 도구:
- CSV 가져오기
- 빠른 대량 로딩
- 오류 처리

```bash
machloader -t table -d csv -i data.csv
```

[전체 레퍼런스](./machloader/)

### machcoordinatoradmin

클러스터 코디네이터 관리 (클러스터 에디션):
- 코디네이터 관리
- 클러스터 설정
- 노드 관리

[전체 레퍼런스](./machcoordinatoradmin/)

### machdeployeradmin

클러스터 디플로이어 관리 (클러스터 에디션):
- 디플로이어 관리
- 웨어하우스 관리
- 클러스터 배포

[전체 레퍼런스](./machdeployeradmin/)

## 도구 빠른 레퍼런스

| 도구 | 용도 | 일반적인 사용 |
|------|---------|------------|
| machadmin | 서버 관리 | 시작/중지, 백업 |
| machsql | SQL 클라이언트 | 쿼리, 스크립트 |
| machloader | 데이터 가져오기 | CSV 로딩 |
| machcoordinatoradmin | 클러스터 코디네이터 | 클러스터 관리 |
| machdeployeradmin | 클러스터 디플로이어 | 클러스터 배포 |

## 일반적인 작업

### 서버 관리

```bash
# 서버 시작
machadmin -u

# 서버 중지
machadmin -s

# 상태 확인
machadmin -e

# 데이터베이스 생성
machadmin -c

# 데이터베이스 삭제
machadmin -d
```

### 데이터 작업

```bash
# 대화형 SQL
machsql

# 스크립트 실행
machsql -f setup.sql

# CSV 가져오기
machloader -t sensors -d csv -i data.csv

# 쿼리 결과 내보내기
machsql -f query.sql -o results.csv -r csv
```

### 백업 및 복구

```bash
# 백업
machadmin -b /backup/machbase_backup

# 복구
machadmin -r /backup/machbase_backup
```

## 환경 변수

```bash
# 필수 환경 변수
export MACHBASE_HOME=/path/to/machbase
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
```

## 설정 파일

### machbase.conf

주요 서버 설정 파일 위치:
```
$MACHBASE_HOME/conf/machbase.conf
```

주요 파라미터:
- `PORT_NO` - 서버 포트 (기본값: 5656)
- `BUFFER_POOL_SIZE` - 메모리 버퍼 크기
- `CHECKPOINT_INTERVAL_SEC` - 체크포인트 간격

[전체 설정 레퍼런스](../configuration/)

## 로그 파일

```bash
# 서버 로그
$MACHBASE_HOME/trc/machbase.log

# SQL 클라이언트 로그
$MACHBASE_HOME/trc/machsql.log

# 로더 로그
$MACHBASE_HOME/trc/machloader.log
```

## 문제 해결

### 서버가 시작되지 않을 때

```bash
# 포트 사용 가능 여부 확인
netstat -an | grep 5656

# 로그 확인
tail -50 $MACHBASE_HOME/trc/machbase.log

# 데이터베이스 생성 여부 확인
ls -la $MACHBASE_HOME/dbs/
```

### 연결 문제

```bash
# 서버 실행 여부 확인
machadmin -e

# 연결 테스트
machsql -s localhost -u SYS -p MANAGER
```

### 가져오기 오류

```bash
# CSV 형식 확인
head -10 data.csv

# 로더 로그 확인
cat $MACHBASE_HOME/trc/machloader.log
```

## 모범 사례

1. **항상 환경 변수 사용** - MACHBASE_HOME을 올바르게 설정하세요
2. **서버 상태 확인** - 작업 전에 `machadmin -e`를 사용하세요
3. **로그 검토** - 오류 및 경고를 위해 로그를 확인하세요
4. **정기 백업** - 백업을 위해 `machadmin -b`를 사용하세요
5. **스크립트 테스트** - 프로덕션 사용 전에 SQL 스크립트를 검증하세요

## 관련 문서

- [일반 작업](../common-tasks/) - 실용적인 사용 가이드
- [설정](../configuration/) - 서버 설정
- [문제 해결](../troubleshooting/) - 문제 해결

## 빠른 시작

```bash
# 1. 환경 설정
export MACHBASE_HOME=/opt/machbase
export PATH=$MACHBASE_HOME/bin:$PATH

# 2. 데이터베이스 생성
machadmin -c

# 3. 서버 시작
machadmin -u

# 4. 연결
machsql

# 5. 데이터 가져오기
machloader -t mytable -d csv -i data.csv
```

자세한 도구 문서는 원본 문서의 [도구 레퍼런스](../../dbms/tools-reference/)를 참조하세요.
