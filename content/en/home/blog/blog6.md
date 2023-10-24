---
title: Blog
description: "Deep Anomaly Detection in Time Series (1): Anomaly Detection Model"
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
    <h4 class="blog-title">
      Deep Anomaly Detection in Time Series (1) : Time Series Data
    </h4>
    <div class="blog-date">
      <div>
        <span>by Machbase / 12 Jul 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">Introduction</li></a
      >
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">Time Series Data</li></a
      >
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">
          Anomaly in Time Series
        </li></a
      >
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">Conclusion</li>
      </a>
    </ul>
    <div class="tech-contents">
      <div>
        <p class="tech-title" id="anchor1">Introduction</p>
        <p class="tech-contents-text">
          Recently, 4th Industrial Revolution technologies are being actively
          researched and applied in the fields of manufacturing management
          systems, smart factories, and predictive maintenance. Among them,
          “Anomaly Detection” is a key field for implementing AI and IoT
          technologies, and is based on the principle of data analysis and
          application.
        </p>
        <p class="tech-contents-text">
          As a DBMS specializing in time series databases, Machbase has the core
          and original technology for anomaly detection due to its long history
          of boasting the world’s №1 speed and performance in this field. In
          this post, I will give you an overview of Deep Anomaly Detection, the
          characteristics of time series data, and types of anomalies.
        </p>
        <p class="tech-contents-text">
          Let’s start by looking at Time Series data itself.
        </p>
        <p class="tech-title" id="anchor2">Time Series Data</p>
        <p class="tech-contents-text">
          we need to look at the data itself. Data called a time series, or time
          series, is a sequence of data placed at regular time intervals. What
          are the characteristics of this time series data? Let’s look at it
          from two perspectives.
        </p>
        <div class="tech-contents-title">Time Series Decomposition</div>
        <p class="tech-contents-text">
          First, let’s look at how time series data is organized. Time series
          data can be decomposed into Seasonality, Trend, and Remainder.
          Seasonality is a recurring pattern with short intervals throughout the
          time series data, Trend is the overall increase or decrease in the
          time series, and Remainder is the irregularities that cannot be
          explained by these two factors.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/anomaly-1.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          The organization of time series data: data consists of seasonality,
          trend, and residuals (1)
        </p>
        <p class="tech-contents-text">
          For example, temperature or gasoline engines (in some cases, seasonal
          changes may be included in the temperature data)
        </p>
        <div class="tech-contents-text">
          <b>&lt;Temperature in Seoul at 1-hour intervals></b>
        </div>
        <ul class="tech-ul">
          <li>Seasonality : temperature change according to day and night</li>
          <li>
            Trend : Changes in temperature due to weather and seasonal changes
          </li>
          <li>
            Remainder : Noise that cannot be expressed as Seasonality or Trend
          </li>
        </ul>
        <div class="tech-contents-text">
          <b>&lt;Vibration sensor attached to gasoline engine></b>
        </div>
        <ul class="tech-ul">
          <li>
            Seasonality : Periodic vibration changes due to intake, compression,
            explosion, and exhaust
          </li>
          <li>
            Trend : Changes in sensor values due to changes in vehicle speed,
            aging of vehicles, etc.
          </li>
          <li>
            Remainder : Noise that cannot be expressed as Seasonality or Trend
          </li>
        </ul>
        <p class="tech-contents-text">
          This process of identifying the type of time series data and
          categorizing it into Trend, Seasonality, and Remainder is called Time
          Series Decomposition. Time series decomposition can be done in two
          ways depending on the shape of the data: “Additive Model” and
          “Multiplicative Model”.
        </p>
        <p class="tech-contents-text">
          The Additive Model time series is the sum of Seasonality, Trend, and
          Remainder, and the Multiplicative Model time series is the product of
          the three.
        </p>
        <p class="tech-contents-text">
          In the time series of the Additive Model, the frequency and amplitude
          of the data are relatively constant even if the trend changes, but in
          the case of the Multiplicative Model, the frequency and amplitude
          change together as the trend of the data changes.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/anomaly-2.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          Additive Model & Multiplicative Model(2)
        </p>
        <p class="tech-contents-text">
          When predicting time series data, we can use decomposition to simplify
          the problem, but what about from a DAD perspective? We can think of a
          case where the remaining variance of the vibration sensor increases as
          the bearing attached to the vibration sensor ages, or the trend of the
          monthly average temperature increases abnormally due to global
          warming, or the seasonality that has always been the same is suddenly
          deviated from. In other words, it is important to understand the
          components of the time series even in anomaly detection problems.
        </p>
        <div class="tech-contents-title">Univariate vs. Multivariate</div>
        <p class="tech-contents-text">
          This time, let’s categorize time series data according to the number
          of dependent variables. Let’s say you want to predict the weather. If
          you want to predict the temperature in Busan, you can use the
          temperature in the past and the temperature in the future. If you want
          to predict the wind speed, you can consider only the wind speed in the
          past and the wind speed in the future. When there is only one variable
          that depends on time, such as ‘time-temperature’ and ‘time-wind
          speed’, it is called a univariate time series.
        </p>
        <p class="tech-contents-text">
          However, weather cannot be predicted by temperature, wind speed, and
          precipitation in isolation: if it’s sunny, the temperature will rise,
          and if there’s a cold snap, the wind will pick up and the temperature
          will drop. It’s only when the weather, precipitation, humidity, and
          wind are combined that we can predict the weather. When each of these
          dependent variables is affected not only by time but also by other
          dependent variables to form a complex time series, it is called a
          Multivariate Time Series.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/anomaly-3.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          Example of a multivariate time series: Weather forecast for Busan from
          April 27 to April 29 (Korea Meteorological Administration)
        </p>
        <p class="tech-contents-text">
          Not surprisingly, multivariate time series are more difficult to
          analyze than univariate time series. Traditionally, ARIMA
          (Auto-Regressive Integrated Moving Average) models have been used for
          univariate time series, and VAR (Vector Auto-Regressive) models have
          been used for multivariate time series, but due to the complexity of
          multivariate time series, they are not very effective.
        </p>
        <p class="tech-contents-text">
          Nowadays, a lot of research has been done on deep learning, and it is
          possible to recognize patterns in complex problems, so there is a
          movement to solve the analysis of multivariate time series with deep
          learning.
        </p>
        <div class="tech-title" id="anchor3">Anomaly in Time Series</div>
        <p class="tech-contents-text">
          So, what are the different types of anomalies in a time series?
          Different papers have different ways of categorizing time series
          anomalies, but in this article, I’ll introduce the three types that
          more papers have identified.
        </p>
        <p class="tech-contents-title">Point Anomaly</p>
        <p class="tech-contents-text">
          Data that completely deviates from the distribution of normal data is
          known as a point anomaly or global outlier. They are the most commonly
          thought of anomalies and also the most studied. For example, in the
          following image, you can see that the data corresponding to the red
          dots deviates significantly from the distribution of the rest of the
          data. These two red pieces of data can be referred to as Point
          Anomalies.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/anomaly-4.png" alt="" />
        </div>
        <p class="tech-contents-link-text">Example of a Point Anomaly (3)</p>
        <p class="tech-contents-title">Contextual Anomaly</p>
        <p class="tech-contents-text">Also known as a conditional anomaly.</p>
        <p class="tech-contents-text">
          It refers to data where there is nothing strange about the
          distribution of the data itself, but the flow or context of the data
          is not normal. It’s when you expect to see certain data at a certain
          point in time, but you get something else. For example, in the
          following graph.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/anomaly-5.png" alt="" />
        </div>
        <p class="tech-contents-link-text">Example of Contextual Anomaly (4)</p>
        <p class="tech-contents-title">Group Anomaly</p>
        <p class="tech-contents-text">
          Group Anomalies, or Collective Anomalies as they are also called, are
          data that looks normal at first glance when viewed in isolation.
          However, it’s the type of anomaly that looks abnormal when viewed as a
          group of data.
        </p>
        <p class="tech-contents-text">
          In the following image, we see a series of $75 payments over three
          days starting on July 14. If it was a single payment, you might treat
          it as normal, but if it’s the same payment over and over again over
          the course of several days, it’s obviously suspicious. Or, as another
          example, consider a vibration sensor whose graph is slightly but
          consistently trending upward. It might look normal when you look at a
          single or short-term data point, but if it’s consistently upward over
          the long term, shouldn’t you take a look at your device?
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/anomaly-6.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          Group Anomaly : Detecting anomalies in credit card usage(4)
        </p>
        <p class="tech-contents-text">
          These are the three types of anomalies. There are still more
          difficulties in detecting group anomalies than point anomalies or
          contextual anomalies, but recently, there have been many studies to
          solve them with deep learning methods such as Variational AutoEncoders
          (VAE), Adversarial AutoEncoders (AAE), and Generative Adversarial
          Networks (GAN). If you want to apply anomaly detection for smart
          factories, you will need to consider all three types of anomalies and
          build a model.
        </p>
        <p class="tech-title" id="anchor4">Conclusion</p>
        <p class="tech-contents-text">
          Techniques for anomaly detection are constantly being developed, with
          faster and more accurate models becoming available. Deciding which
          models to use in real-world applications and in which data collection
          environments is crucial.
        </p>
        <p class="tech-contents-text">
          In addition, anomaly detection is being applied and utilized in
          various industries by utilizing artificial intelligence and the
          Internet of Things as a basic step for factory automation smart
          factories. In addition, it is very important to select a time series
          database that is specialized for this purpose by compensating for the
          limitations of data collection, processing, and analysis that occur in
          existing relational DBMSs. So far, we have covered various contents on
          anomaly detection, and we will see you next time with more good
          contents.
        </p>
        <p class="tech-contents-text">Thank you.</p>
        <ul class="tech-ul">
          <li>
            Verbesselt, Jan, et al. “Detecting trend and seasonal changes in
            satellite image time series.” Remote sensing of Environment 114.1
            (2010): 106-115.
          </li>
          <li>
            <a
              class="tech-contents-link"
              href="https://kourentzes.com/forecasting/2014/11/09/additive-and-multiplicative-seasonality/"
              >https://kourentzes.com/forecasting/2014/11/09/additive-and-multiplicative-seasonality/</a
            >
          </li>
          <li>
            Talagala, Priyanga Dilini, et al. “Anomaly detection in streaming
            nonstationary temporal data.” Journal of Computational and Graphical
            Statistics 29.1 (2020): 13-27./li>
          </li>
          <li>
            Chalapathy, Raghavendra, and Sanjay Chawla. “Deep learning for
            anomaly detection: A survey.” arXiv preprint arXiv:1901.03407
            (2019).
          </li>
        </ul>
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
