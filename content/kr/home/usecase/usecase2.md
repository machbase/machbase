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
