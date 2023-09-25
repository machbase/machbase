---
title : '쿼리 에러를 Property 수정하여 해결하는 방법'
type: docs
weight: 10
---

쿼리를 실행한 후 메모리 부족 에러가 발생하였을 때 Property를 수정하여 해결하는 방법을 설명한다.


## 쿼리 실행 시 메모리가 부족하여 에러가 발생함
아래와 같은 이유로 쿼리를 실행하는데 필요한 메모리를 제한하고 있다.

* 특정 쿼리가 메모리를 너무 많이 사용하는 경우, 동시에 실행 중인 다른 쿼리가 메모리 부족으로 실행이 안되는 경우가 발생할 수 있다.

이를 방지하기 위해 하나의 쿼리가 사용가능한 메모리 최대 사이즈 Property 값을 증가시켜 에러를 해결할 수 있다.

**MAX_QPX_MEM Property로 하나의 SQL에서 사용할 수 있는 최대 사용 가능 메모리**를 관리한다.

실행 중 설정하는 방법및 메모리가 부족하여 발생하는 에러메세지및 TRC메세지도 SET MAX_QPX_MEM 페이지를 참고한다.

SET 명령어로 Property 값을 설정하면 마크베이스 재시작 시 설정 값이 적용되지 않으므로 machbase.conf 파일도 아래와 같이 함께 수정하여야 한다.

**Standard Edition**

machbase.conf의 MAX_QPX_MEM 를 보다 큰 값으로 수정한다.

**Cluster Edition**

Standard edtion과 동일하다. 단, 모든 클러스터 노드의 machbase.conf 를 수정해야 한다.
