---
title: OPC UA 데이터 수집 데모
type: docs
weight: 969
---

Kepware OPC UA 서버를 Machbase Neo에 연결하고 인증서를 설정해 데이터를 수집하는 과정을 안내합니다.

{{< icon "github" >}} https://github.com/machbase/neo-prom
<p/>

{{< youtube BgrEGzDoQLU >}}

이 가이드에서는 Machbase Neo OPC UA Client로 Kepware의 데이터를 수집하는 전체 과정을 살펴봅니다. 먼저 OPC UA 서버의 Endpoint와 보안 설정을 등록한 뒤, 안전한 통신을 위해 인증서를 생성하고 적용합니다.


서버에 연결한 뒤 제공되는 노드 구조를 탐색하고 수집할 태그를 선택합니다. 선택한 태그를 수집 작업으로 등록하면 Machbase 데이터베이스에 일정한 간격으로 저장됩니다.


이 영상에서는 별도의 수집 프로그램을 개발하지 않고도 웹 화면에서 OPC UA 서버에 연결하고 인증서를 관리해 필요한 설비 데이터를 수집하는 방법을 확인할 수 있습니다.