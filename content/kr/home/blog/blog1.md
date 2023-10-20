---
---

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" type="text/css" href="../../css/common.css" />
  <link rel="stylesheet" type="text/css" href="../../css/style.css" />
</head>
<nav>
  <div class="homepage-menu-wrap">
    <div class="menu-left">
      <ul class="menu-left-ul">
        <li class="menu-logo">
          <a href="/kr/home"
            ><img src="../../img/logo_machbase.png" alt=""
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
              <a class="menu_active_border" id="menuActiveBorder" href=""
                >Document</a
              >
              <div class="dropdown-docs" id="dropdownDocs">
                <a class="dropdown-link" href="/neo" target="_blank">Neo</a>
                <a class="dropdown-link" href="/dbms" target="_blank">Classic</a>
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
  <a href="/kr/home"><img src="../../img/logo_machbase.png" alt="" /></a>
  <div class="tablet-menu-icon">
    <div class="tablet-bar"></div>
    <div class="tablet-bar"></div>
    <div class="tablet-bar"></div>
  </div>
  <div class="tablet-menu">
    <ul>
      <div class="tablet-menu-title">
        <a class="tablet-logo" href="/kr/home"
          ><img src="../../img/logo_machbase.png" alt=""
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
          <div class="docs-num"><a href="/dbms" target="_blank">Classic</a></div>
        </div>
      </li>
      <li><a href="/kr/home/download">Download</a></li>
      <li><a href="https://support.machbase.com/hc/en-us">Support</a></li>
         <li><a href="/kr/home/download">Contact US</a></li>
      <li>
    <select id="languageSelector2" onchange="changeLanguage2()">
      <option value="kr">한국어</option>
      <option value="en">English</option>
    </select>
      </li>
    </ul>
  </div>
</nav>
<section class="pricing_section0 section0">
  <div>
    <h1 class="sub_page_title">Blog</h1>
    <p class="sub_page_titletext">
      “ Mach Speed Horizontally Scalable Time series database. ”
    </p>
  </div>
</section>
<section>
  <div class="tech-inner">
    <h4 class="blog-title">당신의 개발 Know-how를 기록하는 새로운 방법</h4>
    <div class="blog-date">
      <div>
        <span>by James Lee / 7 Sep 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">개요</li></a
      >
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">
          WorkWorksheet 작성 언어 - Markdown
        </li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">Neo Markdown 문법</li>
      </a>
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">Worksheet 관리</li>
      </a>
      <a href="#anchor5">
        <li class="tech-list-li" id="tech-list-li">결론</li>
      </a>
    </ul>
    <div class="tech-contents">
      <div>
        <p class="tech-title" id="anchor1">개요</p>
        <p class="tech-contents-text">
          <b
            >Machbase Neo는 Machbase time series database를 기반으로 사용자
            편의성을 극대화한 All-in-one package 솔루션입니다.</b
          >
        </p>
        <p class="tech-contents-text">
          Machbase Neo에 대한 자세한 내용은 웹사이트
          <a class="tech-contents-link" href="https://neo.machbase.com."
            >https://neo.machbase.com.</a
          >을 참고하면 됩니다.
        </p>
        <p class="tech-contents-text">
          Machbase Neo 기능 중에 문서를 작성할 수 있는 worksheet 라는 기능이
          있다. 단순히 정적인 문서를 작성하는 것이 아니라 SQL 구문 등은 직접
          실행해서 결과를 문서상에 표시할 수 있기 때문에 Interactive 하게 내용을
          이해할 수 있습니다.
        </p>
        <p class="tech-contents-text">
          또한 작성된 worksheet 을 통해 Machbase Neo 사용법 등을 사용자 간
          공유할 수 있어서 서로 간의 정보교류의 수단으로도 활용할 수 있습니다.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/neo-worksheet-1.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          &lt; Machbase Neo worksheet 실행 메뉴 >
        </p>
        <p class="tech-title" id="anchor2">Worksheet 작성 언어 — Markdown</p>
        <p class="tech-contents-text">
          Markdown 문법을 이용하여 worksheet를 작성한다. Markdown은 일반 텍스트
          기반의 경량 마크업 언어로 태그 등을 이용하여 문서나 데이터의 구조 등을
          표시하는 언어이다. 주로 텍스트만으로 서식 있는 문서를 작성할 때
          사용되며, 문법이 간단하고 쉬어서 약간의 학습으로 누구나 문서를 작성할
          수 있습니다.
        </p>
        <p class="tech-contents-text">
          Markdown은 Github, Notion, Discord 등 다양한 서비스 플랫폼에서
          지원하고 있으며 대부분의 텍스트 에디터 환경에서 작성 및 수정이
          가능합니다.
        </p>
        <p class="tech-contents-text">
          다만 파일이나 이미지가 문서 내에 바로 임베딩되지 않기 때문에서 별도의
          서버에 업로드하고 나서 파일 URL을 입력해야 합니다.
        </p>
        <p class="tech-title" id="anchor3">Neo Markdown 문법</p>
        <p class="tech-contents-text">
          일반적인 Markdown 문법은 여기
          <a class="tech-contents-link" href="https://neo.machbase.com."
            >(https://www.markdownguide.org/basic-syntax/).</a
          >
        </p>
        <p class="tech-contents-text">
          Machbase Neo에서는 SQL 구문을 실행할 수 있는 버튼이 있어 SQL쿼리문을
          실행하면 실제로 Neo TSDB에서 SQL 쿼리문을 실행하고 그 결과를 화면에
          표시할 수 있는 기능이 있습니다.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/neo-worksheet-2.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          &lt; Machbase Neo worksheet에서 SQL 구문 실행 화면 예시 >
        </p>
        <p class="tech-contents-text">
          예를 들어, 작성 입력창에서 SQL 구문을 작성하고 문서 타입을 Markdown이
          아닌 SQL로 선택하면 됩니다. 그리고 실행 아이콘을 클릭하면 해당 SQL
          문이 실제로 수행이 되고 그 결과값을 아랫부분에 표시하게 됩니다. 단순히
          static 문서를 read 하는 것이 아니라 interactive 하게 TSDB와 연동해서
          동작 여부를 확인할 수 있습니다.
        </p>
        <p class="tech-contents-text">
          SQL 문장뿐만 아니라 Machbase Neo에서 제공하는 TQL 문법도 바로 실행이
          가능하고 그 결과를 화면에 표시하게 됩니다.
        </p>
        <p class="tech-title" id="anchor4">Worksheet 관리</p>
        <p class="tech-contents-text">
          작성된 Worksheet은 저장하게 되면 Neo가 설치된 경로에 wrk 확장자 파일로
          저장됩니다.
        </p>
        <p class="tech-contents-text">
          작성된 파일을 다른 사용자에게 공유하면 Machbase Neo의 Worksheet에서
          바로 오픈하여 읽어볼 수 있습니다. Machbase Neo를 설치하면 워크시트를
          사용하여 이미 작성된 튜토리얼 문서를 볼 수 있습니다.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/neo-worksheet-3.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          &lt; Machbase Neo built-in worksheet example >
        </p>
        <p class="tech-contents-text">
          Machbase Neo 메인화면에서 Drop&Open 영역에 해당 파일을 마우스로 drag &
          drop 하면 문서가 오픈됩니다.
        </p>
        <p class="tech-title" id="anchor5">결론</p>
        <p class="tech-contents-text">
          Machbase Neo Worksheet 기능은 텍스트 기반의 Markdown 언어를 통해
          간단하고 쉽게 문서를 작성하고 관리할 수 있는 기능이다.
        </p>
        <p class="tech-contents-text">
          Machbase Neo 사용법 또는 가이드 문서를 작성하고 다른 사용자가
          worksheet 문서를 read 하면서 쉽게 따라 해볼 수 있다. 특히 SQL 구문,
          TQL 구문은 문서상에서 바로 실행해서 결과를 확인해 볼 수 있기 때문에
          초보자도 Machbase Neo 상에서 쉽게 따라 해보면서 내용을 파악할 수 있다.
        </p>
      </div>
    </div>
  </div>
</section>

<footer>
  <div class="footer_inner">
    <div class="footer-logo">
      <img class="footer-logo-img" src="../../img/machbase-logo-w.png" />
      <a href="/kr/home/contactus">
        <button class="contactus">고객 문의</button>
      </a>
    </div>
    <div>
      <p class="footertext">
        서울시 강남구 테헤란로 20길 10, 3M 타워, 9층
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
            ><img class="sns-img" src="../../img/twitter.png"
          /></a>
        </div>
        <div>
          <a href="https://github.com/machbase" target="_blank"
            ><img class="sns-img" src="../../img/github.png"
          /></a>
        </div>
        <div>
          <a href="https://www.linkedin.com/company/machbase" target="_blank"
            ><img src="../../img/linkedin.png"
          /></a>
        </div>
        <div>
          <a href="https://www.facebook.com/MACHBASE/" target="_blank"
            ><img class="sns-img" src="../../img/facebook.png"
          /></a>
        </div>
        <div>
          <a href="https://www.slideshare.net/machbase" target="_blank"
            ><img class="sns-img" src="../../img/slideshare.png"
          /></a>
        </div>
        <div>
          <a href="https://medium.com/machbase" target="_blank"
            ><img class="sns-img" src="../../img/medium.png"
          /></a>
        </div>
      </div>
    </div>
  </div>
  <div class="footer_tablet_inner">
    <div class="footer-logo">
      <img class="footer-logo-img" src="../../img/machbase-logo-w.png" />
    </div>
    <div>
      <p class="footertext">
        서울시 강남구 테헤란로 20길 10, 3M 타워, 9층
      </p>
    </div>
    <div class="footer_box">
      <div class="footer_text">
        <p>MACHBASE.COM | sales@machbase.com | support@machbase.com</p>
      </div>
      <div class="sns">
        <div>
          <a href="https://twitter.com/machbase" target="_blank"
            ><img class="sns-img" src="../../img/twitter.png"
          /></a>
        </div>
        <div>
          <a href="https://github.com/machbase" target="_blank"
            ><img class="sns-img" src="../../img/github.png"
          /></a>
        </div>
        <div>
          <a href="https://www.linkedin.com/company/machbase" target="_blank"
            ><img src="../../img/linkedin.png"
          /></a>
        </div>
        <div>
          <a href="https://www.facebook.com/MACHBASE/" target="_blank"
            ><img class="sns-img" src="../../img/facebook.png"
          /></a>
        </div>
        <div>
          <a href="https://www.slideshare.net/machbase" target="_blank"
            ><img class="sns-img" src="../../img/slideshare.png"
          /></a>
        </div>
        <div>
          <a href="https://medium.com/machbase" target="_blank"
            ><img class="sns-img" src="../../img/medium.png"
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
  window.addEventListener("load", function() {
    var elementsWithDarkClass = document.querySelectorAll(".dark");
    for (var i = 0; i < elementsWithDarkClass.length; i++) {
        elementsWithDarkClass[i].classList.remove("dark");
    }
     var elementsWithColorScheme = document.querySelectorAll("[style*='color-scheme: dark;']");
    for (var i = 0; i < elementsWithColorScheme.length; i++) {
        elementsWithColorScheme[i].removeAttribute("style");
    }
});
</script>
