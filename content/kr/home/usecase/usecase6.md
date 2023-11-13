---
title: Use Case
description: "캐롯손해보험은 국내 최초 디지털 손해보험사로서 기술과 데이터를 기반으로 새로운 상품과 서비스를 출시하며 보험을 재정의하고 있으며, 인슈어테크 플랫폼으로 빠르게 성장하고 있습니다. 자동차 보험에서는 주행거리별 보험에 적극적으로 참여하고 있습니다."
images:
  - /namecard/og_img.jpg
---

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" type="text/css" href="../../css/common.css" />
  <link rel="stylesheet" type="text/css" href="../../css/style.css" />
</head>
{{< home_menu_blog_kr >}}
<section class="usecase_section0">
  <div>
    <h2 class="sub_page_title">Use Case</h2>
    <p class="sub_page_titletext">
      Machbase products are the choice of the world's leading companies and are
      in use in countless locations.
    </p>
  </div>
</section>
<section>
  <div class="tech-inner">
    <section>
      <div class="tech-inner">
        <h4 class="blog-title">[Machbase Use Case]보험 - 캐롯손해보험</h4>
        <ul class="tech-list-ul">
          <a href="#anchor1">
            <li class="tech-list-li" id="tech-list-li">회사소개</li></a
          >
          <a href="#anchor2">
            <li class="tech-list-li" id="tech-list-li">개요</li></a
          >
          <a href="#anchor3">
            <li class="tech-list-li" id="tech-list-li">과제</li>
          </a>
          <a href="#anchor4">
            <li class="tech-list-li" id="tech-list-li">해결방법</li></a
          >
          <a href="#anchor5">
            <li class="tech-list-li" id="tech-list-li">적용 결과</li>
          </a>
        </ul>
        <div class="tech-contents">
          <div>
            <div class="tech-img-wrap">
              <img class="tech-img" src="../../img/usecase_carrot.png" alt="" />
            </div>
            <p class="tech-title" id="anchor1">회사소개</p>
            <p class="tech-contents-text">
              캐롯손해보험은 국내 최초 디지털 손해보험사로서 기술과 데이터를
              기반으로 새로운 상품과 서비스를 출시하며 보험을 재정의하고 있으며,
              인슈어테크 플랫폼으로 빠르게 성장하고 있습니다. 자동차 보험에서는
              주행거리별 보험에 적극적으로 참여하고 있습니다.
            </p>
            <p class="tech-title" id="anchor2">개요</p>
            <p class="tech-contents-text">
              마크베이스의 안정적인 클러스터 운영 덕분에 IoT 디바이스를 사용하는
              캐롯 보험의 마일리지 보험은 가입자의 차량 운행 정보를 실시간으로
              수집하고 이를 기반으로 보험료를 부과할 수 있습니다.
            </p>
            <p class="tech-title" id="anchor3">과제</p>
            <p class="tech-contents-text">
              차량 시가잭에 IoT 제품을 설치해 차량 주행거리를 측정하고
              주행거리에 따라 보험료를 부과하기 위해서는 차량 운행 정보에 대한
              실시간 데이터와 가입자 수가 증가해도 안정적으로 수집할 수 있는
              시스템 구축이 필요했습니다.
            </p>
            <p class="tech-title" id="anchor4">해결방법</p>
            <p class="tech-contents-text">
              데이터 처리를 위해 클라우드 인스턴스를 사용했고, 3개의 인스턴스를
              사용해 마크베이스 클러스터를 구축했습니다.
            </p>
            <p class="tech-contents-text">
              마스터 노드와 데이터 노드 모두 이중화해 단일 장애 지점(SPOF)을
              방지하고 장애 발생 시 자동 페일오버가 가능하도록 구성했으며, 365일
              24시간 안정적인 서비스를 보장하기 위해 HA와 스케일아웃도
              지원했습니다.
            </p>
            <p class="tech-title" id="anchor5">적용 결과</p>
            <p class="tech-contents-text">
              서비스 초기 10만 명 미만이었던 가입자 수는 현재 80만 명으로
              증가했으며, 안정적인 클러스터 운영으로 가입자의 차량 운행 정보를
              실시간으로 수집하고 이를 기반으로 보험료를 부과할 수 있게
              되었습니다.
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</section>
{{< home_footer_blog_kr >}}
