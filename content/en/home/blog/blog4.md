---
title: Blog
description: "Comparing Time-Series Database Architectures: Machbase vs. InfluxDB"
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
      Comparing Time-Series Database Architectures: Machbase vs. InfluxDB
    </h4>
    <div class="blog-date">
      <div>
        <span>by Grey Shim / 14 Aug 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">Introduction</li>
      </a>
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">
          Comparison of Architectures
        </li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">
          The implementation language / Client interface
        </li>
      </a>
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">Data Model</li>
      </a>
      <a href="#anchor5">
        <li class="tech-list-li" id="tech-list-li">Query Language</li>
      </a>
      <a href="#anchor6">
        <li class="tech-list-li" id="tech-list-li">Conclusion</li>
      </a>
    </ul>
    <div class="tech-contents">
      <div>
        <p class="tech-title" id="anchor1">Introduction</p>
        <p class="tech-contents-text">
          For those interested in comparing databases specialized for
          time-series data, this time, we will delve into an architecture
          comparison with InfluxDB.
        </p>
        <p class="tech-contents-text">
          Although the performance comparison is based on past versions
          (approximately 3–4 years ago), with Machbase DB notably excelling,
          there is currently no available data for a comparison of the latest
          versions. Additionally, both products have undergone significant
          changes since then, making it less ideal to draw conclusions at the
          current juncture. Therefore, it is advisable to consider this
          information as reference material.
        </p>
        <div class="tech-contents-title">Machbase DB</div>
        <p class="tech-contents-text">
          Machbase is a DBMS developed with the aim of facilitating quick input,
          retrieval, and statistical analysis of time-series sensor data.
        </p>
        <p class="tech-contents-text">
          It supports various environments ranging from edge devices like
          Raspberry Pi to single-server setups and multi-server clusters.
        </p>
        <p class="tech-contents-text">
          It features specialized capabilities and architecture tailored for
          processing time-series sensor data and machine logs.
        </p>
        <div class="tech-contents-title">Influx DB</div>
        <p class="tech-contents-text">
          It is an open-source time-series DBMS being developed by InfluxData.
        </p>
        <p class="tech-contents-text">
          It is one of the most renowned products for processing time-series
          data. InfluxDB also supports clustering.
        </p>
        <div class="tech-title" id="anchor2">
          Comparison of Machbase and InfluxDB Architectures
        </div>
        <p class="tech-contents-text">
          Both Machbase and InfluxDB are specialized products tailored for
          processing time-series data, and their key characteristics can be
          summarized as follows:
        </p>
        <p class="tech-contents-text">
          In this post, the analysis will primarily prioritize usability
          features. Detailed information regarding indexes, internal structures,
          and content related to performance testing will be covered after
          conducting performance tests and will be discussed in future updates.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/compare.png" alt="" />
        </div>
        <p class="tech-contents-link-text">Machbase Neo’s Architecture</p>
        <div class="tech-title" id="anchor3">
          The implementation language / Client interface
        </div>
        <p class="tech-contents-text">
          Machbase has its server code written in C, while the ODBC/CLI and
          embedded tools within the server are written in C++. Additionally,
          libraries for JDBC, C#, and Scala are implemented in their respective
          languages. The communication protocol between the server and clients
          is designed using a dedicated protocol to support common RDBMS
          interfaces such as Prepare/Bind/Execute. This implementation is
          carefully designed for optimal efficiency.
        </p>
        <p class="tech-contents-text">
          The C# connector is publicly available on the Machbase Github
          repository, allowing anyone to reference its internal implementation.
        </p>
        <p class="tech-contents-text">
          InfluxDB is written in the GO programming language, and its
          communication protocol is based on REST. It provides client libraries
          in various languages, although interfaces like Prepare/Bind/Execute
          are not offered. When examining the source code of prominent C++
          client libraries (linked on the InfluxDB website), it becomes apparent
          that all operations are translated into REST and transmitted. The
          implementation uses the open-source HTTP library, curl.
        </p>
        <div class="tech-code-box">
          <span>void</span> HTTP::send(std::string&& post)<br />{<br />
          &nbsp;&nbsp;CURLcode response;<br />&nbsp;&nbsp;long responseCode;<br />&nbsp;&nbsp;curl_easy_setopt(curlHandle.<span
            class="red"
            >get</span
          >(), CURLOPT_POSTFIELDS, post.c_str());<br />&nbsp;&nbsp;
          curl_easy_setopt(curlHandle.<span class="red">get</span>(),
          CURLOPT_POSTFIELDSIZE, (long) post.length());<br />&nbsp;&nbsp;response
          = curl_easy_perform(curlHandle.<span class="red">get</span
          >());<br />&nbsp;&nbsp;curl_easy_getinfo(curlHandle.<span class="red"
            >get</span
          >(), CURLINFO_RESPONSE_CODE, &responseCode);<br />&nbsp;&nbsp;<span
            class="red"
            >if</span
          >
          (response != CURLE_OK) { <br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span
            class="red"
            >throw</span
          >
          std::runtime_error(curl_easy_strerror(response)); <br />&nbsp;&nbsp;}
          <span class="red">if</span> (responseCode &lt;
          <span class="blue">200</span> || responseCode &gt;
          <span class="blue">206</span>) {<br />&nbsp;&nbsp; &nbsp;&nbsp;<span
            class="red"
            >throw</span
          >
          std::runtime_error(<span class="red">"Response code : "</span> +
          std::to_string(responseCode)); } <br />&nbsp;&nbsp;}
        </div>
        <p class="tech-contents-text">
          A REST-based interface offers greater convenience in web environments.
          It allows easy transmission of queries from web servers and convenient
          data input from a multitude of sensors into the time-series database.
          Of course, Machbase also supports REST, so this can’t be seen as a
          unique advantage of Influx.
        </p>
        <p class="tech-contents-text">
          However, in cases where a small number of sensor data generates a
          massive amount of data very rapidly — for instance, with sensors like
          vibration sensors that produce data at very short intervals —
          Machbase’s unique APIs like SQLAppend, or common interfaces like
          Prepare-execute, Array-Binding, and Batch execute in the ODBC
          interface, prove highly efficient. Conversely, for InfluxDB, where all
          protocols are REST-based, achieving the same level of efficiency can
          be challenging. Therefore, in environments where continuous
          large-scale data is generated at short intervals, InfluxDB becomes
          less efficient.
        </p>
        <p class="tech-contents-text">
          Performance testing related to this aspect will be conducted in the
          future.
        </p>
        <p class="tech-contents-text">
          (Note: The translation provided maintains the original structure and
          meaning of the text, but slight modifications might be necessary
          depending on the context in which this translation will be used.)
        </p>
        <div class="tech-title" id="anchor4">Data Model</div>
        <p class="tech-contents-text">
          Machbase supports a relational model. For tables designed for sensor
          data processing, such as TAGs, in addition to mandatory columns
          (sensor ID, input time, input value) created during table creation,
          additional necessary columns can be defined. These must be defined
          using Data Definition Language (DDL).
        </p>
        <p class="tech-contents-text">
          On the other hand, InfluxDB supports a semi-structured data format
          known as “tagset.” A single record is divided into key, tags, and a
          value list. Indexing is only possible for tags. All data inherently
          includes the input time column, without needing explicit
          specification. Even if the “time” column is not selected during a
          “SELECT” query, it is automatically included in the data, ensuring its
          presence in query results. In InfluxDB, the concept corresponding to a
          table is referred to as a “series.” Since there is no explicit Data
          Definition Language (DDL) for creating series, I will elaborate based
          on the provided query below. For this query, there is no need for a
          table creation statement. (There are no table creation queries in the
          provided query.)
        </p>
        <div class="tech-code-box">
          <span class="red">INSERT</span> treasures,captain_id=pirate_king
          <span class="red">value</span>=2
        </div>
        <p class="tech-contents-text">
          It might sound unfamiliar, right? When translated into a Machbase
          query (including table and index creation DDL):
        </p>
        <div class="tech-code-box">
          <span class="red">CREATE TABLE</span> treasures (captain_id
          varchar(<span class="blue">10</span>),
          <span class="red">value</span> integer);<br />
          <span class="red">CREATE</span> INDEX treasures_captain_id
          <span class="red">on</span> treaures(captian_id); <br /><span
            class="red"
            >INSERT INTO</span
          >
          treasures <span class="red">VALUES</span> ('pirate_king', 2);
        </div>
        <p class="tech-contents-text">
          Yes, all column names are included in the insert statement. In
          InfluxDB, since there is no schema, column names need to be explicitly
          specified during insertion. And
        </p>
        <div class="tech-code-box">
          <span class="green">captain_id</span>=pirate_king value=2
        </div>
        <p class="tech-contents-text">
          Furthermore, there is a space between the front “captain_id” and the
          back “value.” The column=value clause before the space (i.e.,
          captain_id=pirate_king) represents the tag clause, and indexing is
          done only for these values. This index can also be applied in a nested
          manner.
        </p>
        <div class="tech-code-box">
          <span class="green">captain_id</span>=pirate_king,other_tag=tag1
          value=2,value2=1
        </div>
        <p class="tech-contents-text">
          These values are indexed for both captain_id and other_tag, whereas
          the space-separated values “value” and “value2” are input as
          non-indexed values. When conducting queries involving non-indexed
          values, the search tends to be slow since it involves a full scan
          query, which is expected. However, for columns that are not indexed,
          you cannot use the GROUP BY clause. The GROUP BY clause can only be
          applied to tag columns.
        </p>
        <p class="tech-contents-text">
          In this manner, the key-value data model configured in the form of
          column=value and tag=value is referred to as “tagset” in InfluxDB.
          This stands as a distinguishing factor from the relational model liked
          Machbase.
        </p>
        <div class="tech-title" id="anchor5">Query Language</div>
        <p class="tech-contents-text">
          Machbase provides additional syntax in SQL queries to accommodate the
          characteristics of time-series data. This allows users familiar with
          SQL to use it with relative ease. In contrast, InfluxDB has
          transformed its query language to be more similar to NoSQL compared to
          Machbase.
        </p>
        <p class="tech-contents-text">
          Let’s take a look at simple queries and their results.
        </p>
        <div class="tech-code-box">
          > <span class="red">SELECT</span> COUNT("water_level")
          <span class="red">FROM</span> h2o_feet<br />name: h2o_feet<br />--------------<br /><span
            class="red"
            >time</span
          >
          count<br /><span class="blue">1970-01-01</span>T<span class="blue"
            >00</span
          >:<span class="blue">00</span>:<span class="blue">00</span>Z
          <span class="blue">15258</span>
        </div>
        <p class="tech-contents-text">
          Yes, even if the “time” column is not included in the SELECT query’s
          column list, it is forcefully inserted, leading to the output of
          meaningless values. While the values corresponding to column names are
          enclosed in double quotation marks, it doesn’t seem too challenging to
          comprehend.
        </p>
        <p class="tech-contents-text">
          In the past, they had a query language called Flux, but it is
          undergoing a transition to a SQL-like query language as described
          earlier.
        </p>
        <div class="tech-code-box">
          <span class="red">from</span>(db:"metrics")<br />|>
          <span class="red">range</span>(<span class="red">start</span>:-1h)
          <br />|> <span class="red">filter</span>(fn: (r) => r._measurement ==
          "foo")
        </div>
        <p class="tech-contents-text">When translated into Machbase SQL:</p>
        <div class="tech-code-box">
          <span class="red">SELECT</span> *<br /><span class="red">FROM</span>
          metrics<br /><span class="red">WHERE</span> measurement =
          <span class="red">'foo'</span> DURATION 1
          <span class="red">hour</span>;
        </div>
        <div class="tech-title" id="anchor6">Conclusion</div>
        <p class="tech-contents-text">
          I will conclude the part of the post that covers interface details at
          this point. While both products are developed with the aim of
          efficiently processing time-series data, Machbase endeavors to support
          relational databases and DBMS standard interfaces to the fullest
          extent, while InfluxDB exhibits features more aligned with NoSQL
          characteristics.
        </p>
        <p class="tech-contents-title">To summarize:</p>
        <p class="tech-contents-text">
          I will conclude the part of the post that covers interface details at
          this point. While both products are developed with the aim of
          efficiently processing time-series data, Machbase endeavors to support
          relational databases and DBMS standard interfaces to the fullest
          extent, while InfluxDB exhibits features more aligned with NoSQL
          characteristics.
        </p>
        <ul class="tech-ul">
          <li>
            Machbase is implemented in C and supports traditional DB interfaces
            like ODBC/JDBC, while InfluxDB is implemented in Go. It operates
            with a REST-based interface and a scripting-like structure, and it
            does not function with Prepare/Bind/Execute.
          </li>
          <li>
            Machbase operates as a relational database, adhering to schemas
            defined using DDL. This aligns with the conventional appearance of
            DBMS. In contrast, InfluxDB takes a different approach. It employs
            its unique data model called “tagset,” and lacks a DDL. Instead, it
            performs real-time column data parsing.
          </li>
          <li>
            Machbase supports extended syntax in its SQL-based query language,
            and InfluxDB offers a similar approach, although it operates in a
            manner closer to NoSQL.
          </li>
        </ul>
        <p class="tech-contents-text">
          While we regret not being able to delve into performance measurements
          through actual architectural comparisons due to time constraints, we
          assure you that this topic will be covered in the future.
        </p>
        <p class="tech-contents-text">
          Feel free to reach out if you have any questions or if there are
          further aspects you’d like to compare.
        </p>
        <p class="tech-contents-text">Thank you.</p>
        <p class="tech-contents-text">Machbase CRO, Grey Shim</p>
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
