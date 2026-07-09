---
type: docs
title: '14. 계정, 권한, 접속 제어'
weight: 140
---

Machbase는 시계열 데이터를 다루는 산업용 데이터베이스로, 운영 환경에서 데이터를 보호하기 위한 다층적 보안 체계를 갖추고 있습니다. 이 장에서는 Machbase의 보안 모델 전반을 이해하고, 계정 관리와 접속 제어를 실무에 맞게 구성하는 방법을 설명합니다.

## 이 장의 구성

| 섹션 | 설명 |
|------|------|
| [보안 모델 개요](./security-model/) | Machbase 보안 구조, 기본 계정, 권한 종류, AUTH KEY 인증 방식 |
| [계정 관리](./account/) | 사용자 생성·삭제·비밀번호 변경, 비밀번호 정책(NONE/LOW/HIGH) |
| [권한 관리](./privileges/) | GRANT/REVOKE, 테이블 권한, 데이터베이스 권한 |
| [AUTH KEY 인증](./authentication-auth-key/) | 공개키 기반 challenge 인증, 키 생성·등록·관리 |
| [접속 제어](./access-control/) | 원격 접속 허용 여부, 바인드 IP, HTTP 인증 설정 |
| [보안 설정 체크리스트](./checklist-configuration/) | 운영 환경 배포 전 점검 항목 |

## 보안의 4대 영역

Machbase의 보안 체계는 다음 네 영역으로 구성됩니다.

**1. 보안 모델**

사용자 계정, 권한 체계, 인증 방식이 어떻게 연동되는지 전체 구조를 파악합니다. Machbase는 슈퍼유저인 SYS 계정을 기반으로 하며, 각 사용자에게 필요한 최소 권한만 부여하는 방식을 권장합니다.

**2. 계정 관리**

데이터베이스에 접근하는 주체를 관리합니다. 사용자 계정을 생성·삭제하고 비밀번호 정책을 적용해 계정 보안 수준을 높입니다. Machbase 8.5부터는 비밀번호 강도 정책(NONE/LOW/HIGH)과 공개키 기반 AUTH KEY 인증을 지원합니다.

**3. 권한 관리**

계정이 수행할 수 있는 작업을 제한합니다. 테이블 단위의 DML 권한(SELECT, INSERT, DELETE, UPDATE)과 데이터베이스 단위의 DDL·운영 권한(CREATE, DROP, ALTER, BACKUP, MOUNT)을 세분화해 최소 권한 원칙을 적용합니다.

**4. 접속 제어**

어떤 네트워크 경로에서, 어떤 인증 방식으로 연결을 허용할지 제어합니다. `GRANT_REMOTE_ACCESS`로 원격 접속 허용 여부를 결정하고, `BIND_IP_ADDRESS`로 리스너가 열리는 네트워크 인터페이스를 지정하며, `HTTP_AUTH`로 REST API 인증 방식을 설정합니다.
