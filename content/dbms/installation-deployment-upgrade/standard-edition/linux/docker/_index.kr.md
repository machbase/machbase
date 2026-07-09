---
type: docs
title: 'Docker 설치'
weight: 30
toc: true
---

Machbase Docker 이미지를 사용하면 별도의 환경 준비 없이 빠르게 구동할 수 있습니다. 개발·테스트
환경에 적합합니다.

Docker 설치가 사전에 완료되어 있어야 합니다. 배포 튜토리얼은 `machbase/machbase` 이미지를
사용합니다. 소스에서 Docker 이미지를 직접 빌드한 경우에는 로컬 이미지 이름(`machbase:latest`
등)으로 바꾸십시오.

## 이미지 확인

```bash
docker pull machbase/machbase
docker image ls machbase/machbase
```

## 컨테이너 실행

```bash
docker run -d \
  --name machbase \
  --ulimit nofile=65535 \
  -p 5656:5656 \
  -p 5657:5657 \
  -v /data/machbase:/home/machbase/machbase/dbs \
  machbase/machbase
```

| 옵션 | 설명 |
|------|------|
| `-p 5656:5656` | SQL 클라이언트 포트 매핑 |
| `-p 5657:5657` | HTTP REST API 포트 매핑 |
| `--ulimit nofile=65535` | 컨테이너 안에서 서버가 사용할 파일 디스크립터 한도 |
| `-v /data/machbase:...` | 데이터 디렉터리 볼륨 마운트 (데이터 영속성 보장) |

볼륨 마운트를 생략하면 컨테이너 삭제 시 데이터가 함께 제거됩니다.

## 컨테이너 상태 확인

```bash
docker ps
docker logs machbase
```

## 접속 테스트

### machsql (컨테이너 내부)

```bash
docker exec -it machbase machsql
# Mach>
```

### 호스트에서 접속

호스트에 machsql이 설치된 경우:

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER
```

HTTP REST API 쿼리는 `/machbase` 경로로 요청합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" --data-urlencode "q=SELECT 1"
```

## 컨테이너 종료 및 재시작

```bash
docker stop machbase
docker start machbase
```

## 라이선스 설치

컨테이너 실행 후 라이선스를 설치하려면 파일을 컨테이너 내부로 복사합니다.

```bash
docker cp license.dat machbase:/home/machbase/machbase/conf/license.dat
docker restart machbase
```

---

**다음 읽을 내용**
- [라이선스 설치](/kr/dbms/installation-deployment-upgrade/pre-install-preparation/license/)
- [설치 검증 체크리스트](/kr/dbms/installation-deployment-upgrade/validation-checklist/)
