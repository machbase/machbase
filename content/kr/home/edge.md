---
title: Tech Paper
description: "엣지 컴퓨팅과 시계열 데이터베이스"
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
      <h2 class="sub_page_title">Tech Paper</h2>
      <p class="sub_page_titletext">
        “ Discover the top DBMS suites for edge computing and take your data
        processing to the next level ”
      </p>
    </div>
  </section>
  <section>
    <div class="tech-inner">
      <h4 class="sub_title main_margin_top">
        엣지 컴퓨팅과 시계열 데이터베이스
      </h4>
      <div class="bar"><img src="../img/bar.png" /></div>
      <div class="tech-contents">
        <div>
          <div class="tech-title">왜 엣지 컴퓨팅인가?</div>
          <p class="tech-contents-text">
            최근 몇 년 동안 엣지 컴퓨팅은 데이터를 처리하고 관리하는 방식을
            변화시키는 중추적인 기술 개념으로 부상했습니다. 이러한 패러다임의
            변화는 사물 인터넷(IoT) 디바이스의 확산과 실시간 로컬 데이터 처리에
            대한 필요성 증가로 인해 그 중요성이 더욱 커지고 있습니다. 엣지
            컴퓨팅은 분석을 위해 모든 데이터를 중앙 집중식 클라우드 서버로
            전송하는 대신 네트워크의 '엣지'에서 데이터 소스에 더 가까운 곳에서
            데이터를 처리하는 방식을 말합니다. 이 접근 방식은 여러 가지 이점을
            제공하며, 여기서 전문 시계열 데이터베이스 엔진인 소프트웨어가 중요한
            역할을 합니다.
          </p>
          <p class="tech-contents-title">엣지 컴퓨팅의 중요성:</p>
          <ul class="tech-ul">
            <li>
              짧은 지연 시간 및 실시간 처리: 산업 자동화, 자율 주행 차량, 원격
              모니터링과 같이 실시간 의사 결정이 필요한 애플리케이션은 멀리
              떨어진 데이터 센터로 데이터를 전송할 때 발생하는 지연 시간을
              감당할 수 없습니다. 엣지 컴퓨팅은 데이터를 로컬에서 처리하여
              이러한 지연을 줄여 빠른 응답을 가능하게 합니다.
            </li>
            <li>
              대역폭 효율성: 대량의 원시 데이터를 중앙 집중식 클라우드 서버로
              전송하려면 상당한 대역폭이 필요합니다. 엣지 컴퓨팅은 관련성이 높고
              처리된 정보만 전송하여 전송되는 데이터의 양을 줄이고 네트워크
              사용량과 비용을 최적화합니다.
            </li>
            <li>
              개인정보 보호 및 보안: 엣지 컴퓨팅은 민감한 데이터를 로컬로
              유지하여 데이터 프라이버시 및 보안에 대한 우려를 해결합니다.
              따라서 퍼블릭 네트워크를 통한 민감한 정보 전송과 관련된 잠재적
              위험을 완화합니다.
            </li>
            <li>
              오프라인 기능: 엣지 컴퓨팅을 사용하면 클라우드 연결이 끊어진
              경우에도 디바이스가 자율적으로 작동할 수 있습니다. 이는 지속적인
              기능이 필수적인 시나리오에 매우 중요합니다.
            </li>
            <li>
              확장성: IoT 디바이스가 빠르게 성장함에 따라 중앙 집중식 클라우드
              처리가 병목 현상이 발생할 수 있습니다. 엣지 컴퓨팅은 처리 부하를
              분산하여 클라우드 리소스를 과도하게 사용하지 않고 확장성을
              보장합니다.
            </li>
          </ul>
        </div>
        <div>
          <div class="tech-title">
            엣지 컴퓨팅에서 시계열 데이터베이스 엔진의 역할
          </div>
          <p class="tech-contents-text">
            시간 경과에 따른 값을 기록하는 시계열 데이터는 온도 판독값, 주가,
            에너지 소비량 등 IoT 애플리케이션에서 널리 사용됩니다. 시계열
            데이터베이스 엔진은 이러한 데이터를 효율적으로 저장, 검색, 분석하는
            데 탁월합니다.
          </p>
          <p class="tech-contents-title">
            시계열 데이터베이스 엔진이 엣지 컴퓨팅에 기여하는 방식은 다음과
            같습니다:
          </p>
          <ul class="tech-ul">
            <li>
              데이터 저장 및 검색: 시계열 데이터베이스는 타임스탬프가 찍힌
              데이터의 대용량 저장 및 검색에 최적화되어 있습니다. 이를 통해
              엣지에서 의사결정을 내리는 데 중요한 과거 및 실시간 데이터에
              빠르게 액세스할 수 있습니다.
            </li>
            <li>
              집계 및 분석: 이러한 데이터베이스를 사용하면 리소스가 제한된
              환경에서도 시계열 데이터에 대한 복잡한 분석을 수행할 수 있습니다.
              집계, 다운샘플링, 통계 계산을 통해 의미 있는 인사이트를 얻을 수
              있습니다.
            </li>
            <li>
              압축: 엣지 기기의 저장 공간이 제한적인 경우가 많기 때문에 시계열
              데이터베이스는 데이터 압축 기술을 제공하여 제한된 환경에서 방대한
              양의 데이터를 효율적으로 저장할 수 있습니다.
            </li>
            <li>
              데이터 컨텍스트화: 시계열 데이터베이스를 사용하면 데이터를 관련
              메타데이터와 연결하여 컨텍스트화할 수 있습니다. 이러한 컨텍스트
              정보는 엣지 디바이스에서 수집된 데이터의 가치를 향상시킵니다.
            </li>
            <li>
              이벤트 트리거링: 시계열 데이터베이스는 이벤트 트리거링 메커니즘을
              지원하여 사전 정의된 조건에 따라 실시간 알림 및 조치를 가능하게
              함으로써 엣지 애플리케이션의 응답성을 직접적으로 향상시킬 수
              있습니다.
            </li>
          </ul>
          <p class="tech-contents-text">
            엣지 컴퓨팅의 부상은 IoT 디바이스의 확산과 효율적인 실시간 데이터
            처리의 필요성과 밀접한 관련이 있습니다. 시계열 데이터를 효율적으로
            관리하는 기능은 로컬화된 처리, 빠른 의사 결정, 최적화된 리소스
            사용을 가능하게 하는 엣지 컴퓨팅의 요구와 완벽하게 일치합니다.
            업계가 계속해서 엣지 컴퓨팅을 채택하고 활용함에 따라 시계열 DBMS는
            이러한 혁신적인 기술 트렌드를 실현하는 데 앞장서고 있습니다.
          </p>
        </div>
        <div>
          <div class="tech-title">엣지 컴퓨팅 및 데이터 처리 요구 사항</div>
          <p class="tech-contents-text">
            엣지에서 얼마나 많은 데이터를 얼마나 빠르게 처리해야 할까요?<br /><br />이
            질문에 대한 답이 명확할수록 엣지 컴퓨팅이 제시하는 미래의 비전은
            고객의 눈높이에 맞을 가능성이 높아집니다. <br /><br />
            극단적인 예로, NC(수치 제어) 장비의 실시간 모니터링 및 관리를 위한
            엣지 디바이스의 데이터 처리 요구사항은 2주마다 약 1T 바이트의
            데이터입니다. 이 값을 더 정확하게 변환하면 초당 872,628바이트를
            소화해야 합니다.<br /><br />이를 실제 센서 데이터의 평균 크기(약
            20바이트)로 변환하면 초당 약 40만 개 이상의 이벤트를 저장할 수
            있어야 한다는 계산이 나옵니다.<br /><br />엣지 디바이스는 초당 40만
            개 이상의 센서 데이터를 수집해야 할 뿐만 아니라 실시간 분석을 위해
            보조 저장 장치에 저장해야 합니다.<br /><br />또한 엣지 디바이스가
            고가용성을 지원해야 하는 환경이라면 더 높은 수준의 데이터 처리
            기술이 필요합니다.<br /><br />결국 산업마다 데이터의 종류, 데이터의
            형태, 데이터의 양이 다르고, 시간이 지날수록 다양한 형태의 요구사항이
            점점 더 엄격해질 것입니다.
          </p>
        </div>
        <div>
          <div class="tech-title">마크베이스와 엣지 컴퓨팅</div>
          <p class="tech-contents-text">
            글로벌 성능평가 1위 시계열 데이터베이스 Machbase는 이미 엣지
            컴퓨팅에서 초고속 데이터 처리를 위한 표준 에디션을 제공하고
            있습니다.<br /><br />이 버전은 라즈베리 파이 4에 초당 400,000개의
            센서 데이터를 저장할 수 있으며, CPU와 디스크 사용량을 매우
            효율적으로 활용합니다.<br /><br />엣지 디바이스임에도 빅데이터
            기술이 적용된 Machbase는 저장 한계까지 데이터를 저장할 수 있으며,
            빅데이터의 검색과 분석이 뛰어납니다. 향후 로드맵에 따라 여러 대의
            엣지 디바이스로 클러스터를 구축할 수 있어 고성능과 고가용성에 대한
            엣지 컴퓨팅 요구사항을 잘 지원합니다. Machbase의 성능을 요약하면
            다음과 같습니다.<br />
          </p>
          <p class="tech-contents-title">수집 관점에서</p>
          <ul class="tech-ul">
            <li>엣지 장치(ARM 2코어): 초당 최대 500,000회 처리</li>
            <li>단일 서버(INTEL 8코어): 최대 2,500,000 rec/sec</li>
            <li>클러스터(16노드): 최대 100,000,000 rec/sec</li>
          </ul>
          <p class="tech-contents-title">추출 관점에서</p>
          <ul class="tech-ul">
            <li>
              4,000억 개의 데이터 저장소에서 10,000개의 무작위 시간 범위를
              추출하는 데 0.1초 소요
            </li>
          </ul>
          <p class="tech-contents-title">압축 관점에서</p>
          <ul class="tech-ul">
            <li>4TB 저장 공간: 약 1조 개의 레코드</li>
          </ul>
          <p class="tech-contents-text">
            보시다시피, Machbase는 이미 엣지 컴퓨팅을 위한 데이터 처리 요구
            사항을 훌륭하게 충족하고 있으며, 제품을 더 자세히 평가하고
            싶으시다면 다운로드하여 테스트해 보시기 바랍니다.
          </p>
        </div>
      </div>
    </div>
  </section>
</body>
<footer>
  <div class="footer_inner">
    <div class="footer-logo">
      <img src="../img/machbase-logo-w.png" />
      <a href="/home/contactus">
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
          <a href="https://medium.com/machbase" target="_blank"
            ><img class="sns-img" src="../img/medium.png"
          /></a>
        </div>
      </div>
    </div>
  </div>
  <div class="footer_tablet_inner">
    <div class="footer-logo">
      <img src="../img/machbase-logo-w.png" />
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
          <a href="https://medium.com/machbase" target="_blank"
            ><img class="sns-img" src="../img/medium.png"
          /></a>
        </div>
      </div>
      <a href="/home/contactus">
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
