---
title: "@jsh/psutil"
type: docs
weight: 100
keywords:
- psutil
---

{{< neo_since ver="8.0.52" />}}

## hostID()

호스트 고유 ID를 반환합니다.

```js
const psutil = require("@jsh/psutil")
console.log("hostID:", psutil.hostID());

// hostID: 6d7174fe-ffe0-58f0-7ff2-35b714de3876
```

## hostBootTime()

시스템 부팅 시간을 초 단위 UNIX 타임스탬프로 반환합니다.

```js
const psutil = require("@jsh/psutil")
let dt = new Date(psutil.hostBootTime()*1000);
console.log("bootTime:", dt);

// bootTime: 2025-05-01 08:06:27 +0900 KST
```

## hostUptime()

시스템 가동 시간을 초 단위로 반환합니다.

```js
const psutil = require("@jsh/psutil")
let uptime = psutil.hostUptime();
console.log("uptime:", uptime, "s.");

// uptime: 11866 s.
```

## cpuCounts()

논리/물리 CPU 개수를 반환합니다.

```js
const psutil = require("@jsh/psutil")
console.log("cpu (logical):", psutil.cpuCounts(true));
console.log("cpu          :", psutil.cpuCounts(false));

// cpu (logical): 8
// cpu          : 4
```

## cpuPercent()

CPU 사용률을 반환합니다.

```js
const psutil = require("@jsh/psutil")
console.log("cpu percent:", ...psutil.cpuPercent(0, false));
console.log("cpu percent:", ...psutil.cpuPercent(0, true));

// cpu percent: 8.70578458648027
// cpu percent: 28.51707154356211 3.343076131816279 21.937084403642285 3.321347888376277 18.3998953983542 3.340130466006715 16.411984704537886 3.3924734292626
```

## loadAvg()

1/5/15분 평균 시스템 부하를 반환합니다.

```js
const psutil = require("@jsh/psutil")
console.log("load:", psutil.loadAvg());

// load: {"load1":2.33349609375,"load5":2.22021484375,"load15":2.1396484375}
```

## memVirtual()

가상 메모리 사용량 정보를 반환합니다.

```js
const psutil = require("@jsh/psutil")
mem = psutil.memVirtual()
for( k in mem) {
    console.log(k, mem[k])
}

// available 7198842880
// used 9981026304
// usedPercent 58.097219467163086
// free 974204928
// ...생략...
```

## memSwap()

스왑 메모리 사용량 정보를 반환합니다.

```js
const psutil = require("@jsh/psutil")
mem = psutil.memSwap()
for( k in mem) {
    console.log(k, mem[k])
}

// total 1073741824
// used 28049408
// free 1045692416
// ...생략...
```

## diskPartitions()

디스크 파티션 정보를 반환합니다.

```js
const psutil = require("@jsh/psutil")
partitions = psutil.diskPartitions()
for( disk of partitions) {
    for (k in disk) {
       console.log(k, disk[k])
    }
}

// device /dev/disk1s5s1
// mountpoint /
// fstype apfs
// opts &[ro journaled multilabel]
// ...생략...
```

## diskUsage()

디스크 사용량과 inode 정보를 반환합니다.

```js
const psutil = require("@jsh/psutil")
usage = psutil.diskUsage("/")
for (k in usage) {
    console.log(k, usage[k])
}

// path /
// fstype apfs
// total 1000240963584
// free 139938320384
// used 860302643200
// usedPercent 86.00953915318746
// inodesTotal 1366942043
// inodesUsed 356883
// inodesFree 1366585160
// inodesUsedPercent 0.026108129589514716
```

## diskIOCounters()

지정한 디스크의 I/O 카운터를 반환합니다.

```js
const psutil = require("@jsh/psutil")
counters = psutil.diskIOCounters("/dev/disk1s1")
for (c in counters) {
    cnt = counters[c];
    for( k in cnt) {
        console.log(k, cnt[k])
    }
}
```

## netIOCounters()

네트워크 인터페이스별 I/O 통계를 반환합니다.

```js
const psutil = require("@jsh/psutil")
console.log(psutil.netIOCounters())
```

## netProtoCounters()

프로토콜별 네트워크 통계를 반환합니다.

```js
const psutil = require("@jsh/psutil")
console.log(psutil.netProtoCounters())
```
