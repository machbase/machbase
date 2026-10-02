---
title: Prometheus 모니터링 데모
type: docs
weight: 971
---

운영체제에 맞게 Machbase Neo의 Prometheus 메트릭 엔드포인트를 수집하고 Grafana 대시보드를 여는 방법을 안내합니다.

{{< icon "github" >}} https://github.com/machbase/neo-prom
<p/>

{{< youtube -pDn6ysLCh0 >}}

이 가이드에서는 Docker 기반 Prometheus로 Machbase Neo의 메트릭 엔드포인트(`http://127.0.0.1:5654/debug/metrics`)를 수집하고, Grafana 대시보드에서 시계열 데이터를 모니터링하는 데모를 재현합니다.


**사전 조건**

- Docker와 Docker Compose를 사용할 수 있어야 합니다.
- 5654, 9090, 3000 포트를 사용할 수 있어야 합니다.
- Machbase Neo 실행 파일이 필요합니다.