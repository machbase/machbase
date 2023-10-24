---
title: Blog
description: "A New Approach to Documenting Your Know-How"
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
<section class="pricing_section0 section0">
  <div>
    <h2 class="sub_page_title">Blog</h2>
    <p class="sub_page_titletext">
      “ Mach Speed Horizontally Scalable Time series database. ”
    </p>
  </div>
</section>
<section>
  <div class="tech-inner">
    <h4 class="blog-title">A New Approach to Documenting Your Know-How</h4>
    <div class="blog-date">
      <div>
        <span>by James Lee / 7 Sep 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">Introduction</li></a
      >
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">
          Worksheet Writing Language — Markdown
        </li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">Neo Markdown syntax</li>
      </a>
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">Manage Worksheet</li>
      </a>
      <a href="#anchor5">
        <li class="tech-list-li" id="tech-list-li">Conclusion</li>
      </a>
    </ul>
    <div class="tech-contents">
      <div>
        <p class="tech-title" id="anchor1">Introduction</p>
        <p class="tech-contents-text">
          <b
            >Machbase Neo is an all-in-one package solution built on the
            foundation of the Machbase time series database, designed to
            maximize user convenience.</b
          >
        </p>
        <p class="tech-contents-text">
          For detailed information about Machbase Neo, please refer to the
          website at
          <a class="tech-contents-link" href="https://neo.machbase.com."
            >https://neo.machbase.com.</a
          >
        </p>
        <p class="tech-contents-text">
          Machbase Neo features a worksheet function that allows you to create
          documents. It’s not just about creating static documents; you can
          directly execute SQL statements and display the results within the
          document. This enables an interactive understanding of the content.
        </p>
        <p class="tech-contents-text">
          Furthermore, through the created worksheets, you can share the usage
          and know-how of Machbase Neo among users, making it a means of
          exchanging information and knowledge among each other.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/neo-worksheet-1.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          &lt; Machbase Neo worksheet launch menu >
        </p>
        <p class="tech-title" id="anchor2">
          Worksheet Writing Language — Markdown
        </p>
        <p class="tech-contents-text">
          Create a worksheet using Markdown syntax. Markdown is a plain
          text-based, lightweight markup language that uses tags to represent
          the structure of documents and data. Markdown is primarily used for
          creating formatted documents with plain text, and its syntax is simple
          and easy to understand, making it accessible for anyone to learn and
          write documents.
        </p>
        <p class="tech-contents-text">
          Markdown is supported by a variety of service platforms, including
          GitHub, Notion, and Discord, and can be written and edited in most
          text editor environments.
        </p>
        <p class="tech-contents-text">
          However, since the file or image is not embedded directly into the
          document, you must upload it to a separate server and enter the file
          URL.
        </p>
        <p class="tech-title" id="anchor3">Neo Markdown syntax</p>
        <p class="tech-contents-text">
          General Markdown syntax can be found here
          <a class="tech-contents-link" href="https://neo.machbase.com."
            >(https://www.markdownguide.org/basic-syntax/).</a
          >
        </p>
        <p class="tech-contents-text">
          Machbase Neo has a button that allows you to execute SQL statements,
          which actually executes the SQL query on the Neo TSDB and displays the
          results on the screen.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/neo-worksheet-2.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          &lt; Example of executing SQL syntax in a Machbase Neo worksheet >
        </p>
        <p class="tech-contents-text">
          For example, if you write an SQL statement in the input field and
          choose the document type as SQL instead of Markdown, you can click the
          execution icon. That will execute the SQL query and display the
          results below. It’s not just about reading static documents; it allows
          to interactive integration with the TSDB to verify its functionality.
        </p>
        <p class="tech-contents-text">
          Not only SQL statements but also the TQL syntax provided by Machbase
          Neo can be executed instantly, with the results displayed on the
          screen.
        </p>
        <p class="tech-title" id="anchor4">Manage Worksheet</p>
        <p class="tech-contents-text">
          When you save a completed worksheet, it saves as a .wrk extension file
          in the path where Neo is installed. When you share a created file with
          other users, they can open and read it directly within Machbase Neo’s
          Worksheet.
        </p>
        <p class="tech-contents-text">
          When you install Machbase Neo, you can view tutorial articles that
          have already been written using worksheets.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/neo-worksheet-3.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          &lt; Machbase Neo built-in worksheet example >
        </p>
        <p class="tech-contents-text">
          On the Machbase NEO main screen, drag & drop the file to the DROP&OPEN
          area to open the document.
        </p>
        <p class="tech-title" id="anchor5">Conclusion</p>
        <p class="tech-contents-text">
          The worksheet feature in Machbase Neo is a simple and easy way to
          create and manage documents through the text-based Markdown language.
          You can write a Machbase Neo how-to or guide document and have others
          follow along as they read the worksheet document.
        </p>
        <p class="tech-contents-text">
          In particular, SQL syntax and TQL syntax can be executed directly on
          the documentation to check the results, so even beginners can easily
          follow along and understand the content on Neo.
        </p>
      </div>
    </div>
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
