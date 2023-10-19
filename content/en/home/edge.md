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
                  <a class="dropdown-link" href="/neo" target="_blank">Neo</a>
                  <a class="dropdown-link" href="/dbms" target="_blank">Classic</a>
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
  <section class="product_sction0 section0">
    <div>
      <h1 class="sub_page_title">Tech Paper</h1>
      <p class="sub_page_titletext">
        “ Discover the top DBMS suites for edge computing and take your data
        processing to the next level ”
      </p>
    </div>
  </section>
  <section>
    <div class="tech-inner">
      <h4 class="sub_title main_margin_top">
        Edge Computing and Time series database
      </h4>
      <div class="bar"><img src="../img/bar.png" /></div>
      <div class="tech-contents">
        <div>
          <div class="tech-title">Why Edge Computing?</div>
          <p class="tech-contents-text">
            In recent years, Edge Computing has emerged as a pivotal
            technological concept, transforming the way we process and manage
            data. This paradigm shift has gained immense significance due to the
            growing proliferation of Internet of Things (IoT) devices and the
            increasing need for real-time, localized data processing. Edge
            Computing refers to the practice of processing data closer to its
            source, right at the "edge" of the network, rather than sending all
            data to centralized cloud servers for analysis. This approach brings
            several advantages, and this is where your software, a specialized
            time-series database engine, plays a crucial role.
          </p>
          <p class="tech-contents-title">The Importance of Edge Computing:</p>
          <ul class="tech-ul">
            <li>
              Low Latency and Real-time Processing: Applications that require
              real-time decision-making, such as industrial automation,
              autonomous vehicles, and remote monitoring, cannot afford the
              latency involved in sending data to distant data centers. Edge
              Computing reduces this delay by processing data locally, enabling
              quick responses.
            </li>
            <li>
              Bandwidth Efficiency: Transmitting large volumes of raw data to
              centralized cloud servers demands substantial bandwidth. Edge
              Computing reduces the amount of data transferred by sending only
              relevant, processed information, optimizing network usage and
              cost.
            </li>
            <li>
              Privacy and Security: Edge Computing addresses concerns about data
              privacy and security by keeping sensitive data localized. This
              mitigates potential risks associated with transmitting sensitive
              information over public networks.
            </li>
            <li>
              Offline Functionality: Edge Computing allows devices to operate
              autonomously even when connectivity to the cloud is lost. This is
              crucial for scenarios where continuous functionality is essential.
            </li>
            <li>
              Scalability: With the rapid growth of IoT devices, centralized
              cloud processing might become a bottleneck. Edge Computing
              distributes the processing load, ensuring scalability without
              overwhelming cloud resources.
            </li>
          </ul>
        </div>
        <div>
          <div class="tech-title">
            The Role of Time-Series Database Engines in Edge Computing
          </div>
          <p class="tech-contents-text">
            Time-series data, which records values over time, is prevalent in
            IoT applications—temperature readings, stock prices, energy
            consumption, etc. Time-series database engines excel at efficiently
            storing, retrieving, and analyzing such data.
          </p>
          <p class="tech-contents-title">
            Here's how they contribute to Edge Computing:
          </p>
          <ul class="tech-ul">
            <li>
              Data Storage and Retrieval: Time-series databases are optimized
              for high-throughput storage and retrieval of time-stamped data.
              This ensures quick access to historical and real-time data,
              crucial for decision-making at the edge.
            </li>
            <li>
              Aggregation and Analysis: These databases allow you to perform
              complex analyses on time-series data, even in resource-constrained
              environments. Aggregations, downsampling, and statistical
              computations can provide meaningful insights.
            </li>
            <li>
              Compression: With edge devices often having limited storage,
              time-series databases offer data compression techniques, enabling
              efficient storage of vast amounts of data in constrained
              environments.
            </li>
            <li>
              Data Contextualization: Time-series databases enable
              contextualizing data by associating it with relevant metadata.
              This contextual information enhances the value of the data
              collected from edge devices.
            </li>
            <li>
              Event Triggering: Time-series databases can support
              event-triggering mechanisms, enabling real-time alerts and actions
              based on predefined conditions, directly enhancing the
              responsiveness of edge applications.
            </li>
          </ul>
          <p class="tech-contents-text">
            The rise of Edge Computing is closely tied to the proliferation of
            IoT devices and the need for efficient, real-time data processing.
            Ability to manage time-series data efficiently aligns perfectly with
            the demands of Edge Computing, enabling localized processing, quick
            decision-making, and optimized resource usage. As industries
            continue to adopt and leverage Edge Computing, Time series DBMS
            stands at the forefront of enabling this transformative
            technological trend.
          </p>
        </div>
        <div>
          <div class="tech-title">
            Edge Computing and Data Processing Requirements
          </div>
          <p class="tech-contents-text">
            How much data do you need to process at the edge, and how fast?<br /><br />The
            clearer the answer to this question, the more likely it is that the
            vision of the future presented by Edge Computing will be at the
            customer's level.<br /><br />
            As an extreme example, the data processing requirements for edge
            devices for real-time monitoring and management of NC (Numerical
            Control) equipment are about 1T Bytes of data every two weeks. To
            translate this value more precisely, it needs to digest 872,628
            bytes per second.<br /><br />Converting this to the average size of
            real-world sensor data (about 20 bytes), we calculate that it should
            be able to store about 400,000+ events per second.<br /><br />Not
            only does the edge device need to ingest 400,000+ sensor data per
            second, but it also needs to store it in a secondary storage device
            for real-time analysis.<br /><br />Furthermore, if the environment
            requires the edge device to support high availability, it will
            require a higher level of data processing technology.<br /><br />In
            the end, different industries will have different types of data,
            different forms of data, and different amounts of data, and the
            requirements in various forms will become more and more stringent
            over time.
          </p>
        </div>
        <div>
          <div class="tech-title">Machbase and Edge Computing</div>
          <p class="tech-contents-text">
            As a real-time time series database, Machbase already offers a
            standard edition for ultra-fast data processing on edge
            computing.<br /><br />It can store 400,000 sensor data per second on
            a Raspberry PI 4, while utilizing CPU and disk usage very
            efficiently.<br /><br />Even if it is an edge device, Machbase with
            big data technology can store data to the storage limit, and the
            search and analysis of big data is excellent.<br /><br />Depending
            on your future roadmap, you can build a cluster on multiple edge
            devices, which means that your edge computing needs for high
            performance and high availability are well supported. To summarize
            Machbase's performance<br />
          </p>
          <p class="tech-contents-title">In ingestion point of view</p>
          <ul class="tech-ul">
            <li>In edge Device (ARM 2 core) : up to 500,000 rec/sec</li>
            <li>In single Server (INTEL 8 core) : up to 2,500,000 rec/sec</li>
            <li>In Cluster (16 node) : up to 100,000,000 rec/sec</li>
          </ul>
          <p class="tech-contents-title">In extraction point of view</p>
          <ul class="tech-ul">
            <li>
              0.1 seconds for extracting 10,000 random time ranges from a 400
              billion data store
            </li>
          </ul>
          <p class="tech-contents-title">In compression point of view</p>
          <ul class="tech-ul">
            <li>4TB store : around 1 trillion record</li>
          </ul>
          <p class="tech-contents-text">
            As you can see, Machbase already fulfills a great data processing
            requirement for edge computing, and if you want to evaluate the
            product in more detail, download and test it.
          </p>
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
