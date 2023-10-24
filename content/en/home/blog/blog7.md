---
title: Blog
description: "A Database for database-for-things"
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
    <h4 class="blog-title">A Database for database-for-things</h4>
    <div class="blog-date">
      <div>
        <span>by Grey Shim / 12 Jul 2023</span>
      </div>
    </div>
    <div class="tech-img-wrap">
      <img class="tech-img" src="../../img/database-1.jpg" alt="" />
    </div>
    <p class="tech-contents-link-text">
      Photo by
      <a
        class="tech-contents-link"
        href="https://unsplash.com/ko/@sortino?utm_source=medium&utm_medium=referral"
        >Joshua Sortino</a
      >
      on
      <a
        class="tech-contents-link"
        href="https://unsplash.com/ko?utm_source=medium&utm_medium=referral"
        >Unsplash</a
      >
    </p>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">Introduction</li>
      </a>
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">
          Types and Characteristics of Internet of Things Data
        </li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">
          Chellenges with IoT sensor data
        </li>
      </a>
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">
          Machbase optimized for IoT data
        </li>
      </a>
    </ul>
    <div class="tech-contents">
      <div>
        <p class="tech-title" id="anchor1">Introduction</p>
        <p class="tech-contents-text">
          The Internet of Things (IoT) refers to the communication and
          processing of data between numerous devices through an Internet
          network. IoT devices include sensors, digital actuators, and mobile
          terminals, excluding general desktops and laptops.
        </p>
        <p class="tech-contents-text">
          This architecture is regardless of the data quality that developers
          need to focus on, there are a lot more other things that need to be
          done to make the service itself work.
        </p>
        <p class="tech-contents-text">
          However, IoT data has slightly different characteristics.
        </p>
        <p class="tech-contents-text">
          Typically, large amounts of data occur sporadically in many places,
          making it very difficult to process with existing data solutions.
        </p>
        <p class="tech-contents-text">
          In this post, we will look at the types and characteristics of IoT
          data, and talk about the challenges that must be overcome to process
          IoT data.
        </p>
        <div class="tech-title" id="anchor2">
          Types and Characteristics of Internet of Things Data
        </div>
        <p class="tech-contents-text">
          The Internet of Things was once a term referring only to systems using
          RFID data, but with the development of ICT technology, more and more
          types of data have been included.
        </p>
        <p class="tech-contents-text">
          Then, there are various types of data, including RFID, and let’s look
          at their characteristics.
        </p>
        <div class="tech-contents-title">
          RFID(Radio Frequency Identification)
        </div>
        <p class="tech-contents-text">
          RFID is a tag that transmits and receives information recorded by
          radio waves and can be attached to or included in equipment. An RFID
          tag consists of an IC chip that stores data and an antenna that
          transmits and receives data, and the tag data is communicated
          wirelessly through a tag reader.
        </p>
        <p class="tech-contents-text">
          RFID is used in a wide variety of fields. For example:
        </p>
        <ul class="tech-ul">
          <li>passport</li>
          <li>Cell Phone</li>
          <li>logistics management</li>
          <li>Inventory Management</li>
          <li>healthcare</li>
        </ul>
        <p class="tech-contents-text">
          Tags can be used in many fields as they become very inexpensive
          through mass production, but they are still more expensive than bar
          codes, so diffusion is slow in areas such as distribution.
        </p>
        <p class="tech-contents-text">
          When RFID is used in logistics, the movement trajectory according to
          the time series can be tracked based on the tag’s location information
          and time information.
        </p>
        <div class="tech-contents-title">Log Data</div>
        <p class="tech-contents-text">
          Log data generated by numerous S/W and H/W plays a very important role
          in managing devices and software.
        </p>
        <p class="tech-contents-text">
          However, since log data is created in text format and can be
          automatically deleted when it reaches a certain amount, other methods
          are needed for long-term collection and analysis of data.
        </p>
        <p class="tech-contents-text">
          Since it is not structured data, a conversion process such as parsing
          of log messages is required to express it as a relational DBMS schema.
        </p>
        <p class="tech-contents-text">
          Log data is recorded in various formats depending on the program that
          creates it, so it is not easy to process.
        </p>
        <div class="tech-contents-title">Location and environmental data</div>
        <p class="tech-contents-text">
          As can be seen in the example of RFID, the location information of the
          place where the data is generated is very important for moving object
          data and meteorological environment data.
        </p>
        <p class="tech-contents-text">
          In general, location information is obtained using a global
          positioning system (GPS). GPS information obtained through several
          satellites can only know an approximate location due to its
          characteristics, and it is difficult to obtain accurate location
          information.
        </p>
        <p class="tech-contents-text">
          In special circumstances, more detailed information can be obtained
          using a local positioning system.
        </p>
        <p class="tech-contents-text">
          Positional data of non-moving equipment can also be treated as very
          important information.
        </p>
        <p class="tech-contents-text">
          For example, by combining environmental information such as
          temperature, humidity, and air pressure from a sensor floating on the
          sea with location information, it is possible to obtain information
          that is very useful for weather forecasts and disaster warnings.
        </p>
        <p class="tech-contents-text">
          Location and environmental data are being studied in convergence with
          technologies such as geographic information systems and mobile
          computing.
        </p>
        <div class="tech-contents-title">Time series data — sensor data</div>
        <p class="tech-contents-text">
          We live surrounded by numerous sensors. Mobile phones are also
          equipped with numerous sensors such as cameras, GPS, and
          accelerometers, and there are many sensors in factories and public
          sectors (roads, railways, ports, and airports).
        </p>
        <p class="tech-contents-text">
          Analyzing this sensor data can solve previously unactionable problems
          in various areas. Each sensor has a unique identifier, and records and
          transmits the read data value and measurement time together.
        </p>
        <p class="tech-contents-text">
          Data recorded in the form of &lt;Timestamp, sensor identifier, sensor
          value> is stored sequentially according to the input time for later
          data analysis, and this is called time-series sensor data.
        </p>
        <div class="tech-contents-title">Time series data — control data</div>
        <p class="tech-contents-text">
          Not only sensor data collected from actuators that change in real
          time, but also control signal data for controlling the actuators are
          recorded in time series.
        </p>
        <p class="tech-contents-text">
          Since these data are data that is changing in real time, a large
          amount of data is generated, making it difficult to store and analyze.
          Afterwards, diagnosis can be made by analyzing existing data such as
          accident analysis, defect prediction, quality improvement, and
          production control.
        </p>
        <div class="tech-contents-title">
          Time series data — Historical Data
        </div>
        <p class="tech-contents-text">
          When sensor data including time is collected, this data becomes
          historical data. The amount of data greatly increases according to the
          data collection cycle.
        </p>
        <p class="tech-contents-text">
          This is a problem to be solved with DBMS because the shorter the data
          collection cycle for detailed analysis, the larger the amount of data.
        </p>
      </div>
    </div>
    <div class="tech-img-wrap">
      <img class="tech-img" src="../../img/database-2.jpg" alt="" />
    </div>
    <p class="tech-contents-link-text">
      Photo by
      <a
        class="tech-contents-link"
        href="https://unsplash.com/ko/@campaign_creators?utm_source=medium&utm_medium=referral"
        >Campaign Creators</a
      >
      on
      <a
        class="tech-contents-link"
        href="https://unsplash.com/ko?utm_source=medium&utm_medium=referral"
        >Unsplash</a
      >
    </p>
    <div class="tech-title" id="anchor3">Chellenges with IoT sensor data</div>
    <p class="tech-contents-text">
      As discussed above, the data generated from a large number of sensors has
      the characteristics of a time series and is stored historically.
    </p>
    <p class="tech-contents-text">
      In the case of a DBMS operating in a single system, index and search
      performance inevitably deteriorates as the storage period increases, and
      it is difficult to maintain uninterrupted collection and storage. Finally,
      Bigdata platforms such as Hadoop emerged to overcome the limitations of
      DBMS, which cannot process PB units of data.
    </p>
    <p class="tech-contents-text">
      However, distributed processing such as Map Reduce is optimized for batch
      processing (distributed storage and retrieval), so real-time data analysis
      has limitations.
    </p>
    <p class="tech-contents-text">
      In other words, new methods are needed for real-time processing of IoT
      sensor data.
    </p>
    <div class="tech-contents-title">Query language</div>
    <p class="tech-contents-text">
      IoT sensor data includes structured data as well as semi-structured data.
      SQL is used as a representative query language for structured data, but
      the query language for semi-structured data is not unified.
    </p>
    <p class="tech-contents-text">
      Of course, with the introduction of the big data system, No-SQL query
      languages appeared, but various disparate languages are still being used
      interchangeably. Eventually, as SQL on Hadoop products such as Spark and
      Impala spread, the SQL query language is being used a lot again.
    </p>
    <div class="tech-contents-title">Interface</div>
    <p class="tech-contents-text">
      DBMS supporting SQL language provides traditional interfaces such as
      ODBC/JDBC, but Operational Historian products often use JSON-based query
      interface through HTTP protocol through REST API.
    </p>
    <p class="tech-contents-text">
      As many operating environments move to the web standard, REST API, which
      is easy to use, has become an interface that must be supported.
    </p>
    <div class="tech-contents-title">transaction processing</div>
    <p class="tech-contents-text">
      Transactions (e.g. ACID, Two-phase locking) are difficult to perform in
      distributed data systems that must process more than 100 billion data per
      second in real time. Because time-series data does not have an update
      operation until it is completely deleted, RDBMS transaction processing
      based on perfect ACID causes performance problems.
    </p>
    <p class="tech-contents-text">
      In real-time processing of massive IoT data, a new efficient data
      processing technique that reflects the characteristics of time-series data
      is required rather than traditional ACID-based transactions.
    </p>
    <div class="tech-contents-title">
      Statistical processing of time series data
    </div>
    <p class="tech-contents-text">
      Time series data frequently requires statistical calculations such as sum,
      count, avg, and sampling. These statistics are used for visualization and
      advanced analysis.
    </p>
    <p class="tech-contents-text">
      Since it is very difficult for RDBMS to input large amounts of data in
      real time and perform statistical work at the same time, Stream DB has
      recently been attracting new attention.
    </p>
    <div class="tech-title" id="anchor4">Machbase optimized for IoT data</div>
    <p class="tech-contents-text">
      Machbase Database is the only database that meets the performance and
      features required for IoT data processing.
    </p>
    <ul class="tech-ul">
      <li>Real-time bulk data processing</li>
      <li>Provides an easy-to-use and efficient query language</li>
      <li>Efficient transaction processing</li>
      <li>Statistical calculation of time series data</li>
    </ul>
    <div class="tech-contents-title">Real-time processing of bulk data</div>
    <p class="tech-contents-text">
      Machbase, which adopts a distributed data storage and query structure, can
      input and index 2 million data in a single device, and can process more
      than 10 million sensor data per second as its performance increases as
      more devices are added.
    </p>
    <p class="tech-contents-text">
      It has a dedicated API for high-speed data input and an index number
      structure that can create indexes at high speed.
    </p>
    <p class="tech-contents-text">
      Performance and space can be expanded by adding equipment to the cluster
      even with time-dependent addition of time-series data.
    </p>
    <div class="tech-contents-title">
      Efficient query language provision and interface
    </div>
    <p class="tech-contents-text">
      Provides SQL language optimized for data processing. No-SQL products are
      starting to offer the SQL language again.
    </p>
    <p class="tech-contents-text">
      By providing an inverted index and related syntax for efficiently
      searching semi-structured data, it is possible to easily search and
      process semi-structured data.
    </p>
    <p class="tech-contents-text">
      Provides REST API as well as ODBC/JDBC which is SQL standard interface
    </p>
    <div class="tech-contents-title">Efficient Transaction Processing</div>
    <ul class="tech-ul">
      <li>Devising optimal transaction techniques for time series data</li>
      <li>
        Update is not provided, but insert and delete are possible, and
        consistency of data and index is maintained through recovery process
        even in case of restart due to node failure.
      </li>
      <li>
        Enterprise edition fundamentally solves data loss due to node failure by
        using a distributed data storage technique
      </li>
    </ul>
    <div class="tech-contents-title">Processing time series statistics</div>
    <ul class="tech-ul">
      <li>
        Automatic statistics function for time-series sensor data: Statistics
        are automatically generated for each unit time (second, minute, hour)
        and sensor identifier of the input sensor data.
      </li>
      <li>
        Provides an extended query conditional clause optimized for time series
        data.
      </li>
      <li>
        Machbase Database is a product implemented considering both functions
        and performance requirements for processing time series data, and is
        suitable for processing Internet of Things data.
      </li>
    </ul>
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
