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
      Deep Anomaly Detection in Time Series (2): Anomaly Detection Model
    </h4>
    <div class="blog-date">
      <div>
        <span>by Machbase / 19 Jul 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">개요</li>
      </a>
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">이상 감지는 왜 어려울까?</li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">
          다양한 종류의 이상 감지 방법
        </li>
      </a>
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">결론</li>
      </a>
    </ul>
    <div class="tech-contents">
      <div>
        <p class="tech-title" id="anchor1">개요</p>
        <p class="tech-contents-text">
          지난 게시글 Deep Anomaly Detection in Time Series (1) : Time Series
          Data에서는 시계열 데이터와 이상치(Anomaly)의 종류에 대해
          알아보았습니다. 그리고 이번 글에선 이상 감지가 어려운 이유와 여러
          종류의 이상 감지 방법을 소개하고자 합니다.
        </p>
        <div class="tech-title" id="anchor2">이상 감지는 왜 어려울까?</div>
        <p class="tech-contents-text">
          근래에 들어 인공지능은 큰 발전을 해 오고 있습니다. 이에 따라 이미지
          인식, 자율주행, Speech-to-Text, Text-to-Speech 등 많은 분야의 연구가
          극적인 성과를 보이고 있고요. 대표적인 예로 이미지 분류(Image
          Classification)를 들 수 있겠네요. 이미지 분류 분야는 이미지를 입력했을
          때 어떠한 종류의 이미지인지 맞추는 인공지능 분야입니다. 이미지 분류
          분야의 대표적인 대회인 ILSVRC(ImageNet Large Scale Visual Recognition
          Challenge)[1]의 경우 백만 장의 이미지를 학습하여 15만 장의 새로운
          이미지를 1000종류로 분류하는 대회인데요, 2011년에는 약 50%의 정확도를
          보였지만 10년이 지난 현재 90%를 넘는 정확도를 보이고 있습니다.
        </p>
        <p class="tech-contents-text">
          인공지능은 이러한 눈부신 성과와 함께 많은 분야에서 산업화가 이루어지고
          있습니다. 하지만 이상 감지 분야는 그 특유의 복잡성과 난제로 인해 아직
          산업화가 이루어지는 곳이 많지 않은 것이 현실입니다. 그러면 왜 이상
          감지가 어려운 것일까요? Lukas 등[2] 은 이상 감지가 어려운 이유로
          다음의 3가지를 들었습니다.
        </p>
        <div class="tech-contents-title">무수히 많은 이상 패턴</div>
        <p class="tech-contents-text">
          ‘이상’이란 단어의 뜻을 조사해보면 다음과 같이 나옵니다. “평소와는 다른
          상태”. 즉, 평소의 데이터 패턴(정상 데이터) 외의 모든 종류의 패턴이
          모두 이상 데이터라고 할 수 있습니다. 정상 데이터는 그 종류가 몇가지 안
          되겠지만 이상 데이터의 패턴은 매우 다양하겠지요. 더군다나 데이터가
          다변량 시계열(Multivariate Time-series, 이전 게시글 참고)이라면 이상
          패턴의 다양성은 기하급수적으로 증가합니다. 또한 이상 패턴이 무수히
          많은 만큼 한 번도 본 적 없는 이상 패턴이 발생할 수도 있는 것이고요.
          이러한 다양성은 당연히 문제를 어렵게 만들 것입니다.
        </p>
        <div class="tech-contents-title">데이터 불균형</div>
        <p class="tech-contents-text">
          일반적인 경우 이상 패턴이 포함된 데이터의 수는 정상 데이터에 비해 매우
          작을 것입니다. 이렇게 데이터의 비율이 큰 차이를 보이는 경우를 ‘데이터
          불균형’이라고 하는데요, 이는 이상 감지 모델을 학습하는 데에도, 이를
          통해 실제로 감지하는 데에도 어려움을 야기합니다.
        </p>
        <p class="tech-contents-text">
          기계학습 및 딥러닝 모델 학습에서 가장 중요한 것 중 하나가 ‘데이터의
          양’인데요, 다음의 그림을 보시면 과거의 기계학습 방법도 데이터의 양이
          중요하지만 딥러닝 방법에서 데이터의 양이 더욱 중요한 것을 알 수
          있습니다. 반면, 이상 감지 문제에서는 정상 데이터의 수가 아무리 많다고
          해도 정작 중요한 이상 데이터가 워낙 적으니 이상 감지의 성능이 좋기가
          힘든 것이지요.
        </p>
        <p class="tech-contents-text">
          데이터 불균형은 실제 현장에 적용하는 입장에서도 어려움을 야기하는데요.
          이상 감지 문제의 특성 상 ‘정상 데이터를 이상으로 분류하는 경우(Type 1
          Error, False Positive)’보다는 ‘이상 데이터를 정상으로 분류하는
          경우(Type 2 Error, False Negative)’가 더 치명적인데, 수많은 정상
          데이터 중에서 모든 이상 데이터를 놓치지 않고 찾아내는 것은 난이도 높은
          문제지요. 그렇다고 정상 데이터의 반을 이상으로 분류해버린다면 이상
          감지의 의미가 없어지고요.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/anomaly_1.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          1종 오류, 2종 오류의 예시(출처: Netflix blog)
        </p>
        <div class="tech-contents-title">다양한 이상 데이터의 종류</div>
        <p class="tech-contents-text">
          이상 데이터의 종류에 대해서는 지난 게시글
          <a
            class="tech-contents-link"
            href="../views/TechBlogAnomaly1KrView.vue"
            >(Deep Anomaly Detection in Time Series (1): Time Series Data).</a
          >
          에서 자세히 다루었습니다.
        </p>
        <p class="tech-contents-text">
          이 이상 데이터는 각각의 특징이 서로 매우 달라서 모든 종류의 이상
          데이터를 전부 감지하는 것은 난이도가 있다고 할 수 있습니다. 이상
          데이터의 종류에 대한 자세한 내용은 지난 게시글을 참고해주세요.
        </p>
        <div class="tech-title" id="anchor3">다양한 종류의 이상 감지 방법</div>
        <p class="tech-contents-text">
          위에서 언급된 문제점에 대해서 시계열 데이터의 이상 감지 분야에는 매우
          많은 방법들이 연구되어왔습니다. 이 글에서 그 모든 방법을 소개하거나
          분류하기에는 무리가 있고, 과거에 사용되던 방법부터 그 한계, 그리고 그
          대안이 되는 방법을 간략하게 소개하고자 합니다.
        </p>
        <div class="tech-contents-title">과거의 이상 감지</div>
        <p class="tech-contents-text">
          과거에는 시계열 데이터의 이상 감지가 어떻게 이루어졌을까요? 여러가지가
          있지만 대표적으로 3-sigma, boxplot, ARIMA 3가지를 간략하게
          소개해드립니다.
        </p>
        <p class="tech-contents-text">
          3-sigma의 경우 정규 분포에서 3표준편차(3σ)의 범위 내에는 데이터의
          99.7%가 들어가는데, 이 이외의 데이터를 이상 데이터로 취급하는 방법이고
          boxplot은 사분위수(Quartile)와 사분범위(Interquartile range)를
          이용하여 이상 데이터의 기준을 정하는 방법입니다. 마지막으로,
          ARIMA(Auto-regressive Integrated Moving Average,
          자기회귀누적이동평균)는 시계열을 예측하는 데에 주로 이용됩니다. 이를
          이용해 미래의 시계열을 예측한 후, 관측 데이터와의 오차 혹은 관측값이
          발생할 확률 등을 통해 이상 데이터를 판별하는 방식으로 이상 감지에
          이용됩니다.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/anomaly_2.jpg"
            alt=""
          />
        </div>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/anomaly_3.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          Univariate time series ARIMA (출처 :
          <a
            class="tech-contents-link"
            href="https://github.com/Jenniferz28/Time-Series-ARIMA-XGBOOST-RNN"
          >
            https://github.com/Jenniferz28/Time-Series-ARIMA-XGBOOST-RNN)</a
          >
        </p>
        <p class="tech-contents-text">
          하지만 이 모든 방법들은 단변량 시계열(Univariate Time-series)
          대상이며, Boxplot과 3-sigma의 경우 Point Anomaly밖에 감지하지 못
          한다는 단점이 있습니다.
        </p>
        <div class="tech-contents-title">예측 기반 이상 감지</div>
        <p class="tech-contents-text">
          위에서 언급한 3가지 방법 중 ARIMA가 시계열 데이터만 잘 예측한다면
          이론적으로는 3가지 종류의 이상 데이터를 모두 감지할 수 있습니다.
          하지만 단변량 시계열이 국한되어 있었죠. 그렇다면 다변량
          시계열(Multivariate Time-series) 또한 예측을 통해 이상 데이터를 감지할
          수 있지 않을까요?
        </p>
        <p class="tech-contents-text">
          하지만 시계열 예측분야에서 가장 유명한 대회 중 하나인 Makridakis
          competitions(M Competition)[5, 6]는 ‘예측의 주된 목적은 불확실성을
          줄이는 것이 아닌, 모든 가능성을 최대한 정교하게 보여주는 것’이라면서,
          ‘모든 예측은 불확실하며, 이러한 불확실성은 무시할 수 없다’고 말하고
          있습니다. 2020년도에 정확성(Accuracy) 분야[5]뿐만 아니라
          불확실성(Uncertainty) 분야[6]의 대회가 같이 열린 이유이기도 하죠.
        </p>
        <p class="tech-contents-text">
          따라서 단변량에 비해 불확실성이 클 수밖에 없는 다변량 시계열의 경우
          예측 기반의 이상 감지는 큰 도움이 되지 않을 수도 있습니다. 다만,
          비교적 작은 불확실성의 데이터와 불확실성을 정교하게 표현할 수 있는
          모델이 있다면 예측 기반 이상 감지가 유효한 선택이 될 수 있겠습니다.
        </p>
        <div class="tech-contents-title">지도학습 기반 이상 감지</div>
        <p class="tech-contents-text">
          그렇다면 예측 기반 이상 감지를 제외하고 인공지능을 사용하여 시계열
          데이터에서 이상 현상을 감지한다고 하면 가장 먼저 떠올릴 수 있는 방법은
          무엇일까요?
        </p>
        <p class="tech-contents-text">
          아마 시계열 데이터를 이상과 정상으로 분류하는 인공지능 모델을 학습하는
          방법이라고 생각합니다. 이미지 분류 분야에서도 딥러닝 모델이 좋은
          성과를 보이고 있기도 하니까요. 이렇게 데이터 별로 사전에 이상/정상을
          라벨링하여 학습시키는 것을 ‘지도학습’이라고 합니다(시계열 예측 모델도
          지도학습의 일종입니다).
        </p>
        <p class="tech-contents-text">
          지도학습 기반의 이상 감지 모델을 만든다면 ’09:00~09:10의 데이터는
          정상, 09:10~09:20 데이터도 정상, 09:20~09:30 데이터는 이상’ 이런
          식으로 학습이 되지 않을까 합니다. 이렇게 학습이 이상적으로 된다면
          모델은 3가지 종류(Point Anomaly, Contextual Anomaly, Group Anomaly)의
          이상 데이터를 모두 높은 정확도로 감지하는 것이 가능할 것입니다.
          실제로도 지도학습은 인공지능 학습 방법 중에서도 성능이 가장 좋은
          방법론으로 알려져 있습니다.
        </p>
        <p class="tech-contents-text">
          하지만 이 직관적인 방법에는 커다란 문제가 있습니다. 데이터가 아무리
          많다 한들 그 중에 이상 데이터는 소수에 불과하고, 그러한 이상 데이터를
          사람이 일일이 찾아서 라벨링하는 것도 어렵습니다. 이러한 상황에서는
          데이터를 준비하는 것도 곤란하고, 준비한다 하더라도 데이터 불균형으로
          인해 모델이 잘 학습될 가능성은 낮습니다.
        </p>
        <div class="tech-contents-title">비지도학습 기반 이상 감지</div>
        <p class="tech-contents-text">
          그러면 라벨링이 필요없는 방법이 있을까요? 라벨링없이 데이터를
          학습시키는 방법을 ‘비지도학습(Unsupervised Learning)’이라고 부릅니다.
        </p>
        <p class="tech-contents-text">
          이 중 대표적인 것이 Autoencoder(오토인코더) 기반의 모델입니다.
          Autoencoder는 입력 데이터를 보다 작은 차원의 데이터로 압축하는
          Encoder와, 압축된 데이터를 다시 입력 데이터와 가깝게 복원하는
          Decoder로 이루어져 있습니다. 그림으로 보면 다음과 같습니다.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/anomaly_4.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          Autoencoder의 개념(출처 : 위키피디아)
        </p>
        <p class="tech-contents-text">
          이렇게 데이터를 압축하고 복원하는 데에는 무슨 의미가 있을까요? 이
          Autoencoder를 사용할 때에는, 고차원의 데이터를 더 간단하게 표현할 수
          있는 저차원의 공간(Manifold)이 있다는 가정이 필요합니다. 이러한 가정이
          성립할 때 Autoencoder는 학습을 통해 이 manifold로의 압축과
          manifold로부터의 복원 방법을 배우는 것입니다.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/anomaly_5.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          고차원의 데이터(좌)를 저차원의 manifold(우)로 표현하는 예시
        </p>
        <p class="tech-contents-text">
          이상 데이터(X표시)는 Autoencoder에 의해 mapping되면서 정상데이터의
          manifold로 변환된다.
        </p>
        <p class="tech-contents-text">
          이러한 manifold는 ‘학습 데이터 전반에 걸친 주요 특징’을 의미하며,
          데이터의 양이 매우 적은 이상 데이터의 특징은 포함되기 어렵습니다.
          그렇다면 학습이 끝났을 때 Auto Encoder에 정상 데이터를 넣으면
          정상적으로 복원된 출력이 나오겠지만, 이상 데이터를 넣는다면 이상
          데이터의 특징은 잘 추출되지 않고 대신 입력 데이터와 그나마 가장 가까운
          정상 데이터가 나올 것입니다. 그렇다면 입력 데이터와 출력 데이터의
          차이(Reconstruction Error)는 정상 데이터에 비해 클 수밖에 없고, 이러한
          차이를 이용해 이상 데이터를 감지할 수 있습니다.
        </p>
        <p class="tech-contents-text">
          이러한 Auto Encoder 기반의 모델을 생성한다면 해당 모델은 정상 패턴이
          아닌 데이터는 이상 데이터의 종류나 패턴에 상관없이 모두 이상 데이터로
          간주할 수 있습니다. 하지만 모델의 구조를 포함한 여러 요인에 따라
          manifold가 좌우되며, 이는 성능의 등락으로 이어집니다. 즉, 사용자의
          모델 설정(hyperparameter)에 따라 성능이 크게 달라질 수 있으며, 최적의
          성능의 모델을 찾는 것이 어려울 수 있습니다.
        </p>
        <p class="tech-contents-text">
          또한 이상 데이터가 정상 데이터와 가까운 경우라면, 혹은 동일한
          manifold로 표현될 수 있다면 Autoencoder가 이상 데이터까지도 성공적으로
          복구해내는 경우가 있을 수 있겠네요. 이런 현상이 발생한다면 이상 감지
          모델은 이상 데이터를 잘 감지하지 못 할 것입니다.
        </p>
        <div class="tech-contents-title">반지도학습 기반 이상 감지</div>
        <p class="tech-contents-text">
          지금까지 모든 데이터에 대해 정상/이상의 라벨링이 필요한 경우와
          라벨링이 필요없는 경우를 소개해드렸습니다. 그런데 사용자가 다수의 정상
          데이터와 소수의 이상 데이터를 이미 파악하고 있는 경우라면 어떻게 할 수
          있을까요? 전체 데이터 중 일부만 라벨링하여 학습시키는 방법을
          ‘반지도학습(Semi-supervised Learning)’이라고 합니다. 다른 두가지
          방법(지도학습과 비지도학습)에 비해 비교적 최근에 성립된 방법론이라고
          할 수 있습니다.
        </p>
        <p class="tech-contents-text">
          반지도학습 기반 이상 감지 모델 중에는 DeepSVDD[6]라는 모델이 있습니다.
          SVDD(Support Vector Data Description)에 딥러닝을 적용시킨 모델인데요.
          간단히 설명하면 데이터를 데이터 특징 만의 공간인 feature space로
          변환하되, 정상 데이터만을 학습하여 정상 feature를 둘러싸는 최적의
          구(Hypershpere)를 찾는 방법입니다. 이 구 안의 데이터는 정상, 밖의
          데이터는 이상으로 판별이 됩니다.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/anomaly_6.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          DeepSVDD의 개념: 데이터(좌)는 모델(중)을 통해 feature space(우)로
          매핑되며, 이때 정상 데이터는 hypersphere 안에, 이상 데이터는
          hypersphere 밖에 위치된다.
        </p>
        <p class="tech-contents-text">
          지금까지 시계열 데이터에서의 이상 감지 방법에 대해서 간략하게
          소개해드렸습니다. 위에서 설명드린 것은 이외에도 다양한 관점에서 이상
          감지 문제를 해결하려는 연구가 활발히 이루어지고 있습니다. 이 중 몇가지
          분야를 나열하자면 다음과 같습니다.
        </p>
        <ul class="tech-ul">
          <li>
            Out-of-Distribution(OD) : 다양한 종류의 정상 상태를 분류하면서도
            처음 보는 데이터를 맞닥뜨리면 이를 Unknown으로 판별할 수 있도록 하는
            분야
          </li>
          <li>
            Contrastive Learning : 정상/이상 등의 레이블 없이 데이터의 유사성을
            학습하여 지도학습 모델에 버금가는 정확도를 보이도록 하는 비지도 학습
            방법
          </li>
          <li>
            생성 모델(Generative Model) : VAE(Variational Autoencoder)나
            GAN(Generative Adversarial Networks) 등의 생성 모델을 적용, 학습
            데이터의 분포를 학습하여 정확도를 올리고자 하는 방법
          </li>
          <li>
            Transformer : 자연어 처리(Natural Language Processing, NLP) 분야에서
            좋은 성과를 보인 Transformer 기반의 모델을 이상 감지에 적용하고자
            하는 방법
          </li>
        </ul>
        <p class="tech-contents-text">
          하지만 이 중 적지 않은 수의 연구가 시계열 데이터가 아닌 이미지
          데이터의 이상 감지를 목적으로 이루어지고 있는데요, 그렇다면 이러한
          모델을 어떻게 시계열 데이터에 적용할 수 있을까요?
        </p>
        <p class="tech-contents-text">
          대표적인 방법으로는 STFT(Short-term Fourier Transform), CWT(Continuous
          Wavelet Transform) 등이 있겠습니다. 요즘에는 CQT(Constant Q
          Transform)가 사용되기도 합니다. 실제로 인공지능 모델을 이용해 시계열
          데이터를 분석할 때에는 사전에 STFT, CWT 등의 방법 뿐만 아니라 다양한
          방법으로 가공이 된 후에 인공지능 모델에 입력됩니다. 이러한 데이터의
          사전 가공을 ‘전처리(Preprocess)’라고 부릅니다. 시계열 데이터에서의
          전처리에 대해서는 다음에 기회가 될 때 소개해드리겠습니다.
        </p>
        <div class="tech-img-wrap">
          <img src="../../img/anomaly_7.jpg" alt="" />
        </div>
        <p class="tech-contents-link-text">
          STFT (출처 : Digital Signal Processing System Design)
        </p>
        <div class="tech-title" id="anchor4">결론</div>
        <p class="tech-contents-text">
          지금까지 시계열 데이터에 대해 이상 데이터를 감지할 수 있는 다양한
          방법을 소개해드렸습니다. 각각의 방법이 다른 문제점을 해결하기 위해
          제안된 만큼, 이상 감지를 적용하고자 하는 업무에 따라 제일 적합한
          방법과 인공지능 모델이 존재할 것입니다. 그리고 가장 적합한 방법을 찾는
          것이 이상 감지 기술의 적용의 시작점이라 할 수 있겠습니다.
        </p>
        <p class="tech-title">Reference</p>
        <ul class="tech-ul">
          <li>
            Ruff, Lukas, et al. “A unifying review of deep and shallow anomaly
            detection.” Proceedings of the IEEE (2021).
          </li>
          <li>
            Russakovsky, Olga, et al. “Imagenet large scale visual recognition
            challenge.” International journal of computer vision 115.3 (2015):
            211-252.
          </li>
          <li>
            Makridakis, S., E. Spiliotis, and V. Assimakopoulos. “The M5
            accuracy competition: Results, findings and conclusions.” Int J
            Forecast (2020).
          </li>
          <li>
            Makridakis, S., et al. “The M5 Uncertainty competition: Results,
            findings and conclusions.” International Journal of Forecasting
            (2020): 1-24.
          </li>
          <li>
            <a
              class="tech-contents-link"
              href=" https://en.wikipedia.org/wiki/Autoencoder"
              >https://en.wikipedia.org/wiki/Autoencoder</a
            >
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
        <button class="contactus">고객 문의</button>
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
