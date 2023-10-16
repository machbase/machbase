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
        <li class="menu-a"><a href="/">Docs</a></li>
        <li class="menu-a"><a href="/kr/home/blog">Blog</a></li>
        <li class="menu-a"><a href="/kr/home/customers">Customers</a></li>
        <li class="menu-a"><a href="/kr/home/usecase">Use Case</a></li>
        <li class="menu-a"><a href="/kr/home/company">Company</a></li>
      </ul>
    </div>
    <div class="menu-right">
      <ul class="menu-right-ul">
        <li class="menu-a"><a href="/kr/home/download">Download</a></li>
        <li class="menu-a">
          <a href="https://support.machbase.com/hc/en-us">Support</a>
        </li>
        <li class="menu-a"><a href="/kr/home/contactus">Contact US</a></li>
      </ul>
    </div>
  </div>
</nav>
<section class="usecase_section0">
  <div>
    <h1 class="sub_page_title">Use Case</h1>
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
        <h4 class="blog-title">[Machbase Use Case]제조업 - Mando Brose</h4>
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
              <img class="tech-img" src="../../img/usecase_mando.png" alt="" />
            </div>
            <p class="tech-contents-link-text">
              Machbase solution Architecture
            </p>
            <p class="tech-title" id="anchor1">회사소개</p>
            <p class="tech-contents-text">
              만도 브로제는 2011년 한국의 만도 코퍼레이션과 글로벌 자동차 부품
              회사인 독일의 브로제가 합작하여 설립한 자동차용 모터 전문
              기업입니다.
            </p>
            <p class="tech-title" id="anchor2">개요</p>
            <p class="tech-contents-text">
              각 생산 라인의 각 에지 디바이스에 Machbase 시계열 DB를 내장하여
              생산 라인별로 여러 데이터를 수집하는 동시에 기존 MES 시스템에서
              알람 및 공정 진행 데이터를 표시할 수 있습니다.
            </p>
            <p class="tech-title" id="anchor3">과제</p>
            <p class="tech-contents-text">
              생산 라인별로 여러 PLC 데이터를 실시간으로 수집하고 각 라인의
              상태를 모니터링하는 한편, 알람 및 공정 진행률 데이터를 전달하고
              기존 MES 시스템과 연동하여 MES 화면에 표시해야 했습니다.
            </p>
            <p class="tech-title" id="anchor4">해결방법</p>
            <p class="tech-contents-text">
              7개의 에지 디바이스 각각에 마크베이스 시계열 DB를 내장하여 각 생산
              라인에 맞게 구축했습니다. 에지 디바이스에서 수집된 데이터는
              실시간으로 중앙 서버로 자동 전송되어 저장되었습니다. MES에 필요한
              알람 및 진행 상황 데이터는 에지 디바이스에서 MS-SQL과의
              인터페이스를 통해 전송되었습니다.
            </p>
            <p class="tech-title" id="anchor5">적용 결과</p>
            <p class="tech-contents-text">
              알람 및 진행률 데이터를 MES 시스템에서 확인할 수 있어 공정 상태를
              실시간으로 모니터링할 수 있습니다. 또한 설비 데이터의 빅데이터
              분석이 가능해져 품질 분석 및 설비 예지보전을 위한 기반을 마련할 수
              있게 되었습니다.
            </p>
          </div>
        </div>
      </div>
    </section>
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
          <a href="https://blog.naver.com/machbasekr" target="_blank"
            ><img class="sns-img" src="../../img/naver.png"
          /></a>
        </div>
      </div>
    </div>
  </div>
  <div class="footer_tablet_inner">
    <div class="logo">
      <img class="footer-logo-img" src="../../img/machbase-logo-w.png" />
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
          <a href="https://blog.naver.com/machbasekr" target="_blank"
            ><img class="sns-img" src="../../img/naver.png"
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
  const dropdown = document.getElementById("dropdown");
  dropdown.style.display = "none";
  productsMenuWrap.addEventListener("mouseover", function () {
    dropdown.style.display = "block";
  });
  productsMenuWrap.addEventListener("mouseout", function () {
    dropdown.style.display = "none";
  });
</script>
