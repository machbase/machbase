---
type: docs
title: 'RSA / ECDSA / RSA_PSS 지원 범위'
weight: 70
---

## 알고리즘 특성 비교

| 항목 | ECDSA | RSA_PKCS1_V15 | RSA_PSS |
|------|-------|--------------|---------|
| 키 알고리즘 | ECDSA | RSA | RSA |
| 지원 키 파라미터 | P-256, P-384, P-521 | 2048, 3072, 4096 bit | 2048, 3072, 4096 bit |
| 서명 스킴 문자열 | `ECDSA` | `RSA_PKCS1_V15` | `RSA_PSS` |
| 해시 알고리즘 | SHA-256 | SHA-256 | SHA-256 |
| 키 크기 대비 보안성 | 높음 | 보통 | 보통 |
| 서명 크기 | 작음 | 중간 | 중간 |
| 성능 | 빠름 | 보통 | 보통 |
| 표준 권고 | NIST 권장 | 레거시 호환 | PKCS#1 v1.5 대체 권고 |

### ECDSA

타원곡선 암호화 기반 서명 방식입니다. RSA보다 짧은 키로 동등한 보안 수준을 제공합니다.

- P-256: 128-bit 보안 수준. 성능과 보안의 균형이 좋아 일반 용도에 적합합니다.
- P-384: 192-bit 보안 수준. 고보안 요구 환경에 적합합니다.
- P-521: 260-bit 보안 수준. 최고 보안 수준이 필요한 경우 사용합니다.

### RSA_PKCS1_V15

RSA PKCS#1 v1.5 패딩 방식의 서명입니다. 광범위한 레거시 호환성을 제공하지만 이론적 취약점이 알려져 있어 새로운 환경에서는 RSA_PSS 사용을 권장합니다.

### RSA_PSS

RSA Probabilistic Signature Scheme의 약자입니다. PKCS#1 v1.5보다 향상된 보안 특성을 가지며, RSA 서명 방식 중에서는 현대적인 선택입니다. RSA 키를 사용해야 하는 환경에서 `RSA_PKCS1_V15` 대신 권장합니다.

## SDK별 지원 범위

| SDK | ECDSA | RSA_PKCS1_V15 | RSA_PSS |
|-----|-------|--------------|---------|
| JDBC | P-256, P-384, P-521 | 2048, 3072, 4096 | 2048, 3072, 4096 |
| Python | P-256, P-384, P-521 | 2048, 3072, 4096 | 2048, 3072, 4096 |
| Go | P-256, P-384, P-521 | 2048, 3072, 4096 | 2048, 3072, 4096 |
| .NET | P-256, P-384, P-521 | 2048, 3072, 4096 | 2048, 3072, 4096 |
| Node.js | P-256, P-384, P-521 | 2048, 3072, 4096 | 2048, 3072, 4096 |

## 권장 알고리즘

신규 환경에서는 **ECDSA P-256**을 권장합니다.

- 짧은 키 크기로 높은 보안 수준 제공
- 서명 생성 및 검증 성능이 RSA보다 빠름
- NIST, IETF 등 표준 기관에서 권장하는 알고리즘

RSA 키 인프라를 이미 운영 중인 환경에서는 `RSA_PSS`를 선택합니다.

## openssl을 이용한 키 생성 명령 요약

```bash
# ECDSA P-256
openssl ecparam -name prime256v1 -genkey -noout -out key.pem
openssl ec -in key.pem -pubout -out pub.pem

# ECDSA P-384
openssl ecparam -name secp384r1 -genkey -noout -out key.pem
openssl ec -in key.pem -pubout -out pub.pem

# ECDSA P-521
openssl ecparam -name secp521r1 -genkey -noout -out key.pem
openssl ec -in key.pem -pubout -out pub.pem

# RSA 2048-bit (RSA_PKCS1_V15 또는 RSA_PSS 모두 사용 가능)
openssl genrsa -out key.pem 2048
openssl rsa -in key.pem -pubout -out pub.pem

# RSA 3072-bit
openssl genrsa -out key.pem 3072
openssl rsa -in key.pem -pubout -out pub.pem

# RSA 4096-bit
openssl genrsa -out key.pem 4096
openssl rsa -in key.pem -pubout -out pub.pem

# 생성 후 개인키 권한 설정
chmod 600 key.pem
```
