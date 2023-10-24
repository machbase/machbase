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
          <a href="/home"><img src="../../img/logo_machbase.png" alt="" /></a>
        </li>
        <li class="menu-a products-menu-wrap" id="productsMenuWrap">
          <div>
            <a
              class="menu_active_border"
              id="menuActiveBorder"
              href="/home/tsdb"
              >Products</a
            >
            <div class="dropdown" id="dropdown">
              <a class="dropdown-link" href="/home/tsdb">TSDB</a>
              <a class="dropdown-link" href="/home/mos">MOS</a>
              <a
                class="dropdown-link"
                href="https://www.cems.ai/home-eng/"
                target="_blank"
                >CEMS</a
              >
            </div>
          </div>
        </li>
        <li class="menu-a"><a href="/home/blog">Blog</a></li>
        <li class="menu-a"><a href="/home/customers">Customers</a></li>
        <li class="menu-a"><a href="/home/usecase">Use Case</a></li>
        <li class="menu-a"><a href="/home/company">Company</a></li>
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
        <li class="menu-a"><a href="/home/download">Download</a></li>
        <li class="menu-a">
          <a href="https://support.machbase.com/hc/en-us">Support</a>
        </li>
        <li class="menu-a"><a href="/home/contactus">Contact US</a></li>
        <li class="menu-a">
          <select id="languageSelector" onchange="changeLanguage()">
            <option value="en">English</option>
            <option value="kr">한국어</option>
          </select>
        </li>
      </ul>
    </div>
  </div>
</nav>
<nav class="tablet-menu-wrap">
  <a href="/kr/home"><img src="../../img/logo_machbase.png" alt="" /></a>
  <div class="hamberger-right">
    <select id="languageSelector2" onchange="changeLanguage2()">
      <option value="en">English</option>
      <option value="kr">한국어</option>
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
        <a class="tablet-logo" href="/home"
          ><img src="../../img/logo_machbase.png" alt=""
        /></a>
      </div>
      <li></li>
      <li class="products-toggle">Products</li>
      <li>
        <div class="products-content">
          <div class="products-sub"><a href="/home/tsdb">TSDB</a></div>
          <div class="products-num"><a href="/home/mos">MOS</a></div>
          <div class="products-cems">
            <a href="https://www.cems.ai/home-eng/" target="_blank">CEMS</a>
          </div>
        </div>
      </li>
      <li><a href="/home/blog">Blog</a></li>
      <li><a href="/home/customers">Customers</a></li>
      <li><a href="/home/usecase">Use Cases</a></li>
      <li><a href="/home/company">Company</a></li>
      <li class="docs-toggle">Document</li>
      <li>
        <div class="docs-content">
          <div class="docs-sub"><a href="/neo" target="_blank">Neo</a></div>
          <div class="docs-num">
            <a href="/dbms" target="_blank">Classic</a>
          </div>
        </div>
      </li>
      <li><a href="/home/download">Download</a></li>
      <li><a href="https://support.machbase.com/hc/en-us">Support</a></li>
      <li><a href="/home/download">Contact US</a></li>
    </ul>
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
        <h4 class="blog-title">
          [Machbase Use Case]Manufacturing - Hankuk Carbon
        </h4>
        <ul class="tech-list-ul">
          <a href="#anchor1">
            <li class="tech-list-li" id="tech-list-li">Company Profile</li>
          </a>
          <a href="#anchor2">
            <li class="tech-list-li" id="tech-list-li">Challenges</li>
          </a>
          <a href="#anchor3">
            <li class="tech-list-li" id="tech-list-li">Reason for Selection</li>
          </a>
          <a href="#anchor4">
            <li class="tech-list-li" id="tech-list-li">Solution</li>
          </a>
          <a href="#anchor5">
            <li class="tech-list-li" id="tech-list-li">Application Result</li>
          </a>
        </ul>
        <div class="tech-contents">
          <div>
            <div class="tech-img-wrap">
              <img
                class="tech-img"
                src="../../img/usecase_hankukcarborn.png"
                alt=""
              />
            </div>
            <p class="tech-contents-link-text">
              Machbase solution Architecture
            </p>
            <p class="tech-title" id="anchor1">Company Profile</p>
            <p class="tech-contents-text">
              Hankuk Carbon is a company that produces insulation panels, which
              are a key part of LNG carriers. Carbon prepregs are characterized
              by high strength and high elasticity, so their uses are endless,
              and they are currently used mainly in sports and leisure products
              such as fishing rods, golf, and skiing.
            </p>
            <p class="tech-title" id="anchor2">Challenges</p>
            <p class="tech-contents-text">
              The data generated from the existing production process was
              analyzed in batches instead of in real time using Excel, which was
              not only time-consuming but also not immediately efficient for the
              business.
            </p>
            <p class="tech-contents-text">
              It was a priority to create real-time dashboards by building a
              system to replace manual Excel work, and furthermore, it was
              necessary to have a system that could trace the cause of quality
              when product defects occurred.
            </p>
            <p class="tech-title" id="anchor3">Reason for Selection</p>
            <p class="tech-contents-text">
              Although "H" is building a smart factory for one plant, the
              company is considering expanding to factories not only in Korea
              but also overseas in the future, and selected Machbase’s time
              series database as a reliable and scalable data infrastructure for
              collecting large amounts of facility data.
            </p>
            <p class="tech-title" id="anchor4">Solution</p>
            <p class="tech-contents-text">
              Edge devices for data collection were installed in each of the two
              production processes to collect data from PLCs and automatically
              transmit it to the central server for integration. Based on this,
              a process data analysis application was built to generate duration
              charts and dashboards for facility and process data. In addition,
              vibration sensors were attached to key points in the facility and
              vibration sensor data was collected to detect facility
              abnormalities.
            </p>
            <p class="tech-title" id="anchor5">Application Result</p>
            <p class="tech-contents-text">
              The system was built to automatically generate data in real time,
              which was previously analyzed manually in Excel, increasing worker
              productivity and enabling them to check the process status
              immediately from the office. In addition, the quality department
              was able to analyze the factors affecting product defects,
              resulting in cost savings through improved quality and increased
              productivity.
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
      <a href="/home/contactus">
        <button class="contactus">Contact Us</button>
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
          <a href="https://medium.com/machbase" target="_blank"
            ><img class="sns-img" src="../../img/medium.png"
          /></a>
        </div>
      </div>
      <a href="/home/contactus">
        <button class="contactus">Contact US</button>
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
    if (userLang !== "ko") {
      sessionStorage.setItem("lang", userLang);
      language = "en";
    } else {
      sessionStorage.setItem("lang", "ko");
      language = "kr";
      location.href = location.origin + "/kr" + location.pathname;
    }
  }
  function changeLanguage() {
    var languageSelector = document.getElementById("languageSelector");
    var selectedLanguage = languageSelector.value;
    if (selectedLanguage === "kr") {
      location.href = location.origin + "/kr" + location.pathname;
    }
  }
  function changeLanguage2() {
    var languageSelector = document.getElementById("languageSelector2");
    var selectedLanguage = languageSelector.value;
    if (selectedLanguage === "kr") {
      location.href = location.origin + "/kr" + location.pathname;
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
