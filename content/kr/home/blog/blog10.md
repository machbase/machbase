---
title: Blog
description: "IoT 센서 데이터 플랫폼 구축과 MQTT"
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
    <h4 class="blog-title">IoT 센서 데이터 플랫폼 구축과 MQTT</h4>
    <div class="blog-date">
      <div>
        <span>by Eirny Kwon / 2 Nov 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">개요</li></a
      >
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">MQTT 프로토콜의 특징</li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">MQTT 패킷 구조</li>
      </a>
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">MQTT와 IoT 애플리케이션</li>
      </a>
      <a href="#anchor5">
        <li class="tech-list-li" id="tech-list-li">
          마크베이스와 machbase-neo
        </li>
      </a>
      <a href="#anchor6">
        <li class="tech-list-li" id="tech-list-li">결론</li>
      </a>
    </ul>
    <div class="tech-contents">
      <div>
        <p class="tech-contents-text">
          MQTT 프로토콜은 OASIS 개방형 표준 (ISO/IEC 20922)이다.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/blog10-1.jpg" alt="" />
        </div>
        <p class="tech-contents-link-text">
          Photo by
          <a
            class="tech-contents-link"
            href="https://unsplash.com/ko/@markusspiske?utm_medium=referral&utm_source=medium"
            >Markus Spiske</a
          >
          on
          <a
            class="tech-contents-link"
            href="https://unsplash.com/ko?utm_source=medium&utm_medium=referral"
            >Unsplash</a
          >
        </p>
        <p class="tech-title" id="anchor1">개요</p>
        <p class="tech-contents-text">
          1999년에 앤디 스탠포드-크라크(IBM)과 앨런 니퍼 (그 당시 유로테크사에서
          근무)가 초기 버전의 프로토콜을 작성해서 SCADA(Supervisory Control and
          Data Acquisition) 제어 시스템으로 송유관을 모니터링하는데 사용하였다.
          그 시절의 시스템들은 다양한 이기종들로 이루어졌고 각자의 고유
          프로토콜만을 지원했기 때문에 상호 연동이 불가능했을 뿐만 아니라 그
          당시로는 엄청나게 비싼 비용의 위성 링크를 통해 연동해야 했기 때문에
          대역폭-효율적으로 경량화하면서 배터리 소모를 최소화하는 것이 설계의
          목표였다.
        </p>
        <p class="tech-contents-text">
          “MQTT”에서 “MQ”는 역사적으로 IBM MQ (메시지 큐 Message Queue를
          의미하는 MQ (당시에는 MQSeries라는 이름이었다) 제품라인에서 유래된
          것이다. “큐”라는 이름에도 불구하고 프로토콜은 PUBLISH-SUBSCRIBE 메시지
          전송에 관한 정의만 있고 정작 큐(Queue)에 대한 규정은 없다. IBM에 의해
          공개된 3.1 버전의 규격서에서는 MQTT가 “MQ Telemetry Transport”의
          줄임말이라고 표현되어 있는데 그 이후 OASIS에 의해 발표된 버전에서는 이
          프로토콜을 단순히 “MQTT”라고만 기술하고 있다.
        </p>
        <p class="tech-contents-text">
          OASIS의 기술 위원회의 이름이 “OASIS Message Queuing Telemetry
          Transport Technical Committee”임에도 불구하고 2013년 기술 위원회
          회의에서 “MQTT”가 무언가를 뜻하는 것이 아니어야 한다고 정의하였다.
          ▶[OASIS_MQTT_TC_minutes_25042013.pdf (oasis-open.org)]<a
            class="tech-link"
            href="https://www.oasis-open.org/committees/download.php/49028/OASIS_MQTT_TC_minutes_25042013.pdf"
            >(https://www.oasis-open.org/committees/download.php/49028/OASIS_MQTT_TC_minutes_25042013.pdf)</a
          >
        </p>
        <p class="tech-contents-text">
          2013년에 IBM은 약간의 변경사항들을 담은 MQTT v3.1을 OASIS에
          제출하였고, IBM으로부터 표준에 대한 관리 권한을 이양 받은 이후 OASIS가
          2014년 10월 29일 3.1.1 버전을 공개하였다. 새로운 기능들이 추가된
          실질적인 업그레이드로 볼 수 있는 MQTT 버전 5는 2019년 3월 7일에
          발표되었다. 참고로 MQTT-SN (MQTT for Sensor Networks) 규격은 비-TCP/IP
          네트워크(예: Zigbee)에서 배터리로 동작하는 임베드 디바이스를 대상으로
          하는 MQTT의 변형 프로토콜이다.
        </p>
        <div class="tech-title" id="anchor2">MQTT 프로토콜의 특징</div>
        <p class="tech-contents-text">
          1. 연결지향적 (Connection Oriented) <br />
          MQTT 서버와 연결을 요청하는 클라이언트는 TCP/IP 소켓을 연결한 후
          명시적으로 연결을 끊거나 네트워크 상의 문제로 연결이 끊어질 때까지
          상태를 유지하며 메시지를 전송하도록 설계되어 있다.
        </p>
        <p class="tech-contents-text">
          2. 발행-구독 (Publish- Subscribe)<br />
          토픽을 기반한 메시지의 발행-구독 모델로 클라이언트들 간의 직접적인
          메시지 송수신은 발생하지 않으며 모든 메시지들은 서버(혹은 브로커)를
          통한 연계만 가능하다.
        </p>
        <p class="tech-contents-text">
          3. Quality of Service (QoS)<br />
          메시지를 대상 토픽으로 송신할 때 QoS를 0, 1, 2 중에 설정할 수 있다.<br />
          - 0: 최대 1회 전송, 메시지 전송에 대한 보장을 하지 않는다.<br />
          - 1: 최소 1회 전송, 메시지 전송에 대한 보장을 하지만 동일 메시지가
          중복하여 전송될 가능성이 있다.<br />
          - 2: 메시지가 중복 없이 정확히 1회만 전송되도록 보장한다.
        </p>
        <p class="tech-contents-text">
          4. 메시지의 종류<br />
          MQTT 규격에는 아래와 같은 메시지들이 정의되어 있다.<br />
          - CONNECT, CONNACK<br />
          - DISCONNECT<br />
          - PUBLISH, PUBACK, PUBREC, PUBREL, PUBCOMP<br />
          - SUBSCRIBE, SUBACK<br />
          - UNSUBSCRIBE, UNSUBACK<br />
          - PINGREQ, PINGRESP<br />
        </p>
        <p class="tech-contents-text">
          MQTT의 메시지는 오버헤드가 거의 없고 (토픽 경로를 제외하면 2바이트
          고정 헤더와 가변 길이 헤더) QoS를 지원하며 다양한 응용이 가능한
          유연성을 제공하므로 엔터프라이즈 애플리케이션에서부터, 게임,
          엔터테인먼트에 이르기까지 다양한 분야에서 활용되어 있다. 특히 IoT
          분야에서는 텔레메트릭 전송에 있어 표준으로 자리 잡고 있다.
        </p>
        <div class="tech-title" id="anchor3">MQTT 패킷 구조</div>
        <p class="tech-contents-text">
          패킷은 아래 그림처럼 항상 존재해야 하는 2바이트의 고정 헤더, 크기
          변동이 가능한 헤더로 이뤄지며 이어서 페이로드가 존재한다.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-2.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          최초 4비트는 패킷의 유형을 나타내며 다음과 같이 정의되어 있다.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-3.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          이어서 하위 4비트는 제어 명령에 추가적인 플래그를 표시한다. PUBLISH
          메시지 외의 다른 메시지에서는 정의된 값만 사용해야 한다.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-4.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          MQTT를 사용하는 애플리케이션의 기본적인 메시지 시퀀스는 아래 그림과
          같다. 클라이언트인 발행자(Publisher)와 구독자(Subscriber)는 서버인
          브로커로 CONNECT 메시지를 전송하고 브로커는 답변으로 CONNACT를
          반환한다. 구독자는 관심 대상이 되는 토픽에 구독(SUBSCRIBE) 요청을 하고
          응답은 SUBACK를 반환한다. PUBLISH는 발행자가 대상 토픽으로 전송하거나
          브로커가 구독자에게 전송하는 메시지이며 QoS 1 인 경우 수신자는
          PUBACK로 수신 확인한다.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-5.jpg"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          CONNECT 메시지에는 다음과 같은 필드가 포함될 수 있다.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-6.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          클라이언트의 CONNECT 요청에 대해 서버는 CONNACK로 응답하면 응답 코드의
          의미는 다음과 같다.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-7.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          서버-클라이언트 간 메시지 송수신은 PUBLISH 메시지를 통해 이루어지며
          다음과 같은 필드를 설정할 수 있다.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-8.webp"
            alt=""
          />
        </div>
        <div class="tech-title" id="anchor4">MQTT와 IoT 애플리케이션</div>
        <p class="tech-contents-text">
          MQTT가 IoT 분야에 적용된 사례를 단순화해서 보면 대부분 아래의 그림과
          같은 형태이다.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-9.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          센서에서 수집된 텔레메트릭 데이터를 사전에 약속된 MQTT 브로커의
          토픽으로 JSON이나 CSV 등의 형식으로 전송하면 해당 토픽을
          구독(SUBSCRIBE) 중인 서버 측 애플리케이션이 메시지를 브로커로부터
          전달받아 데이터베이스에 저장하고 응용 애플리케이션은 필요할 때
          데이터베이스를 액세스하여 데이터를 조회하거나 처리한다.​
        </p>
        <p class="tech-contents-text">
          이런 아키텍처가 가장 보편적이고 익숙한 형태일 것이고 당연하게 느껴질
          수도 있다. 하지만 크고 작은 다양한 IoT 프로젝트를 거치면서 이런 구조가
          가져오는 문제점을 경험하게 되었고 그런 문제점들은 대부분 아래와 같은
          원인으로 귀결되었다.​
        </p>
        <p class="tech-contents-title">문제 1) MQTT 브로커의 가용성</p>
        <p class="tech-contents-text">
          시중에는 오픈소스를 포함해서 다양하고 품질 좋은 MQTT 브로커들이
          존재한다. 이런 브로커들은 그 자체로는 완성도도 높아 문제가 없다.
          이러한 브로커들을 도입하여 여러 가지 형태의 IoT 프로젝트를 경험한 결과
          MQTT 브로커의 가용성이 전체 IoT 서비스의 가용성에 직결된다는 사실을
          알게 된다. 모든 데이터는 브로커를 통해 소통되므로 전체 서비스의
          가용성은 절대 사용하는 MQTT 브로커의 가용성을 넘어설 수 없다. 즉
          선택한 브로커에 대한 개발 및 운영 노-하우가 전체 서비스의 품질을
          결정하는 가장 중요한 요소로 부상하였다. 손쉽게 접근할 수 있는 오픈소스
          브로커에 대해 충분한 기술력을 축적하는 것은 여러분들이 개발하려고 하는
          애플리케이션을 안정적으로 만드는 것만큼 혹은 그보다 더 많은 노력이
          들어가는 일이 되어 버렸고 부차적인 요소로 생각했던 컴포넌트가 핵심
          요소가 되어 버린 것이다.​
        </p>
        <p class="tech-contents-title">문제 2) ‘중복’ 스토리지 관리</p>
        <p class="tech-contents-text">
          MQTT 브로커의 목적은 센서(퍼블리셔 publisher)가 전송한 메시지를 해당
          토픽의 구독자(subscriber)인 수집 애플리케이션으로 유실 없이 정확히
          전달하는 데 있다. 여기서 “유실 없이 전달”한다는 뜻은 브로커 자체적으로
          수신한 메시지들을 어떤 형태로든 스토리지에 일단 저장해야 한다는
          뜻이다. 저장 후 전달 (store and forward) 전략이 MQTT뿐만 아니라 모든
          메시지 브로커들의 일반적인 설계 전략이라고 할 수 있다. 브로커가 전달한
          메시지를 수신한 수집 애플리케이션은 서비스에 이용하기 편리한 구조로
          변환하여 (RDBMS나 NoSQL과 같은 데이터베이스에) 저장한다. 시스템을
          구축한 후에는 서비스를 안정적으로 운영하기 위해서 두 가지의 스토리지
          (MQTT의 저장소, 애플리케이션의 저장소)를 관리해야만 하며 장애에
          대처해야 한다. 그리고 새로운 종류의 센서가 추가되거나 데이터 형태가
          추가될 때 수집 애플리케이션을 추가 개발하거나 수정해야만 한다.​
        </p>
        <p class="tech-contents-text">
          결과적으로 모든 IoT 서비스 개발자나 시스템 설계자들은 MQTT 브로커의
          운영과 “중복되는” 저장소 관리의 어려움을 항상 짊어지고 가야만
          하는가?라는 의문에서 출발하여 대량의 IoT 데이터를 효율적으로 처리할 수
          있는 방법은 없을까라는 고민에 도달하게 된다.
        </p>
        <div class="tech-title" id="anchor5">마크베이스와 machbase-neo</div>
        <p class="tech-contents-text">
          센서가 텔레 메트릭 데이터를 MQTT를 통해 직접 데이터베이스로 전송하면
          어떨까? 아래의 그림과 같은 형태가 될 것이다.
        </p>
        <p class="tech-contents-text">기존형태의 아키텍처:</p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-10.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          Machbase에서 생각하는 MQTT 인터페이스의 활용:
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-11.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          이런 형태의 데이터베이스가 존재한다면 MQTT 브로커 운영 관리와 메시지
          유실 방지를 위한 중복된 스토리지 운영 관리의 문제를 해결할 수 있다.
          추가로 수집 애플리케이션의 필요성도 없어질 수 있다. 센서는 기존과
          동일하게 MQTT로 텔레메트릭 데이터를 전송하고 응용 애플리케이션은
          데이터베이스가 제공하는 HTTP Restful API나 프로그래밍 언어의 표준
          데이터베이스 인터페이스(JDBC, ODBC, Go Driver …)를 통해 필요한
          데이터를 조회할 수 있다.​
        </p>
        <p class="tech-contents-text">
          이런 접근법으로 실현한 결과물이 machbase-neo이다.(<a
            class="tech-link"
            href="https://machbase.com/neo"
            >https://machbase.com/neo</a
          >)
        </p>
        <p class="tech-contents-text">
          마크베이스는 tpc.org가 인증한 세계 1위 성능의 국산 데이터베이스이며
          (TPCx-IoT V2 참고
          <a
            class="tech-link"
            href="https://www.tpc.org/tpcx-iot/results/tpcxiot_perf_results5.asp?version=2"
            >https://www.tpc.org/tpcx-iot/results/tpcxiot_perf_results5.asp?version=2</a
          >), machbase-neo는 마크베이스를 내장하고 MQTT 서버와 같은 IoT 지향적인
          편의 기능들을 합쳐 놓은 것이다. 모든 기능을 하나의 실행파일로 배포하기
          때문에 파일의 복사만으로 설치가 가능하며 IoT 개발자의 개발
          워크플로우에 적합하도록 UX가 구현되어 있다.​
        </p>
        <p class="tech-contents-text">
          간략하게 센서의 데이터를 저장하기 위한 machbase-neo의 MQTT
          인터페이스를 간략히 살펴보도록 하겠다. 더 자세한 내용은 공식 사이트의
          문서(<a class="tech-link" href="https://machbase.com/neo"
            >(https://machbase.com/neo)</a
          >) 와 튜토리얼을 참고하면 된다. 여기서는 데모를 위해 mosquito_pub
          명령어로 MQTT를 시험할 것이므로 먼저 mosquito-client 도구가 설치되어
          있어야 한다. 그리고 machbase-neo는 사이트에서 내려받거나 아래와 같은
          명령어로 다운로드가 가능하다. (참고: 윈도우즈 사용자는 사이트의 릴리즈
          페이지에서 직접 다운로드해야 한다.)
        </p>
        <div class="tech-code-box">
          <span
            >$ sh -c "$(curl -fsSL https://neo.machbase.com/install.sh)"</span
          >
        </div>
        <p class="tech-contents-text">
          내려받은 압축파일을 풀고 “machbase-neo” 실행 파일을 원하는 위치로
          복사하면 설치가 완료된다. 실행을 위해 machbase-neo serve 을 실행하면
          아래와 같이 데이터베이스를 생성하며 실행된다. 화면에 표시되는 것처럼
          MQTT 서버는 5653 포트, HTTP 서버는 5654 포트에 열린다.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-12.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          그리고 아래 명령어로 데모를 위해 필요한 테이블을 생성한다.
        </p>
        <div class="tech-code-box">
          <span
            >$ curl -o - http://127.0.0.1:5654/db/query \<br />
            &nbsp;&nbsp;&nbsp;&nbsp;--data-urlencode \<br />
            &nbsp;&nbsp;&nbsp;&nbsp;"q=create tag table EXAMPLE (name
            varchar(40) primary key, time datetime basetime, value
            double)"</span
          >
        </div>
        <p class="tech-contents-text">
          이제 아래와 같이 mosquito_pub로 센서가 데이터를 MQTT로 전송하는 것을
          흉내 낼 수 있다. 토픽 경로를 보면 테이블 명인 EXAMPLE이 사용된 것을 알
          수 있다.
        </p>
        <div class="tech-code-box">
          <span
            >$ mosquitto_pub -h 127.0.0.1 -p 5653 \<br />
            &nbsp;&nbsp;&nbsp;&nbsp;-t db/append/EXAMPLE \<br />
            &nbsp;&nbsp;&nbsp;&nbsp;-m '[ "my-car", 1670380342000000000, 32.1
            ]'</span
          >
        </div>
        <p class="tech-contents-text">
          응용 애플리케이션은 HTTP로 입력된 데이터를 조회할 수 있다.
        </p>
        <div class="tech-code-box">
          <span
            >$ curl -o - http://127.0.0.1:5654/db/query \<br />
            &nbsp;&nbsp;&nbsp;&nbsp;--data-urlencode "q=select * from EXAMPLE"
          </span>
        </div>
        <div class="tech-title" id="anchor6">Conclusion</div>
        <p class="tech-contents-text">
          여기서 소개한 machbase-neo는 시계열 데이터베이스(timeseries database)
          개발로 축적된 기술이 IoT 분야의 개발자들의 고민 해결에 어떻게 기여할
          수 있는지를 보여주는 좋은 사례라고 생각한다.
          <br />많은 개발자들에게 조금이나마 도움이 되기를 바라며 문의 사항이나
          커뮤니티의 도움과 기여를 원한다면 Github<a
            class="tech-link"
            href="https://github.com/machbase/neo-server"
            >(https://github.com/machbase/neo-server)</a
          >
          를 방문해 주기를 바라며 IoT, MQTT 그리고 machbase-neo에 대한 글을
          마친다.
        </p>
        <p class="tech-contents-text">by Eirny Kwon</p>
      </div>
    </div>
  </div>
</section>
{{< home_footer_blog_en >}} {{< home_lang_en >}}
