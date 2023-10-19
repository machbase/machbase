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
        <li class="menu-a">
          <select id="languageSelector" onchange="changeLanguage()">
            <option value="kr">한국어</option>
            <option value="en">English</option>
          </select>
        </li>
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
          <div class="docs-num"><a href="/dbms" target="_blank">Classic</a></div>
        </div>
      </li>
      <li><a href="/kr/home/download">Download</a></li>
      <li><a href="https://support.machbase.com/hc/en-us">Support</a></li>
         <li><a href="/kr/home/download">Contact US</a></li>
      <li>
    <select id="languageSelector2" onchange="changeLanguage2()">
      <option value="kr">한국어</option>
      <option value="en">English</option>
    </select>
      </li>
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
      Deep Anomaly Detection in Time Series (1) : Time Series Data
    </h4>
    <div class="blog-date">
      <div>
        <span>by Machbase / 12 Jul 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">개요</li></a
      >
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">시계열 데이터</li></a
      >
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">
          Anomaly in Time Series
        </li></a
      >
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">Conclusion</li>
      </a>
    </ul>
    <div class="tech-contents">
      <div>
        <p class="tech-title" id="anchor1">개요</p>
        <p class="tech-contents-text">
          최근 4차 산업 혁명 기술은 제조 관리 시스템, 스마트공장, 예지보전 분야
          등에서 활발한 연구와 응용을 시도하고 있습니다. 그중에서도 ‘이상
          탐지(Anomaly Detection)’는 AI, IoT 기술을 구현하는 핵심 분야로써
          데이터 분석과 응용을 원리로 합니다.
        </p>
        <p class="tech-contents-text">
          마크베이스는 시계열 데이터베이스 전문 DBMS로써 이 분야에 있어 세계
          1위의 속도와 퍼포먼스를 자랑하는 오랜 성과로 인해 이상 탐지 분야에
          있어 핵심·원천 기술을 보유하고 있습니다.
        </p>
        <p class="tech-contents-text">
          이번 포스트에서는 Deep Anomaly Detection에 대한 개요, 시계열데이터의
          특징, 이상의 종류 등을 설명해 드리겠습니다.
        </p>
        <p class="tech-title" id="anchor2">시계열 데이터</p>
        <p class="tech-contents-text">
          먼저 데이터 자체에 대해 들여다볼 필요가 있습니다. Time Series, 혹은
          시계열이라 불리는 데이터는 일정 시간 간격으로 배치된 데이터들의
          수열이라고 합니다. 이 시계열 데이터는 무슨 특징이 있을까요? 두가지
          관점에서 살펴보겠습니다.
        </p>
        <div class="tech-contents-title">Time Series Decomposition</div>
        <p class="tech-contents-text">
          우선 Time Series 데이터가 어떻게 구성되는지 보겠습니다. Time Series
          데이터는 Seasonality(계절성), Trend(추세), Remainder(잔차) 로 분해할
          수 있습니다. Seasonality는 Time Series 데이터 전체에 걸쳐 짧은 주기로
          반복되는 패턴을 의미하고 Trend는 시계열에서 전반적으로 나타나는 증가
          혹은 감소세라고 할 수 있습니다. 그리고 이 두가지로 설명되지 못하는
          불규칙 요인을 Remainder라고 부릅니다.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/anomaly-1.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          시계열 데이터의 구성: data는 seasonality, trend, 그리고 remainder로
          이루어져 있다(1).
        </p>
        <p class="tech-contents-text">
          기온이나 가솔린 엔진을 예를 들면 다음과 같습니다(경우에 따라서 기온
          데이터에서 계절의 변화를 Seasonality에 포함시킬 수도 있겠네요)
        </p>
        <div class="tech-contents-text">
          <b>&lt;1시간 간격의 서울의 기온></b>
        </div>
        <ul class="tech-ul">
          <li>Seasonality : 낮과 밤에 따른 기온 변화</li>
          <li>Trend : 날씨, 계절의 변화에 따른 기온 변화</li>
          <li>Remainder : Seasonality나 Trend로 표현되지 않는 노이즈</li>
        </ul>
        <div class="tech-contents-text">
          <b>&lt;가솔린 엔진에 부착된 진동 센서></b>
        </div>
        <ul class="tech-ul">
          <li>Seasonality :흡기, 압축, 폭발, 배기에 따른 주기적인 진동 변화</li>
          <li>
            Trend : 자동차의 속도 변화, 자동차의 노후 등에 따른 센서 값의 변화
          </li>
          <li>Remainder : Seasonality나 Trend로 표현되지 않는 노이즈</li>
        </ul>
        <p class="tech-contents-text">
          이렇게 Time Series 데이터의 종류를 파악하고 Trend, Seasonality,
          Remainder로 나누는 작업을 Time Series Decomposition(시계열 분해)라고
          합니다. Time Series Decomposition 시에는 데이터의 모양에 따라 두 가지
          방법으로 진행되는데, 바로 Additive Model과 Multiplicative Model입니다.
        </p>
        <p class="tech-contents-text">
          Additive Model 시계열은 Seasonality와 Trend, Remainder의 합으로
          이루어지며 Multiplicative Model 시계열은 셋의 곱으로 이루어집니다.
        </p>
        <p class="tech-contents-text">
          Additive Model의 시계열은 Trend가 변한다 하더라도 데이터의 진동수와
          진폭이 비교적 일정하지만 Multiplicative Model의 경우 데이터의 Trend가
          변함에 따라 진동수와 진폭이 같이 변하는 것이 특징입니다.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/anomaly-2.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          Additive Model & Multiplicative Model(2)
        </p>
        <p class="tech-contents-text">
          Time Series 데이터를 예측할 때 Decomposition을 통해 문제를 보다
          단순화시킬 수 있습니다. 그렇다면 DAD의 관점에서는 어떨까요? 진동센서가
          부착된 베어링이 노후화되면서 진동센서의 Remainder 분산이 커진다거나,
          지구온난화로 인해 월 평균 기온의 Trend가 비정상적으로 증가하는 경우를
          생각해볼 수 있지 않을까요? 혹은 항상 동일하던 Seasonality가 어느 순간
          어긋나는 경우를 비정상이라 할 수 있습니다. 즉, 이상 감지 문제에서도
          Time Series의 구성요소를 파악하는 것은 중요하다고 할 수 있겠습니다.
        </p>
        <div class="tech-contents-title">Univariate vs. Multivariate</div>
        <p class="tech-contents-text">
          이번에는 종속변수의 갯수에 따라 Time Series 데이터를 구분해보겠습니다.
          날씨를 예측한다고 해봅시다. 아까는 서울의 기온으로 예를 들었으니
          이번에는 부산의 날씨로 예를 들어보겠습니다. 부산의 기온을 예측하는데
          먼저 단순하게 생각한다면 시간과 과거의 기온을 사용해볼 수가 있겠죠?
          풍속을 예측한다 하더라도 시간과 과거의 풍속만을 고려할 수도 있고요.
          이렇게 ‘시간-기온’, ‘시간-풍속’처럼 시간에 종속되는 변수가 하나뿐인
          경우를 Univariate Time Series(단변량 시계열)이라고 합니다.
        </p>
        <p class="tech-contents-text">
          하지만 날씨라는 것이 기온, 풍속, 강수량 각각 별개로 예측할 수는
          없습니다. 날씨가 맑으면 기온은 높아지고 한파라도 닥치면 바람이 거세져
          기온은 내려가겠지요. 날씨, 강수량, 습도, 바람 등이 복합적으로
          고려되어야 비로소 날씨를 예측할 수 있습니다. 이렇게 각각의 종속변수가
          시간 뿐만 아니라 다른 종속변수에도 영향을 받아 복잡한 시계열을 이루는
          경우를 Multivariate Time Series(다변량 시계열)이라고 합니다.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/anomaly-3.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          다변량 시계열의 예시 : 4월 27일부터 4월 29일까지의 부산의
          일기예보(기상청)
        </p>
        <p class="tech-contents-text">
          당연하게도 Multivariate Time Series가 Univarite Time Series보다
          분석하기가 어렵습니다. 기존에는 Univariate Time Series의 경우
          ARIMA(Auto-Regressive Integrated Moving Average) 모델 등을
          사용하였으며, Multivariate의 경우 VAR(Vector Auto-Regressive) 모델
          등을 사용하였지만 Multivariate Time Series 특유의 복잡성으로 인해 큰
          효과가 없었습니다.
        </p>
        <p class="tech-contents-text">
          오늘날에 와서는 딥러닝에 관한 많은 연구가 이루어지면서 복잡한 문제의
          패턴 인식이 가능해졌기 때문에 Multivariate Time Series의 분석을
          딥러닝으로 해결하고자 하는 움직임이 있습니다.
        </p>
        <div class="tech-title" id="anchor3">Anomaly in Time Series</div>
        <p class="tech-contents-text">
          그렇다면 Time Series에는 어떠한 Anomaly가 있을까요? 논문 별로 Time
          Series Anomaly를 구분하는 방법이 다르지만 이 글에서는 보다 많은 논문이
          구분하는 데로 3가지 종류를 소개하겠습니다.
        </p>
        <p class="tech-contents-title">Point Anomaly</p>
        <p class="tech-contents-text">
          정상 데이터의 분포로부터 완전히 벗어난 데이터를 Point Anomaly, 혹은
          Global Outlier라고 합니다. 가장 일반적으로 생각되는 Anomaly이며 동시에
          가장 많은 연구가 진행된 Anomaly입니다. 예를 들면, 다음의 그림에서 빨간
          점에 해당하는 데이터가 나머지 데이터의 분포로부터 크게 벗어난 것을
          확인할 수 있습니다. 이 두 개의 빨간 데이터를 Point Anomaly라고 할 수
          있습니다.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/anomaly-4.png" alt="" />
        </div>
        <p class="tech-contents-link-text">Point Anomaly의 예시(3)</p>
        <p class="tech-contents-title">Contextual Anomaly</p>
        <p class="tech-contents-text">Conditional Anomaly라고도 불립니다.</p>
        <p class="tech-contents-text">
          데이터의 분포 자체에는 이상한 점이 없지만 데이터의 흐름 또는 맥락 상
          정상이 아닌 데이터를 의미합니다. 시간을 고려했을 때 특정 시점에서는
          특정 데이터가 나와야 하는데 다른 데이터가 나온 경우라고 할 수
          있습니다. 예를 들면 다음의 그래프처럼요.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../img/anomaly-5.png" alt="" />
        </div>
        <p class="tech-contents-link-text">Contextual Anomaly의 예시(4)</p>
        <p class="tech-contents-title">Group Anomaly</p>
        <p class="tech-contents-text">
          Group Anomaly, 혹은 Collective Anomaly라고 불리는 이것은 단일 데이터만
          봤을 때는 언뜻 정상 데이터처럼 보입니다.
        </p>
        <p class="tech-contents-text">
          하지만 데이터를 모아놓고 봤을 때 비정상으로 판단되는 Anomaly의
          종류입니다. 다음의 그림을 보시죠. 7월 14일부터 3일에 걸쳐 지속적으로
          75달러의 결제가 이루어지고 있습니다. 한번의 결제라면 정상으로 취급할
          수 있겠지만 며칠에 걸쳐 계속 같은 결제가 반복적으로 이루어진다면
          분명히 수상할 것입니다. 혹은 다른 예시로, 그래프가 미미하지만
          지속적으로 우상향하고 있는 진동센서를 생각할 수 있습니다. 단일의
          데이터나 단기적 데이터만을 봤을 때는 정상처럼 보이겠지만 장기적으로
          봤을 때 끈임없이 우상향하고 있다면 이것은 한번은 기기를 점검해보아야
          하지 않을까요?
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/anomaly-6.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          Group Anomaly : 신용카드 사용에서의 이상감지(4)
        </p>
        <p class="tech-contents-text">
          이렇게 Anomaly의 3가지 종류를 알아봤습니다. 아직까지는 Point Anomaly나
          Contextual Anomaly보다는 Group Anomaly를 감지하는 데에 보다 많은
          어려움이 있지만 최근에는 VAE(Variational AutoEncoders),
          AAE(Adversarial AutoEncoders), GAN(Generative Adversarial Networks)
          등의 딥러닝 방법으로 이를 해결하려는 연구가 많이 이루어지고 있습니다.
          스마트 팩토리를 위해 Anomaly Detection을 적용시키고자 한다면 이 세
          가지 Anomaly에 대해 모두 고려하여 모델을 구성하여야 할 것입니다.
        </p>
        <p class="tech-title" id="anchor4">결론</p>
        <p class="tech-contents-text">
          이상 징후 탐지를 위한 기술들은 현재도 지속해서 개발되고 있으며 점점 더
          빠르고, 정확한 모델이 출시되고 있습니다. 또한 실제로 적용할 때 어떤
          모델을 어떤 데이터 수집 환경에서 써야 할 것인지 의사 결정이 매우
          중요합니다. 또 이상 탐지 기능은 공장 자동화 스마트 팩토리를 위한 기초
          단계로 인공지능과 사물인터넷을 활용하여 다양한 산업 분야에서
          응용·활용되고 있습니다.
        </p>
        <p class="tech-contents-text">
          더불어 기존의 관계형 DBMS에서 발생하는 데이터 수집 및 처리·분석의
          한계점을 보완하여 여기에 특화된 시계열 데이터베이스를 선택하는 것이
          아주 중요하다고 볼 수 있습니다. 지금까지 이상 탐지에 대한 다양한
          내용을 다뤄 보았으며 다음에 더 좋은 컨텐츠로 찾아뵙겠습니다.
        </p>
        <p class="tech-contents-text">감사합니다.</p>
        <ul class="tech-ul">
          <p class="tech-title">Reference</p>
          <li>
            Verbesselt, Jan, et al. “Detecting trend and seasonal changes in
            satellite image time series.” Remote sensing of Environment 114.1
            (2010): 106-115.
          </li>
          <li>
            <a
              class="tech-contents-link"
              href="https://kourentzes.com/forecasting/2014/11/09/additive-and-multiplicative-seasonality/"
              >https://kourentzes.com/forecasting/2014/11/09/additive-and-multiplicative-seasonality/</a
            >
          </li>
          <li>
            Talagala, Priyanga Dilini, et al. “Anomaly detection in streaming
            nonstationary temporal data.” Journal of Computational and Graphical
            Statistics 29.1 (2020): 13-27./li>
          </li>
          <li>
            Chalapathy, Raghavendra, and Sanjay Chawla. “Deep learning for
            anomaly detection: A survey.” arXiv preprint arXiv:1901.03407
            (2019).
          </li>
        </ul>
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
        서울시 강남구 테헤란로 20길 10, 3M 타워, 9층
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
  </div>
  <div class="footer_tablet_inner">
    <div class="footer-logo">
      <img class="footer-logo-img" src="../../img/machbase-logo-w.png" />
    </div>
    <div>
      <p class="footertext">
        서울시 강남구 테헤란로 20길 10, 3M 타워, 9층
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
