---
title: Blog
description: "사물을 위한 데이터베이스"
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
        <li class="menu-a"><a href="/kr/home/download">Download</a></li>
        <li class="menu-a">
          <a href="https://support.machbase.com/hc/en-us">Support</a>
        </li>
        <li class="menu-a"><a href="/kr/home/contactus">Contact US</a></li>
        <li class="menu-a">
          <select id="languageSelector" onchange="changeLanguage()">
            <option value="kr">한국어</option>
            <option value="en">English</option>
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
      <option value="kr">한국어</option>
      <option value="en">English</option>
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
            <a href="https://www.cems.ai/" target="_blank">CEMS</a>
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
          <div class="docs-sub"><a href="/neo" target="_blank">Neo</a></div>
          <div class="docs-num">
            <a href="/dbms" target="_blank">Classic</a>
          </div>
        </div>
      </li>
      <li><a href="/kr/home/download">Download</a></li>
      <li><a href="https://support.machbase.com/hc/en-us">Support</a></li>
      <li><a href="/kr/home/download">Contact US</a></li>
      <li></li>
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
    <h4 class="blog-title">사물을 위한 데이터베이스</h4>
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
        <li class="tech-list-li" id="tech-list-li">개요</li>
      </a>
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">
          사물인터넷 데이터의 종류와 특성
        </li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">
          IoT 센서 데이터를 활용한 도전
        </li>
      </a>
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">
          IoT 데이터에 최적화된 마크베이스
        </li>
      </a>
    </ul>
    <div class="tech-contents">
      <div>
        <p class="tech-title" id="anchor1">개요</p>
        <p class="tech-contents-text">
          사물인터넷(IoT, Internet of Things)은 수많은 장치들이 인터넷
          네트워크를 통해 데이터를 상호 전달 및 처리하는 것을 말합니다. IoT
          장치들에는 일반적인 데스크탑과 랩탑 등을 제외한 센서, 디지털
          구동기(actuator) 및 이동 단말 등이 포함됩니다.
        </p>
        <p class="tech-contents-text">
          이들 장치에서 생성되는 데이터를 수집, 가공, 분석하여 정보를 생성하고,
          새로운 부가가치를 창출하는 것이 4차 산업 시대의 모습입니다.
        </p>
        <p class="tech-contents-text">
          다만, IoT 데이터는 조금 다른 특징이 있습니다.
        </p>
        <p class="tech-contents-text">
          대표적으로 여러 곳에서 대량의 데이터가 산발적으로 발생하기 때문에 기존
          데이터 솔루션으로 처리하기가 매우 어렵습니다.
        </p>
        <p class="tech-contents-text">
          이번 포스트에서는 IoT 데이터의 종류와 특징을 살펴보고, 사물 인터넷
          데이터를 처리하기 위해서 극복해야 할 과제에 대해서 말씀드리겠습니다.
        </p>
        <div class="tech-title" id="anchor2">
          사물인터넷 데이터의 종류와 특성
        </div>
        <p class="tech-contents-text">
          사물 인터넷은 한때 RFID 데이터를 이용하는 시스템만을 지칭하는
          용어였지만, ICT 기술의 발달로 더욱 다양한 종류의 데이터가 포함되게
          되었습니다.
        </p>
        <p class="tech-contents-text">
          그럼 RFID를 비롯한 어떤 다양한 종류의 데이터가 있고, 그 특성을
          알아보겠습니다.
        </p>
        <div class="tech-contents-title">
          RFID(Radio Frequency Identification)
        </div>
        <p class="tech-contents-text">
          RFID는 전파로 기록된 정보를 송수신하는 tag로 장비에 붙여두거나 장비
          내에 포함시킬 수 있습니다. RFID의 tag는 데이터를 저장하는 IC chip과
          데이터를 송수신하는 안테나로 구성되고, tag의 데이터는 tag reader를
          통해 무선으로 통신됩니다.
        </p>
        <p class="tech-contents-text">
          RFID는 매우 다양한 분야에서 활용되고 있습니다. 예로 들면:
        </p>
        <ul class="tech-ul">
          <li>여권</li>
          <li>휴대전화</li>
          <li>물류 관리</li>
          <li>재고 관리</li>
          <li>헬스케어</li>
        </ul>
        <p class="tech-contents-text">
          tag는 대량생산으로 매우 저렴해지면서 많은 분야에서 사용될 수 있지만,
          bar code에 비해서는 아직 비싸기 때문에 유통 등의 분야에서는 확산이
          더디게 진행되고 있습니다. RFID를 물류에서 사용할 경우에는 tag의
          위치정보, 시간 정보를 기반으로 시계열에 따른 이동 궤적을 추적할 수
          있습니다.
        </p>
        <div class="tech-contents-title">로그 데이터(Log Data)</div>
        <p class="tech-contents-text">
          수많은 S/W와 H/W에서 생성되는 로그 데이터(Log Data)는 장치와
          소프트웨어를 관리하는 데 있어 매우 중요한 역할을 수행합니다.
        </p>
        <p class="tech-contents-text">
          하지만, 로그 데이터는 텍스트 형태로 생성되고 일정 용량이 되면 자동
          삭제될 수 있어, 데이터의 장기 수집과 분석을 위해 다른 방식이
          필요합니다.
        </p>
        <p class="tech-contents-text">
          로그 데이터는 일반적으로 로그의 생성 시점을 반드시 기록하고, 입력된
          메시지 내용으로부터 다양한 정보(ip address, mac address 등의 id 정보,
          시스템 사용량 및 부하 정보, 온도 및 습도 등 환경 정보 등)를 포함하고
          있습니다.
        </p>
        <p class="tech-contents-text">
          정형 데이터가 아니어서 관계형 DBMS의 스키마로 나타내기 위해서는 로그
          메시지의 파싱 등의 변환 과정이 필요합니다. 로그 데이터는 생성하는
          프로그램에 따라 여러 가지의 format으로 기록되므로 처리하기에 쉽지 않은
          측면이 있습니다.
        </p>
        <div class="tech-contents-title">위치 및 환경 데이터</div>
        <p class="tech-contents-text">
          RFID의 예에서 볼 수 있듯이 이동 객체 데이터 및 기상 환경 데이터는 그
          데이터가 발생한 곳의 위치 정보가 매우 중요합니다.
        </p>
        <p class="tech-contents-text">
          일반적으로 위치정보는 GPS(global positioning system)을 이용하여 얻게
          되는데, 여러 개의 위성을 통해 얻는 GPS 정보는 그 특성상 대략의
          위치만을 알 수 있을 뿐, 정확한 위치 정보를 얻기가 쉽지 않은 특징이
          있습니다.
        </p>
        <p class="tech-contents-text">
          특수한 환경에서는 local positioning system을 이용하여 더 상세한 정보를
          얻을 수 있는 경우도 있습니다.
        </p>
        <p class="tech-contents-text">
          이동하지 않는 장비의 위치 데이터도 매우 중요한 정보로 취급될 수
          있습니다.
        </p>
        <p class="tech-contents-text">
          예를 들어 해상에 떠 있는 센서의 온도, 습도, 기압 등의 환경 정보와 위치
          정보를 조합하면, 기상 예보, 재난 경보등에 매우 도움이 되는 정보를 얻을
          수 있습니다.
        </p>
        <p class="tech-contents-text">
          위치 및 환경 데이터는 지리정보 시스템(Geographical information
          system)과 모바일 컴퓨팅 등의 기술과 융합하여 연구되고 있습니다.
        </p>
        <div class="tech-contents-title">시계열 데이터 — 센서 데이터</div>
        <p class="tech-contents-text">
          우리는 수많은 센서들에 둘러싸여 생활하고 있습니다. 휴대 전화에도
          카메라, GPS, 가속도 센서 등의 수많은 센서가 부착되어 있으며 공장이나
          공공 부문(도로, 철도, 항만, 공항)에도 매우 많은 센서들이 있습니다.
        </p>
        <p class="tech-contents-text">
          이 센서 데이터를 분석하면 다양한 부분에서 이전에 실행할 수 없었던
          문제들을 해결할 수 있습니다. 각 센서는 유일 식별자를 갖고, 읽어들인
          데이터 값과 측정 시간을 같이 기록하여 전달합니다.
        </p>
        <p class="tech-contents-text">
          &lt;Timstamp, 센서 식별자, 센서 값>의 형태로 기록되는 데이터는 차후에
          데이터 분석을 위해 순차적으로 입력시간에 따라 저장되며 이를 시계열
          센서 데이터라고 합니다.
        </p>
        <div class="tech-contents-title">시계열 데이터 — 제어 데이터</div>
        <p class="tech-contents-text">
          실시간으로 변화하는 구동기(actuator) 등에서 수집한 센서 데이터뿐만
          아니라, 그 구동기를 제어하기 위한 제어 신호 데이터도 시계열로
          기록됩니다.
        </p>
        <p class="tech-contents-text">
          이러한 데이터들은 실시간으로 변화하는 중의 데이터이므로 대량의
          데이터가 발생하여 저장 및 분석에 어려움을 주고 있습니다. 이후 사고
          분석, 불량 예측, 품질 개선, 생산량 조절 등에 기존의 데이터를 분석하여
          진단할 수 있습니다.
        </p>
        <div class="tech-contents-title">시계열 데이터 — Historical Data</div>
        <p class="tech-contents-text">
          시간을 포함하는 센서 데이터를 모으면 이 데이터는 historical data가
          됩니다. 데이터를 수집하는 주기에 따라 데이터의 양은 매우 증가합니다.
        </p>
        <p class="tech-contents-text">
          자세한 분석을 위해서 데이터 수집 주기를 짧게 할수록 데이터양이 커지기
          때문에, 시계열 데이터베이스(TSDBD, Machbase)로 해결해야 합니다.
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
    <div class="tech-title" id="anchor3">IoT 센서 데이터를 활용한 도전</div>
    <p class="tech-contents-text">
      앞서 논의한 것과 같이, 많은 수의 센서에서 발생되는 데이터들은 시계열(Time
      Series)의 특성을 가지며 Historical하게 저장됩니다.
    </p>
    <p class="tech-contents-text">
      단일 시스템에서 동작하는 DBMS의 경우 저장 기간이 길어질수록 색인 및 검색
      성능은 악화될 수 밖에 없고, 중단 없는 수집과 저장을 유지하는 것도
      어렵습니다. 마침내 PB단위에 달하는 데이터 처리 자체가 불가능한 DBMS의
      한계를 극복하고자 Hadoop과 같은 Bigdata 플랫폼들이 등장하게 되었습니다.
    </p>
    <p class="tech-contents-text">
      하지만 Map Reduce와 같은 분산 처리의 경우에도 배치 처리(분산 저장과
      검색)에 최적화되어 있어서 실시간 데이터 분석에는 한계가 있습니다.
    </p>
    <p class="tech-contents-text">
      즉, IoT 센서 데이터에 대한 실시간 처리를 위한 새로운 방법이 필요합니다.
    </p>
    <div class="tech-contents-title">Query language</div>
    <p class="tech-contents-text">
      IoT 센서 데이터에는 정형 데이터(Structured data) 뿐만 아니라 반정형
      데이터(Semi-structured data)도 많이 있습니다.
    </p>
    <p class="tech-contents-text">
      정형 데이터의 경우 SQL이 대표적인 Query language로 사용 되고 있지만,
      반정형 데이터를 위한 Query 언어는 통일되어 있지 않습니다.
    </p>
    <p class="tech-contents-text">
      물론 Big data 시스템이 도입되면서 No-SQL Query language들이 등장했지만,
      여전히 다양한 이질적 언어들이 혼용되고 있습니다. 결국 Spark, Impala 등의
      SQL on Hadoop 제품들이 보급되면서 다시 SQL Query language를 많이 사용하고
      있는 추세입니다.
    </p>
    <div class="tech-contents-title">Interface</div>
    <p class="tech-contents-text">
      SQL언어를 지원하는 DBMS는 ODBC/JDBC등의 전통적 인터페이스를 제공하지만,
      Operational Historian제품들은 REST API를 통해 HTTP 프로토콜을 통한 JSON
      기반의 Query 인터페이스를 많이 사용합니다.
    </p>
    <p class="tech-contents-text">
      많은 운영 환경들이 WEB 기준으로 이동하면서 사용이 편리한 REST API는 반드시
      지원해야 할 인터페이스가 되었습니다.
    </p>
    <div class="tech-contents-title">트랜잭션 처리</div>
    <p class="tech-contents-text">
      초당 1000억건 이상의 데이터를 실시간으로 처리해야 하는 분산 데이터
      시스템에서 트랜잭션(e.g. ACID, Two-phase locking)은 수행되기 어렵습니다.
      시계열 데이터는 완전 삭제 전까지 갱신 연산이 없기 때문에, 완벽한 ACID를
      기반으로 하는 RDBMS의 트랜잭션 처리는 성능 문제를 야기합니다.
    </p>
    <p class="tech-contents-text">
      방대한 IoT 데이터를 실시간으로 처리하는 데 있어서, 전통적인 ACID 기반
      트랜잭션 보다 시계열 데이터의 특징을 반영한 새로운 효율적 데이터 처리
      기법이 요구되고 있습니다.
    </p>
    <div class="tech-contents-title">시계열 데이터 통계 처리</div>
    <p class="tech-contents-text">
      시계열 데이터는 sum, count, avg, sampling 등의 통계연산이 빈번하게
      필요합니다. 이들 통계값은 시각화와 고급 분석을 위해서 사용됩니다.
    </p>
    <p class="tech-contents-text">
      RDBMS는 대량의 데이터를 실시간으로 입력하면서 동시에 통계 작업을 수행하는
      것이 매우 어렵기 때문에, 최근에는 Stream DB가 새롭게 주목받고 있습니다.
    </p>
    <div class="tech-title" id="anchor4">IoT 데이터에 최적화된 Machbase</div>
    <p class="tech-contents-text">
      Machbase Database는 IoT 데이터 처리에서 요구하는 성능과 기능들을 충족하는
      유일한 데이터베이스입니다.
    </p>
    <ul class="tech-ul">
      <li>실시간 대량 데이터 처리</li>
      <li>사용하기 편리하고 효율적인 Query 언어 제공</li>
      <li>효율적으로 트랜잭션 처리</li>
      <li>시계열 데이터 통계 연산</li>
    </ul>
    <div class="tech-contents-title">대량 데이터의 실시간 처리</div>
    <p class="tech-contents-text">
      분산 데이터 저장 및 Query 구조를 채택한 Machbase는 단일 장비에서 200만
      데이터의 입력 및 색인이 가능하고, 장비를 추가함에 따라 성능이 증가하여
      초당 천만건 이상의 센서 데이터도 처리가 가능합니다.
    </p>
    <p class="tech-contents-text">
      고속 데이터 입력을 위한 전용 API와 고속으로 색인을 생성할 수 있는 인덱수
      구조를 갖고 있습니다.
    </p>
    <p class="tech-contents-text">
      시계열 데이터의 시간에 따른 추가에도 Cluster에 장비를 추가하여 성능과
      공간을 확장할 수 있습니다.
    </p>
    <div class="tech-contents-title">
      효율적인 Query 언어 제공 및 인터페이스
    </div>
    <p class="tech-contents-text">
      데이터 처리에 최적화된 SQL언어를 제공합니다. No-SQL 제품들도 다시
      SQL언어를 제공하기 시작하고 있습니다.
    </p>
    <p class="tech-contents-text">
      반정형 데이터를 효율적으로 검색하기 위한 Inverted index및 관련 구문을
      제공하여 반정형 데이터로 쉽게 검색 및 처리가 가능합니다.
    </p>
    <p class="tech-contents-text">
      SQL 표준 인터페이스인 ODBC/JDBC 뿐만 아니라 REST Api도 제공 합니다.
    </p>
    <div class="tech-contents-title">효율적인 트랜잭션 처리</div>
    <ul class="tech-ul">
      <li>시계열 데이터에 대한 최적의 트랜잭션 기법을 고안</li>
      <li>
        Update는 제공하지 않으나 Insert, Delete가 가능 하며, Node fail에 의한
        재시작시에도 recovery과정을 거쳐 data와 index의 consistency 유지
      </li>
      <li>
        Enterprise edition에서는 분산 데이터 저장 기법을 이용하여 node fail에
        의한 데이터 유실을 원천적으로 해결
      </li>
    </ul>
    <div class="tech-contents-title">시계열 통계 처리</div>
    <ul class="tech-ul">
      <li>
        시계열 센서 데이터에 대한 자동 통계 기능 : 입력된 센서 데이터를 단위
        시간(초, 분, 시)별, 센서 식별자 별로 자동으로 통계를 생성한다.
      </li>
      <li>시계열 데이터에 최적화된 확장 Query 조건절을 제공한다.</li>
      <li>
        Machbase Database는 시계열 데이터를 처리하기 위한 기능과 성능 요구사항을
        모두 고려하여 구현한 제품으로 사물 인터넷 데이터 처리에 적합하다.
      </li>
    </ul>
  </div>
</section>
<footer>
  <div class="footer_inner">
    <div class="footer-logo">
      <img class="footer-logo-img" src="../../img/machbase-logo-w.png" />
      <a href="/kr/home/contactus">
        <button class="contactus">고객 문의</button>
      </a>
    </div>
    <div>
      <p class="footertext">서울시 강남구 테헤란로 20길 10, 3M 타워, 9층</p>
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
  </div>
  <div class="footer_tablet_inner">
    <div class="footer-logo">
      <img class="footer-logo-img" src="../../img/machbase-logo-w.png" />
    </div>
    <div>
      <p class="footertext">서울시 강남구 테헤란로 20길 10, 3M 타워, 9층</p>
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
  function changeLanguage2() {
    var languageSelector = document.getElementById("languageSelector2");
    var selectedLanguage = languageSelector.value;
    if (selectedLanguage !== "kr") {
      let locationPath = location.pathname.split("/");
      locationPath.splice(1, 1);
      location.href = location.origin + locationPath.join("/");
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
