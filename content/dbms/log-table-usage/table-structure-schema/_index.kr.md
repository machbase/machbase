---
title: '7.2 테이블 구조와 스키마'
weight: 20
toc: true
---
테이블 구조와 스키마에 해당하는 세부 문서를 모았습니다.


<a id="log-table-design"></a>

## LOG 테이블 설계

LOG 테이블은 이벤트·로그·패킷처럼 추가 전용(append-only) 데이터를 저장하는 기본 테이블 타입입니다. `CREATE TABLE` 문으로 생성하며, `_arrival_time` 컬럼이 자동으로 추가됩니다.

- **[활용 사례](/dbms/log-table-usage/patterns-scenarios/#use-cases-log)**
- **[_arrival_time 시간 모델](/dbms/log-table-usage/arrival-time-model/#time-model-arrival-time)**
- **[스키마 설계](/dbms/log-table-usage/table-structure-schema/#log-table-design-design-schema-log)**
- **[전문 검색 설계](/dbms/log-table-usage/text-search-keyword-index/#design-text-search)**
- **[네트워크 데이터 타입 설계](/dbms/log-table-usage/regex-network-query/#design-type-network-data-types)**
- **[제약 및 주의사항](/dbms/log-table-usage/constraints-errors-troubleshooting/#limitations-log)**

<a id="log-table-design-design-schema-log"></a>

### 스키마 설계

LOG 테이블 스키마 설계의 핵심은 조회 패턴에 맞게 컬럼을 구성하는 것입니다.

#### 기본 원칙

1. **컬럼 수 최소화**: 불필요한 컬럼은 쿼리 성능에 영향을 줍니다.
2. **적절한 데이터 타입**: 네트워크 주소는 `IPV4`/`IPV6`, 포트는 `USHORT` 또는 `INTEGER`
3. **이벤트 시각 컬럼 별도 추가**: `_arrival_time` 외에 이벤트 발생 시각이 필요하면 `DATETIME` 컬럼을 추가합니다.

#### 데이터 타입 선택

| 데이터 | 권장 타입 | 이유 |
|--------|---------|------|
| IP 주소 (v4) | `IPV4` | 4바이트 저장, 비교 연산 최적화 |
| IP 주소 (v6) | `IPV6` | 16바이트 저장 |
| 포트 번호 | `USHORT` | 0~65535, 2바이트 |
| 짧은 문자열 | `VARCHAR(n)` | 가변 길이 |
| 긴 텍스트 | `TEXT` | 전문 검색 가능 |
| 플래그/코드 | `SHORT` 또는 `INTEGER` | 숫자 비교가 빠름 |
| 바이트 크기 | `INTEGER` 또는 `LONG` | 오버플로우 주의 |

#### 예시: 통합 보안 이벤트 로그

```sql
CREATE TABLE security_event (
    event_time  DATETIME,        -- 이벤트 발생 시각
    severity    SHORT,           -- 1=INFO, 2=WARN, 3=ERROR, 4=CRITICAL
    category    VARCHAR(32),     -- 이벤트 카테고리
    src_ip      IPV4,
    dst_ip      IPV4,
    src_port    USHORT,
    dst_port    USHORT,
    protocol    SHORT,
    action      VARCHAR(16),
    description TEXT             -- 상세 설명 (전문 검색 대상)
);
```

#### 주의사항

- LOG 테이블에는 PRIMARY KEY, UNIQUE 제약을 지정할 수 없습니다.
- UPDATE와 일반 조건 DELETE가 불가능하므로 잘못 입력된 데이터는 수정할 수 없습니다. 보존/정리 목적의 `BEFORE`, `OLDEST`, `EXCEPT` DELETE는 별도로 사용합니다.
- 컬럼 추가(`ALTER TABLE ... ADD COLUMN`)는 지원하지만, 컬럼 삭제·변경은 지원하지 않습니다.
