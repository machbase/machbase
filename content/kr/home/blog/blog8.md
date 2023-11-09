---
title: Blog
description: "시계열 DB(Time-Series Database) 아키텍처 및 성능 비교_ 마크베이스Machbase와 MongoDB(센서 데이터 처리시)"
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
    <h4 class="blog-title">
      시계열 DB(Time-Series Database) 아키텍처 및 성능 비교_ 마크베이스Machbase와 MongoDB(센서 데이터 처리시)
    </h4>
    <div class="blog-date">
      <div>
        <span>by Grey Shim / 14 Sep 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">개요</li></a
      >
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">
          시계열 센서 데이터의 특징과 아키텍처 비교
        </li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">
          센서 데이터 인덱스 vs B+Tree
        </li>
      </a>
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">
          입력 및 단순 질의 성능 비교
        </li>
      </a>
      <a href="#anchor5">
        <li class="tech-list-li" id="tech-list-li">결론</li>
      </a>
    </ul>
    <div class="tech-contents">
      <div>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/blog8-1.webp" alt="" />
        </div>
        <p class="tech-contents-link-text"></p>
        <p class="tech-title" id="anchor1">개요</p>
        <p class="tech-contents-text">
          이 포스트에서는 마크베이스와 MongoDB의 아키텍처 차이를 살펴 보고, 시계열 센서 데이터 처리의 성능을 비교해 보는 시간을 가져보겠습니다.
          센서 데이터 처리 시스템의 개발을 시작할 때, 개발자 자신에게 익숙한 DBMS를 선택하는 경향이 강합니다. 하지만 시계열 센서 데이터가 가진 특성을 고려하지 않고 익숙한 툴을 써서 개발하면 데이터 처리에 있어서 알지 못하던 어려움이 있다는 사실도 함께 기술하고자 합니다.
        </p>
        <div class="tech-contents-title">Machbase 소개</div>
        <p class="tech-contents-text">
          마크베이스는 시계열 센서 데이터의 빠른 입력, 검색, 통계등을 목표로 개발된 DBMS입니다. 라즈베리 파이와 같은 에지 장비를 비롯하여, 일반 단일 서버, 다중 서버 클러스터등을 지원합니다. 시계열 센서 데이터 및 머신 로그 데이터 처리에 특화된 기능 및 아키텍처를 갖고 있습니다. 마크베이스의 아키텍처에 관한 자세한 내용은 아래에 계속됩니다.
        </p>
        <div class="tech-contents-title">MongoDB 소개</div>
        <p class="tech-contents-text">
          MongoDB는 문서(Document)기반의 데이터베이스 엔진으로, 스키마가 없는 데이터를 json형태로 그대로 저장하고 불려낼 수가 있어서, 웹 관련 분야에서 매우 편리하게 사용되고 있습니다.
          시계열 센서 데이터 응용 영역에서는 그다지 적합하지는 않습니다만, 반도체 생산 공정 데이터가 생산 설비에서 xml 형태로 생성되기 때문에 이런 경우 사용상의 편의성으로 인해 활용하는 경우가 많은 것 같습니다.
        </p>
        <div class="tech-title" id="anchor2">
          시계열 센서 데이터의 특징과 아키텍처 비교
        </div>
        <p class="tech-contents-text">
          시계열 센서 데이터는 단위 데이터의 양은 적으며, 업데이트가 되지 않고 시간이 지남에 따라 지속적으로 증가하는 형태의 데이터 입니다. 센서 하나당 데이터를 시간 순으로 값만 계속 변경되는 형태입니다.<br>
          설치된 센서의 수가 증가하고 데이터 수집 주기가 짧아지는 경향이 있으므로 단위 시간당 생성되는 데이터의 양이 엄청나게 증가합니다.
        </p>
        <p class="tech-contents-text">
          더군다나, 데이터를 더 오랫동안 보관해야 하기 때문에 매우 대량의 데이터가 생성되므로 이를 저장하고, 처리하기 위한 시스템의 개발이 어려운 것이 현실입니다.<br>
          시계열 센서 데이터는 결국, 시간과 센서의 식별자를 key로 하여 검색을 수행하는 경우가 많다는 점, 실시간 처리를 위해서는 입력성능이 매우 중요하다는 점 또한 유의해야 할 사항입니다.
        </p>
        <p class="tech-contents-text">
          다음 절에서 상세한 내용 비교를 해 보겠습니다.
        </p>
        <div class="tech-contents-title">Schema vs schema-less</div>
        <p class="tech-contents-text">
          마크베이스는 관계형 모델에 의한 SQL DDL로 정의되는 스키마 정의가 필요하고, MongoDB는 스키마가 필요 없습니다.
        </p>
        <p class="tech-contents-text">
          웹사이트의 사용자 관련 설정 데이터를 json형태로 정의하여 이를 웹 응용에서 처리하는 것은 매우 빈번하게 사용되는 기법입니다. 이 데이터를 변경하지 않고 MongoDB에 입력하고, 사용자 id로 이 데이터를 빠르게 불러오는데 있어 MongoDB는 매우 편리합니다. MongoDB는 데이터를 binary json형태로 저장합니다. 아래의 예를 보시죠.
        </p>
        <div class="tech-code-box">
          <span>Bson:</span><br />
          \x16\x00\x00\x00&nbsp;&nbsp;<span class="green"
            >// total document size</span
          ><br />
          \x02&nbsp;&nbsp;<span class="green">// 0x02 = type String</span><br />
          hello\x00&nbsp;&nbsp;<span class="green">// field name</span><br />
          \x06\x00\x00\x00world\x00&nbsp;&nbsp;<span class="green"
            >// field value (size of value, value, null terminator)</span
          ><br />
          \x00&nbsp;&nbsp;<span class="green"
            >// 0x00 = type EOO ('end of object')</span
          ><br />
        </div>
        <p class="tech-contents-link-text">&lt; 출처 Wikiped ></p>
        <p class="tech-contents-text">
          텍스트로 나타낸 Json의 장황한(그러나 알기 쉬운) 데이터에 비해서는 매우 간략화 되어 있습니다만, 각 attribute마다 attribute의 타입, 이름, 길이 등을 모두 표현하고 있습니다.
          <br>
          스키마가 없기 때문에 이전 데이터에 있던 칼럼이 이 데이터에는 없을 수도 있습니다. 길이도 항상 유동적이니 반드시 필요하죠. 원하는 애트리뷰트 ‘b’를 찾기 위해서는 bson 문서하나를 다 읽어서 b가 있는지 찾고 (없을 수도 있어요!) 그 타입을 얻어서 읽어야 합니다(같은 ‘b’ 애트리뷰트라도 타입이 다를 수 있습니다.)
        </p>
        <p class="tech-contents-text">
          반면 스키마 데이터는 항상 칼럼 명이 일정하며, 칼럼 타입도 또한 동일합니다. 그리고 레코드 전체를 파싱하지 않고, 원하는 칼럼 데이터가 어디에 있는지 바로 알 수 있습니다. (물론 자유롭게~ 데이터를 표현하고 싶은 분은 쓸 수가 없습니다.)
        </p>
        <p class="tech-contents-text">
          실시간 센서 데이터에 대해서는 어떨까요?, 센서 데이터는 정형 데이터로 사전에 설정된 칼럼 값들을 갖고 있으며, 이를 고정된 스키마로 표현하고, 처리하는 데 아무런 문제가 없습니다.
        </p>
        <p class="tech-contents-text">물론 MongoDB도 가능은 합니다. 여기서 정형 데이터와 비정형 데이터를 간단히 비교해 보면 다음과 같습니다.</p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/blog8-2.webp" alt="" />
        </div>
        <p class="tech-contents-text">
          데이터가 비정형일때 이를 정형데이터로 변환하기 위해서는 ER모델을 이용하여 데이터 모델을 설계해서 원 데이터를 적절한 테이블로 변환하여 입력해야 하고, 때에 따라서는 표현이 안될 수도 있습니다.
        </p>
        <p class="tech-contents-text">
         MongoDB와 같이 비정형 데이터를 변환 없이 그대로 사용할 수 있으면 정말 편리합니다. 하지만, 비정형 데이터는 검색이나 통계시에 원하는 데이터의 칼럼값을 얻기 위해서는 데이터의 실시간 파싱이 필요하며, 이는 큰 성능저하를 유발합니다. 이 성능저하를 분산처리등의 기법을 통해 해결할 수 있으나 다수의 서버를 이용해야 하므로 이에 따른 비용 문제가 발생합니다.
        </p>
        <p class="tech-contents-text">
          정형 데이터를 처리하는데 있어서 스키마 모델은 원하는 데이터가 어디에 있는지 (파싱 없이) 바로 읽어낼 수가 있고, 이는 대량의 데이터 처리시에 많은 성능 향상 요인이 됩니다. 앞서 말한 바와 같이, 실시간 시계열 데이터는 정형 데이터이므로 MongoDB의 비정형 데이터 모델 보다 정형 데이터 모델이 훨씬 더 효율적인 것을 알 수 있습니다.
        </p>
        <div class="tech-contents-title">SQL vs No-sql</div>
        <p class="tech-contents-text">
          마크베이스는 데이터 질의 언어로 SQL을 지원하며, MongoDB는 고유한 질의 방법이 있습니다. 이 절에서는 두 가지의 차이점을 살펴봅니다.
        </p>
        <p class="tech-contents-text">
          보통 스키마 데이터는 구조화된 질의 언어(SQL)을 이용하여 질의합니다. 워낙 오래전부터 개발된 언어이고, 널리 사용되고 있으므로 특별히 설명할 필요는 없겠죠. No-SQL또한 요즘에 널리 사용되고 있으며, 각 제품마다 처리 방식이 상이하여 전체적인 설명보다는 MongoDB의 질의 언어에 대해서만 설명하려 합니다.
        </p>
        <p class="tech-contents-text">
          앞서 말씀드린 바와 같이, MongoDB는 웹서비스 등의 활용 분야에 최적화되어 있습니다. 웹서비스에서 데이터를 json으로 표현하고, 이 데이터의 집합을 collection객체로 매핑합니다.(관계형 데이터 모델에서는 Table이죠). 주로 사용되는 연산은 키값으로 원하는 특정 데이터를 찾는 것입니다. 매우 단순한 질의이며, 대부분의 웹서비스는 데이터 입력과 키값으로 데이터 찾기로 원하는 부분을 거의 커버할 수 있습니다.
        </p>
        <div class="tech-code-box">
          <span>db.</span><span class="orange">collection.find</span>( {
          _id:<span class="blue">5</span>} )
        </div>
        <p class="tech-contents-text">
          Find 메서드에 원하는 조건을 늘어놓으면 추가로 검색조건절을 확장할 수 있습니다. 객체모델에서 매우 자연스럽게 보입니다.
        </p>
        <p class="tech-contents-text">
          시계열 데이터는 어떨까요? 시계열 데이터의 경우 가장 많이 쓰일 법한 질의는 특정한 기간 동안 특정 센서 id를 갖는 데이터들을 얻는것입니다. 물론 mongoDB도 가능합니다만 두 질의를 비교해 보면 차이점이 보이기 시작합니다.
        </p>
        <div class="tech-contents-title">마크베이스 질의(SQL)</div>
        <div class="tech-code-box">
          <span class="red">SELECT</span>&nbsp;*<br />
          <span class="red">FROM</span>&nbsp;tag<br />
          <span class="red">WHERE</span>&nbsp;name =
          <span class="orange">'EQ0^TAG287'</span><br />
          &nbsp;&nbsp;&nbsp;&nbsp;<span class="red">AND</span
          >&nbsp;time&nbsp;<span class="red">BETWEEN</span> to_date (<span
            class="orange"
            >'2018-01-01 00:00:00'</span
          >)<br />
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="red"
            >AND</span
          >
          to_date (<span class="orange">'2018-01-01 00:00:00'</span>) )
        </div>
        <p class="tech-contents-text">
         매우 선언적이며, 알기 쉽습니다. 특정 센서 식별자를 갖는 데이터를 하루치 검색하는 예제입니다.
        </p>
        <div class="tech-contents-title">mongoDB 질의</div>
        <div class="tech-code-box">
          <span>db.sensor.find(</span><span class="green">{name</span>:<span
            class="orange"
            >"EQ0^TAG287"</span
          >,<br />
          <span class="green">time</span>: {
          <span class="blue">$gte</span>:ISODate(<span class="orange"
            >"2018-01-01T00:00:00Z"</span
          >),<br />
          <span class="blue">$lt</span>:ISODate(<span class="orange"
            >"2018-01-02T00:00:00Z"</span
          >)}}).count()
        </div>
        <p class="tech-contents-text">
          검색언어가 좀 장황하고 복잡해 지기 시작했습니다. 아직은 그래도 쉬운가요?
        </p>
        <div class="tech-contents-title">통계</div>
        <p class="tech-contents-text">
          시계열 센서 데이터는 양이 너무나도 많기 때문에 시간별로 통계를 내서 그 값을 가시화하는 경우가 많습니다. Machbase는 이를 위해서 자동을 시간별 통계를 생성하며 이는 나중에 설명할 자동 Rollup 실행이라고 합니다. 이 통계 데이터를 이용하여 원하는 시간별 통계를 쉽게 얻을 수 있으며 통계데이터를 SQL로 얻는것도 가능합니다.
        </p>
        <div class="tech-code-box">
          <span class="red">SELECT</span
          ><span class="green"> /*+ ROLLUP(TAG, hour, max) */ </span>time,
          <span class="red">value as</span> max<br />
          <span class="red">FROM</span> TAG<br />
          <span class="red">FROM</span> name =
          <span class="ornage">'EQ1^TAG1024'</span>
          <span class="red"> AND</span> time
          <span class="red">BETWEEN</span> to_date(<span class="orange"
            >'2018-01-01 00:00:00'</span
          >)<br />
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="red"
            >AND</span
          >
          to_date (<span class="orange">'2018-01-01 23:59:59'</span>) )<br />
          <span class="red">ORDER BY</span> time<br />
        </div>
        <p class="tech-contents-text">
          ROLLUP 힌트를 이용하여, 실제로 통계를 수행하지 않고 사전에 계산해 둔 통계를 표시했습니다.
        </p>
        <p class="tech-contents-text">
          MongoDB도 유사한 질의를 실행할 수 있습니다. 이제 질의가 매우 복잡해 집니다.
        </p>
        <div class="tech-code-box">
          <span>db.sensor.aggregate(</span><br />[<br />
          { <span class="green">$match </span>: {<span class="green">name</span
          >:<span class="orange">"EQ1^TAG1024"</span>,<span class="green"
            >time</span
          >: { <span class="green">$gte</span>:ISODate(<span class="ornage"
            >"2018-01-01T00:00:00Z"</span
          >),<br />
          <span class="green">$lt</span>:ISODate(<span class="orange"
            >"2018-01-02T00:00:00Z"</span
          >)}}},<br />
          { <span class="green">$project</span> : {<br />
          &nbsp;&nbsp;&nbsp;&nbsp;_id : <span class="blue">0</span>,<br />
          &nbsp;&nbsp;<span class="red">"time"</span>:
          <span class="blue">1</span>,<br />
          <span class="red">"value"</span>: <span class="blue">1</span>,<br />
          }<br />
          },<br />
          { <span class="green">$group</span> : {<br />
          <span class="red">"_id"</span>: { <br />
          <span class="red">"year"</span>: { <span class="green">$year</span> :
          <span>"$time"</span>},<br />
          <span class="red">"month"</span>: {
          <span class="green">$month</span> : <span>"$time"</span>},<br />
          <span class="red">"day"</span>: {
          <span class="green">$dayOfMonth</span> : <span>"$time"</span>},<br />
          <span class="red">"hour"</span>: { <span class="green">$hour</span> :
          <span>"$time"</span>},<br />
          },<br />
          <span class="red">"maxValue"</span>: {
          <span class="green">$max</span> : <span>"$value"</span>},<br />
          <span class="red">"count"</span>: { <span class="green">$sum</span> :
          <span class="blue">1</span>}<br />
          }<br />
          },<br />
          { <span class="green">$sort</span>: { <br />
          <span class="red">"_id.year"</span>:
          <span class="blue">1</span>,<br />
          <span class="red">"_id.month"</span>:
          <span class="blue">1</span>,<br />
          <span class="red">"_id.day"</span>: <span class="blue">1</span>,<br />
          <span class="red">"_id.hour"</span>:
          <span class="blue">1</span>,<br />
          }<br />
          }<br />
          ])
        </div>
        <p class="tech-contents-text">
          사용상의 편리함은 개인의 의견에 따라 다르지만, 통계나 복잡한 조건절을 표현하면 MongoDB는 질의가 매우 장황해지는 경향을 띱니다.
        </p>
        <p class="tech-contents-text">
          시계열 센서 데이터 처리에서는 시간별 통계 기능이 매우 많이 사용되는 질의이기 때문에 질의가 복잡해질수록 MongoDB에서의 질의를 만드는 노력이 상상 이상으로 어려울 것이라는 것을 예상할 수 있습니다.
        </p>
        <div class="tech-title" id="anchor3">센서 데이터 인덱스 vs B+Tree</div>
        <p class="tech-contents-text">
          일반적으로 RDBMS에서도 많이 사용되는 B+Tree색인은 아래와 같이 생겼습니다.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog8-3.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          각 키는 leaf노드에 입력되며 leaf노드에는 키값들이 연결리스트 형태로 순차 접근이 가능합니다.
        </p>
        <p class="tech-contents-text">
          각 키는 leaf노드에 입력되며 leaf노드에는 키값들이 연결리스트 형태로 순차 접근이 가능합니다.
          데이터가 입력되어 leaf노드에 더이상 입력할 공간이 없으면 상위노드가 추가되는 형태로, 이 알고리즘은 입력되는 키값의 분포에 관계없이 트리가 한쪽으로 몰리는 현상이 없도록 디자인 되었습니다.
        </p>
        <p class="tech-contents-text">
          그런 이유로 이 구조는 디스크 기반 RDBMS에서 단일 조건의 검색 성능에 있어서는 나름 탁월한 성능을 발휘합니다.
          그러나, 시계열 센서 데이터와 같이 시간과 센서 식별자를 동시에 고려해야 하는 2차원 문제도 잘 풀 수 있을까요?
        </p>
        <p class="tech-contents-text">
          한편, 마크베이스의 센서 데이터 인덱스는 시간 및 센서 식별자 조건으로 정렬된 특수한 구조를 갖습니다.
        </p>
        <p class="tech-contents-text">
          시계열 센서 데이터의 경우 대부분의 질의는 시간 범위와 센서 아이디를 조건으로 검색하므로 이러한 질의에 최대한 최적화된 색인 구조를 구현하였습니다. 이 두 가지 색인의 특징을 비교하면 다음과 같습니다.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog8-4.webp"
            alt=""
          />
        </div>
        <ul class="tech-ul">
          <li>
            B+Tree 색인은 대량 데이터 입력시 입력 성능이 저하될 수 있습니다.
          </li>
          <li>
            B+TB+Tree 색인은 빠르게 데이터를 입력하면 지속적으로 SMO(Structure modification operation)이 발생하며, 데이터 입력과 읽기 연산(색인 검색)의 일관성의 유지를 위해서 SMO도중에 tree의 일부 혹은 전체에 대한 locking이 발생합니다. 물론 이때, 다른 세션에서 실행중인 입력이 중지될 수도 있습니다.
          </li>
          <li>
            B+Tree색인은 수천만에서 수억건 까지의 입력이 드물고 부분적으로 갱신만 발생하는 환경에서 검색에 최적화된 색인입니다. MongoDB가 주로 사용되는 웹관련 응용에서도 좋은 성능을 냅니다만, 대량의 데이터가 고속으로 발생하는 시계열 센서 데이터의 입력되는 환경에서는 충분한 성능을 낼 수가 없습니다.
          </li>
          <li>
            B+Tree 색인을 이용하여 검색할 시, 색인에는 &lt;키값, 레코드 식별자>의 형태로 저장이 됩니다. 키값 기준으로 레코드 데이터를 기록하는 경우도 있는데, 이를 클러스터드 인덱스라고 합니다. MongoDB는 클러스터드 인덱스는 제공을 하지 않네요. 일단 키값을 탐색하여 레코드 식별자를 얻은 다음에는 데이터 파일에서 원하는 레코드를 레코드 식별자를 통해서 읽게 됩니다. 이 때 디스크에 대한 랜덤 읽기 연산이 발생합니다.
          </li>
          <li>
            아래의 예제에서 시간 기준으로 색인을 만들었다면, 두 시간 범위 사이에는 수많은 센서 데이터가 입력됩니다. 원하는 데이터를 적색 사각형으로 가정하면 두 시간 범위 내의 적색 사각형은 군집되어 있지 않아서, B+Tree색인의 리프노드를 순차 탐색하고, 각 RID를 얻어서 매번 랜덤 읽기를 수행합니다. 센서 종류가 많아지고, 데이터 수집 주기가 짧아질수록, 인덱스 순차검색으로 방문해야 하는 인덱스 레코드의 수가 많아지고, 더 많은 랜덤 읽기 연산이 발생합니다. 이것이 B+Tree 색인을 생성하더라도, 원하는 수준의 데이터 검색 속도를 얻지 못하게 되는 이유입니다.
          </li>
        </ul>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog8-5.webp"
            alt=""
          />
        </div>
        <ul class="tech-ul">
          <li>
            반면 마크베이스의 센서 데이터 인덱스는 시간별로 파티셔닝하여 색인 파일을 생성합니다. 각 색인 파일은 &lt;센서 ID, 시간, 센서 값>의 형태로 데이터를 정렬하여 저장하고 있으며, 인덱스 파티션은 그 파티션의 최소 시간값과 최대 시간값의 정보를 메모리에 유지하고 있습니다. 그래서 검색 대상 시간값을 포함하지 않는 색인 파티션은 검색의 대상에서 제외합니다.
          </li>
          <li>
            인덱스 파티션에 의한 검색 성능의 향상과 함께, 파티션된 인덱스는 데이터가 아주 많이 입력되더라도 동일한 성능을 얻을 수 있습니다. B+Tree와는 다르게 새롭게 입력되는 데이터는 마지막 기록중인 인덱스 파티션에만 반영되며 과거에 생성된 인덱스 파티션이 변경되지 않기 때문입니다. 그 때문에, 마크베이스는 입력, 색인, 검색이 동시에 수행되더라도 병렬적으로 잘 동작하도록 구현되어 있습니다.
          </li>
          <li>
            다시 검색으로 돌아가 보면, 선택된 인덱스 파티션에서 키값을 찾고, 같은 키 값을 갖는 데이터는 시간순으로 정렬되어 모여 있으므로 검색 대상 시간조건을 빨리 필터링할 수 있습니다. 원하는 결과인 시간별 특정 센서 데이터의 값은 모두 같은 인덱스에 기록되어 있기 때문에 짧은 범위의 순차 읽기 만으로 검색을 수행할 수 있습니다.
          </li>
        </ul>
        <p class="tech-contents-text">
         두 색인 아키텍처를 비교해 보면, B+Tree가 가진 시계열 데이터 처리에 적용될 때 발생하는 문제점들을 시계열 센서 데이터 색인은 모두 해결하였음을 알 수 있습니다.
        </p>
        <div class="tech-title" id="anchor4">
          입력 및 단순 질의 성능 비교
        </div>
        <p class="tech-contents-text">
          앞서 설명한 정형 스키마 구조와 센서 데이터에 특화된 인덱스의 영향으로 시계열 센서 데이터는 마크베이스가 더 좋은 성능을 얻을 수 있을 것이라는 점은 쉽게 예측할 수 있습니다.
        </p>
        <p class="tech-contents-text">
          테스트는 다음과 같은 환경에서 실행하였습니다.
        </p>
        <ul class="tech-ul">
          <li>
            사전에 작성한 csv파일(107GB)을 각 제품 전용 도구(csvloader, mongoimport)를 통하여 입력
          </li>
          <li>Tag name 및 timestamp에 대해서 색인을 생성함</li>
          <li>4Core Xeon CPU, 32GB RAM, SSD</li>
        </ul>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog8-6.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          MongoDB는 더 많은 자원을 소모하면서 데이터의 입력이 느린데 비해 마크베이스는 8 배 이상의 속도로 데이터를 입력한 것을 볼 수 있습니다.
        </p>
        <p class="tech-contents-text">
          다음으로 단순 검색 성능은, 스키마 구조, 인덱스 차이점으로 다음의 결과를 얻을 수 있었습니다.
        </p>
        <div class="tech-contents-title">
          단순 검색 질의 성능
        </div>
        <p class="tech-contents-text">
          특정 tag의 1일치 데이터를 모두 fetch하는 질의입니다.
        </p>
        <div class="tech-code-box">
          <span class="red">SELECT</span><span> count(*) </span
          ><span class="red">FROM</span> ( <br />
          <span class="red">&nbsp;&nbsp;&nbsp;&nbsp;SELECT</span> *
          <span class="red">FROM</span> tag<br />
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="red"
            >WHERE</span
          >
          name = <span class="ornage">'EQ0^TAG287' </span>
          <span class="red">AND</span> time
          <span class="red">between</span> to_date (<span class="orange"
            >'2018-01-01 00:00:00'</span
          >)<br />
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="red"
            >AND</span
          >
          to_date (<span class="orange">'2018-01-01 23:59:59'</span>)<br />
        </div>
        <div class="tech-code-box">
          <span>db.sensor.find(</span><span class="green">{name</span>:<span
            class="orange"
            >"EQ0^TAG287"</span
          >,<br />
          <span class="green">time</span>: {
          <span class="blue">$gte</span>:ISODate(<span class="orange"
            >"2018-01-01T00:00:00Z"</span
          >),<br />
          <span class="blue">$lt</span>:ISODate(<span class="orange"
            >"2018-01-02T00:00:00Z"</span
          >)}}).count()
        </div>
        <p class="tech-contents-text">
         위 두 질의의 성능은 다음과 같은 결과를 얻을 수 있었습니다.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog8-7.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          결과적으로 200배 이상의 성능 차이를 나타내는 것을 보면, 마크베이스의 시계열 센서 데이터 인덱스가 효과를 발휘한 것을 알 수 있습니다.
        </p>
        <div class="tech-contents-title">
          센서 데이터의 자동 rollup 생성 vs 실시간 통계
        </div>
        <p class="tech-contents-text"></p>
        <p class="tech-contents-text">
          센서 데이터는 너무나도 많은 데이터를 저장하고 있기 때문에, 장기간의 통계 (예를 들어 10년치 데이터의 전체 경향)을 시각화하기 위해서, 대량의 데이터 읽기와 통계 연산의 수행이 필요합니다.
        </p>
        <p class="tech-contents-text">
          시각화 응용프로그램에서는 데이터를 읽는 시간이 너무 오래 걸리면 대화형으로 데이터를 표출할 수가 없으므로(확대 축소, 시간범위 이동 등) 빠른 통계값의 추출은 필수적입니다. 시각화 대상 데이터를 빠르게 검색하더라도, 데이터가 수억 건이면 이를 시간별로 표시하려면 다시 방대한 연산을 필요로 하게 됩니다.
        </p>
        <p class="tech-contents-text">
          만약, 시간기준으로 사전에 통계를 설정해 둘 수 있다면시간값 기준 통계질의를 매우 빠르게 실행할 수 있습니다. 마크베이스는 시계열 센서 데이터에 대하여 자동 통계생성 기능을 이용하여 이를 저장해 두고, 질의문을 통해서 빠르게 검색할 수 있는 기능을 제공하고 있습니다.
        </p>
        <p class="tech-contents-text">
          마크베이스와 MongoDB를 같은 통계 질의를 통하여 수행한 결과는 다음과 같습니다. 또한 MongoDB는 SQL언어를 지원하지 않아 검색언어가 매우 복잡해 지는 것도 참고하실 만한 사항입니다.
        </p>
        <p class="tech-contents-text">
          다음 질의는 특정 센서의 분당 최대값을 1일 간의 기간에 대해서 검색하는 것입니다. 마크베이스는 아래의 hint를 통해서 사전에 입력한 통계데이터를 검색하도록 합니다.
        </p>
        <div class="tech-code-box">
          <span class="red">SELECT</span
          ><span class="green"> /*+ ROLLUP(TAG, hour, max) */ </span>time,
          <span class="red">value as</span> max<br />
          <span class="red">FROM</span> TAG<br />
          <span class="red">FROM</span> name =
          <span class="ornage">'EQ1^TAG1024'</span>
          <span class="red"> AND</span> time
          <span class="red">BETWEEN</span> to_date(<span class="orange"
            >'2018-01-01 00:00:00'</span
          >)<br />
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="red"
            >AND</span
          >
          to_date (<span class="orange">'2018-01-01 23:59:59'</span>) )<br />
          <span class="red">ORDER BY</span> time<br />
        </div>
        <p class="tech-contents-text">
          MongoDB는 다음의 json을 질의 언어로 전달하여 실행합니다.
        </p>
        <div class="tech-code-box">
          <span>db.sensor.aggregate(</span><br />[<br />
          { <span class="green">$match </span>: {<span class="green">name</span
          >:<span class="orange">"EQ1^TAG1024"</span>,<span class="green"
            >time</span
          >: { <span class="green">$gte</span>:ISODate(<span class="ornage"
            >"2018-01-01T00:00:00Z"</span
          >),<br />
          <span class="green">$lt</span>:ISODate(<span class="orange"
            >"2018-01-02T00:00:00Z"</span
          >)}}},<br />
          { <span class="green">$project</span> : {<br />
          &nbsp;&nbsp;&nbsp;&nbsp;_id : <span class="blue">0</span>,<br />
          &nbsp;&nbsp;<span class="red">"time"</span>:
          <span class="blue">1</span>,<br />
          <span class="red">"value"</span>: <span class="blue">1</span>,<br />
          }<br />
          },<br />
          { <span class="green">$group</span> : {<br />
          <span class="red">"_id"</span>: { <br />
          <span class="red">"year"</span>: { <span class="green">$year</span> :
          <span>"$time"</span>},<br />
          <span class="red">"month"</span>: {
          <span class="green">$month</span> : <span>"$time"</span>},<br />
          <span class="red">"day"</span>: {
          <span class="green">$dayOfMonth</span> : <span>"$time"</span>},<br />
          <span class="red">"hour"</span>: { <span class="green">$hour</span> :
          <span>"$time"</span>},<br />
          },<br />
          <span class="red">"maxValue"</span>: {
          <span class="green">$max</span> : <span>"$value"</span>},<br />
          <span class="red">"count"</span>: { <span class="green">$sum</span> :
          <span class="blue">1</span>}<br />
          }<br />
          },<br />
          { <span class="green">$sort</span>: { <br />
          <span class="red">"_id.year"</span>:
          <span class="blue">1</span>,<br />
          <span class="red">"_id.month"</span>:
          <span class="blue">1</span>,<br />
          <span class="red">"_id.day"</span>: <span class="blue">1</span>,<br />
          <span class="red">"_id.hour"</span>:
          <span class="blue">1</span>,<br />
          }<br />
          }<br />
          ])
        </div>
         <p class="tech-contents-text">
          성능 결과는 다음과 같습니다.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog8-8.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          거의 400배의 성능 차이가 나는 것을 확인할 수 있습니다.
        </p>
        <div class="tech-title" id="anchor5">결론</div>
        <p class="tech-contents-text">
         아키텍처에 대한 관점에서 마크베이스와 MongoDB가 어떻게 다른지를 살펴보고, 그 차이점이 시계열 센서 데이터 처리에 있어서 어떤 성능 결과를 내는 것인지 확인해 보았습니다. MongoDB는 Web application과 같은 환경에서는 매우 편리하고, 쓸만한 성능을 얻을 수 있었지만, 시계열 센서 데이터 응용 부문에는 맞지 않는 인덱스를 제공하는 아키텍쳐를 갖고 있다는 사실도 알 수 있었습니다.
        </p>
        <p class="tech-contents-text">
          최근들어 화두가 되고 있는 스마트팩토리 및 스마트시티와 같은 곳에서는 대량의 센서 데이터가 나올 뿐만 아니라, 이의 처리에 대한 수 많은 고민들과 시도가 있습니다. 마크베이스가 그 고민의 중심에서 좋은 해결책이 될 수 있으면 어떨까 하는 바램으로 이 글을 작성해 보았습니다.
        </p>
        <p class="tech-contents-text">
          기회가 된다면 시계열 센서 데이터에 대한 더 다양한 데이터베이스와의 비교를 약속드리면서 이만 줄이겠습니다.
        </p>
        <p class="tech-contents-text">감사합니다.</p>
        <p class="tech-contents-text">마크베이스 CTO 심광훈</p>
      </div>
    </div>

  </div>
</section>
{{< home_footer_blog_kr >}} {{< home_lang_kr >}}
