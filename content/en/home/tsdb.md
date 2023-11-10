---
title: Products
description: "Machbase TSDB(time series database) is the world’s fastest time series database with a minimal footprint."
images:
  - /namecard/og_img.jpg
---

<head>
  <link rel="stylesheet" type="text/css" href="../css/common.css" />
  <link rel="stylesheet" type="text/css" href="../css/style.css" />
</head>
<body>
  {{< home_menu_sub_en >}}
  <section class="product_sction0 section0">
    <div>
      <h2 class="sub_page_title">Products</h2>
      <p class="sub_page_titletext">
        “ Discover the top DBMS suites for edge computing and take your data
        processing to the next level ”
      </p>
    </div>
  </section>
  <div class="product-inner">
  <section class="section2 main_section2">
    <div>
      <h4 class="sub_title company-margin-top">Time Series Database</h4>
      <div class="bar"><img src="../img/bar.png" /></div>
    </div>
    <div class="product-sub-titlebox">
      <div>
        <p class="product-sub-title-text">
          Machbase TSDB(time series database) is the world’s fastest time series
          database with a minimal footprint.<br /><br />In the performance
          evaluation organized by the Transaction Processing Performance Council
          (TPC), a global performance evaluation organization,
          <a href="/home/company#performance" class="products-tpc-link"
            >it has been ranked first in the "TPCx-IoT" field since 2019 and is
            listed as an international standard in this field.<span>
              <!-- <img
              class="products-link-img"
              src="../img/company_link.png"
              alt="" /> -->
            </span></a
          ><br /><br />
          And it’s an ideal solution for environments that require scalability,
          from small servers with limited resources like the Raspberry Pi to
          horizontally scaled clusters.<br /><br />Machbase Neo, built on
          Machbase, adds crucial features required for the IoT industry. It
          ingests and handles query data through various protocols, such as MQTT
          for direct data transfer from IoT sensors, and SQL via HTTP for data
          retrieval by applications
        </p>
      </div>
    </div>
  </section>
  <section class="neo_scroll_map_wrap">
    <div class="neo_scroll_map">
      <div ref="scrollLeft" class="neo_scroll_left">
        <div class="neo_scroll"><img src="../img/tsdb.png" /></div>
      </div>
      <div class="neo_scroll_right">
        <div class="neo_scorll_box_wrap">
          <div class="classic_sub_wrap">
            <div class="classic_sub">
              <div class="scroll-title-wrap">
                <p>Classic Edition features</p>
              </div>
              <div class="scroll-contents-wrap">
                <p class="scroll-content">
                  Machbase engine is written entirely in C. For this reason, it
                  has very fast performance and is very efficient in CPU and
                  memory usage for data processing. In particular, we invented
                  an innovative multi-dimensional index structure to handle the
                  explosion of IoT data in real time, which is at the core of
                  Machbase's performance. Due to these performance and resource
                  efficiency characteristics, it is being utilized as a
                  high-speed database for small-scale edge device and as a core
                  data processing engine for edge computing.
                </p>
              </div>
              <div class="scroll-sub-title-wrap">
                <p class="scroll-sub-title">Machbase's performance</p>
                <p class="scroll-sub-text">In ingestion point of view</p>
                <ul>
                  <li>In edge Device (ARM 2 core) : up to 500,000 rec/sec</li>
                  <li>
                    In single Server (INTEL 8 core) : up to 2,500,000 rec/sec
                  </li>
                  <li>In Cluster (16 node) : up to 100,000,000 rec/sec</li>
                </ul>
                <p class="scroll-sub-text">In extraction point of view</p>
                <ul>
                  <li>
                    0.1 seconds for extracting 10,000 random time ranges from a
                    400 billion data store
                  </li>
                </ul>
                <p class="scroll-sub-text">In compression point of view</p>
                <ul>
                  <li>4TB store : around 1 trillion record</li>
                </ul>
              </div>
              <span>
                <a
                  class="main_why_more product-margin-bottom"
                  href="https://machbase.com/dbms"
                >
                  View More<ArrowSvg />
                </a>
              </span>
            </div>
          </div>
          <div ref="classicSubWrapRef" class="neo_sub_wrap" id="scroll1">
            <div class="neo_sub">
              <div class="scroll-title-wrap">
                <p>Neo Edition components</p>
              </div>
              <div class="scroll-sub-title-wrap">
                <p class="scroll-sub-title">
                  Machbase Neo is a database engine with its own
                </p>
                <ul class="product-margin-bottom">
                  <a
                    class="product-link"
                    href="https://machbase.com/neo/api-mqtt/"
                    ><li>MQTT server for IoT data</li></a
                  >
                  <a
                    class="product-link"
                    href="https://machbase.com/neo/api-http/"
                    ><li>
                      Web server with HTTP protocol support for Rest APIs
                    </li></a
                  >
                  <a
                    class="product-link"
                    href="https://machbase.com/neo/api-grpc/"
                    ><li>
                      A gRPC server, a high-performance, high-definition,
                      language-neutral remote procedure call framework developed
                      by Google
                    </li></a
                  >
                  <a
                    class="product-link"
                    href="https://machbase.com/neo/operations/13.ssh-access/"
                    ><li>
                      SSH server for secure data and manipulation security — all
                      four essential features are integrated
                    </li></a
                  >
                </ul>
                <div class="scroll-contents-wrap">
                  <p class="scroll-content">
                    So users can just fire up Neo and start using all the
                    features above without any complications. In addition,
                    support for the line protocol enables integration with
                    telegraf, a leading open source product for data collection,
                    and the influxdb application, an open source time series
                    DBMS, can be used unchanged, greatly expanding the options
                    for developers. Anyone can download all the source code via
                    github to test and validate.
                  </p>
                  <a
                    class="main_why_more product-margin-bottom"
                    href="https://machbase.com/neo"
                  >
                    View More<ArrowSvg />
                  </a>
                </div>
              </div>
            </div>
          </div>
          <div ref="neoSubWrapRef" class="neo_use_sub_wrap" id="scroll2">
            <div class="neo_use_sub product-link-bottom">
              <div class="scroll-title-wrap">
                <p>Neo Edition features</p>
              </div>
              <div class="scroll-contents-wrap">
                <p class="scroll-content">
                  Neo Edition was developed to save resources on unnecessary
                  feature development and focus resources on core service
                  modules.
                </p>
              </div>
              <div class="scroll-sub-title-wrap">
                <p class="scroll-sub-title">Key features include</p>
                <p class="scroll-sub-item">
                  # Convenient and user-friendly interface.
                </p>
                <ul>
                  <li>Offer a web browser-based interface.</li>
                  <li>
                    Extremely easy to operate by installing it as a single
                    executable file
                  </li>
                </ul>
                <p class="scroll-sub-item">
                  # Support various operating systems.
                </p>
                <ul>
                  <li>Linux, Windows, macOS (Intel/M1)</li>
                </ul>
                <p class="scroll-sub-item">
                  # Flexible integration with existing solutions.
                </p>
                <ul>
                  <li>Grafana plug-in</li>
                  <li>Telegraf, Tableau, and others</li>
                </ul>
                <p class="scroll-sub-item">
                  # Change settings to take advantage of smaller edges
                </p>
                <ul>
                  <li>Raspberry Pi, ODROID, etc.</li>
                </ul>
                <p class="scroll-sub-item"># Support embedded broker.</p>
                <ul>
                  <li>Moreover, it supports various brokers!</li>
                  <li>Data loss and performance concerns eliminate.</li>
                </ul>
                <p class="scroll-sub-item">
                  #Support standard security features.
                </p>
                <ul>
                  <li>Distant from the headache-inducing security issues!</li>
                  <li>Support TLS-based X.509, SSH console support.</li>
                </ul>
                <p class="scroll-sub-item">
                  # Provide worksheet functionality.
                </p>
                <ul>
                  <li>
                    Enable the creation and sharing of interactive user
                    education manuals and tutorials.
                  </li>
                </ul>
                <p class="scroll-sub-item">
                  # Provide a powerful built-in data transformation language
                  (TQL).
                </p>
                <ul>
                  <li>
                    Allow immediate implementation of Restful APIs without
                    separate coding, enabling service availability.
                  </li>
                  <li>
                    Offer specialized analysis functions such as the FFT
                    function.
                  </li>
                </ul>
                <p class="scroll-sub-item">
                  # Provide built-in scripting language.
                </p>
                <ul>
                  <li>
                    Allow for the utilization of scripting language through TQL.
                  </li>
                  <li>
                    Enable direct integration with external data sources and
                    data transformation. (SQLite, MySQL, PostgreSQL, and more)
                  </li>
                </ul>
                <p class="scroll-sub-item"># Provide visualization.</p>
                <ul>
                  <li>Enable real-time monitoring of incoming data.</li>
                  <li>Allow visual analysis of SQL, charts, and more.</li>
                </ul>
                <p class="scroll-sub-item"># Built-in scheduler</p>
                <ul>
                  <li>
                    Provide engine-level repetitive task automation
                    functionality.
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  </div>
  <section>
    <h4 class="sub_title company-margin-top">Neo Interface</h4>
    <div class="bar"><img src="../img/bar.png" /></div>
    <div class="neo_interface_wrap">
      <img class="neo_interface" src="../img/neo_interface.png" alt="" />
    </div>
  </section>
  <section>
    <div class="next-navi_wrap">
      <div class="next-navi">
        <div class="next-navi-wrap">
          <div class="next-navi-text-wrap">
            <p class="next-navi-text">Ready to start in an instant</p>
          </div>
          <div class="next-navi-btn-wrap">
            <button
              onclick="location.href='/home/download'"
              class="next-navi-btn"
            >
              Get Machbase
            </button>
            <a href="https://machbase.com/neo"
              ><button class="next-navi-btn">Document</button></a
            >
          </div>
        </div>
      </div>
    </div>
  </section>
</body>
{{< home_footer_sub_en >}}
{{< home_lang_en >}}
