---
title: Blog
description: "Machbase 6.1 vs InfluxDB 2.7"
images:
  - /namecard/og_img.jpg
---

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" type="text/css" href="../../css/common.css" />
  <link rel="stylesheet" type="text/css" href="../../css/style.css" />
</head>
{{< home_menu_blog_en >}}
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
      Machbase 6.1 vs InfluxDB 2.7
    </h4>
    <div class="blog-date">
      <div>
        <span>by Grey Shim / 18 Oct 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">Introduction</li></a
      >
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">Test</li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">Conclusion</li>
      </a>
    </ul>
    <div class="tech-contents">
      <div>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/blog9-1.webp" alt="" />
        </div>
        <p class="tech-title" id="anchor1">Introduction</p>
        <p class="tech-contents-text">
          In the last article, we compared InfluxDB 1.8.1 with Mchbase. While
          1.8 is installed by default using the Linux package manager, we wanted
          to see how it compares to Machbase 6.1, the latest open-source
          version, 2.7.
        </p>
        <div class="tech-contents-title">Machbase</div>
        <p class="tech-contents-text">
          Machbase is a DBMS designed for fast input, search and statistics of
          time series sensor data.
        </p>
        <p class="tech-contents-text">
          It supports regular single servers, multi-server clusters, including
          edge devices such as Raspberry Pi. It has special features and
          architecture for processing time series sensor data and machine log
          data.
        </p>
        <div class="tech-contents-title">InfluxDB</div>
        <p class="tech-contents-text">
          It is an open-source time series DBMS developed by InfluxData. It is
          one of the most popular products for processing time series data.
          InfluxDB also supports clustering.
        </p>
        <p class="tech-contents-text">
          For more information about InfluxDB, see the sitebelow.
          <a
            class="tech-contents-link"
            href="https://docs.influxdata.com/influxdb"
            >https://docs.influxdata.com/influxdb</a
          >
        </p>
        <div class="tech-title" id="anchor2">Test</div>
        <div class="tech-contents-title">Test environment</div>
        <p class="tech-contents-text">
          For this test, we used the following environment.
        </p>
        <ul class="tech-ul">
          <li>CPU : AMD EPYC 7742 64-Core Processor(128 thread)</li>
          <li>Memory : 256GB</li>
          <li>Disk : Samsung NVME 2TB(PCI Express 3.0 x 4)</li>
          <li>OS : CentOS Linux release 7.8.2003</li>
          <li>Database : Machbase 6.1.8 Fog / InfluxDB v2.7.0</li>
        </ul>
        <div class="tech-contents-title">Test constraints</div>
        <p class="tech-contents-text">
          In InfluxDB 2. x and above, the removal of the database concept from
          version 1.8, the addition of buckets and organizations, the reduction
          of SQL support, and the enhancement of security and authentication
          with tokens make existing client applications incompatible. As a
          result, existing tests written in SQL cannot be used and will be
          executed by rewriting queries in the Flux language.
        </p>
        <p class="tech-contents-text">
          Machbase used the existing test results.
        </p>
        <div class="tech-contents-title">Test input performance</div>
        <p class="tech-contents-text">
          With the update of InfluxDB from 1.8 to 2.7, resource usage has
          increased significantly.
        </p>
        <p class="tech-contents-text">
          As before, we ran tests in the following environments
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog9-2.webp"
            alt=""
          />
        </div>
        <div class="tech-contents-title">
          Ingestion performance test results
        </div>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog9-3.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          Despite the increased resource headroom on our test machine,
          InfluxDB’s input performance is slightly worse than before (160,000
          eps). You can see that InfluxDB input performance has not improved
          with the version.
        </p>
        <div class="tech-contents-title">Performance testing of queries</div>
        <p class="tech-contents-text">
          InfluxDB is reducing support for SQL queries and increasing support
          for flux, its own query language. As a result, the existing test query
          tool is no longer available, and the following SQL query has been
          transformed into a flux query for testing purposes. The query is shown
          in the figure below.
        </p>
        <ul class="tech-ul">
          <li>Machbase(SQL) / Q1</li>
          <div class="tech-code-box">
            <span class="red">select</span><span> count(*) </span
            ><span class="red">from</span> tag;
          </div>
          <li>ㆍInfluxDB(Flux) / Q1</li>
          <div class="tech-code-box">
            <span class="red">from</span>(<span class="red">bucket</span>:<span
              class="orange"
              >"sensor_data/autogen"</span
            >)<br />
            <br />
            |> <span class="red">range</span>(<span class="red">start</span
            >:<span class="blue">2018</span><span class="red">-01-01T00</span
            ><span class="blue">:00:00+09:00</span>,
            <span class="red">stop</span><span class="red">:2018</span
            ><span class="red">-01-02T01</span
            ><span class="blue">00:00+09:00</span>)
            <br />
            <br />
            |> <span class="red">filter</span>(<span class="red">fn</span
            ><span>: (r) => r._measurement == </span
            ><span class="orange">"tag_data" </span>)<br /><br />
            |> <span class="red">group</span>()<br /><br />
            |> <span class="red">count</span>() |>
            <span class="red">yield</span>(<span class="red">name</span>:
            <span class="orange">"count"</span>)
          </div>
          <li>Machbase(SQL) / Q2</li>
          <div class="tech-code-box">
            <span class="red">select</span><span> count(*) </span
            ><span class="red">from</span> (<span class="red">select</span> *
            <span class="red">from</span> tag
            <span class="red">where</span> name =
            <span class="orange">'EQ0^TAG1' </span> <span class="red">and</span
            ><br /><br />
            <span>time </span><span class="red">between </span>to_date(
            <span class="orange">'2018-01-01 00:00:00'</span>)
            <span class="red">and </span>to_date(
            <span class="orange">'2018-01-02 00:00:00'</span>));
          </div>
          <li>ㆍInfluxDB(Flux) / Q2</li>
          <div class="tech-code-box">
            <span class="red">from</span>(<span class="red">bucket</span>:<span
              class="orange"
              >"sensor_data/autogen"</span
            >)<br />
            <br />
            |> <span class="red">range</span>(<span class="red">start</span
            >:<span class="blue">2018</span><span class="red">-01-01T00</span
            ><span class="blue">:00:00+09:00</span>,
            <span class="red">stop</span><span class="red">:2018</span
            ><span class="red">-01-02T01</span
            ><span class="blue">00:00+09:00</span>)
            <br />
            <br />
            |> <span class="red">filter</span>(<span class="red">fn</span
            ><span>: (r) => r._measurement == </span
            ><span class="orange">"tag_data" </span>)
            <span class="red">and</span> r.name ==
            <span class="orange">"EQ0^TAG1" </span>)<br /><br />
            |> <span class="red">group</span>()<br /><br />
            |> <span class="red">count</span>() |>
            <span class="red">yield</span>(<span class="red">name</span>:
            <span class="orange">"count"</span>)
          </div>
          <li>Machbase(SQL) / Q3</li>
          <div class="tech-code-box">
            <span class="red">select</span><span> count(*) </span
            ><span class="red">from</span> (<span class="red">select</span> *
            <span class="red">from</span> tag
            <span class="red">where</span> name
            <span class="red">in</span> (<span class="orange">'EQ0^TAG1'</span>,
            <span class="orange">'EQ0^TAG2'</span>,
            <span class="orange">'EQ0^TAG3'</span>,<br /><br /><span
              class="orange"
              >'EQ0^TAG4'</span
            >, <span class="orange">'EQ0^TAG5'</span>,
            <span class="orange">'EQ0^TAG6'</span>,
            <span class="orange">'EQ0^TAG7'</span>,
            <span class="orange">'EQ0^TAG8'</span>,
            <span class="orange">'EQ0^TAG9'</span>,
            <span class="orange">'EQ0^TAG10'</span>,<span class="red">and</span
            ><br /><br />
            <span>time </span><span class="red">between </span>to_date(
            <span class="orange">'2018-01-01 00:00:00'</span>)
            <span class="red">and </span>to_date(
            <span class="orange">'2018-01-02 00:00:00'</span>));
          </div>
          <li>InfluxDB(Flux) / Q3</li>
          <div class="tech-code-box">
            <span class="red">from</span>(<span class="red">bucket</span>:<span
              class="orange"
              >"sensor_data/autogen"</span
            >)<br />
            <br />
            |> <span class="red">range</span>(<span class="red">start</span
            >:<span class="blue">2018</span><span class="red">-01-01T00</span
            ><span class="blue">:00:00+09:00</span>,
            <span class="red">stop</span><span class="red">:2018</span
            ><span class="red">-01-02T01</span
            ><span class="blue">00:00+09:00</span>)
            <br />
            <br />
            |> <span class="red">filter</span>(<span class="red">fn</span
            ><span>: (r) => r._measurement == </span
            ><span class="orange">"tag_data" </span>)
            <span class="red">and</span> r.name ==
            <span class="orange">"EQ0^TAG1" </span> or r.name ==
            <span class="orange">"EQ0^TAG2" </span> or r.name ==
            <span class="orange">"EQ0^TAG3" </span>or r.name ==
            <span class="orange">"EQ0^TAG4" </span>or r.name ==
            <span class="orange">"EQ0^TAG5" </span>or r.name ==
            <span class="orange">"EQ0^TAG6" </span>or r.name ==
            <span class="orange">"EQ0^TAG7" </span>or r.name ==
            <span class="orange">"EQ0^TAG8" </span>or r.name ==
            <span class="orange">"EQ0^TAG9" </span>or r.name ==
            <span class="orange">"EQ0^TAG10" </span>)<br /><br />
            |> <span class="red">group</span>()<br /><br />
            |> <span class="red">count</span>() |>
            <span class="red">yield</span>(<span class="red">name</span>:
            <span class="orange">"count"</span>)
          </div>
          <li>Machbase(SQL) / Q4</li>
          <div class="tech-code-box">
            <span class="red">select</span
            ><span>
              name, stddev(<span class="red">value</span>)
              <span class="red">from</span> tag
              <span class="red">where </span>name =
              <span class="orange">'EQ0^TAG1'</span><br /><br />
              <span class="red">and </span>time >= to_date</span
            ><span class="orange">'2018-01-01 00:00:00'</span>)<span
              class="red"
            >
              and</span
            >
            time < to_date(<span class="orange">'2018-01-02 00:00:00'</span
            >)<br /><br />
            <span class="red">group by </span>name;
          </div>
          <li>InfluxDB(Flux) / Q4</li>
          <div class="tech-code-box">
            <span class="red">from</span>(<span class="red">bucket</span>:<span
              class="orange"
              >"sensor_data/autogen"</span
            >)<br />
            <br />
            |> <span class="red">range</span>(<span class="red">start</span
            >:<span class="blue">2018</span><span class="red">-01-01T00</span
            ><span class="blue">:00:00+09:00</span>,
            <span class="red">stop</span><span class="red">:2018</span
            ><span class="red">-01-02T01</span
            ><span class="blue">00:00+09:00</span>)
            <br />
            <br />
            |> <span class="red">filter</span>(<span class="red">fn</span
            ><span>: (r) => r._measurement == </span
            ><span class="orange">"tag_data" </span>)
            <span class="red">and</span> r.name ==
            <span class="orange">"EQ0^TAG1" </span>
            <span class="red">and</span> r._field ==
            <span class="orange">"value" </span>)<br /><br />
            |> <span class="red">stddev</span>()<br /><br />
            |> <span class="red">group</span>(<span class="red">columns</span>:
            [<span class="orange">"_measurement"</span>],
            <span class="red">mode</span>: <span class="orange">"by"</span>)
          </div>
        </ul>
        <div class="tech-contents-title">
          Test results for query performance
        </div>
        <p class="tech-contents-text">
          The query execution time was measured using Machsql and influx
          executable tools respectively. The results are shown below.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog9-4.webp"
            alt=""
          />
        </div>
        <div class="tech-contents-title">
          Comparison of test results in aggregate
        </div>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog9-5.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          The performance of the first query to get the number of records is so
          different that the performance of the other three queries is shown
          below.
        </p>
        <div class="tech-title" id="anchor3">Conclusion</div>
        <p class="tech-contents-text">
          Similar to the previous Machbase vs. InfluxDB performance comparison,
          we see that InfluxDB is very slow on input and Machbase is better on
          queries. We can also see that InfluxDB has reduced its support for SQL
          and increased its support for proprietary query languages, making it
          less compatible with existing applications.
        </p>
        <p class="tech-contents-text">
          Machbase promises to continue to maintain compatibility with existing
          programs by adhering to industry standards, including SQL, to improve
          support for various new APIs in Machbase neo and to continue to
          improve performance.
        </p>
        <p class="tech-contents-text">Thank you.</p>
        <p class="tech-contents-text">Machbase CRO, Grey Shim</p>
      </div>
    </div>
  </div>
</section>
{{< home_footer_blog_en >}} {{< home_lang_en >}}
