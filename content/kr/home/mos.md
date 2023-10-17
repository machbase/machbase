---
---

<head>
  <link rel="stylesheet" type="text/css" href="../css/common.css" />
  <link rel="stylesheet" type="text/css" href="../css/style.css" />
</head>
<body>
 <nav>
  <div class="homepage-menu-wrap">
    <div class="menu-left">
      <ul class="menu-left-ul">
        <li class="menu-logo">
          <a href="/kr/home"
            ><img src="../img/logo_machbase.png" alt=""
          /></a>
        </li>
        <li class="menu-a products-menu-wrap" id="productsMenuWrap">
          <div>
            <a
              class="menu_active_border"
              id="menuActiveBorder"
              href="/kr/home/tsdb"
              >Products</a
            >
            <div class="dropdown" id="dropdown">
              <a class="dropdown-link" href="/kr/home/tsdb">TSDB</a>
              <a class="dropdown-link" href="/kr/home/mos">MOS</a>
              <a
                class="dropdown-link"
                href="https://www.cems.ai/"
                target="_blank"
                >CEMS</a
              >
            </div>
          </div>
        </li>
        <li class="menu-a"><a href="/kr/home/blog">Blog</a></li>
        <li class="menu-a"><a href="/kr/home/customers">Customers</a></li>
        <li class="menu-a"><a href="/kr/home/usecase">Use Case</a></li>
        <li class="menu-a"><a href="/kr/home/company">Company</a></li>
      </ul>
    </div>
    <div class="menu-right">
      <ul class="menu-right-ul">
        <li class="menu-a docs-menu-wrap" id="docsMenuWrap">
          <a href=""
            ><div>
              <a class="menu_active_border" id="menuActiveBorder" href="/"
                >Document</a
              >
              <div class="dropdown-docs" id="dropdownDocs">
                <a class="dropdown-link" href="/neo">Neo</a>
                <a class="dropdown-link" href="/dbms">Classic</a>
              </div>
            </div></a
          >
        </li>
        <li class="menu-a"><a href="/kr/home/download">Download</a></li>
        <li class="menu-a">
          <a href="https://support.machbase.com/hc/en-us">Support</a>
        </li>
        <li class="menu-a"><a href="/kr/home/contactus">Contact US</a></li>
      </ul>
    </div>
  </div>
</nav>
<nav class="tablet-menu-wrap">
  <a href="/kr/home"><img src="../img/logo_machbase.png" alt="" /></a>
  <div class="tablet-menu-icon">
    <div class="tablet-bar"></div>
    <div class="tablet-bar"></div>
    <div class="tablet-bar"></div>
  </div>
  <div class="tablet-menu">
    <ul>
      <div class="tablet-menu-title">
        <a class="tablet-logo" href="/kr/home"
          ><img src="../img/logo_machbase.png" alt=""
        /></a>
      </div>
      <li></li>
      <li class="products-toggle">Products</li>
      <li>
        <div class="products-content">
          <div class="products-sub"><a href="/kr/home/tsdb">TSDB</a></div>
          <div class="products-num"><a href="/kr/home/mos">MOS</a></div>
          <div class="products-cems">
            <a href="https://www.cems.ai/">CEMS</a>
          </div>
        </div>
      </li>
      <li><a href="/kr/home/blog">Blog</a></li>
      <li><a href="/kr/home/customers">Customers</a></li>
      <li><a href="/kr/home/usecase">Use Cases</a></li>
      <li><a href="/kr/home/company">Company</a></li>
      <li class="docs-toggle">Document</li>
      <li>
        <div class="docs-content">
          <div class="docs-sub"><a href="/neo">Neo</a></div>
          <div class="docs-num"><a href="/dbms">Classic</a></div>
        </div>
      </li>
      <li><a href="/kr/home/download">Download</a></li>
      <li><a href="https://support.machbase.com/hc/en-us">Support</a></li>
      <li><a href="/kr/home/download">Contact US</a></li>
    </ul>
  </div>
</nav>
  <section class="product_sction0 section0">
    <div>
      <h1 class="sub_page_title">Products</h1>
      <p class="sub_page_titletext">
        “ Discover the top DBMS suites for edge computing and take your data
        processing to the next level ”
      </p>
    </div>
  </section>
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
          이로써 불량률 감소/ 품질 향상/ 생산성 향상/ 제품 생산 이력 추적 가능/
          고객 클레임 감소/ 원가 절감을 모두 달성할 수 있게 되어 최종적으로는
          기업의 이익과 가치를 상승시킬 수 있게 될 것입니다.
        </p>
      </div>
    </div>
  </section>
  <section class="neo_scroll_map_wrap">
    <div class="neo_scroll_map">
      <div ref="scrollLeft" class="mos_scroll_left">
        <div class="neo_scroll"><img src="../img/mos.png"></div>
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
                    다양한 설비의 센서 데이터를 TSDB에 초단위로 수집하고 고객의
                    생산 관련 Legacy System과 ERP/MES 등과 연계된 데이터를
                    RDBMS로 수집
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
                  국제공인 성능평가 세계 1위 마크베이스의 시계열 데이터베이스를
                  사용하여 센서로부터 나오는 초당 수십만건 이상의 데이터가 수집,
                  저장, 입출력이 가능하도록 구성
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
                  가능하도록 데이터 연결 작업을 수행하고, 향후 생산, 품질, 설비
                  등의 표준화된 AAS 정보가 반영 되게 연계 기반을 구축함
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
            <a target="_blank" href="https://neo.machbase.com/"
              ><button class="next-navi-btn">Document</button></a
            >
          </div>
        </div>
      </div>
    </div>
  </section>
</body>
<footer>
  <div class="footer_inner">
    <div class="footer-logo">
      <img class="footer-logo-img" src="../img/machbase-logo-w.png" />
      <a href="/kr/home/contactus">
        <button class="contactus">고객 문의</button>
      </a>
    </div>
    <div>
      <p class="footertext">
        3003 North First street #206 San Jose, CA 95134. USA
      </p>
    </div>
    <div class="footer_box">
      <div class="footer_text">
        <p>MACHBASE.COM | sales@machbase.com | support@machbase.com</p>
        <p class="footer_margin_top"></p>
      </div>
      <div class="sns">
        <div>
          <a href="https://twitter.com/machbase" target="_blank"
            ><img class="sns-img" src="../img/twitter.png"
          /></a>
        </div>
        <div>
          <a href="https://github.com/machbase" target="_blank"
            ><img class="sns-img" src="../img/github.png"
          /></a>
        </div>
        <div>
          <a href="https://www.linkedin.com/company/machbase" target="_blank"
            ><img class="sns-img" src="../img/linkedin.png"
          /></a>
        </div>
        <div>
          <a href="https://www.facebook.com/MACHBASE/" target="_blank"
            ><img class="sns-img" src="../img/facebook.png"
          /></a>
        </div>
        <div>
          <a href="https://www.slideshare.net/machbase" target="_blank"
            ><img class="sns-img" src="../img/slideshare.png"
          /></a>
        </div>
        <div>
          <a href="https://blog.naver.com/machbasekr" target="_blank"
            ><img class="sns-img" src="../img/naver.png"
          /></a>
        </div>
      </div>
    </div>
  </div>
  <div class="footer_tablet_inner">
    <div class="logo">
      <img class="footer-logo-img" src="../img/machbase-logo-w.png" />
    </div>
    <div>
      <p class="footertext">
        3003 North First street #206 San Jose, CA 95134. USA
      </p>
    </div>
    <div class="footer_box">
      <div class="footer_text">
        <p>MACHBASE.COM | sales@machbase.com | support@machbase.com</p>
      </div>
      <div class="sns">
        <div>
          <a href="https://twitter.com/machbase" target="_blank"
            ><img class="sns-img" src="../img/twitter.png"
          /></a>
        </div>
        <div>
          <a href="https://github.com/machbase" target="_blank"
            ><img class="sns-img" src="../img/github.png"
          /></a>
        </div>
        <div>
          <a href="https://www.linkedin.com/company/machbase" target="_blank"
            ><img class="sns-img" src="../img/linkedin.png"
          /></a>
        </div>
        <div>
          <a href="https://www.facebook.com/MACHBASE/" target="_blank"
            ><img class="sns-img" src="../img/facebook.png"
          /></a>
        </div>
        <div>
          <a href="https://www.slideshare.net/machbase" target="_blank"
            ><img class="sns-img" src="../img/slideshare.png"
          /></a>
        </div>
        <div>
          <a href="https://blog.naver.com/machbasekr" target="_blank"
            ><img class="sns-img" src="../img/naver.png"
          /></a>
        </div>
      </div>
      <a href="/kr/home/contactus">
        <button class="contactus">고객 문의</button>
      </a>
    </div>
  </div>
  <div class="machbase_right">
    <p>@2023 MACHBASE All rights reserved.</p>
  </div>
</footer>
<script>
  //drop down menu
  const productsMenuWrap = document.getElementById("productsMenuWrap");
  const docsMenuWrap = document.getElementById("docsMenuWrap");
  const dropdown = document.getElementById("dropdown");
  dropdown.style.display = "none";
  productsMenuWrap.addEventListener("mouseover", function () {
    dropdown.style.display = "block";
  });
  productsMenuWrap.addEventListener("mouseout", function () {
    dropdown.style.display = "none";
  });
  docsMenuWrap.addEventListener("mouseover", function () {
    dropdownDocs.style.display = "block";
  });
  docsMenuWrap.addEventListener("mouseout", function () {
    dropdownDocs.style.display = "none";
  });
//tablet menu
  const menuIcon = document.querySelector(".tablet-menu-icon");
  const tabletMenu = document.querySelector(".tablet-menu");
  const productsToggle = document.querySelector(".products-toggle");
  const productsSub = document.querySelector(".products-sub");
  const productsNum = document.querySelector(".products-num");
  const productsCems = document.querySelector(".products-cems");
  const docsToggle = document.querySelector(".docs-toggle");
  const docsSub = document.querySelector(".docs-sub");
  const docsNum = document.querySelector(".docs-num");
  menuIcon.addEventListener("click", () => {
    tabletMenu.classList.toggle("show");
    menuIcon.classList.toggle("is-active");
  });
  productsToggle.addEventListener("click", () => {
    productsSub.classList.toggle("show");
    productsNum.classList.toggle("show");
    productsCems.classList.toggle("show");
  });
  docsToggle.addEventListener("click", () => {
    docsSub.classList.toggle("show");
    docsNum.classList.toggle("show");
  });
</script>
