---
type: docs
title: '7.9.1 활용 사례'
weight: 10
---

LOG 테이블은 다음과 같은 데이터를 저장하는 데 적합합니다.

## 적합한 데이터 유형

| 유형 | 예시 |
|------|------|
| 시스템 이벤트 | syslog, Windows Event Log |
| 애플리케이션 로그 | 웹 서버 액세스 로그, 오류 로그 |
| 네트워크 패킷 | NetFlow, IPFIX, 패킷 메타데이터 |
| 보안 이벤트 | IDS/IPS 경보, 방화벽 로그 |
| 트랜잭션 감사 | 데이터베이스 감사 로그 |

## 예시 스키마

### 웹 액세스 로그

```sql
CREATE TABLE web_access_log (
    method    VARCHAR(8),
    uri       VARCHAR(1024),
    status    SHORT,
    bytes     INTEGER,
    src_ip    IPV4,
    user_agent VARCHAR(512)
);
```

### 방화벽 이벤트 로그

```sql
CREATE TABLE fw_event (
    action    VARCHAR(8),
    src_ip    IPV4,
    dst_ip    IPV4,
    src_port  INTEGER,
    dst_port  INTEGER,
    protocol  SHORT
);
```

## 부적합한 경우

- 수정이 필요한 데이터 (UPDATE 불가)
- KEY 기반 조회가 빈번한 소규모 참조 데이터 → LOOKUP 테이블 권장
- 센서 계측값 → TAG 테이블 권장
