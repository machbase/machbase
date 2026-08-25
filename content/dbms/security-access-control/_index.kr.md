---
type: docs
title: '15. 계정, 권한, 접속 제어'
weight: 150
toc: true
---

운영 환경에서 데이터를 보호하려면 계정, 권한, 접속 제어를 체계적으로 구성해야 합니다. 이 장에서는 보안 모델 전반을 다루며, 실무에 맞는 설정 방법을 안내합니다.

## 이 장의 구성

| 섹션 | 설명 |
|------|------|
| [보안 모델 개요](./security-model/) | Machbase 보안 구조, 기본 계정, 권한 종류, AUTH KEY 인증 방식 |
| [계정 관리](./account/) | 사용자 생성·삭제·비밀번호 변경, 비밀번호 정책(NONE/LOW/HIGH) |
| [권한 관리](./privileges/) | GRANT/REVOKE, 테이블 권한, 데이터베이스 권한 |
| [AUTH KEY 인증](./authentication-auth-key/) | 공개키 기반 challenge 인증, 키 생성·등록·관리 |
| [접속 제어](./access-control/) | 원격 접속 허용 여부와 바인드 IP 설정 |
| [보안 설정 체크리스트](./checklist-configuration/) | 운영 환경 배포 전 점검 항목 |

## 보안의 4대 영역

**1. 보안 모델** -- 사용자 계정, 권한 체계, 인증 방식의 연동 구조를 파악합니다. SYS는 관리
작업으로 제한하고 각 사용자에게 최소 권한만 부여합니다.

**2. 계정 관리** -- 데이터베이스에 접근하는 주체를 관리합니다. 사용자 계정을 생성·삭제하고
비밀번호 정책(NONE/LOW/HIGH)과 공개키 기반 AUTH KEY 인증을 적용합니다.

**3. 권한 관리** -- 계정이 수행할 수 있는 작업을 제한합니다. 테이블 단위 DML 권한(SELECT, INSERT, DELETE, UPDATE)과 데이터베이스 단위 DDL·운영 권한(CREATE, DROP, ALTER, BACKUP, MOUNT)을 세분화해 최소 권한 원칙을 적용합니다.

**4. 접속 제어** -- 어떤 네트워크 경로에서 연결을 허용할지 제어합니다. `GRANT_REMOTE_ACCESS`로 원격 접속 허용 여부를 결정하고, `BIND_IP_ADDRESS`로 리스너가 열리는 네트워크 인터페이스를 지정합니다.
