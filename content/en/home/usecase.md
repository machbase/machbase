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
            <a href="/home"><img src="../img/logo_machbase.png" alt="" /></a>
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
    <a href="/kr/home"><img src="../img/logo_machbase.png" alt="" /></a>
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
            ><img src="../img/logo_machbase.png" alt=""
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
        Machbase products are the choice of the world's leading companies and
        are in use in countless locations.
      </p>
    </div>
  </section>
  <div class="tech-inner">
    <section>
      <div class="blog-pc">
        <div class="blog-first-wraper">
          <div class="blog-text-wraper">
            <div class="tech-first-link-wrap">
              <a class="blog-link" href="/home/usecase/usecase1"
                >[Machbase Use Case]Ship Management - Hyundai Global Services</a
              >
              <div class="blog-date">
                <div>
                  <span>7 Sep 2023</span>
                  <span></span>
                </div>
              </div>
              <div class="blog-first-div">
                Machbase was able to provide a real-time monitoring service by
                collecting and storing CSV files containing data from sensors on
                ship engines through a schema structure that fits time series
                data.
              </div>
              <div class="blog_usecase_more_box">
                <p class="blog_usecase_more_wrap">
                  <span>
                    <a class="blog_usecase_more" href="/home/usecase/usecase1"
                      >View More <ArrowSvg
                    /></a>
                  </span>
                </p>
              </div>
            </div>
          </div>
          <div class="blog-first-img-wrap">
            <a href="/home/usecase/usecase1"
              ><img class="blog-img" src="../img/usecase_hyundai.png" alt=""
            /></a>
          </div>
        </div>
        <div class="blog-wraper">
          <div class="tech-link-wrap">
            <div class="blog-img-wrap">
              <a href="/home/usecase/usecase2"
                ><img
                  class="blog-img blog-margin-bottom"
                  src="../img/uscase_lotte.png"
                  alt=""
              /></a>
            </div>
            <a class="tech-link" href="/home/usecase/usecase2"
              >[Machbase Use Case]Manufacturing - Lotte Chilsung</a
            >
            <div>
              Transforming a SCADA system that only stored facility alarm
              history in MS-SQL into a system that can collect, store, and
              retrieve 200,000 pieces of data per second in real time.
            </div>
          </div>
          <div class="tech-link-wrap">
            <div class="blog-img-wrap">
              <a href="/home/usecase/usecase3"
                ><img
                  class="blog-img blog-margin-bottom"
                  src="../img/usecase_mando.png"
                  alt=""
              /></a>
            </div>
            <a class="tech-link" href="/home/usecase/usecase3"
              >[Machbase Use Case]Manufacturing - Mando Brose</a
            >
            <div>
              Embedded Machbase time series DB in each edge device of each
              production line to collect multiple data per production line,
              while allowing alarms and process progress data to be displayed in
              the existing MES system.
            </div>
          </div>
          <div class="tech-link-wrap">
            <div class="blog-img-wrap">
              <a href="/home/usecase/usecase4"
                ><img
                  class="blog-img blog-margin-bottom"
                  src="../img/usecase_etri2.png"
                  alt=""
              /></a>
            </div>
            <a class="tech-link" href="/home/usecase/usecase4"
              >[Machbase Use Case]Public - ETRI</a
            >
            <div>
              Using Machbase Time Series DB, we shortened the timeframe of a
              project to build an energy big data platform that collects and
              stores real-time power data to develop deep learning algorithms.
            </div>
          </div>
        </div>
        <div class="blog-wraper">
          <div class="tech-link-wrap">
            <div class="blog-img-wrap">
              <a href="/home/usecase/usecase5"
                ><img
                  class="blog-img blog-margin-bottom"
                  src="../img/usecase_hankukcarborn.png"
                  alt=""
              /></a>
            </div>
            <a class="tech-link" href="/home/usecase/usecase5"
              >[Machbase Use Case]Manufacturing - Hankuk Carbon</a
            >
            <div>
              Established a system that enables real-time process monitoring and
              identification of abnormalities in facilities and quality through
              real-time synchronization of sensor information of production
              facilities and quality information data of products.
            </div>
          </div>
          <div class="tech-link-wrap">
            <div class="blog-img-wrap">
              <a href="/home/usecase/usecase6">
                <img
                  class="blog-img blog-margin-bottom"
                  src="../img/usecase_carrot.png"
                  alt=""
              /></a>
            </div>
            <a class="tech-link" href="/home/usecase/usecase6"
              >[Machbase Use Case] Insurance - Carrot Insurance</a
            >
            <div>
              Machbase's reliable cluster operation has enabled Carrot's mileage
              insurance, which uses IoT devices, to collect real-time
              information on subscribers' vehicle operations and charge premiums
              based on that information.
            </div>
          </div>
        </div>
      </div>
      <div class="blog-tablet">
        <div class="blog-first-wraper">
          <div class="blog-text-wraper">
            <div class="tech-first-link-wrap">
              <a class="blog-link" href="/home/usecase/usecase1"
                >[Machbase Use Case]Ship Management - Hyundai Global Services</a
              >
              <div class="blog-date">
                <div>
                  <span>7 Sep 2023</span>
                  <span></span>
                </div>
              </div>
              <div class="blog-first-div">
                Hyundai Global Services is a company that provides real-time
                ship operation information to ship owners and performs onshore
                control services for ships manufactured by Hyundai Heavy
                Industries.
              </div>
              <div class="blog_usecase_more_box">
                <p class="blog_usecase_more_wrap">
                  <span>
                    <a class="blog_usecase_more" href="/home/usecase/usecase1"
                      >View More <ArrowSvg
                    /></a>
                  </span>
                </p>
              </div>
            </div>
          </div>
          <div class="blog-first-img-wrap">
            <a href="/home/usecase/usecase1"
              ><img class="blog-img" src="../img/usecase_hyundai.png" alt=""
            /></a>
          </div>
        </div>
        <div class="blog-wraper">
          <div class="tech-link-wrap">
            <div class="blog-img-wrap">
              <a href="/home/usecase/usecase2"
                ><img
                  class="blog-img blog-margin-bottom"
                  src="../img/uscase_lotte.png"
                  alt=""
              /></a>
            </div>
            <a class="tech-link" href="/home/usecase/usecase2"
              >[Machbase Use Case]Manufacturing - Lotte Chilsung</a
            >
            <div>
              Transforming a SCADA system that only stored facility alarm
              history in MS-SQL into a system that can collect, store, and
              retrieve 200,000 pieces of data per second in real time.
            </div>
          </div>
          <div class="tech-link-wrap">
            <div class="blog-img-wrap">
              <a href="/home/usecase/usecase3"
                ><img
                  class="blog-img blog-margin-bottom"
                  src="../img/usecase_mando.png"
                  alt=""
              /></a>
            </div>
            <a class="tech-link" href="/home/usecase/usecase3"
              >[Machbase Use Case]Manufacturing - Mando Brose</a
            >
            <div>
              Embedded Machbase time series DB in each edge device of each
              production line to collect multiple data per production line,
              while allowing alarms and process progress data to be displayed in
              the existing MES system.
            </div>
          </div>
        </div>
        <div class="blog-wraper">
          <div class="tech-link-wrap">
            <div class="blog-img-wrap">
              <a href="/home/usecase/usecase4"
                ><img
                  class="blog-img blog-margin-bottom"
                  src="../img/usecase_etri2.png"
                  alt=""
              /></a>
            </div>
            <a class="tech-link" href="/home/usecase/usecase4"
              >[Machbase Use Case]Public - ETRI</a
            >
            <div>
              Using Machbase Time Series DB, we shortened the timeframe of a
              project to build an energy big data platform that collects and
              stores real-time power data to develop deep learning algorithms.
            </div>
          </div>
          <div class="tech-link-wrap">
            <div class="blog-img-wrap">
              <a href="/home/usecase/usecase5"
                ><img
                  class="blog-img blog-margin-bottom"
                  src="../img/usecase_hankukcarborn.png"
                  alt=""
              /></a>
            </div>
            <a class="tech-link" href="/home/usecase/usecase5"
              >[Machbase Use Case]Manufacturing - Hankuk Carbon</a
            >
            <div>
              Established a system that enables real-time process monitoring and
              identification of abnormalities in facilities and quality through
              real-time synchronization of sensor information of production
              facilities and quality information data of products.
            </div>
          </div>
        </div>
        <div class="blog-wraper">
          <div class="tech-link-wrap">
            <div class="blog-img-wrap">
              <a href="/home/usecase/usecase6">
                <img
                  class="blog-img blog-margin-bottom"
                  src="../img/usecase_carrot.png"
                  alt=""
              /></a>
            </div>
            <a class="tech-link" href="/home/usecase/usecase6"
              >[Machbase Use Case] Insurance - Carrot Insurance</a
            >
            <div>
              Machbase's reliable cluster operation has enabled Carrot's mileage
              insurance, which uses IoT devices, to collect real-time
              information on subscribers' vehicle operations and charge premiums
              based on that information.
            </div>
          </div>
        </div>
      </div>
      <div class="blog-mobile">
        <div class="blog-first-wraper">
          <div class="blog-first-img-wrap">
            <a href="/home/usecase/usecase1"
              ><img class="blog-img" src="../img/usecase_hyundai.png" alt=""
            /></a>
          </div>
          <div class="blog-text-wraper">
            <div class="tech-first-link-wrap">
              <a class="blog-link" href="/home/usecase/usecase1"
                >[Machbase Use Case]Ship Management - Hyundai Global Services</a
              >
              <div class="blog-date">
                <div>
                  <span>7 Sep 2023</span>
                  <span></span>
                </div>
              </div>
              <div class="blog-first-div">
                Hyundai Global Services is a company that provides real-time
                ship operation information to ship owners and performs onshore
                control services for ships manufactured by Hyundai Heavy
                Industries.
              </div>
              <div class="blog_usecase_more_box">
                <p class="blog_usecase_more_wrap">
                  <span>
                    <a class="blog_usecase_more" href="/home/usecase/usecase1"
                      >View More
                    </a>
                  </span>
                </p>
              </div>
            </div>
          </div>
        </div>
        <div class="blog-wraper">
          <div class="tech-link-wrap">
            <div class="blog-img-wrap">
              <a href="/home/usecase/usecase2"
                ><img
                  class="blog-img blog-margin-bottom"
                  src="../img/uscase_lotte.png"
                  alt=""
              /></a>
            </div>
            <a class="tech-link" href="/home/usecase/usecase2"
              >[Machbase Use Case]Manufacturing - Lotte Chilsung</a
            >
            <div>
              Transforming a SCADA system that only stored facility alarm
              history in MS-SQL into a system that can collect, store, and
              retrieve 200,000 pieces of data per second in real time.
            </div>
          </div>
        </div>
        <div class="blog-wraper">
          <div class="tech-link-wrap">
            <div class="blog-img-wrap">
              <a href="/home/usecase/usecase3"
                ><img
                  class="blog-img blog-margin-bottom"
                  src="../img/usecase_mando.png"
                  alt=""
              /></a>
            </div>
            <a class="tech-link" href="/home/usecase/usecase3"
              >[Machbase Use Case]Manufacturing - Mando Brose</a
            >
            <div>
              Embedded Machbase time series DB in each edge device of each
              production line to collect multiple data per production line,
              while allowing alarms and process progress data to be displayed in
              the existing MES system.
            </div>
          </div>
        </div>
        <div class="blog-wraper">
          <div class="tech-link-wrap">
            <div class="blog-img-wrap">
              <a href="/home/usecase/usecase4"
                ><img
                  class="blog-img blog-margin-bottom"
                  src="../img/usecase_etri2.png"
                  alt=""
              /></a>
            </div>
            <a class="tech-link" href="/home/usecase/usecase4"
              >[Machbase Use Case]Public - ETRI</a
            >
            <div>
              Using Machbase Time Series DB, we shortened the timeframe of a
              project to build an energy big data platform that collects and
              stores real-time power data to develop deep learning algorithms.
            </div>
          </div>
        </div>
        <div class="blog-wraper">
          <div class="tech-link-wrap">
            <div class="blog-img-wrap">
              <a href="/home/usecase/usecase5"
                ><img
                  class="blog-img blog-margin-bottom"
                  src="../img/usecase_hankukcarborn.png"
                  alt=""
              /></a>
            </div>
            <a class="tech-link" href="/home/usecase/usecase5"
              >[Machbase Use Case]Manufacturing - Hankuk Carbon</a
            >
            <div>
              Established a system that enables real-time process monitoring and
              identification of abnormalities in facilities and quality through
              real-time synchronization of sensor information of production
              facilities and quality information data of products.
            </div>
          </div>
        </div>
        <div class="blog-wraper">
          <div class="tech-link-wrap">
            <div class="blog-img-wrap">
              <a href="/home/usecase/usecase6"
                ><img
                  class="blog-img blog-margin-bottom"
                  src="../img/usecase_carrot.png"
                  alt=""
              /></a>
            </div>
            <a class="tech-link" href="/home/usecase/usecase6"
              >[Machbase Use Case] Insurance - Carrot Insurance</a
            >
            <div>
              Machbase's reliable cluster operation has enabled Carrot's mileage
              insurance, which uses IoT devices, to collect real-time
              information on subscribers' vehicle operations and charge premiums
              based on that information.
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</body>
<footer>
  <div class="footer_inner">
    <div class="footer-logo">
      <img src="../img/machbase-logo-w.png" />
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
          <a href="https://medium.com/machbase" target="_blank"
            ><img class="sns-img" src="../img/medium.png"
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
