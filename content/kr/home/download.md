---
title: Download
description: "마크베이스의 TSDB 제품 라인은 통합 기능을 제공하는 새로 출시된 NEO 제품으로 구성됩니다.
그리고 기존 CLASSIC 제품. 사용자는 자신의 환경에 가장 적합한 제품을 선택하고 활용할 수 있습니다."
images:
  - /namecard/og_img.jpg
---

<head>
  <link rel="stylesheet" type="text/css" href="../css/common.css" />
  <link rel="stylesheet" type="text/css" href="../css/style.css" />
</head>
<body>
   {{< home_menu_sub_kr >}}
  <section class="download_section0">
    <div>
      <h2 class="sub_page_title">Download</h2>
      <p class="sub_page_titletext download-sub">
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
              >wget https://github.com/machbase/neo-server/releases/download/{{<
              neo_latestver >}}/machbase-neo-{{< neo_latestver
              >}}-linux-arm32.zip
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
              >wget https://github.com/machbase/neo-server/releases/download/{{<
              neo_latestver >}}/machbase-neo-{{< neo_latestver
              >}}-linux-arm64.zip
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
              >wget https://github.com/machbase/neo-server/releases/download/{{<
              neo_latestver >}}/machbase-neo-{{< neo_latestver
              >}}-linux-amd64.zip
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
              >wget https://github.com/machbase/neo-server/releases/download/{{<
              neo_latestver >}}/machbase-neo-{{< neo_latestver
              >}}-darwin-arm64.zip
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
              >wget https://github.com/machbase/neo-server/releases/download/{{<
              neo_latestver >}}/machbase-neo-{{< neo_latestver
              >}}-darwin-amd64.zip
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
              >wget https://github.com/machbase/neo-server/releases/download/{{<
              neo_latestver >}}/machbase-neo-{{< neo_latestver
              >}}-windows-amd64.zip
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
              https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-LINUX-X86-64-release.tgz
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="sdkLinuxX64" class="download_copy_btn">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-LINUX-X86-64-release.tgz"
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
              https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-LINUX-ARM_CORTEX_A53-64-release.tgz
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="sdkLinuxArm" class="download_copy_btn">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-LINUX-ARM_CORTEX_A53-64-release.tgz"
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
              https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-WINDOWS-X86-64-release.msi</span
            >
          </td>
          <td class="puple download_th1_5">
            <button data-code="sdkWindowsX64" class="download_copy_btn">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-WINDOWS-X86-64-release.msi"
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
              https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-WINDOWS-X86-32-release.msi
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="sdkWindows32" class="download_copy_btn">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-WINDOWS-X86-32-release.msi"
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
              https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-DARWIN-ARM_M1-64-release.tgz
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="sdkMacArm" class="download_copy_btn">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-DARWIN-ARM_M1-64-release.tgz"
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
              https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-DARWIN-X86-64-release.tgz
            </span>
          </td>
          <td class="puple download_th1_5">
            <button data-code="sdkMacX64" class="download_copy_btn">
              <img src="../img/btn_codecopy.png" /></button
            ><button class="download_link_btn">
              <a
                href="https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-DARWIN-X86-64-release.tgz"
              >
                <img src="../img/btn_newlink.png" />
              </a>
            </button>
          </td>
        </tr>
      </table>
    </div>
  </section>
  {{< home_footer_sub_kr >}}
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
        "https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-LINUX-X86-64-release.tgz",
      sdkLinuxArm:
        "https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-LINUX-ARM_CORTEX_A53-64-release.tgz",
      sdkWindowsX64:
        "https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-WINDOWS-X86-64-release.msi",
      sdkWindows32:
        "https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-WINDOWS-X86-32-release.msi",
      sdkMacArm:
        "https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-DARWIN-ARM_M1-64-release.tgz",
      sdkMacX64:
        "https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-DARWIN-X86-64-release.tgz",
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

</script>
