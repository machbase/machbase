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
                  <a class="dropdown-link" href="/neo" >Neo</a>
                  <a class="dropdown-link" href="/dbms" >Classic</a>
                </div>
              </div></a
            >
          </li>
          <li class="menu-a"><a href="/home/download">Download</a></li>
          <li class="menu-a">
            <a href="https://support.machbase.com/hc/en-us">Support</a>
          </li>
           <li class="menu-a"><a href="/home/contactus">Contact US</a></li>
        <li class="menu-a"><select id="languageSelector" onchange="changeLanguage()">
        <option value="en">English</option>
        <option value="kr">한국어</option>
    </select></li>
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
            <div class="docs-num"><a href="/dbms" target="_blank">Classic</a></div>
          </div>
        </li>
        <li><a href="/home/download">Download</a></li>
        <li><a href="https://support.machbase.com/hc/en-us">Support</a></li>
           <li><a href="/home/download">Contact US</a></li>
<li><select id="languageSelector2" onchange="changeLanguage2()">
        <option value="en">English</option>
        <option value="kr">한국어</option>
    </select>
    </li>
      </ul>
    </div>
  </nav>
  <section class="customers_section0">
    <div>
      <h1 class="sub_page_title">Customers</h1>
      <p class="sub_page_titletext">Growing Companies with Machbase</p>
    </div>
  </section>
  <section class="section1 customers_section1">
    <div class="logo_wrap">
      <div class="usecase_logos" :style="{ 'flex-wrap': wrapStyle }">
        <div class="Usecase_logo intell">
          <img alt="samsung" src="../img/samsung.png" />
        </div>
        <div class="Usecase_logo dsme">
          <img alt="DSME" src="../img/DSME.png" />
        </div>
        <div class="Usecase_logo lotte">
          <img alt="lotte" src="../img/lotte_logo.png" />
        </div>
        <div class="Usecase_logo">
          <img alt="hankukcarbon" src="../img/hankukcarbon_logo.png" />
        </div>
      </div>
      <div class="usecase_logos">
        <div class="Usecase_logo">
          <img alt="hyundai global" src="../img/hyundai_global.png" />
        </div>
        <div class="Usecase_logo">
          <img alt="hyundai heavy" src="../img/hyundail_heavy.png" />
        </div>
        <div class="Usecase_logo hansol">
          <img alt="hansol" src="../img/hansol.png" />
        </div>
        <div class="Usecase_logo ls_electric">
          <img alt="ls electric" src="../img/LS-ELECTRIC.png" />
        </div>
      </div>
      <div class="usecase_logos">
        <div class="Usecase_logo wia">
          <img alt="hyundaiwia" src="../img/hyundaiwia.png" />
        </div>
        <div class="Usecase_logo sk_bio">
          <img alt="sk biosience" src="../img/sk_bioscience.png" />
        </div>
        <div class="Usecase_logo">
          <img alt="lscable" src="../img/lscable.png" />
        </div>
        <div class="Usecase_logo sk_hynix">
          <img alt="sk hynix" src="../img/SK-hynix_RGB_EN.png" />
        </div>
      </div>
      <div class="usecase_logos">
        <div class="Usecase_logo">
          <img alt="hm" src="../img/HM.png" />
        </div>
        <div class="Usecase_logo">
          <img alt="kepco" src="../img/kepco.png" />
        </div>
        <div class="Usecase_logo kict">
          <img alt="kict" src="../img/kict.png" />
        </div>
        <div class="Usecase_logo kitech">
          <img alt="kitech" src="../img/kitech.png" />
        </div>
      </div>
      <div class="usecase_logos">
        <div class="Usecase_logo">
          <img alt="koen" src="../img/koen.png" />
        </div>
        <div class="Usecase_logo">
          <img alt="kolmar" src="../img/kolmar.png" />
        </div>
        <div class="Usecase_logo">
          <img alt="korail" src="../img/korail.png" />
        </div>
        <div class="Usecase_logo korearail">
          <img alt="korearail" src="../img/korearail.png" />
        </div>
      </div>
      <div class="usecase_logos">
        <div class="Usecase_logo korens">
          <img alt="korens" src="../img/korens.png" />
        </div>
        <div class="Usecase_logo intell">
          <img alt="intellvix" src="../img/intellivix.jpg" />
        </div>
        <div class="Usecase_logo">
          <img alt="lae" src="../img/lae.png" />
        </div>
        <div class="Usecase_logo">
          <img alt="etri" src="../img/ETRI_logo.png" />
        </div>
      </div>
      <div class="usecase_logos">
        <div class="Usecase_logo">
          <img alt="daeati" src="../img/daeati.png" />
        </div>
        <div class="Usecase_logo">
          <img alt="huons" src="../img/huons.png" />
        </div>
        <div class="Usecase_logo">
          <img alt="seoul" src="../img/seoul.png" />
        </div>
        <div class="Usecase_logo">
          <img alt="mandobrose" src="../img/mandobrose_logo.png" />
        </div>
      </div>
      <div class="usecase_logos">
        <div class="Usecase_logo">
          <img alt="seoulmetro" src="../img/seoulmetro.png" />
        </div>
        <div class="Usecase_logo impix">
          <img alt="impix" src="../img/impix.png" />
        </div>
        <div class="Usecase_logo hkc">
          <img alt="hkc" src="../img/hkc.png" />
        </div>
        <div class="Usecase_logo sampyo">
          <img alt="sampyo" src="../img/smapyo.jpg" />
        </div>
      </div>
      <div class="usecase_logos">
        <div class="Usecase_logo smic">
          <img alt="smic" src="../img/SMIC_logo.png" />
        </div>
        <div class="Usecase_logo snet">
          <img alt="snet" src="../img/snet.png" />
        </div>
        <div class="Usecase_logo">
          <img alt="woojin" src="../img/woojin.png" />
        </div>
        <div class="Usecase_logo">
          <img alt="xslab" src="../img/xslab_logo.png" />
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