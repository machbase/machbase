---
toc: false
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
            <a href="/kr/home"><img src="../img/logo_machbase.png" alt="" /></a>
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
                <a class="menu_active_border" id="menuActiveBorder" href=""
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
          <li class="menu-a">
            <select id="languageSelector" onchange="changeLanguage()">
              <option value="kr">한국어</option>
              <option value="en">English</option>
            </select>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <nav class="tablet-menu-wrap">
    <a href="/kr/home"><img src="../img/logo_machbase.png" alt="" /></a>
    <div class="hamberger-right">
      <select id="languageSelector2" onchange="changeLanguage2()">
        <option value="kr">한국어</option>
        <option value="en">English</option>
      </select>
      <div class="tablet-menu-icon">
        <div class="tablet-bar"></div>
        <div class="tablet-bar"></div>
        <div class="tablet-bar"></div>
      </div>
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
              <a href="https://www.cems.ai/" target="_blank">CEMS</a>
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
            <div class="docs-sub"><a href="/neo" target="_blank">Neo</a></div>
            <div class="docs-num">
              <a href="/dbms" target="_blank">Classic</a>
            </div>
          </div>
        </li>
        <li><a href="/kr/home/download">Download</a></li>
        <li><a href="https://support.machbase.com/hc/en-us">Support</a></li>
        <li><a href="/kr/home/download">Contact US</a></li>
        <li></li>
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
      <h4 class="sub_title company-margin-top">Time Series Database</h4>
      <div class="bar"><img src="../img/bar.png" /></div>
    </div>
    <div class="product-sub-titlebox">
      <div>
        <p class="product-sub-title-text">
          Machbase TSDB(시계열 데이터베이스)는 최소한의 설치 공간으로 최고의
          성능을 구현하는 세계에서 가장 빠른 시계열 데이터베이스입니다.
          <a href="/kr/home/company#performance" class="products-tpc-link"
            >글로벌 성능 평가 기관인 TPC(Transaction Processing Performance
            Council)가 주관하는 성능 평가에서 2019년부터 'TPCx-IoT' 분야 1위를
            차지하며 이 분야 국제 표준으로 등재되어 있습니다.</a
          ><br /><br />
          또한 라즈베리 파이와 같이 리소스가 제한된 소형 서버부터 수평적으로
          확장되는 클러스터까지 확장성이 필요한 환경에 이상적인
          솔루션입니다.Machbase를 기반으로 구축된 Machbase Neo는 산업 IoT 구축에
          필요한 중요한 기능을 더 포함합니다. IoT 센서에서 직접 데이터를
          전송하기 위한 MQTT, 애플리케이션에서 데이터를 검색하기 위한 HTTP를
          통한 SQL 등 다양한 프로토콜을 통해 쿼리 데이터를 수집하고 처리합니다.
        </p>
      </div>
    </div>
  </section>
  <section class="neo_scroll_map_wrap">
    <div class="neo_scroll_map">
      <div ref="scrollLeft" class="neo_scroll_left">
        <div class="neo_scroll"><img src="../img/tsdb.png" /></div>
      </div>
      <div class="neo_scroll_right">
        <div class="neo_scorll_box_wrap">
          <div class="classic_sub_wrap">
            <div class="classic_sub">
              <div class="scroll-title-wrap">
                <p>클래식의 특징</p>
              </div>
              <div class="scroll-contents-wrap">
                <p class="scroll-content">
                  마크베이스 TSDB 엔진은 C언어로 작성되었기 때문에 성능이 매우
                  빠르고 데이터 처리를 위한 CPU와 메모리 사용 효율이 매우
                  높습니다. 특히, 실시간으로 폭증하는 IoT 데이터를 처리하기 위해
                  혁신적인 다차원 인덱스 구조를 고안해냈는데, 이것이 Machbase
                  성능의 핵심입니다. 이러한 성능과 자원 효율성 특성으로 인해
                  소규모 엣지 디바이스의 고속 데이터베이스 및 엣지 컴퓨팅의 핵심
                  데이터 처리 엔진으로 활용되고 있습니다.
                </p>
              </div>
              <div class="scroll-sub-title-wrap">
                <p class="scroll-sub-title">Machbase의 주요 성능</p>
                <p class="scroll-sub-text">수집 관점</p>
                <ul>
                  <li>
                    엣지 디바이스(ARM 2코어): 초당 최대 500,000개의 레코드 수집
                  </li>
                  <li>단일 서버(INTEL 8코어): 최대 2,500,000 rec/sec</li>
                  <li>클러스터(16노드): 최대 100,000,000 rec/sec</li>
                </ul>
                <p class="scroll-sub-text">추출 관점</p>
                <ul>
                  <li>
                    4,000억 개의 데이터 저장소에서 10,000개의 무작위 시간 범위를
                    추출하는 데 0.1초 소요
                  </li>
                </ul>
                <p class="scroll-sub-text">압축 관점</p>
                <ul>
                  <li>4TB 저장 공간: 약 1조 개의 레코드</li>
                </ul>
              </div>
              <span>
                <a
                  class="main_why_more product-margin-bottom"
                  href="https://docs.machbase.com/en/"
                  target="_blank"
                >
                  View More
                </a>
              </span>
            </div>
          </div>
          <div ref="classicSubWrapRef" class="neo_sub_wrap" id="scroll1">
            <div class="neo_sub">
              <div class="scroll-title-wrap">
                <p>네오의 구성</p>
              </div>
              <div class="scroll-sub-title-wrap">
                <p class="scroll-sub-title">
                  Machbase Neo에는 이하의 요소가 내장되어 있습니다.
                </p>
                <ul class="product-margin-bottom">
                  <a
                    class="product-link"
                    href="https://neo.machbase.com/docs/api-mqtt/"
                    target="_blank"
                    ><li>IoT 데이터를 위한 MQTT 서버</li></a
                  >
                  <a
                    class="product-link"
                    href="https://neo.machbase.com/docs/api-http/"
                    target="_blank"
                    ><li>
                      Rest API를 위한 HTTP 프로토콜을 지원하는 웹 서버
                    </li></a
                  >
                  <a
                    class="product-link"
                    href="https://neo.machbase.com/docs/api-grpc/"
                    target="_blank"
                    ><li>
                      Google에서 개발한 고성능, 고화질, 언어 중립적인 원격
                      프로시저 호출 프레임워크인 gRPC 서버
                    </li></a
                  >
                  <a
                    class="product-link"
                    href="https://neo.machbase.com/docs/operations/13.ssh-access/"
                    target="_blank"
                    ><li>
                      안전한 데이터 및 조작 보안을 위한 SSH 서버 - 네 가지 필수
                      기능이 모두 통합되어 있습니다.
                    </li></a
                  >
                </ul>
                <div class="scroll-contents-wrap">
                  <p class="scroll-content">
                    따라서 사용자는 Neo를 실행하기만 하면 복잡한 과정 없이 위의
                    모든 기능을 사용할 수 있습니다. 또한, 라인 프로토콜을
                    지원하여 데이터 수집을 위한 대표적인 오픈소스 제품인
                    Telegraf와 통합이 가능하며, 오픈소스 시계열 DBMS인 InfluxDB
                    애플리케이션을 그대로 사용할 수 있어 개발자의 선택의 폭이
                    크게 넓어졌습니다. 또한 누구나 깃허브를 통해 모든 소스
                    코드를 다운로드하여 테스트 및 검증할 수 있습니다.
                  </p>
                  <a
                    class="main_why_more product-margin-bottom"
                    href="https://neo.machbase.com/"
                    target="_blank"
                  >
                    View More<ArrowSvg />
                  </a>
                </div>
              </div>
            </div>
          </div>
          <div ref="neoSubWrapRef" class="neo_use_sub_wrap" id="scroll2">
            <div class="neo_use_sub product-link-bottom">
              <div class="scroll-title-wrap">
                <p>네오의 특징</p>
              </div>
              <div class="scroll-contents-wrap">
                <p class="scroll-content">
                  네오 에디션은 불필요한 기능 개발에 소요되는 리소스를 절약하고
                  핵심 서비스 모듈에 리소스를 집중하기 위해 개발되었습니다.
                </p>
              </div>
              <div class="scroll-sub-title-wrap">
                <p class="scroll-sub-title">주요 기능은 다음과 같습니다.</p>
                <p class="scroll-sub-item"># 편하고, 쉬운 인터페이스</p>
                <ul>
                  <li>웹 브라우저 기반의 인터페이스 제공</li>
                  <li>단일 실행 화일로 설치/운용이 매우 매우 간편</li>
                </ul>
                <p class="scroll-sub-item">#다양한 운영체제 지원</p>
                <ul>
                  <li>리눅스, 윈도우즈, 맥(intel/M1)</li>
                </ul>
                <p class="scroll-sub-item"># 기존 솔루션과의 유연한 연동</p>
                <ul>
                  <li>Grafana plug-in</li>
                  <li>Telegraf, 타블로 등</li>
                </ul>
                <p class="scroll-sub-item"># 내장 브로커 지원</p>
                <ul>
                  <li>거기다가 다양한 브로커를 더 지원하고!</li>
                  <li>데이터 유실/성능 걱정 제거</li>
                </ul>
                <p class="scroll-sub-item">
                  # 설정 변경으로 소규모 에지 활용 가능
                </p>
                <ul>
                  <li>라즈베리파이, 오드로이드 등</li>
                </ul>
                <p class="scroll-sub-item"># 표준 보안 기능 지원</p>
                <ul>
                  <li>머리 아픈 보안 문제를 저 멀리!</li>
                  <li>TLS 기반 X.509 지원, SSH 콘솔 지원</li>
                </ul>
                <p class="scroll-sub-item"># Worksheet 기능 제공</p>
                <ul>
                  <li>살아있는 사용자 교육 매뉴얼, 튜토리얼 직접 생성, 공유</li>
                </ul>
                <p class="scroll-sub-item">
                  # 강력한 자체 데이터 변환 언어(TQL)을 제공
                </p>
                <ul>
                  <li>별도 코딩 없이 Restful API를 즉시 구현 및 서비스 가능</li>
                  <li>FFT 함수 등의 특별 용도의 분석 함수 제공</li>
                </ul>
                <p class="scroll-sub-item"># 내장 스크립트 언어 제공</p>
                <ul>
                  <li>TQL을 통한 스크립트 언어 활용</li>
                  <li>
                    외부 데이터 소스와의 직접 연동 및 데이터 변환 가능(sqlite,
                    mysql, postgreSQL 등)
                  </li>
                </ul>
                <p class="scroll-sub-item"># 시각화 기능 제공</p>
                <ul>
                  <li>실시간으로 입력되는 데이터 즉시 확인</li>
                  <li>SQL, Chart 등을 시각적으로 분석</li>
                </ul>
                <p class="scroll-sub-item"># 내장 스케쥴러</p>
                <ul>
                  <li>엔진 레벨 반복 업무 자동화 기능 제공</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  <section>
    <h4 class="sub_title company-margin-top">Neo Interface</h4>
    <div class="bar"><img src="../img/bar.png" /></div>
    <div class="neo_interface_wrap">
      <img class="neo_interface" src="../img/neo_interface.png" alt="" />
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
      <p class="footertext">서울시 강남구 테헤란로 20길 10, 3M 타워, 9층</p>
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
    <select id="languageSelector" onchange="changeLanguage()">
      <option value="kr">한국어</option>
      <option value="en">English</option>
    </select>
  </div>
  <div class="footer_tablet_inner">
    <div class="footer-logo">
      <img class="footer-logo-img" src="../img/machbase-logo-w.png" />
    </div>
    <div>
      <p class="footertext">서울시 강남구 테헤란로 20길 10, 3M 타워, 9층</p>
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
  function changeLanguage() {
    var languageSelector = document.getElementById("languageSelector");
    var selectedLanguage = languageSelector.value;
    if (selectedLanguage !== "kr") {
      let locationPath = location.pathname.split("/");
      locationPath.splice(1, 1);
      location.href = location.origin + locationPath.join("/");
    }
  }
  function changeLanguage2() {
    var languageSelector = document.getElementById("languageSelector2");
    var selectedLanguage = languageSelector.value;
    if (selectedLanguage !== "kr") {
      let locationPath = location.pathname.split("/");
      locationPath.splice(1, 1);
      location.href = location.origin + locationPath.join("/");
    }
  }
  window.addEventListener("load", function () {
    var elementsWithDarkClass = document.querySelectorAll(".dark");
    for (var i = 0; i < elementsWithDarkClass.length; i++) {
      elementsWithDarkClass[i].classList.remove("dark");
    }
    var elementsWithColorScheme = document.querySelectorAll(
      "[style*='color-scheme: dark;']"
    );
    for (var i = 0; i < elementsWithColorScheme.length; i++) {
      elementsWithColorScheme[i].removeAttribute("style");
    }
  });
</script>
