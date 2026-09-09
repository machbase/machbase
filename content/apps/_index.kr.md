---
type: docs
title: Apps
weight: 30
---

Machbase Neo 패키지는 데이터 수집과 복제, 영상 모니터링, AI 기반 분석 기능을 확장합니다.
웹 UI의 패키지 목록에서 필요한 패키지를 설치하고, 브라우저에서 설정과 운영을 관리할 수 있습니다.

------

{{< cards >}}

  <!-- 대표 이미지: neo-pkg-replication/docs/images/dashboard-main.png. 추후 이미지 교체 가능. -->
  {{< card link="https://machbase.github.io/neo-pkg-replication/kr/" 
    image="/images/package/replication.png" icon="gift"
    title="Replication"
    subtitle="Replication 패키지(`neo-pkg-replication`)는 Machbase 테이블의 데이터를 다른 Machbase 서버로 복제합니다. 웹 화면에서 복제 조건과 컬럼 매핑을 설정하고, 진행 상태와 로그를 확인할 수 있습니다. 네트워크 연결 문제나 서버 정지로 복제가 중단되더라도, 연결이 복구되면 중단 지점부터 이어서 복제해데이터 누락을 방지합니다.">}}

  <!-- 대표 이미지: neo-pkg-opcua-client/docs/images/opcua-dashboard-main.png. 추후 이미지 교체 가능. -->
  {{< card link="https://machbase.github.io/neo-pkg-opcua-client/kr/" 
    image="/images/package/opcua-client.png" icon="gift"
    title="OPC UA Client"
    subtitle="OPC UA Client 패키지(`neo-pkg-opcua-client`)는 OPC UA 서버의 설비·센서 데이터를 수집해 Machbase Neo에 저장합니다. 서버의 노드를 탐색하여 수집 대상을 선택하고, 컬럼 매핑과 값 변환을 설정할 수 있습니다. 수집 작업의 시작·중지, 상태 확인과 로그 조회도 웹 화면에서 처리합니다. 데이터 뷰어에서 수집한 데이터를 표와 차트로 확인할 수 있습니다.">}}

  <!-- 대표 이미지: neo-pkg-blackbox/docs/images/blackbox-dashboard-video-sync.png. 추후 이미지 교체 가능. -->
  {{< card link="https://machbase.github.io/neo-pkg-blackbox/kr/"
    image="/images/package/blackbox.png" icon="gift" 
    title="Blackbox"
    subtitle="Blackbox 패키지(`neo-pkg-blackbox`)는 카메라 영상과 감지 이벤트를 관리하는 영상 모니터링 기능을 제공합니다. Blackbox 서버와 카메라를 등록하고, 객체 감지와 이벤트 규칙을 설정하며, 이벤트 발생 이력을 조회할 수 있습니다. Neo 대시보드의 Video 패널에서는 실시간·녹화 영상을 확인할 수 있으며, 녹화 영상은 시계열 차트와 시점을 맞춰 살펴볼 수 있습니다.">}}

  <!-- 대표 이미지: neo-pkg-llm-chat/docs/images/llm-chat-main.png. 추후 이미지 교체 가능. -->
  {{< card link="https://machbase.github.io/neo-pkg-llm-chat/kr/"
    image="/images/package/llm-chat.png" icon="gift"
    title="LLM Chat"
    subtitle="LLM Chat 패키지(`neo-pkg-llm-chat`)는 자연어 대화로 Machbase Neo 데이터를 조회하고 분석하는 AI 채팅 기능을 제공합니다. 테이블과 태그를 탐색하고, 대화를 통해 대시보드와 분석 리포트를 만들 수 있습니다. 다양한 LLM 모델을 지원하며, 웹 설정 화면에서 사용할 모델과 연결 정보를 관리할 수 있습니다.">}}
{{< /cards >}}
