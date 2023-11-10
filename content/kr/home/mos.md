---
title: Products
description: "Machbase MOS (Manufacturing Optimization Suite)는 설비상태 데이터와 제품품질 정보 데이터의 동기화를 통해 실시간 공정 모니터링 및 설비 및 품질의 이상 파악이 가능하며, 향후 예지보전까지도 가능한 최고의 솔루션입니다."
images:
  - /namecard/og_img.jpg
---

<head>
  <link rel="stylesheet" type="text/css" href="../css/common.css" />
  <link rel="stylesheet" type="text/css" href="../css/style.css" />
</head>
<body>
  {{< home_menu_sub_kr >}}
  <section class="product_sction0 section0">
    <div>
      <h2 class="sub_page_title">Products</h2>
      <p class="sub_page_titletext">
        “ Discover the top DBMS suites for edge computing and take your data
        processing to the next level ”
      </p>
    </div>
  </section>
  <div class="product-inner">
    <section class="section2 main_section2">
      <div>
        <h4 class="sub_title company-margin-top">MOS</h4>
        <div class="bar"><img src="../img/bar.png" /></div>
      </div>
      <div class="product-sub-titlebox">
        <div>
          <p class="product-sub-title-text">
            Machbase MOS (Manufacturing Optimization Suite)는 설비상태 데이터와
            제품품질 정보 데이터의 동기화를 통해 실시간 공정 모니터링 및 설비 및
            품질의 이상 파악이 가능하며, 향후 예지보전까지도 가능한 최고의
            솔루션입니다.
            <br /><br />
            기업은 MOS를 통해 설비단의 센서 정보와 생산제품을 연계한 품질 유지
            모니터링뿐 아니라 품질문제 발생 시점 추적, 원인 분석과 활용을 위한
            현실적 빅데이터를 구축할수 있습니다.
            <br /><br />
            이로써 불량률 감소/ 품질 향상/ 생산성 향상/ 제품 생산 이력 추적
            가능/ 고객 클레임 감소/ 원가 절감을 모두 달성할 수 있게 되어
            최종적으로는 기업의 이익과 가치를 상승시킬 수 있게 될 것입니다.
          </p>
        </div>
      </div>
    </section>
    <section class="neo_scroll_map_wrap">
      <div class="neo_scroll_map">
        <div ref="scrollLeft" class="mos_scroll_left">
          <div class="neo_scroll"><img src="../img/mos.png" /></div>
        </div>
        <div class="neo_scroll_right">
          <div class="neo_scorll_box_wrap">
            <div class="data_sub_wrap">
              <div class="classic_sub">
                <div class="scroll-title-wrap">
                  <p>데이터 수집 및 연동</p>
                </div>
                <div class="scroll-sub-title-wrap">
                  <p class="scroll-sub-title">센서데이터(to TSDB)</p>
                  <!-- <p class="scroll-sub-text">In ingestion point of view</p> -->
                  <ul class="tech-margin-bottom">
                    <li>OPC-UA/DA</li>
                    <li>MQTT Pub/Sub</li>
                    <li>Modbus RTU/TCP</li>
                    <li>Melsec</li>
                    <li>Simatic</li>
                    <li>Ethernet</li>
                  </ul>
                  <p class="scroll-sub-title">제품정보데이터(to RDBMS)</p>
                  <ul>
                    <li>Portal</li>
                    <li>ERP</li>
                    <li>MES/POP</li>
                    <li>QMS</li>
                    <li>Legacy</li>
                  </ul>
                  <div class="scroll-contents-wrap">
                    <p class="mos-scroll-content">
                      다양한 설비의 센서 데이터를 TSDB에 초단위로 수집하고
                      고객의 생산 관련 Legacy System과 ERP/MES 등과 연계된
                      데이터를 RDBMS로 수집
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div ref="classicSubWrapRef" class="database_sub_wrap" id="scroll1">
              <div class="neo_sub">
                <div class="scroll-title-wrap">
                  <p>데이터베이스 구성</p>
                </div>
                <div class="scroll-sub-title-wrap">
                  <p class="scroll-sub-title">TSDB</p>
                  <p class="scroll-content">
                    국제공인 성능평가 세계 1위 마크베이스의 시계열
                    데이터베이스를 사용하여 센서로부터 나오는 초당 수십만건
                    이상의 데이터가 수집, 저장, 입출력이 가능하도록 구성
                  </p>
                  <p class="scroll-sub-title">RDBMS</p>
                  <p class="scroll-content">
                    생산 공정상 필요한 생산품 정보, 설비 정보, 작업지시정보 등을
                    Legacy System과 연동하여 관리를 할 수 있도록 RDBMS 구성
                    (RDBMS는 기업의 Needs에 따라 구성이 가능)
                  </p>
                  <p class="scroll-sub-title">AAS</p>
                  <p class="scroll-content">
                    인더스트리 4.0 데이터 표준 체계인 AAS(Asset Administration
                    Shell)를 기반으로 설비/Tag 항목별 생산, 품질, 설비 등의
                    분류체계 속성을 정의하여 관련 부서들 간에 쉽게 상호 참조가
                    가능하도록 데이터 연결 작업을 수행하고, 향후 생산, 품질,
                    설비 등의 표준화된 AAS 정보가 반영 되게 연계 기반을 구축함
                  </p>
                </div>
              </div>
            </div>
            <div ref="neoSubWrapRef" class="feature_sub_wrap" id="scroll2">
              <div class="neo_use_sub product-link-bottom">
                <div class="scroll-title-wrap">
                  <p>대시보드 및 주요 기능</p>
                </div>
                <div class="scroll-sub-title-wrap">
                  <p class="scroll-sub-title">Monitoring</p>
                  <ul class="tech-margin-bottom">
                    <li>Tag Monitoring</li>
                    <li>품질조건 Monitoring</li>
                    <li>설비상태 Monitoring</li>
                    <li>이상발생 시점 추적 등</li>
                  </ul>
                  <p class="scroll-sub-title">설비/품질</p>
                  <ul class="tech-margin-bottom">
                    <li>공정능력비교(CpK)</li>
                    <li>품질규격 이탈현황</li>
                    <li>Raw Data 검색</li>
                    <li>생산실적</li>
                  </ul>
                  <p class="scroll-sub-title">기준정보</p>
                  <ul class="tech-margin-bottom">
                    <li>Item 관리</li>
                    <li>Asset 관리</li>
                    <li>Asset Hierarchy(AAS)</li>
                    <li>Bill of Process(BOP)</li>
                  </ul>
                  <p class="scroll-sub-title">System</p>
                  <ul class="tech-margin-bottom">
                    <li>Lookup(공통코드)</li>
                    <li>조직/사용자/권한</li>
                    <li>시스템 설정/메뉴 관리 등</li>
                  </ul>
                  <!-- <p class="scroll-sub-title">예지/분석</p>
                    <ul>
                        <li>AI Module를 활용한 분석 및 예지 (Optional)</li>
                    </ul> -->
                  <p class="scroll-content">
                    Machbase MOS는 실시간 데이터 수집-저장-가공- 분석 및 시각화,
                    주기적 리포트 출력은 물론이고 설비의 이상 징후를 종합적으로
                    수집하고 원인을 파악하며, 로트별 생산 실적을 추적하고 공정을
                    실시간으로 모니터링하여 품질 이상을 예측할 수 있는 기능을
                    제공합니다.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
  <section>
    <h4 class="sub_title company-margin-top">MOS Interface</h4>
    <div class="bar"><img src="../img/bar.png" /></div>
    <div class="neo_interface_wrap">
      <img
        class="neo_interface tech-margin-bottom"
        src="../img/Mos-En.png"
        alt=""
      />
      <img class="neo_interface" src="../img/Kpi-En.png" alt="" />
    </div>
  </section>
  <section>
    <div class="next-navi_wrap">
      <div class="next-navi">
        <div class="next-navi-wrap">
          <div class="next-navi-text-wrap">
            <p class="next-navi-text">Ready to start in an instant</p>
          </div>
          <div class="next-navi-btn-wrap">
            <button
              onclick="location.href='/kr/home/download'"
              class="next-navi-btn"
            >
              Get Machbase
            </button>
            <a href="https://machbase.com/neo"
              ><button class="next-navi-btn">Document</button></a
            >
          </div>
        </div>
      </div>
    </div>
  </section>
</body>
{{< home_footer_sub_kr >}}
<script>
  //change lang
  let language;
  let storageData = sessionStorage.getItem("lang");
  if (storageData) {
    language = storageData;
  } else {
    var userLang = navigator.language || navigator.userLanguage;
    if (userLang === "ko") {
      sessionStorage.setItem("lang", userLang);
      language = "kr";
    } else {
      sessionStorage.setItem("lang", "en");
      language = "en";
      let locationPath = location.pathname.split("/");
      locationPath.splice(1, 1);
      location.href = location.origin + locationPath.join("/");
    }
  }
</script>
