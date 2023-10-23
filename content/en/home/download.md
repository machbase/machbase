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
  <section class="download_section0">
    <div>
      <h1 class="sub_page_title">Download</h1>
      <p class="sub_page_titletext">
        Machbase`s TSDB product line consists of the newly launched NEO product,
        offering integrated functionality,<br />
        and the existing CLASSIC product. Users can choose and utilize the
        product that best suits their environment.
      </p>
    </div>
  </section>
  <section class="section1">
    <div class="sub_titlebox">
      <h4 class="sub_page_sub_title download_marin_top">Machbase NEO</h4>
      <div class="bar"><img src="../img/bar.png" /></div>
    </div>
    <div class="downlaod_explanation_wrap">
      <div class="download_explanation">
        <div>
          <p class="explanation_title">NEO Product Features :</p>
          <p class="explanation_text">
            ・Ideal for customers seeking to quickly and easily collect,
            integrate, and visualize time-series data
          </p>
          <p class="explanation_text">
            ・Single binary supports MQTT, HTTP, gRPC, SSH servers and includes
            web-based built-in visualization tools
          </p>
          <p class="explanation_text">
            ・Utilities and SDKs for client are not included (Utilize it
            included in the CLASSIC)
          </p>
          <p class="explanation_text">・Embedded with CLASSIC engine</p>
          <p class="explanation_text">・MacOS supported</p>
          <p class="explanation_text">・Open source available through GitHub</p>
        </div>
      </div>
    </div>
    <div class="download_table_wrap">
      <table class="download_table1">
        <tr class="tabel_title">
          <th>OS</th>
          <th>CPU Architecture</th>
          <th class="border_top_right" colspan="2">Download</th>
        </tr>
        <tr class="top_line">
          <!-- <td class="pricing_table_subtitle download_th1_1" rowspan="5">
            Edge
          </td> -->
          <td class="download_th1_1 pricing_table_subtitle" rowspan="3">
            Linux
          </td>
          <td class="download_th1_2">arm32</td>
          <td class="download_th1_4">
            <span
              >wget
              https://github.com/machbase/neo-server/releases/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-arm32.zip
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="neoLinuxArm32" class="download_copy_btn">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://github.com/machbase/neo-server/releases/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-arm32.zip"
              >
                <img src="../img/btn_newlink.png" />
              </a>
            </button>
          </td>
        </tr>
        <tr class="top_line">
          <td class="download_th1_3">arm64</td>
          <td class="download_th1_4">
            <span
              >wget
              https://github.com/machbase/neo-server/releases/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-arm64.zip
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="neoLinuxArm64" class="download_copy_btn">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://github.com/machbase/neo-server/releases/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-arm64.zip"
              >
                <img src="../img/btn_newlink.png" />
              </a>
            </button>
          </td>
        </tr>
        <tr class="top_line">
          <td>x64</td>
          <td class="download_th1_4">
            <span
              >wget
              https://github.com/machbase/neo-server/releases/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-amd64.zip
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="neoLinuxX64" class="download_copy_btn">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://github.com/machbase/neo-server/releases/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-amd64.zip"
              >
                <img src="../img/btn_newlink.png" />
              </a>
            </button>
          </td>
        </tr>
        <tr class="top_line">
          <td rowspan="2">MacOS</td>
          <td>arm64(M1)</td>
          <td class="download_th1_4">
            <span
              >wget
              https://github.com/machbase/neo-server/releases/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-darwin-arm64.zip
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="neoMacArm64" class="download_copy_btn">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://github.com/machbase/neo-server/releases/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-darwin-arm64.zip"
              >
                <img src="../img/btn_newlink.png" />
              </a>
            </button>
          </td>
        </tr>
        <tr class="top_line">
          <td>x64</td>
          <td class="download_th1_4">
            <span
              >wget
              https://github.com/machbase/neo-server/releases/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-darwin-amd64.zip
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="neoMacX64" class="download_copy_btn">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://github.com/machbase/neo-server/releases/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-darwin-amd64.zip"
              >
                <img src="../img/btn_newlink.png" />
              </a>
            </button>
          </td>
        </tr>
        <tr class="top_line">
          <td>Windows</td>
          <td>x64</td>
          <td class="download_th1_4">
            <span
              >wget
              https://github.com/machbase/neo-server/releases/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-windows-amd64.zip
            </span>
          </td>
          <td class="puple border_bottom_right">
            <button data-code="neoWindowsX64" class="download_copy_btn">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://github.com/machbase/neo-server/releases/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-windows-amd64.zip"
              >
                <img src="../img/btn_newlink.png" />
              </a>
            </button>
          </td>
        </tr>
      </table>
    </div>
  </section>
  <section class="section2">
    <div class="sub_titlebox">
      <h4 class="sub_page_sub_title download_marin_top">
        Machbase Classic (+SDK)
      </h4>
      <div class="bar"><img src="../img/bar.png" /></div>
    </div>
    <div class="downlaod_explanation_wrap">
      <div class="download_explanation">
        <div>
          <p class="explanation_title">Classic (+SDK) Product Features :</p>
          <p class="explanation_text">
            ・Suitable for users and developers familiar with traditional
            database environments
          </p>
          <p class="explanation_text">
            ・Provides a lightweight database server binary for console
            environments
          </p>
          <p class="explanation_text">
            ・Various client console-based utilities and Software Development
            Kits (SDKs) provided (ODBC, JDBC, C#,
          </p>
          <p class="explanation_text2">Python, etc.)</p>
          <p class="explanation_text">・Offers samples for various languages</p>
        </div>
      </div>
    </div>
    <div class="download_table_wrap2">
      <table class="download_table2">
        <tr class="tabel_title">
          <th class="download_th1_2">OS</th>
          <th class="download_th1_3">CPU Architecture</th>
          <th class="border_top_right" colspan="2">Download</th>
        </tr>
        <tr class="top_line">
          <td rowspan="2">Linux</td>
          <td>64bit/x64</td>
          <td class="download_th1_4">
            <span
              >wget
              https://stage.machbase.com/package/download/machbase-SDK-8.0.2.official-LINUX-X86-64-release.tgz
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="sdkLinuxX64" class="download_copy_btn">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://stage.machbase.com/package/download/machbase-SDK-8.0.2.official-LINUX-X86-64-release.tgz"
              >
                <img src="../img/btn_newlink.png" />
              </a>
            </button>
          </td>
        </tr>
        <tr class="top_line">
          <td>64bit/ARM</td>
          <td class="download_th1_4">
            <span
              >wget
              https://stage.machbase.com/package/download/machbase-SDK-8.0.2.official-LINUX-ARM_CORTEX_A53-64-release.tgz
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="sdkLinuxArm" class="download_copy_btn">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://stage.machbase.com/package/download/machbase-SDK-8.0.2.official-LINUX-ARM_CORTEX_A53-64-release.tgz"
              >
                <img src="../img/btn_newlink.png" />
              </a>
            </button>
          </td>
        </tr>
        <tr class="top_line">
          <td rowspan="2">Windows</td>
          <td>64bit/x64</td>
          <td class="download_th1_4">
            <span
              >wget
              https://stage.machbase.com/package/download/machbase-SDK-8.0.2.official-WINDOWS-X86-64-release.msi</span
            >
          </td>
          <td class="puple download_th1_5">
            <button data-code="sdkWindowsX64" class="download_copy_btn">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://stage.machbase.com/package/download/machbase-SDK-8.0.2.official-WINDOWS-X86-64-release.msi"
              >
                <img src="../img/btn_newlink.png" />
              </a>
            </button>
          </td>
        </tr>
        <tr class="top_line">
          <td>32bit SDK</td>
          <td class="download_th1_4">
            <span
              >wget
              https://stage.machbase.com/package/download/machbase-SDK-8.0.2.official-WINDOWS-X86-32-release.msi
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="sdkWindows32" class="download_copy_btn">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://stage.machbase.com/package/download/machbase-SDK-8.0.2.official-WINDOWS-X86-32-release.msi"
              >
                <img src="../img/btn_newlink.png" />
              </a>
            </button>
          </td>
        </tr>
        <tr class="top_line">
          <td rowspan="2">Mac OS</td>
          <td>64bit/ARM</td>
          <td class="download_th1_4">
            <span
              >wget
              https://stage.machbase.com/package/download/machbase-SDK-8.0.2.official-DARWIN-ARM_M1-64-release.tgz
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="sdkMacArm" class="download_copy_btn">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://stage.machbase.com/package/download/machbase-SDK-8.0.2.official-DARWIN-ARM_M1-64-release.tgz"
              >
                <img src="../img/btn_newlink.png" />
              </a>
            </button>
          </td>
        </tr>
        <tr class="top_line">
          <td>64bit/x64</td>
          <td class="download_th1_4">
            <span
              >wget
              https://stage.machbase.com/package/download/machbase-SDK-8.0.2.official-DARWIN-X86-64-release.tgz
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="sdkMacX64" class="download_copy_btn">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://stage.machbase.com/package/download/machbase-SDK-8.0.2.official-DARWIN-X86-64-release.tgz"
              >
                <img src="../img/btn_newlink.png" />
              </a>
            </button>
          </td>
        </tr>
      </table>
    </div>
  </section>
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
          </div>ㄷ
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
</body>
<script>
  const jsonData = {
    codes: {
      neoLinuxArm32:
        "https://github.com/machbase/neo-server/releases/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-arm32.zip",
      neoLinuxArm64:
        "https://github.com/machbase/neo-server/releases/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-arm64.zip",
      neoLinuxX64:
        "https://github.com/machbase/neo-server/releases/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-amd64.zip",
      neoMacArm64:
        "https://github.com/machbase/neo-server/releases/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-darwin-arm64.zip",
      neoMacX64:
        "https://github.com/machbase/neo-server/releases/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-darwin-amd64.zip",
      neoWindowsX64:
        "https://github.com/machbase/neo-server/releases/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-windows-amd64.zip",
      sdkLinuxX64:
        "https://stage.machbase.com/package/download/machbase-SDK-8.0.2.official-LINUX-X86-64-release.tgz",
      sdkLinuxArm:
        "https://stage.machbase.com/package/download/machbase-SDK-8.0.2.official-LINUX-ARM_CORTEX_A53-64-release.tgz",
      sdkWindowsX64:
        "https://stage.machbase.com/package/download/machbase-SDK-8.0.2.official-WINDOWS-X86-64-release.msi",
      sdkWindows32:
        "https://stage.machbase.com/package/download/machbase-SDK-8.0.2.official-WINDOWS-X86-32-release.msi",
      sdkMacArm:
        "https://stage.machbase.com/package/download/machbase-SDK-8.0.2.official-DARWIN-ARM_M1-64-release.tgz",
      sdkMacX64:
        "https://stage.machbase.com/package/download/machbase-SDK-8.0.2.official-DARWIN-X86-64-release.tgz",
    },
  };
  function copyToClipboard(text, button) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand("copy");
    document.body.removeChild(textArea);
    alert("Copied");
  }
  const copyButtons = document.querySelectorAll(".download_copy_btn");
  copyButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const codeType = button.getAttribute("data-code");
      const codeToCopy = jsonData.codes[codeType];
      copyToClipboard(codeToCopy, button);
    });
  });
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
