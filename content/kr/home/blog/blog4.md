---
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
          <a href="/kr/home"
            ><img src="../../img/logo_machbase.png" alt=""
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
  <a href="/kr/home"><img src="../../img/logo_machbase.png" alt="" /></a>
  <div class="tablet-menu-icon">
    <div class="tablet-bar"></div>
    <div class="tablet-bar"></div>
    <div class="tablet-bar"></div>
  </div>
  <div class="tablet-menu">
    <ul>
      <div class="tablet-menu-title">
        <a class="tablet-logo" href="/kr/home"
          ><img src="../../img/logo_machbase.png" alt=""
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
<section class="pricing_section0 section0">
  <div>
    <h1 class="sub_page_title">Blog</h1>
    <p class="sub_page_titletext">
      “ Mach Speed Horizontally Scalable Time series database. ”
    </p>
  </div>
</section>
<section>
  <div class="tech-inner">
    <h4 class="blog-title">
      시계열 DB(Time-Series Database) 아키텍처 비교_ 마크베이스Machbase vs
      인플럭스 InfluxDB
    </h4>
    <div class="blog-date">
      <div>
        <span>by Grey Shim / 14 Aug 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">개요</li>
      </a>
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">아키텍쳐 비교</li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">
          구현 언어 / Client interface
        </li>
      </a>
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">Data Model</li>
      </a>
      <a href="#anchor5">
        <li class="tech-list-li" id="tech-list-li">Query Language</li>
      </a>
      <a href="#anchor6">
        <li class="tech-list-li" id="tech-list-li">결론</li>
      </a>
    </ul>
    <div class="tech-contents">
      <div>
        <p class="tech-title" id="anchor1">개요</p>
        <p class="tech-contents-text">
          시계열 데이터를 위한 DBMS 간의 비교에 흥미 있으실 분들을 위해
          InfluxDB와의 아키텍처 비교를 해 보겠습니다.
        </p>
        <p class="tech-contents-text">
          제품 성능 비교는 과거(3–4년 전) 버전으로 비교한 것이 있지만(물론
          마크베이스 Machbase DB가 월등합니다.) 최신 제품 비교 자료는 아직
          마련된 것이 없고, 그 이후로 두 제품 모두 많은 변화가 있어 현시점에서
          이야기하기에는 바람직해 보이지 않으므로 참고 자료로만 보시는 것이
          좋겠습니다.
        </p>
        <div class="tech-contents-title">Machbase DB 소개</div>
        <p class="tech-contents-text">
          마크베이스Machbase는 시계열 센서 데이터의 빠른 입력, 검색, 통계 등을
          목표로 개발된 DBMS입니다.
        </p>
        <p class="tech-contents-text">
          라즈베리 파이와 같은 에지 장비를 비롯하여, 일반 단일 서버, 다중 서버
          클러스터 등을 지원합니다.
        </p>
        <p class="tech-contents-text">
          시계열 센서 데이터 및 머신 로그 데이터 처리에 특화된 기능 및
          아키텍처를 갖고 있습니다.
        </p>
        <div class="tech-contents-title">Influx DB 소개</div>
        <p class="tech-contents-text">
          InfluxData에서 개발 중인 오픈소스 시계열 DBMS입니다.
        </p>
        <p class="tech-contents-text">
          시계열 데이터 처리에 있어서 가장 유명한 제품 중 하나입니다. InfluxDB
          또한 클러스터를 지원합니다.
        </p>
        <div class="tech-title" id="anchor2">
          Machbase 마크베이스 DB VS InfluxDB 아키텍처 비교
        </div>
        <p class="tech-contents-text">
          마크베이스(Machbase), InfluxDB 제품 모두 시계열 데이터 처리에 특화된
          제품으로 주요 특징을 요약하면 아래와 같습니다.
        </p>
        <p class="tech-contents-text">
          이 포스트에서는 사용성(Usability) 위주의 특징 분석을 먼저 수행하고,
          성능 테스트 등이 필요한 인덱스, 내부 구조와 관련한 내용은 성능
          테스트를 진행하고 차후에 기술하겠습니다.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/compare.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          마크베이스 machbase vs InfluxDB 아키텍처 비교
        </p>
        <div class="tech-title" id="anchor3">구현 언어 / Client interface</div>
        <p class="tech-contents-text">
          마크베이스Machbase는 서버 코드는 C로, ODBC/CLI 및 서버 내장 도구들은
          C++로 작성되어 있으며, JDBC, C#, Scala는 각기 그 언어로 라이브러리가
          작성되어 있습니다. 서버와 클라이언트 간의 통신 프로토콜은 일반적인
          RDBMS가 지원하는 인터페이스(Prepare/Bind/Execute)를 위한 전용
          프로토콜로 작성되어 최적의 효율성을 내도록 주의 깊게 구현되어
          있습니다.
        </p>
        <p class="tech-contents-text">
          C# connector는 마크베이스Machbase github에 공개되어 누구나 내부 구현을
          참조할 수 있습니다.
        </p>
        <p class="tech-contents-text">
          InfluxDB는 GO 언어로 작성되어 있으며, 통신프로토콜은 REST 기반으로
          구성되어 있습니다. 다양한 언어로 된 client 라이브러리를 제공하지만
          Prepare/Bind/Execute를 비롯한 인터페이스는 제공되지 않습니다. 대표적인
          C++ 클라이언트 라이브러리(InfluxDB 홈페이지에서 연결된) 소스 코드를
          보면 모든 연산이 REST로 변환되어 전달되는 것을 알 수 있습니다.
          오픈소스 http 라이브러리인 curl을 이용하여 구현되어 있네요.
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
          REST 기반의 인터페이스는 Web 환경에서는 더 편리하게 사용할 수
          있습니다. 웹서버에서 질의를 전송하거나, 대량의 센서들이 시계열 DB에
          데이터를 입력하기 위해서 REST를 사용하면 매우 편리하게 사용할 수
          있습니다. 물론 Machbase도 REST를 지원하므로 Influx의 고유한 장점으로
          볼 수는 없습니다.
        </p>
        <p class="tech-contents-text">
          하지만, 소수의 센서 데이터가 대량의 데이터를 매우 빠르게 생성하는 경우
          — 예를 들어, 진동센서와 같이 매우 짧은 주기로 데이터를 생성된다면
          Machbase 고유의 API인 SQLAppend나, 일반적인 ODBC Interface인
          Prepare-execute, Array-Binding, Batch execute 등의 기법을 이용하면
          매우 효율적이지만 모든 프로토콜이 REST인 InfluxDB는 이를 수행하기
          어렵습니다. 따라서 지속적으로 대량의 데이터가 짧은 주기로 발생하는
          환경에서는 InfluxDB는 비효율적입니다.
        </p>
        <p class="tech-contents-text">
          이와 관련한 성능 테스트는 차후에 진행해 볼 예정입니다.
        </p>
        <div class="tech-title" id="anchor4">Data Model</div>
        <p class="tech-contents-text">
          마크베이스Machbase는 관계형 모델을 지원합니다. 센서 데이터 처리용
          테이블인 TAG는 생성 시 필수적인 칼럼(센서 ID, 입력 시간, 입력 값)을
          제외하고 추가로 필요한 칼럼들을 정의할 수 있고, 이는 반드시 DDL을
          이용하여 정의되어야 합니다.
        </p>
        <p class="tech-contents-text">
          반면 InfluxDB는 tagset이라는 반정형 데이터 포맷을 지원합니다. 하나의
          레코드는 key, tag, value list로 구분됩니다. 인덱스는 tag에 대해서만
          생성 가능합니다. 모든 데이터는 명시적으로 지정하지 않더라도 입력 시간
          칼럼 값을 갖고, select 시에 time 칼럼을 선택하지 않더라도 데이터에
          반드시 포함되어 있어서 질의 결과에 포함됩니다. influxDB에서 테이블에
          해당하는 것은 series로, 이를 생성하는 명시적인 DDL이 없으므로 아래의
          질의문을 보고 이야기를 하겠습니다. 이 질의에서 입력될 데이터를 위한
          테이블 생성문은 필요치 않습니다.(테이블 생성 질의가 없습니다.)
        </p>
        <div class="tech-code-box">
          <span class="red">INSERT</span> treasures,captain_id=pirate_king
          <span class="red">value</span>=2
        </div>
        <p class="tech-contents-text">
          참참 생소하죠? 이를 machbase query로 바꾸면(테이블과 인덱스 생성을
          위한 DDL을 포함하여),
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
          예, 칼럼명이 insert 문에 다 들어가 있습니다. InfluxDB는 스키마가
          없으므로, 칼럼명을 입력 시에 일일이 지정해야 합니다. 그리고
        </p>
        <div class="tech-code-box">
          <span class="green">captain_id</span>=pirate_king value=2
        </div>
        <p class="tech-contents-text">
          앞쪽의 captain_id와 뒤쪽의 value 사이의 space가 있는데, 스페이스
          앞쪽에 있는 column=value 절 (즉 captain_id=pirate_king) 이 tag 절이며,
          이 값에 대해서만 인덱싱이 됩니다. 이 인덱스는 중첩해서 적용될 수도
          있습니다.
        </p>
        <div class="tech-code-box">
          <span class="green">captain_id</span>=pirate_king,other_tag=tag1
          value=2,value2=1
        </div>
        <p class="tech-contents-text">
          이 값은 captain_id와 other_tag에 대해서 인덱싱이 되고, space 문자로
          나눠어진 value, value2는 인덱싱이 안되는 값으로 입력됩니다. 질의시에
          인덱스가 안된 값에 대해서 검색을 하면 검색이 느린데, 이것은 fullscan
          질의 가 되므로 당연하게 보입니다. 그런데 인덱스가 안되는 칼럼에 대해서
          GROUP BY 절을 쓸 수가 없습니다. GROUP BY 절은 반드시 tag 칼럼에
          대해서만 적용됩니다.
        </p>
        <p class="tech-contents-text">
          이와 같이 column=value, tag=value 형태로 설정되는 key-value 데이터
          모델을 InfluxDB는 tagset이라고 하며, Machbase와 같은 relational
          model과 차이점으로 볼 수가 있습니다.
        </p>
        <div class="tech-title" id="anchor5">Query Language</div>
        <p class="tech-contents-text">
          Machbase는 SQL 질의에 시계열 데이터 특성을 위해 추가 문법을
          제공합니다. 그래서 SQL에 익숙한 사용자들은 별 무리 없이 사용이
          가능하죠. InfluxDB는 이를 좀 더 많이 변화시켜서 Machbase에 비해
          No-SQL과 비슷하게 변형하였습니다.
        </p>
        <p class="tech-contents-text">간단한 Query와 결과를 살펴보겠습니다.</p>
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
          네, SELECT로 질의하는 칼럼명에 time이 없음에도 불구하고 강제적으로
          해당 칼럼이 삽입되어 의미 없는 값이 출력되기도 하고, 칼럼명에 해당하는
          값을 쌍따옴표로 둘러치기는 하지만 이해하기에는 별 무리가 없어
          보입니다.
        </p>
        <p class="tech-contents-text">
          과거에는 Flux라는 Query 언어를 갖고 있었는데 앞서 설명한 SQL like 한
          Query 언어로 변경하고 있다고 합니다.
        </p>
        <div class="tech-code-box">
          <span class="red">from</span>(db:"metrics")<br />|>
          <span class="red">range</span>(<span class="red">start</span>:-1h)
          <br />|> <span class="red">filter</span>(fn: (r) => r._measurement ==
          "foo")
        </div>
        <p class="tech-contents-text">이것은 Machbase SQL로 변환하면,</p>
        <div class="tech-code-box">
          <span class="red">SELECT</span> *<br /><span class="red">FROM</span>
          metrics<br /><span class="red">WHERE</span> measurement =
          <span class="red">'foo'</span> DURATION 1
          <span class="red">hour</span>;
        </div>
        <div class="tech-title" id="anchor6">결론</div>
        <p class="tech-contents-text">
          이 포스트에서 다룰 인터페이스 내용에 대한 부분은 이 정도로 마칠까
          합니다. 두 제품 모두 시계열 데이터를 빠르게 처리할 목적으로
          개발되었지만, 관계형 데이터베이스와 DBMS 표준 인터페이스를 최대한
          지원하는 Machbase와 달리 InfluxDB는 좀 더 No-SQL에 가까운 특징을 갖고
          있습니다.
        </p>
        <p class="tech-contents-title">요약하면,</p>
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
            Machbase는 C로 구현되었으며 전통적인 DB 인터페이스(ODBC/JDBC 등)을
            지원하지만, InfluxDB는 GO로 구현되었고 REST 기반의 인터페이스와 이를
            crappting 하는 구조로 Prepare/Bind/Execute로 동작하지 않는다.
          </li>
          <li>
            Machbase는 관계형 데이터베이스로 DDL을 이용하여 정의된 스키마대로
            동작하고, 이는 기존 DBMS와 동일한 외형을 갖지만, InfluxDB는 그렇지
            않고, tagset이라는 독자적인 데이터 모델을 이용하며, DDL이 존재하지
            않고 칼럼 데이터 파싱을 실시간으로 수행한다.
          </li>
          <li>
            Machbase는 Query 언어로 SQL 기반에 추가 확장 구문을 지원하고,
            InfluxDB도 유사하지만 보다 No-SQL에 가까운 형태로 동작한다.
          </li>
        </ul>
        <p class="tech-contents-text">
          실제로 아키텍처 비교에 의한 성능 측정까지 다루어야 했지만 시간 관계로
          다루지 못하여 안타깝습니다. 다음에 이 내용은 반드시 다루도록
          하겠습니다.
        </p>
        <p class="tech-contents-text">
          추가로 의문사항이나 비교해야 할 내용이 있으면 연락 주십시오.
        </p>
        <p class="tech-contents-text">감사합니다</p>
        <p class="tech-contents-text">Machbase CRO, Grey Shim</p>
      </div>
    </div>
  </div>
</section>
<footer>
  <div class="footer_inner">
    <div class="footer-logo">
      <img class="footer-logo-img" src="../../img/machbase-logo-w.png" />
      <a href="/kr/home/contactus">
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
          <a href="https://blog.naver.com/machbasekr" target="_blank"
            ><img class="sns-img" src="../../img/naver.png"
          /></a>
        </div>
      </div>
    </div>
        <select id="languageSelector" onchange="changeLanguage()">
      <option value="kr">한국어</option>
      <option value="en">English</option>
    </select>
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
          <a href="https://blog.naver.com/machbasekr" target="_blank"
            ><img class="sns-img" src="../../img/naver.png"
          /></a>
        </div>
      </div>
      <a href="/kr/home/contactus">
        <button class="contactus">고객 문의</button>
      </a>
    </div>
        <select id="languageSelector" onchange="changeLanguage()">
      <option value="kr">한국어</option>
      <option value="en">English</option>
    </select>
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
  function changeLanguage() {
    var languageSelector = document.getElementById("languageSelector");
    var selectedLanguage = languageSelector.value;
    if (selectedLanguage !== "kr") {
      let locationPath = location.pathname.split("/");
      locationPath.splice(1, 1);
      location.href = location.origin + locationPath.join("/");
    }
  }
</script>
