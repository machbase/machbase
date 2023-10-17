---
toc: false
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
          <a href="/kr/home"
            ><img src="../img/logo_machbase.png" alt=""
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
              <a class="menu_active_border" id="menuActiveBorder" href="/"
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
            <a href="https://www.cems.ai/">CEMS</a>
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
          <div class="docs-sub"><a href="/neo">Neo</a></div>
          <div class="docs-num"><a href="/dbms">Classic</a></div>
        </div>
      </li>
      <li><a href="/kr/home/download">Download</a></li>
      <li><a href="https://support.machbase.com/hc/en-us">Support</a></li>
      <li><a href="/kr/home/download">Contact US</a></li>
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
          <p class="explanation_title">네오 제품 특징 :</p>
          <p class="explanation_text">
            ・시계열 데이터를 빠르고 쉽게 수집, 통합, 시각화하려는 고객에게
            이상적입니다.
          </p>
          <p class="explanation_text">
            ・단일 바이너리는 MQTT, HTTP, gRPC, SSH 서버를 지원하고 웹 기반 내장
            시각화 도구를 포함합니다.
          </p>
          <p class="explanation_text">
            ・클라이언트용 유틸리티 및 SDK는 포함되어 있지 않습니다. (CLASSIC에
            포함되어 활용)
          </p>
          <p class="explanation_text">・CLASSIC 엔진 내장</p>
          <p class="explanation_text">・MacOS 지원</p>
          <p class="explanation_text">・GitHub를 통해 오픈소스 이용 가능</p>
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
              https://github.com/machbase/neo-server/releases/download/v8.0.3/machbase-neo-v8.0.3-linux-arm32.zip
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="neoLinuxArm32" class="download_copy_btn ">
                <img src="../img/btn_codecopy.png"
              /></button
            ><button class="download_link_btn">
                 <a
                href="https://github.com/machbase/neo-server/releases/download/v8.0.3/machbase-neo-v8.0.3-linux-arm32.zip"
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
              https://github.com/machbase/neo-server/releases/download/v8.0.3/machbase-neo-v8.0.3-linux-arm64.zip
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="neoLinuxArm64" class="download_copy_btn ">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://github.com/machbase/neo-server/releases/download/v8.0.3/machbase-neo-v8.0.3-linux-arm64.zip"
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
              https://github.com/machbase/neo-server/releases/download/v8.0.3/machbase-neo-v8.0.3-linux-amd64.zip
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="neoLinuxX64" class="download_copy_btn ">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn ">
              <a
                href="https://github.com/machbase/neo-server/releases/download/v8.0.3/machbase-neo-v8.0.3-linux-amd64.zip"
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
              https://github.com/machbase/neo-server/releases/download/v8.0.3/machbase-neo-v8.0.3-darwin-arm64.zip
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="neoMacArm64" class="download_copy_btn ">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://github.com/machbase/neo-server/releases/download/v8.0.3/machbase-neo-v8.0.3-darwin-arm64.zip"
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
              https://github.com/machbase/neo-server/releases/download/v8.0.3/machbase-neo-v8.0.3-darwin-amd64.zip
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="neoMacX64" class="download_copy_btn ">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://github.com/machbase/neo-server/releases/download/v8.0.3/machbase-neo-v8.0.3-darwin-amd64.zip"
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
              https://github.com/machbase/neo-server/releases/download/v8.0.3/machbase-neo-v8.0.3-windows-amd64.zip
            </span>
          </td>
          <td class="puple border_bottom_right">
            <button data-code="neoWindowsX64" class="download_copy_btn ">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://github.com/machbase/neo-server/releases/download/v8.0.3/machbase-neo-v8.0.3-windows-amd64.zip"
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
          <p class="explanation_title">Classic (+SDK) 제품 특징 :</p>
          <p class="explanation_text">
            ・기존 데이터베이스 환경에 익숙한 사용자 및 개발자에게 적합
          </p>
          <p class="explanation_text">
            ・콘솔 환경을 위한 경량 데이터베이스 서버 바이너리 제공
          </p>
          <p class="explanation_text">
            ・다양한 클라이언트 콘솔 기반 유틸리티 및 소프트웨어 개발 키트(SDK)
            제공(ODBC, JDBC, C#, 파이썬 등)
          </p>
          <p class="explanation_text2"></p>
          <p class="explanation_text">・다양한 언어의 샘플 제공</p>
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
              https://www.machbase.com/package/download/machbase-SDK-8.0.2.official-LINUX-X86-64-release.tgz
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="sdkLinuxX64" class="download_copy_btn ">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://www.machbase.com/package/download/machbase-SDK-8.0.2.official-LINUX-X86-64-release.tgz"
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
              https://www.machbase.com/package/download/machbase-SDK-8.0.2.official-LINUX-ARM_CORTEX_A53-64-release.tgz
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="sdkLinuxArm" class="download_copy_btn ">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://www.machbase.com/package/download/machbase-SDK-8.0.2.official-LINUX-ARM_CORTEX_A53-64-release.tgz"
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
              https://www.machbase.com/package/download/machbase-SDK-8.0.2.official-WINDOWS-X86-64-release.msi</span
            >
          </td>
          <td class="puple download_th1_5">
            <button data-code="sdkWindowsX64" class="download_copy_btn ">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://www.machbase.com/package/download/machbase-SDK-8.0.2.official-WINDOWS-X86-64-release.msi"
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
              https://www.machbase.com/package/download/machbase-SDK-8.0.2.official-WINDOWS-X86-32-release.msi
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="sdkWindows32" class="download_copy_btn ">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://www.machbase.com/package/download/machbase-SDK-8.0.2.official-WINDOWS-X86-32-release.msi"
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
              https://www.machbase.com/package/download/machbase-SDK-8.0.2.official-DARWIN-ARM_M1-64-release.tgz
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="sdkMacArm" class="download_copy_btn ">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://www.machbase.com/package/download/machbase-SDK-8.0.2.official-DARWIN-ARM_M1-64-release.tgz"
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
              https://www.machbase.com/package/download/machbase-SDK-8.0.2.official-DARWIN-X86-64-release.tgz
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="sdkMacX64" class="download_copy_btn ">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://www.machbase.com/package/download/machbase-SDK-8.0.2.official-DARWIN-X86-64-release.tgz"
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
            <a href="https://blog.naver.com/machbasekr" target="_blank"
              ><img class="sns-img" src="../img/naver.png"
            /></a>
          </div>
        </div>
      </div>
    </div>
    <div class="footer_tablet_inner">
      <div class="logo">
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
            <a href="https://blog.naver.com/machbasekr" target="_blank"
              ><img class="sns-img" src="../img/naver.png"
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
</body>
<script>
    const jsonData = {
codes: {
  neoLinuxArm32:"https://github.com/machbase/neo-server/releases/download/v8.0.3/machbase-neo-v8.0.3-linux-arm32.zip",
  neoLinuxArm64:"https://github.com/machbase/neo-server/releases/download/v8.0.3/machbase-neo-v8.0.3-linux-arm64.zip",
  neoLinuxX64:"https://github.com/machbase/neo-server/releases/download/v8.0.3/machbase-neo-v8.0.3-linux-amd64.zip",
  neoMacArm64:"https://github.com/machbase/neo-server/releases/download/v8.0.3/machbase-neo-v8.0.3-darwin-arm64.zip",
  neoMacX64:"https://github.com/machbase/neo-server/releases/download/v8.0.3/machbase-neo-v8.0.3-darwin-amd64.zip",
  neoWindowsX64:"https://github.com/machbase/neo-server/releases/download/v8.0.3/machbase-neo-v8.0.3-windows-amd64.zip",
  sdkLinuxX64:"https://www.machbase.com/package/download/machbase-SDK-8.0.2.official-LINUX-X86-64-release.tgz",
  sdkLinuxArm:"https://www.machbase.com/package/download/machbase-SDK-8.0.2.official-LINUX-ARM_CORTEX_A53-64-release.tgz",
  sdkWindowsX64:"https://www.machbase.com/package/download/machbase-SDK-8.0.2.official-WINDOWS-X86-64-release.msi",
  sdkWindows32:"https://www.machbase.com/package/download/machbase-SDK-8.0.2.official-WINDOWS-X86-32-release.msi",
  sdkMacArm:"https://www.machbase.com/package/download/machbase-SDK-8.0.2.official-DARWIN-ARM_M1-64-release.tgz",
  sdkMacX64:"https://www.machbase.com/package/download/machbase-SDK-8.0.2.official-DARWIN-X86-64-release.tgz"
},};
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
</script>
