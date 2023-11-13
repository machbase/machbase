---
title: Use Case
description: "롯데칠성 음료는 탄산음료, 차, 과일주스 등 다양한 제품을 생산하는 비알코올 음료 제조업체입니다."
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
        <h4 class="blog-title">[Machbase Use Case]제조업 - 롯데칠성</h4>
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
              <img class="tech-img" src="../../img/uscase_lotte.png" alt="" />
            </div>
            <p class="tech-contents-link-text">
              Machbase solution Architecture
            </p>
            <p class="tech-title" id="anchor1">회사소개</p>
            <p class="tech-contents-text">
              롯데칠성 음료는 탄산음료, 차, 과일주스 등 다양한 제품을 생산하는
              비알코올 음료 제조업체입니다.
            </p>
            <p class="tech-title" id="anchor2">개요</p>
            <p class="tech-contents-text">
              설비 알람 이력을 MS-SQL로만 저장하던 SCADA 시스템을 초당 20만 건의
              데이터를 실시간으로 수집, 저장, 검색할 수 있는 시스템으로
              전환했습니다.
            </p>
            <p class="tech-title" id="anchor3">Reason for Selection</p>
            <p class="tech-contents-text">
              생산 공정 장비의 모든 태그 데이터를 수집하기 위해서는 초당 20만
              건의 데이터를 실시간으로 수집하고 저장하는 것은 물론 주기적인
              백업과 백업된 데이터의 즉각적인 검색이 필요했습니다.
            </p>
            <p class="tech-title" id="anchor4">해결방법</p>
            <p class="tech-contents-text">
              SSD 디스크의 용량 한계로 인해 과거 데이터는 HDD 디스크에 백업하여
              저장하고, 필요시 Machbase TSDB의 마운트 기능을 사용하여 운영 중인
              DB에 즉시 연결하여 복원 프로세스 없이 데이터를 검색합니다.
            </p>
            <p class="tech-title" id="anchor5">적용 결과</p>
            <p class="tech-contents-text">
              시계열 데이터베이스에 저장된 데이터를 JDBC 또는 REST API를 통해
              추출하여 장기적인 추세 분석과 품질 원인 분석 등을 위해 R, Python,
              Grafana, Tableau 등의 데이터 분석 도구를 활용하였습니다.
            </p>
            <p class="tech-contents-text">
              생산 공정에서 발생하는 전체 데이터를 저비용으로 저장, 분석할 수
              있게 되었고 결함이 줄어들고 생산성 향상을 기대할 수 있었습니다.
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</section>
{{< home_footer_blog_kr >}}
