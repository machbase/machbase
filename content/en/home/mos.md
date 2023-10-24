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
          Machbase MOS (Manufacturing Optimization Suite) is the best solution
          for real-time process monitoring and identification of facility and
          quality abnormalities through synchronization of facility status data
          and product quality information data.
          <br /><br />
          Through MOS, companies can build realistic big data for quality
          maintenance monitoring, quality problem tracking, analyzing causes and
          utilizing them by linking sensor data of facilities and product data.
          <br /><br />
          This will enable companies to reduce defect rates, improve quality,
          increase productivity, trace product production history, reduce
          customer claims, and reduce costs, which will ultimately increase
          profits and value.
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
                <p>Data Collection and Integration</p>
              </div>
              <div class="scroll-sub-title-wrap">
                <p class="scroll-sub-title">Sensor Data (to TSDB)</p>
                <ul class="tech-margin-bottom">
                  <li>OPC-UA/DA</li>
                  <li>MQTT Pub/Sub</li>
                  <li>Modbus RTU/TCP</li>
                  <li>Melsec</li>
                  <li>Simatic</li>
                  <li>Ethernet</li>
                </ul>
                <p class="scroll-sub-title">
                  Product Information Data (to RDBMS)
                </p>
                <ul>
                  <li>Portal</li>
                  <li>ERP</li>
                  <li>MES/POP</li>
                  <li>QMS</li>
                  <li>Legacy</li>
                </ul>
                <div class="scroll-contents-wrap">
                  <p class="mos-scroll-content">
                    Collect sensor data from various facilities into TSDB in
                    seconds Collect data linked to customer's production-related
                    legacy system and ERP/MES into RDBMS
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div ref="classicSubWrapRef" class="database_sub_wrap" id="scroll1">
            <div class="neo_sub">
              <div class="scroll-title-wrap">
                <p>Database Configuration</p>
              </div>
              <div class="scroll-sub-title-wrap">
                <p class="scroll-sub-title">TSDB</p>
                <p class="scroll-content">
                  Time series database from Machbase, the world's #1
                  internationally recognised performance evaluation by TPC,
                  enabling the collection, storage, input and output of hundreds
                  of thousands of data points per second from sensors.
                </p>
                <p class="scroll-sub-title">RDBMS</p>
                <p class="scroll-content">
                  Configuration of RDBMS to manage product information, facility
                  information, work instruction information, etc. required in
                  the production process in conjunction with the legacy system
                  (RDBMS can be configured according to the needs of the
                  company)
                </p>
                <p class="scroll-sub-title">AAS</p>
                <p class="scroll-content">
                  Based on AAS (Asset Administration Shell), an industry 4.0
                  data standard system, it defines classification system
                  attributes such as production, quality, and facilities by
                  facility/tag item to perform data connection work for easy
                  cross-reference between related departments, and builds a
                  linkage foundation to reflect standardized AAS information
                  such as production, quality, and facilities in the future.
                </p>
              </div>
            </div>
          </div>
          <div ref="neoSubWrapRef" class="feature_sub_wrap" id="scroll2">
            <div class="neo_use_sub product-link-bottom">
              <div class="scroll-title-wrap">
                <p>Dashboard and Key Features</p>
              </div>
              <div class="scroll-sub-title-wrap">
                <p class="scroll-sub-title">Monitoring</p>
                <ul>
                  <li>Tag Monitoring</li>
                  <li>Quality Condition Monitoring</li>
                  <li>Facility Condition Monitoring</li>
                  <li>Tracking when an abnormality occurs, etc.</li>
                </ul>
                <p class="scroll-sub-title">Equipment/Quality</p>
                <ul>
                  <li>Process capability comparison (CpK)</li>
                  <li>Quality standard deviation status</li>
                  <li>Raw Data Search</li>
                  <li>Production Performance</li>
                </ul>
                <p class="scroll-sub-title">Master Data</p>
                <ul>
                  <li>Item Management</li>
                  <li>Asset Management</li>
                  <li>Asset Hierarchy(AAS)</li>
                  <li>Bill of Process(BOP)</li>
                </ul>
                <p class="scroll-sub-title">System</p>
                <ul class="tech-margin-bottom">
                  <li>Lookup (Common Code)</li>
                  <li>Organization/Users/Permissions</li>
                  <li>System Settings/Menu Management, etc.</li>
                </ul>
                <!-- <p class="scroll-sub-title">Prediction/Analysis</p>
                                <ul>
                                    <li>Analysis and prediction using AI Module (Optional)</li>
                                </ul> -->
                <p class="scroll-content">
                  Machbase MOS provides real-time data collection, storage,
                  processing, analysis and visualization, periodic report
                  output, as well as the ability to comprehensively collect and
                  identify causes of abnormalities in facilities, track
                  production performance by lot, and monitor processes in real
                  time to predict quality abnormalities.
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
              onclick="location.href='/home/download'"
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
