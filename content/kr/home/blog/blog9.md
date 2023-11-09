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
{{< home_menu_blog_kr >}}
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
    <h4 class="blog-title">마크베이스 6.1 vs InfluxDB 2.7</h4>
    <div class="blog-date">
      <div>
        <span>by Grey Shim / 18 Oct 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">소개</li></a
      >
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">테스트</li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">결론</li>
      </a>
    </ul>
    <div class="tech-contents">
      <div>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/blog9-1.webp" alt="" />
        </div>
        <p class="tech-title" id="anchor1">소개</p>
        <p class="tech-contents-text">
          지난 기사에서는 InfluxDB 1.8.1과 Mchbase를 비교했습니다. 1.8은 Linux
          패키지 관리자를 사용하여 기본적으로 설치되지만 최신 오픈 소스 버전인
          마크베이스 6.1이 InfluxDB의 2.7과 어떻게 비교되는지 보고 싶었습니다.
        </p>
        <div class="tech-contents-title">마크베이스</div>
        <p class="tech-contents-text">
          마크베이스는 시계열 센서 데이터의 빠른 입력, 검색, 통계를 위해 설계된
          DBMS입니다.
        </p>
        <p class="tech-contents-text">
          Raspberry Pi와 같은 에지 장치를 포함하여 일반 단일 서버, 다중 서버
          클러스터를 지원합니다. 시계열 센서 데이터와 머신 로그 데이터를
          처리하기 위한 특별한 기능과 아키텍처를 갖추고 있습니다.
        </p>
        <div class="tech-contents-title">InfluxDB</div>
        <p class="tech-contents-text">
          InfluxData에서 개발한 오픈소스 시계열 DBMS입니다. 시계열 데이터 처리에
          가장 인기 있는 제품 중 하나입니다. InfluxDB는 클러스터링도 지원합니다.
        </p>
        <p class="tech-contents-text">
          InfluxDB에 대한 자세한 내용은 아래 사이트를 참조하세요.
          <a
            class="tech-contents-link"
            href="https://docs.influxdata.com/influxdb"
            >https://docs.influxdata.com/influxdb</a
          >
        </p>
        <div class="tech-title" id="anchor2">테스트</div>
        <div class="tech-contents-title">테스트 환경</div>
        <p class="tech-contents-text">
          본 테스트에서는 다음 환경을 사용했습니다.
        </p>
        <ul class="tech-ul">
          <li>CPU : AMD EPYC 7742 64-Core Processor(128 thread)</li>
          <li>메모리 : 256GB</li>
          <li>디스크 : 삼성 NVME 2TB(PCI Express 3.0 x 4)</li>
          <li>OS : CentOS Linux release 7.8.2003</li>
          <li>데이터베이스 : 마크베이스 6.1.8 Fog / InfluxDB v2.7.0</li>
        </ul>
        <div class="tech-contents-title">테스트 제약</div>
        <p class="tech-contents-text">
          In InfluxDB 2. x and above, the removal of the database concept from
          InfluxDB 2.x 이상에서는 버전 1.8에서 데이터베이스 개념 제거, 버킷 및
          조직 추가, SQL 지원 감소, 토큰을 통한 보안 및 인증 강화로 인해 기존
          클라이언트 애플리케이션이 호환되지 않습니다. 따라서 기존에 SQL로
          작성된 테스트는 사용할 수 없으며 쿼리를 Flux 언어로 다시 작성하여
          실행하게 됩니다.
        </p>
        <p class="tech-contents-text">
          마크베이스는 기존 테스트 결과를 활용했습니다.
        </p>
        <div class="tech-contents-title">테스트 입력 성능</div>
        <p class="tech-contents-text">
          InfluxDB가 1.8에서 2.7로 업데이트되면서 리소스 사용량이 크게
          늘어났습니다.
        </p>
        <p class="tech-contents-text">
          이전과 마찬가지로 다음 환경에서 테스트를 실행했습니다.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog9-2.webp"
            alt=""
          />
        </div>
        <div class="tech-contents-title">수집 성능 테스트 결과</div>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog9-3.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          테스트 머신의 리소스 헤드룸이 증가했음에도 불구하고 InfluxDB의 입력
          성능은 이전(160,000eps)보다 약간 나쁩니다. InfluxDB 입력 성능이 버전에
          따라 향상되지 않은 것을 볼 수 있습니다.
        </p>
        <div class="tech-contents-title">쿼리 성능 테스트</div>
        <p class="tech-contents-text">
          InfluxDB는 SQL 쿼리에 대한 지원을 줄이고 자체 쿼리 언어인 Flux에 대한
          지원을 늘리고 있습니다. 이에 따라 기존 테스트 쿼리 도구는 더 이상
          사용할 수 없으며, 테스트 목적으로 다음 SQL 쿼리를 플럭스 쿼리로
          변환하였습니다. 쿼리는 아래 그림과 같습니다.
        </p>
        <ul class="tech-ul">
          <li>마크베이스(SQL) / Q1</li>
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
          <li>마크베이스(SQL) / Q2</li>
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
          <li>마크베이스(SQL) / Q3</li>
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
          <li>마크베이스(SQL) / Q4</li>
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
        <div class="tech-contents-title">쿼리 성능 테스트 결과</div>
        <p class="tech-contents-text">
          쿼리 실행 시간은 각각 Machsql 및 influx 실행 도구를 사용하여
          측정되었습니다. 결과는 아래와 같습니다.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog9-4.webp"
            alt=""
          />
        </div>
        <div class="tech-contents-title">테스트 결과를 종합적으로 비교</div>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog9-5.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          레코드 수를 가져오기 위한 첫 번째 쿼리의 성능이 너무 다르기 때문에
          나머지 세 쿼리의 성능은 아래와 같습니다.
        </p>
        <div class="tech-title" id="anchor3">결론</div>
        <p class="tech-contents-text">
          이전 Machbase와 InfluxDB 성능 비교와 마찬가지로 InfluxDB는 입력 속도가
          매우 느리고 Machbase는 쿼리 성능이 더 우수하다는 것을 알 수 있습니다.
          또한 InfluxDB가 SQL에 대한 지원을 줄이고 독점 쿼리 언어에 대한 지원을
          늘려 기존 애플리케이션과의 호환성이 떨어지는 것을 볼 수 있습니다.
        </p>
        <p class="tech-contents-text">
          마크베이스는 SQL을 포함한 업계 표준을 준수하여 기존 프로그램과의
          호환성을 지속적으로 유지하고, 마크베이스 neo에서 다양한 신규 API에
          대한 지원을 개선하고 지속적인 성능 향상을 약속드립니다.
        </p>
        <p class="tech-contents-text">감사합니다.</p>
        <p class="tech-contents-text">마크베이스 CRO 심광훈</p>
      </div>
    </div>
  </div>
</section>
{{< home_footer_blog_kr >}} {{< home_lang_kr >}}
