---
layout : post
title : '참조 테이블 활용 샘플 예제'
type: docs
---

참조 테이블은 갱신이 가능하며, 원본 로그 데이터가 갖고 있지 않은 데이터를 join을 통하여 추가하는데 사용된다. 아래 예제는 로그 테이블과 참조 테이블을 생성하는 예를 보여준다.

```sql
-- 로그 테이블의 생성
create table weblog (addr ipv4, msg varchar(100));
-- 샘플 데이터 입력
insert into weblog values ('127.0.0.1', 'a test msessage');
-- 참조 테이블의 생성
create lookup table dnslookup (addr ipv4 primary key, hostname varchar (100));
```

참조 테이블에 데이터를 삽입 혹은 갱신해 보자.

```sql
insert into dnslookup values ('127.0.0.1', 'localhost') on duplicate key update set hostname = '127.0.0.1'
```

참조 테이블과 로그 테이블에 join을 통하여 데이터를 검색할 수 있다.

```sql
select msg, hostname from weblog, dnslookup where weblog.addr = dnslookup.addr;
```
