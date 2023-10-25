---
title: Customers
description: "마크베이스와 함께 성장하는 기업"
---

<head>
  <link rel="stylesheet" type="text/css" href="../css/common.css" />
  <link rel="stylesheet" type="text/css" href="../css/style.css" />
</head>
<body>
 {{< home_menu_sub_kr >}}
  <section class="customers_section0">
    <div>
      <h2 class="sub_page_title">Customers</h2>
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
{{< home_footer_sub_kr >}}
<script>
  //change lang
  let language;
  let storageData = sessionStorage.getItem("lang");
  if (storageData) {
    language = storageData;
  } else {
    var userLang = navigator.language || navigator.userLanguage;
    if (userLang === "ko") {
      sessionStorage.setItem("lang", userLang);
      language = "kr";
    } else {
      sessionStorage.setItem("lang", "en");
      language = "en";
      let locationPath = location.pathname.split("/");
      locationPath.splice(1, 1);
      location.href = location.origin + locationPath.join("/");
    }
  }
</script>
