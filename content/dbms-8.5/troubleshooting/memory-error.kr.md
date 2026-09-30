---
title : '메모리 부족 에러'
type: docs
weight: 100
---

이 섹션에서는 쿼리 실행 중 메모리 부족 에러가 발생했을 때 프로퍼티를 수정하는 방법을 설명합니다.

## 쿼리 실행 시 메모리 부족으로 인한 에러 발생

쿼리 실행에 사용할 수 있는 메모리는 다음과 같은 이유로 제한됩니다.

특정 쿼리가 너무 많은 메모리를 사용하면 동시에 실행 중인 다른 쿼리가 메모리 부족으로 실행되지 못할 수 있습니다.

메모리 부족 에러는 한 쿼리가 사용할 수 있는 최대 메모리 프로퍼티 값을 늘려 해결할 수 있습니다.

`MAX_QPX_MEM` 프로퍼티는 하나의 SQL이 사용할 수 있는 최대 메모리를 관리합니다.

실행 중에 설정하는 방법과 메모리 부족으로 발생하는 에러 메시지 및 TRC 메시지는 [SET MAX_QPX_MEM](../../sql-reference/sys-session-manage/#set-max_qpx_mem)을 참조하세요.

`SET` 명령으로 설정한 프로퍼티 값은 Machbase를 재시작하면 유지되지 않으므로, 다음과 같이 `machbase.conf` 파일도 수정해야 합니다.

**Standard Edition**

`machbase.conf`의 `MAX_QPX_MEM`을 더 큰 값으로 수정합니다.

**Cluster Edition**

Standard Edition과 동일합니다. 단, 모든 클러스터 노드의 `machbase.conf`를 수정해야 합니다.
