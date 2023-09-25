---
title : "라이선스 설치"
type : docs
weight: 40
---

라이선스 키 설치는 일반적으로 마크베이스 설치가 끝난 후에 수행한다. 설치 이후에 라이선스를 설치하지 않았다면 일부 제약이 있는 상태로 마크베이스의 사용이 가능하다. 이 장은 마크베이스의 라이선스 정책과 구조 및 설치 방법 등에 대해 기술한다.

## 라이선스 파일 구조

마크베이스의 라이선스는 license.dat 파일로 관리된다. 제품을 구매하거나 혹은 테스트를 위해 받는 라이선스는 텍스트 파일의 형태이다.

```bash
mach@localhost:~$ cat license.dat 
 
#Company\#ID-ProjectName: test\#0-Machbase 
#License Policy: SIZE4DAY 
#License Type \(Version 2\): OFFICIAL 
#Issue DATE: 20160216 
#Expiry DATE: 20160319 
Bz5h4TC-d3+Bf3Efkpdp/Tx873PpZA-78LRSdrxbPY-xhGf4355/iXaY5/jfnn+Jdpjn+N+ef4l2mOf4355/iXaY5/jfnn+Jdpjn+N+ef4l2mOf4355/iXaY5/jfnn+Jdpjn+N+ef4l2mOf4355/iXaY5/jfnn+Jdpjn+
```

## 라이선스 파일이 없는 경우

라이선스가 없는 경우에도 서버가 구동되지만 일부 제약 사항이 있다. 평가 용도로만 사용할 수 있으며, 정식으로 사용하려는 경우에는 적법한 절차로 라이선스를 취득하여야 한다.

라이선스 파일이 없을 경우에는 아래와 같은 기능적인 제약이 존재한다.

* 한 세션에서 Append 프로토콜을 통해 1억건 이상의 레코드를 입력할 경우 경고 메시지가 출력된다. 이후 Append 입력이 정지된다. 서버를 재시작할 경우에만 입력 제한 상태가 해제된다.
* 테이블스페이스를 생성할 때 2개 이상의 디스크 디렉터리에 대해 생성할 수 없으며, 만약 2개 이상 사용할 경우 아래와 같은 오류가 출력된다. 즉, 고성능 데이터 입력을 위한 병렬 I/O 기능을 사용할 수 없다. 

```bash
CREATE TABLESPACE tbs1 DATADISK disk1 (disk_path="tbs1_disk1"), disk2 (disk_path="tbs1_disk2"), disk3 (disk_path="tbs1_disk3");
[ERR-00867 : Error in adding disk to tablespace. You cannot use multiple disks for tablespace without valid license.]
```

## 라이선스 설치

마크베이스의 라이선스는 반드시 `$MACHBASE_HOME/conf`` 에 설치하고, license.dat를 기본 이름으로 한다. 라이선스를 설치하는 방법에는 아래처럼 세 가지가 있다.

라이선스 파일을 `$MACHBASE_HOME/conf`에 복사

이때 발급 받은 라이선스 파일의 이름을 반드시 license.dat 로 바꾼 후 복사해야 한다. 이후 서버 구동시 해당 라이선스가 적합한지 판별하여 서버를 구동한다. 

machadmin -t 'licensefile_path' 실행
이 방법의 장점은 라이선스 파일 이름이나 위치를 맞춰줄 필요가 없이 명령어로 손쉽게 설치가 가능하다. 

쿼리문으로 설치: 이 방법은 서버 구동 중에 쿼리문을 이용하여 라이선스를 설치하는 방법이다.

## 라이선스 설치 확인

### 라이선스가 설치된 경우

라이선스 파일이 설치된 경우 서버 구동 이후에 machbase.trc에 아래와 같이 출력된다.

```bash
[2016-02-17 14:51:00 P-20913 T-140709874054912][INFO] LICENSE [License Type (Version 2)][OFFICIAL]
[2016-02-17 14:51:00 P-20913 T-140709874054912][INFO] LICENSE [License Policy] [CORE]
[2016-02-17 14:51:00 P-20913 T-140709874054912][INFO] LICENSE [Host ID] [FFFFFFFFFFFFFFF]
[2016-02-17 14:51:00 P-20913 T-140709874054912][INFO] LICENSE [Expiry DATE] [25300318]
[2016-02-17 14:51:00 P-20913 T-140709874054912][INFO] Machbase Logs Signature! : OFFICIAL:CORE:FFFFFFFFFFFFFFF:25300318-3.5.0.826b8f2.official-LINUX-X86-64-release
```

그리고 machadmin -f 명령어로도 확인 할 수 있다.

### 라이선스가 없는 경우

라이선스 파일이 설치되지 않았거나 비정상 파일을 사용할 경우에는 아래와 같이 출력된다.

```bash
[2016-02-17 14:49:54 P-6620 T-140539052701440][INFO] LICENSE [License Type(Version 2)][Only for evaluation (No license)]
[2016-02-17 14:49:54 P-6620 T-140539052701440][INFO] LICENSE [License Policy] [None]
[2016-02-17 14:49:54 P-6620 T-140539052701440][INFO] LICENSE [Host ID] [Unknown]
[2016-02-17 14:49:54 P-6620 T-140539052701440][INFO] LICENSE [Expiry DATE] [N/A]
```
