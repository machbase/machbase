---
title : '라이선스 설치'
type : docs
weight: 40
---

라이선스 키 설치는 일반적으로 MACHBASE 설치가 완료된 후에 수행됩니다. 설치 후 특정 라이선스를 설치하지 않으면 일부 제약 사항과 함께 MACHBASE를 사용할 수 있습니다. 이 섹션에서는 MACHBASE의 라이선스 정책, 구조 및 설치 방법에 대해 설명합니다.


## 라이선스 파일 구조

MACHBASE 라이선스는 license.dat 파일로 관리됩니다. 제품용 또는 테스트용으로 구매한 라이선스는 텍스트 파일 형식으로 표시됩니다.

```bash
mach@localhost:~$ cat license.dat

\#Company\#ID-ProjectName: test\#0-Machbase
 \#License Policy: SIZE4DAY
 \#License Type \(Version 2\): OFFICIAL
 \#Issue DATE: 20160216
 \#Expiry DATE: 20160319
 \#Tag Count Limit: 0
 VBz5h4TC-d3+Bf3Efkpdp/Tx873PpZA-78LRSdrxbPY-xhGf4355/iXaY5/jfnn+Jdpjn+N+ef4l2mOf4355/iXaY5/jfnn+Jdpjn+N+ef4l2mOf4355/iXaY5/jfnn+Jdpjn+N+ef4l2mOf4355/iXaY5/jfnn+Jdpjn+
```


## 라이선스 파일이 없는 경우

라이선스가 없어도 서버는 실행되지만 몇 가지 제한 사항이 있습니다. 서버는 평가 목적으로만 사용할 수 있으므로 정식으로 사용하려는 경우 합법적인 절차를 통해 라이선스를 취득해야 합니다.

라이선스 파일이 없는 경우 다음과 같은 기능 제한이 있습니다.

    1. 한 세션에서 Append 프로토콜을 통해 1억 개 이상의 레코드를 입력하면 경고 메시지가 표시됩니다. 그러면 Append 입력이 중지됩니다. 입력 제한 상태는 서버를 재시작할 때만 해제됩니다.

    2. 테이블스페이스를 생성할 때 두 개 이상의 디스크 디렉토리를 생성할 수 없습니다. 둘 이상의 디스크를 사용하면 고성능 데이터 입력을 위한 병렬 I/O 기능을 사용할 수 없다는 다음 경고가 표시됩니다.

```bash
CREATE TABLESPACE tbs1 DATADISK disk1 (disk_path="tbs1_disk1"), disk2 (disk_path="tbs1_disk2"), disk3 (disk_path="tbs1_disk3");
[ERR-00867 : Error in adding disk to tablespace. You cannot use multiple disks for tablespace without valid license.]
```


## 라이선스 설치

MACHBASE 라이선스는 $MACHBASE_HOME/conf에 설치해야 하며, 기본 이름은 license.dat입니다.

라이선스 파일을 `$MACHBASE_HOME/conf`에 복사합니다.

이때 발급받은 라이선스 파일의 이름을 **license.dat**로 변경하여 복사해야 합니다. 그러면 서버가 시작될 때 라이선스가 적절한지 판단하고 설치를 시작합니다.

**machadmin -t 'licensefile_path'**를 실행합니다.

이 방법의 장점은 라이선스 파일 이름이나 위치를 조정할 필요 없이 명령으로 쉽게 설치할 수 있다는 것입니다.

쿼리로 설치: 서버가 실행 중일 때 쿼리 문을 사용하여 라이선스를 설치하는 방법입니다.


## 라이선스 설치 확인

### 라이선스가 설치된 경우

라이선스 파일이 설치된 경우 서버가 시작된 후 machbase.trc에 다음과 같이 표시됩니다.

```bash
[2016-02-17 14:51:00 P-20913 T-140709874054912][INFO] LICENSE [License Type (Version 2)][OFFICIAL]
[2016-02-17 14:51:00 P-20913 T-140709874054912][INFO] LICENSE [License Policy] [CORE]
[2016-02-17 14:51:00 P-20913 T-140709874054912][INFO] LICENSE [Host ID] [FFFFFFFFFFFFFFF]
[2016-02-17 14:51:00 P-20913 T-140709874054912][INFO] LICENSE [Expiry DATE] [25300318]
[2016-02-17 14:51:00 P-20913 T-140709874054912][INFO] Machbase Logs Signature! : OFFICIAL:CORE:FFFFFFFFFFFFFFF:25300318-3.5.0.826b8f2.official-LINUX-X86-64-release
```

machadmin -f 명령을 사용할 수도 있습니다.

### 라이선스가 설치되지 않은 경우

라이선스 파일이 설치되지 않았거나 비정상적인 파일을 사용한 경우 다음 출력이 표시됩니다.

```bash
[2016-02-17 14:49:54 P-6620 T-140539052701440][INFO] LICENSE [License Type(Version 2)][Only for evaluation (No license)]
[2016-02-17 14:49:54 P-6620 T-140539052701440][INFO] LICENSE [License Policy] [None]
[2016-02-17 14:49:54 P-6620 T-140539052701440][INFO] LICENSE [Host ID] [Unknown]
[2016-02-17 14:49:54 P-6620 T-140539052701440][INFO] LICENSE [Expiry DATE] [N/A]
```
