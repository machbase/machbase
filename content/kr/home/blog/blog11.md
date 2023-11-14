---
title: Blog
description: "How to make Sensor Data send directly to a Database via MQTT?"
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
      ESG를 위한 선택: 시계열 데이터베이스 엔진
    </h4>
    <div class="blog-date">
      <div>
        <span>by Timothy Cha / 11 Nov 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">글을 시작하며</li></a
      >
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">
          데이터 센터와 관련된 환경 이슈들
        </li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">해결책</li>
      </a>
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">
          ESG를 위한 방법으로서의 시계열 데이터베이스
        </li>
      </a>
      <a href="#anchor5">
        <li class="tech-list-li" id="tech-list-li">글을 마치며</li>
      </a>
    </ul>
    <div class="tech-contents">
      <p class="tech-title" id="anchor1">글을 시작하며</p>
      <p class="tech-contents-text">
        디지털 시대가 도래하면서 우리의 생활 영역 어느 것이나 데이터를 만들어 내고 데이터를 필요로 하고 있다. 이로 인해 데이터는 비즈니스에서 핵심 자산으로 간주되며, 데이터를 효과적으로 수집, 관리, 분석하고 활용할 수 있는 능력과 함께 그를 위한 핵심 인프라의 구축이 중요해지고 있다.
      </p>
      <p class="tech-contents-text">
        특히 빅데이터를 이용한 데이터 분석 기술의 발전과 인공지능(AI)과 이를 위한 머신러닝(ML) 알고리즘의 발전은 이러한 흐름에 박차를 가하고 있다.
      </p>
      <p class="tech-contents-text">
        하지만 이를 위한 인프라 특히 데이터 센터에 대해서는 ESG, 특히 환경 분야에서 여러가지 문제가 제기되고 있다.
      </p>
      <p class="tech-contents-text">
        이 글에서는 이와 관련하여 어떤 환경적인 이슈가 제기되고 있고 이를 위해 어떤 해결책들이 논의되고 있는가를 살펴보고자 한다.
      </p>
      <div class="tech-title" id="anchor2">
        데이터 센터와 관련된 환경 이슈들
      </div>
      <p class="tech-contents-text">
        데이터를 관리하기 위해서는 서버, 스토리지, 네트워킹 장비 등 다양한 장비를 필요로 한다.
      </p>
      <p class="tech-contents-text">
        데이터와 직간접적으로 관련이 있는 회사는 대부분 이러한 장비를 보관하고 있는 서버실이라는 공간을 가지고 있고 특히 데이터를 전문적으로 다루는 IT 기업들은 데이터 센터라는 대규모 시설을 가지고 있다. 이 데이터센터란 앞서 이야기한 서버, 스토리지, 네트워킹 장비 등 다양한 장비를 한 곳에 모아 놓은 컴퓨터를 위한 호텔 같은 곳이라고 보면 될 것이다.
      </p>
      <p class="tech-contents-text">
        데이터가 더 중요해지고 필요로 할수록 이 기반 시설인 데이터 센터도 더 거대화되고 있으며 이로 인해 환경적으로 미치는 영향도 더 커지고 있다.
      </p>
      <p class="tech-contents-text">이를 나누어 보면 다음과 같다.</p>
      <p class="tech-contents-title">전력 에너지 사용</p>
      <div class="tech-img-wrap">
        <img
          class="tech-img "
          src="../../img/blog11-1.png"
          alt=""
        />
      </div>
      <p class="tech-contents-link-text">
        Inside a customer data suite at Union Station. Image: Global Access
        Point. Public domain. 2008
      </p>
      <p class="tech-contents-text">
        데이터 센터에 관련된 이슈 중 가장 먼저 제기되는 것은 전력 사용량이다. 전자기기를 사용하는 이상 전력을 사용하는 것은 피할 수 없는 것이기는 하지만 데이터 센터라는 시설이 환경적인 이슈로까지 문제가 제기되는 것은 이 곳에서 사용되는 전력 사용량이 우리가 생각하는 것보다 더 엄청나기 때문이다.
      </p>
      <p class="tech-contents-text">
        기본적으로 수십만대의 전자기기가 돌아가는 자체 만으로도 어마어마한 전기를 필요로 하지만 이와 별도로 전력을 소모시키는 추가적인 이유도 있다.
      </p>
      <p class="tech-contents-text">1. 24시간 운영</p>
      <p class="tech-contents-text">
        데이터 센터는 24시간 운영을 원칙으로 한다. 실시간 처리가 필요로 하는 분야가 많을 뿐 아니라 글로벌 비즈니스 환경에서는 지역 및 시간에 관계없이 서비스를 지속적으로 제공해야 하기 때문이다. 그 외에 시간대에 따라 자원 사용을 최적화하기 위해서도 24시간 운영을 한다.
      </p>
      <p class="tech-contents-text">2. 온도와 습도 유지</p>
      <p class="tech-contents-text">
        컴퓨터 서버, 스토리지 시스템, 네트워크 장비 등 데이터 센터의 핵심 장비들은 작동하면서 열을 발생시키지만 일정한 온도 범위에서 가장 효과적으로 작동하며, 과다한 온도 상승은 부품의 손상을 유발하므로 일정한 온도가 유지될 수 있도록 냉각하는 것이 중요하다.
      </p>
      <p class="tech-contents-text">
        한편 온도의 관리와 함께 습도의 관리도 중요한데 습도가 높으면 컨덴세이션(이슬점 현상)이 발생할 가능성이 높아져 전자 부품에 수분이 침투하여 단락이나 부식이 발생할 수 있고 반대로 습도가 낮으면 정전기를 발생하기 쉬워지기 때문이다. 정전기는 전자 기기에 영향을 미쳐 데이터 손실이나 하드웨어 손상을 유발할 수 있다.
      </p>
      <p class="tech-contents-text">3. 이중화</p>
      <p class="tech-contents-text">
        이중화란 데이터 센터 내의 주요 구성 요소들을 중복하여 설치, 가동되도록 하여 시스템의 안정성과 가용성을 확보하는 방법을 말한다.
      </p>
      <p class="tech-contents-text">
        데이터 센터는 이중화를 원칙으로 하고 있으며 이것이 설비를 늘리고 전력 사용을 2배로 하게 하는 원인이 된다. 이중화를 하는 이유는 핵심 장비의 고장, 각종 재해로 인한 사고, 더 나아가 시스템 전체의 보안의 측면에서 이중화가 거의 유일한 해결책이 되기 때문이다.
      </p>
      <p class="tech-contents-text">
        한편 이러한 데이터센터가 사용하는 전력량을 보다 구체적으로 살펴보자면 다음과 같다.
      </p>
      <p class="tech-contents-text">
        데이터 센터의 평방 미터당 전력소비량은 대략 1,000kWh라고 한다.이는 일반적인 상업용 사무실에 비해 바닥 면적당 10~50배에 해당하는 수치라고 하며 수만 개의 서버를 갖춘 대규모 데이터센터가 필요로 하는 전력량은 5만 가구의 전력 소비량과 맞먹는다고도 한다.
      </p>
      <p class="tech-contents-text">
        한국의 경우 2022년 12월 기준 국내 147개 데이터센터가 있고 2029년까지 5배 이상(약 700여개) 증가할 것으로 전망되고 있으나 현재 147개 데이터센터의 전력사용량(3,337GWh) 만으로도 원전 1기가 연간 생산하는 전력생산량(7,000GWh)을 절반 가까이 소비하고 있어 향후 필요한 전력량을 확보하기 위해서는 원전 2~3기의 증설까지도 고민되어야 하는 상황이다.
      </p>
      <p class="tech-contents-title">물 사용량</p>
      <div class="tech-img-wrap">
        <img
          class="tech-img"
          src="../../img/blog11-2.png"
          alt=""
        />
      </div>
      <p class="tech-contents-link-text">
        Steam rises above cooling towers at the Google Dalles data center in
        Oregon. Google photo
      </p>
      <p class="tech-contents-text">
        데이터 센터에서의 물 사용량도 이슈가 된다. 데이터 센터에서 사용되는 물의 사용량이 상상 외로 많기 때문이다. 구글은 21년 전세계의 구글 데이터센터의 물 사용량이 162억 리터이고 이는 미국 남서부의 29개 골프장이 사용한 물의 량과 비슷하다고 밝힌 바 있다.
      </p>
      <p class="tech-contents-text">
        데이터 센터에서 물이 사용되는 곳은 서버 과열을 방지하기 위한 냉각 장치와 비상시의 전력을 보충하기 위한 발전기다.
      </p>
      <p class="tech-contents-text">
        기존의 냉각 장치 외에도 서버 랙의 격자에 냉각수를 흘려보내는 등 다양한 방식의 냉각 장치가 개발되어 있으나 어떤 방식을 쓰더라도 냉각 탑의 쿨링 시스템에서 물을 사용하는 사실은 피할 수가 없다.
      </p>
      <p class="tech-contents-text">
        한편 데이터 센터는 비상시의 전력 공급을 위해 발전기를 설치하는데, 정전 시 전원을 백업하는 목적이라 평상시 가동이 거의 없으나 발전기 가동시에는 증기로 터빈을 돌려 발전을 하기 때문에 이를 위해 막대한 양의 물이 필요하다.
      </p>
      <p class="tech-contents-title">전자 및 독성 폐기물</p>
      <div class="tech-img-wrap">
        <img
          class="tech-img "
          src="../../img/blog11-3.png"
          alt=""
        />
      </div>
      <p class="tech-contents-link-text">
        This amazing pile of English e-waste awaits recycling. Photograph by Stefan Czapski, courtesy Geograph. CC-BY-SA-2.0
        <a
          class="tech-contents-link"
          href="https://blog.education.nationalgeographic.org/"
          >https://blog.education.nationalgeographic.org/</a
        >
      </p>
         <p class="tech-contents-text">
  일반적으로 하이퍼스케일 데이터센터는 연면적 2만2500㎡ 수준의 규모에 최소 10만대 이상의 서버를 갖춘 데이터센터로 정의된다
      </p>
      <p class="tech-contents-text">
       전세계 하이퍼스케일 데이터센터는 2021년 기준 628개(출처: 시스코)이고 한국 내에도 LG유플러스의 평촌 데이터센터와 네이버의 각 세종 데이터센터 등 10만대 이상의 서버를 보유한 하이퍼스케일 데이터센터가 있다.
      </p>
      <p class="tech-contents-text">
        문제는 데이터 센터에서 사용하는 수십만개의 서버들의 수명이 4~5년에 불과하며 EPA(미국 환경보호청)에 따르자면 전자 쓰레기, 즉 버려지는 전자장비가 독성 쓰레기로 분류된다는 것에 있다. (독성 쓰레기의 70%가 전자장비 쓰레기)
      </p>
      <p class="tech-contents-text">
        이는 전자제품에 브롬계 난연제와 같은 독성 화학물질뿐만 아니라 납이나 수은, 카드뮴, 베릴륨 등을 사용하기 때문이다.
      </p>
      <p class="tech-contents-text">
        UN의 최근 보고서에 따르면 2019년 한 해 전 세계에 버려진 전자폐기물은 5360만 톤에 달하는데 17.4%만이 재활용되고 82.6%는 매립, 소각되고 있다고 한다. 게다가 대부분의 전자 폐기물은 각 국가의 엄격한 환경규제와 높은 처리비용 등에 따라 중국·인도·아프리카 등의 개발도상국으로 수출되고 있는데 이는 전자 폐기물이 지구 전체를 오염시키고 있다는 의미이기도 하다.
      </p>
      <p class="tech-contents-title">열과 소음, 전자파</p>
      <p class="tech-contents-text">
        앞에서 언급한 3가지에 비하면 심각성이 덜하지만 데이터 센터는 그 자체로 엄청난 열을 발생시킨다. 냉각 장치로 데이터 센터 내부의 온도를 낮추는 것에 엄청난 에너지를 사용한다는 것은 데이터 센터 내부에서 엄청난 열이 발생하고 있고 그것이 외부로 방출되고 있다는 것을 의미한다. 이는 지구온난화라는 문제이기도 하다.
      </p>
      <p class="tech-contents-text">
        또 수십만대의 서버에서 발생하는 막대한 량의 전자파와 수많은 전자장비와 에어컨에서 발생하는 소음 또한 사람들의 생활 뿐 아니라 생태계에도 영향을 미칠 수 있다.
      </p>
      <div class="tech-title" id="anchor3">해결책</div>
      <p class="tech-contents-text">
        앞서의 문제들에 대한 주요 해결책들은 다음과 같다.
      </p>
      <p class="tech-contents-title">
        냉각에 필요한 전력 최소화
      </p>
      <div class="tech-img-wrap">
        <img
          class="tech-img "
          src="../../img/blog11-4.png"
          alt=""
        />
      </div>
      <p class="tech-contents-link-text">
        Project Natick —
        <a
          class="tech-contents-link"
          href="https://natick.research.microsoft.com/"
          >https://natick.research.microsoft.com/</a
        >
      </p>
      <p class="tech-contents-text">
       냉각을 위해 사용되는 전기를 최소화하기 위해 다양한 방법이 사용되고 있다.
      </p>
      <p class="tech-contents-text">
        온도 조절 특히 냉각은 전체 전기 사용량의 40~55%를 차지하여 데이터 센터에서 가장 많은 전력을 사용하는 부분이므로 이 부분이 전체 전기 사용량을 줄이는 데 있어서 가장 중요한 부분이라 할 수 있다.
      </p>
      <p class="tech-contents-text">
        구글은 수냉식 냉각방식으로 기존 냉각방식에 비해 전력 사용량을 10% 줄였다고 밝힌 바 있으며 이외에도 많은 기업들이 다양한 방식의 냉각방식으로 전력량을 줄이기 위한 노력을 하고 있다.
      </p>
      <p class="tech-contents-text">
        메타(페이스북)은 유럽 전역을 위한 데이터 센터를 일년 내내 서늘한 지역인 스웨덴 룰레오에 지어 냉각 비용을 절감하였고 MS는 프로젝트 나틱을 통해 바다 속에 데이터센터를 두는 것을 실험 중이다.
      </p>
      <p class="tech-contents-text">
        한국의 LG 유플러스의 평촌 안양 데이터 센터, 네이버의 춘천 각 데이터 센터 등도 외부공기를 이용한 공냉식 냉각방식을 적극적으로 사용하여 냉각을 위해 사용되는 전기량을 줄이는 노력을 하고 있다.
      </p>
      <p class="tech-contents-title">데이터 센터 최적화</p>
      <div class="tech-img-wrap">
        <img
          class="tech-img "
          src="../../img/blog11-5.webp"
          alt=""
        />
      </div>
      <p class="tech-contents-link-text">Image creator from Microsoft Bing</p>
      <p class="tech-contents-text">
        데이터 센터 내의 서버, 스토리지 등 여러 장비의 최적화를 통해 에너지 소비를 줄이는 방법 또한 검토되어야 하는 주제이다.
      </p>
      <p class="tech-contents-text">
        데이터 센터를 운영하다보면 서버에 설치해둔 애플리케이션이 시간이 지나면서 쓸모 없게 되거나 서비스 구독이 중단되어 해당 서버를 사용하지 않게 되었는데도 그대로 방치되어 전력을 소모하는 경우가 발생하기 때문이다.
      </p>
      <p class="tech-contents-text">
        인프라 관리 회사인 코만트(Cormant)에 따르면 좀비 서버라고도 불리는 이러한 서버가 데이터 센터의 서버들 중 10~30%라고 한다.
      </p>
      <p class="tech-contents-text">
        보다 철저한 관리를 통해 좀비 상태의 서버 제거, 서버의 통합 및 가상화, 데이터 삭제를 통한 스토리지 장비의 축소 등으로 불필요한 시설들을 줄이는 것만으로도 상당한 량의 에너지 소비를 줄일 수 있다.
      </p>
      <p class="tech-contents-title">전력 공급 효율 개선</p>
      <div class="tech-img-wrap">
        <img
          class="tech-img "
          src="../../img/blog11-6.png"
          alt=""
        />
      </div>
      <p class="tech-contents-link-text">
        Comparison of AC and HVDC power feed systems in a datacenter or
        communications building.(NTT Technical Review)
      </p>
      <p class="tech-contents-text">
        데이터 센터 내의 여러 설비들을 24시간에 걸쳐 안정적으로 운용하기 위해서는 비상용 축전지, 발전장치, 장치 냉각용 고신뢰 공조설비 등 많은 기반 설비를 필요로 한다. 이러한 설비들에 전력이 공급되는 구조와 방식의 개선을 통해 전력을 절약할 수 있는지도 검토되고 있다.
      </p>
      <p class="tech-contents-text">
        대표적인 것이 직류급전이다. 서버들은 내부적으로 직류를 사용하므로 파워를 직류로 바로 공급하게 되면 서버 내부 전원에서 교류에서 직류로 변환 작업을 수행할 필요가 없어져 전력을 절약할 수 있기 때문이다. 일반적으로 전력변환 1회당 10% 정도의 손실이 발생하므로 직류급전은 교류급전에 비해 전력변환단수가 적은 만큼 원리적으로 효율의 개선을 얻을 수 있다.
      </p>
      <p class="tech-contents-text">
        이외에도 기존 발전기를 연료전지와 같은 대체 전력 솔루션으로 교체하여, 탄소 배출량과 각종 비용을 최소화하는 방안이 연구되고 있다.
      </p>
      <div class="tech-title" id="anchor4">
        ESG를 위한 방법으로서의 시계열 데이터베이스
      </div>
      <p class="tech-contents-text">
        최근 들어 ESG가 중요한 개념으로 떠오르고 있다.
      </p>
      <p class="tech-contents-text">
        ESG란 환경 (Environment), 사회 (Social), 지배구조 (Governance)의 세 가지 측면을 나타내는 개념으로, 기업이 사회적 책임을 다하고 지속가능한 경영을 추구하는가를 평가하기 위한 개념이다.
      </p>
      <p class="tech-contents-text">
        ESG가 중요해진 이유는 기업의 ESG에 대한 규제가 강화되면서 ESG와 관련된 성과가 기업의 가치평가에 큰 영향을 주고 있기 때문이다.
      </p>
      <p class="tech-contents-text">
        ESG의 관점에서 시계열 데이터베이스 엔진은 앞서 이야기한 3가지와 다른 방식으로 환경을 위한 해결책을 제시할 수 있다.
      </p>
      <p class="tech-contents-text">
        시계열 데이터란 센서 데이터와 같이 시간의 흐름에 데이터 값이 대응되는 형태의 데이터인데 시계열 데이터베이스 엔진은 이러한 종류의 데이터를 저장하고 제공하는 용도에 최적화된 소프트웨어 시스템을 말한다.
      </p>
      <p class="tech-contents-text">
        즉 센서 데이터와 같은 시계열 데이터를 처리해야 하는 경우에 시계열 데이터베이스 엔진을 사용할 경우 기존 데이터베이스 엔진보다 훨씬 적은 설비로도 처리가 가능하기 때문이다.
      </p>
      <p class="tech-contents-text">
        결국 운영과 냉방에 필요한 전력과 물 사용을 줄일 수 있을 뿐 아니라 폐기물의 발생도 줄일 수 있는 상당히 의미 있는 해결책이다.
      </p>
      <p class="tech-contents-text">
        필자가 일하고 있는 마크베이스의 시계열 데이터베이스 엔진의 경우 국제 공인 성능 평가 기관인 TPC(Transaction Processing Performance Council)에서 진행한 가격/성능 평가 테스트에서 세계 최고의 성능을 가진 것으로 평가 받았고 미국의 하둡에 비해 6배 가까운 성능 차이가 있음을 입증한 바 있다.
      </p>
      <div class="tech-img-wrap">
        <img
          class="tech-img "
          src="../../img/blog11-7.webp"
          alt=""
        />
      </div>
      <p class="tech-contents-link-text">
        <a
          class="tech-contents-link"
          href="https://www.tpc.org/tpcx-iot/results/tpcxiot_price_perf_results5.asp?version=2"
          >https://www.tpc.org/tpcx-iot/results/tpcxiot_price_perf_results5.asp?version=2</a
        >
      </p>
      <p class="tech-contents-text">
        이 테스트에서 동일 성능 기준을 충족시키기 위한 비용 산정에서 하둡은 $329.75, 마크베이스는 $54.85를 기록하였다.
      </p>
      <p class="tech-contents-text">
        이 6배 가까운 차이가 나는 이유는 데이터베이스 엔진 자체의 성능이 뛰어날 뿐 아니라 아키텍처를 단순화할 수 있기 때문이다.
      </p>
      <p class="tech-contents-text">
        예를 들어 마크베이스는 하둡을 쓰는 시스템을 마크베이스로 단순화할 수 있음을 ETRI와의 프로젝트로 실제로 증명하기도 하였다.
      </p>
      <div class="tech-img-wrap">
        <img
          class="tech-img "
          src="../../img/blog11-8.png"
          alt=""
        />
      </div>
      <p class="tech-contents-link-text">Before: Hadoop</p>
      <div class="tech-img-wrap">
        <img
          class="tech-img "
          src="../../img/blog11-9.png"
          alt=""
        />
      </div>
      <p class="tech-contents-link-text">After: Machbase TSDB</p>
      <p class="tech-contents-text">
        본 건은 전력 빅데이터를 수집하고 딥러닝 알고리즘 개발을 하기 위한 에너지 빅데이터 플랫폼을 구축하는 프로젝트였는데 마크베이스는 하둡 대신 시계열 데이터베이스 엔진을 적용시 플랫폼 아키텍처를 단순하게 만들 수 있어 하드웨어의 구축 비용과 시간을 줄일 수 있을 뿐 아니라 전체적인 설비의 물리적인 사이즈도 줄일 수 있음을 입증하였다.
      </p>
      <div class="tech-title" id="anchor5">글을 마치며</div>
      <p class="tech-contents-text">
        환경과 에너지의 중요성은 아무리 강조해도 지나침이 없다. ESG라는 지속가능한 발전에 대한 지표가 실질적으로 기업의 투자가치 평가에 사용됨은 실제로 환경 이슈가 기업의 생존과도 직결되는 이슈라는 것을 이야기하고 있다.
      </p>
      <p class="tech-contents-text">
        데이터의 증가와 이를 위한 설비의 증가는 피할 수 없는 흐름이다. 하지만 이것이 환경에 미치는 영향을 최소화하는 것은 우리가 어떻게 하는가에 달린 문제일 것이다.
      </p>
      <p class="tech-contents-text">
        모든 분야에 적용할 수 있는 만병통치약은 아니지만 시계열 데이터를 사용하는 영역에서는 시계열 데이터베이스 엔진의 적용을 통해 환경에 가해지는 충격을 최소화할 수 있다는 것은 입증된 사실이다.
      </p>
      <p class="tech-contents-text">
        현재 개발된 DBMS 중 시계열 데이터 관련 설비를 가장 최소화할 수 있음이 공식적으로 입증된 것은 마크베이스의 시계열 데이터 엔진이다.
      </p>
      <p class="tech-contents-text">
        지구 환경, 더 나아가 ESG라는 이슈에 대해 고민하는 사람들이라면 마크베이스의 시계열 데이터베이스 엔진으로 환경에 대한 충격을 최소화하는 방법을 검토하기를 추천드린다.
      </p>
    </div>
  </div>
</section>
{{< home_footer_blog_kr >}}
