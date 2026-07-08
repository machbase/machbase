---
type: docs
title: '인증키 관리'
weight: 40
---

## AUTH KEY란

AUTH KEY는 공개키 기반 챌린지-응답(challenge-response) 인증 방식입니다. 클라이언트가 보유한 개인키로 서버가 보낸 챌린지(nonce)에 서명하고, 서버가 사전에 등록된 공개키로 서명을 검증합니다. 비밀번호를 네트워크로 전송하지 않기 때문에 도청이나 재전송 공격에 강합니다.

## 비밀번호 인증과 AUTH KEY 인증 비교

| 항목 | 비밀번호 인증 | AUTH KEY 인증 |
|------|-------------|--------------|
| 인증 방식 | 비밀번호 전송 | 챌린지-응답 서명 |
| 네트워크 전송 | 비밀번호(해시) 전송 | 서명값만 전송 |
| 재전송 공격 | 취약 | 강건 (nonce 일회성) |
| 키 관리 | 비밀번호 주기 변경 필요 | 개인키 파일 보호 |
| 만료 관리 | 비밀번호 만료 | AUTH KEY `valid_before` 설정 |
| 복수 키 | 불가 | 가능 (롤오버 지원) |

## 인증 흐름 요약

1. 클라이언트가 접속 요청 (`AUTH_MODE=CHALLENGE`)
2. 서버가 32바이트 nonce(챌린지) 생성 후 전송
3. 클라이언트가 개인키(`AUTH_KEY_FILE`)로 nonce에 서명
4. 서버가 등록된 공개키로 서명 검증
5. 검증 성공 시 세션 개시

## 주요 설정 항목

| 설정 항목 | 역할 | 위치 |
|-----------|------|------|
| `AUTH_MODE` | 인증 방식 선택 (`PASSWORD` / `CHALLENGE`) | 연결 옵션 |
| `AUTH_KEY_FILE` | 클라이언트 개인키 파일 경로 | 연결 옵션 |
| `AUTH_SIG_SCHEME` | 서명 스킴 (`ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS`) | 연결 옵션 |

`AUTH_MODE`는 서버 `machbase.conf` 속성이 아니라 클라이언트 연결 옵션입니다.
서버 전체를 PASSWORD/CHALLENGE 모드로 전환하는 절차는 현재 nfx 기준으로 제공되지 않습니다.

## 이 섹션의 구성

- [AUTH KEY challenge 인증](authentication-auth-key-challenge/) — 챌린지-응답 인증 흐름 상세 설명
- [SYS AS USER 인증 제약](authentication-sys-user/) — SYS 계정의 AUTH KEY 사용 제약
- [AUTH_MODE=CHALLENGE](auth-mode-challenge/) — CHALLENGE 전용 모드 설정
- [AUTH_KEY_FILE](auth-key-file/) — 개인키 파일 경로 설정
- [AUTH_SIG_SCHEME](auth-sig-scheme/) — 서명 알고리즘 설정
- [RSA / ECDSA / RSA_PSS 지원 범위](support-scope-rsa-ecdsa-rsa-pss/) — 알고리즘별 특성과 SDK 지원 현황
- [사용자 AUTH KEY 관리](user-auth-key/) — AUTH KEY 등록·수정·삭제 SQL
