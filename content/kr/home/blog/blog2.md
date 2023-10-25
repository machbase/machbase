---
title: Blog
description: "마크베이스 네오(Machbase Neo)는 왜 프론트엔드 프레임워크를 vue.js에서 react로 바꾸었는가?"
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
    <h4 class="blog-title">
      마크베이스 네오(Machbase Neo)는 왜 프론트엔드 프레임워크를 vue.js에서
      react로 바꾸었는가?
    </h4>
    <div class="blog-date">
      <div>
        <span>by Andrew Kim / 1 Sep 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">
          프론트엔드 프레임워크에 대해
        </li></a
      >
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">
          지난 3년간의 vue.js 활용기
        </li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">
          마크베이스 네오를 위한 새로운 시도
        </li>
      </a>
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">
          마크베이스 네오 8.0에서 vue.js를 React로 대체하다!
        </li>
      </a>
      <a href="#anchor5">
        <li class="tech-list-li" id="tech-list-li">결론</li>
      </a>
    </ul>
    <div class="tech-contents">
      <div>
        <div class="tech-title" id="anchor1">프론트엔드 프레임워크에 대해</div>
        <p class="tech-contents-text">
          오늘날의 소프트웨어 환경에서 웹 기반 프런트 엔드 부분을 디자인하고
          개발하는 것은 의심할 여지 없이 어렵고 복잡합니다. 그러나 이는 사용자와
          직접적으로 소통하는 사용자 인터페이스를 포함하는 가장 중요한 측면 중
          하나입니다. 이러한 이유로 특정 회사의 개발 조직 내에서 사용자
          인터페이스 개발을 위한 프레임워크를 선택하는 것은 다양한 요인의 복잡한
          결과입니다. 이러한 요소에는 다양한 지식 배경, 고유한 요구 사항, 문화
          및 개인 특성, 회사 철학이 포함됩니다.
        </p>
        <p class="tech-contents-text">
          결과적으로, 사용자 인터페이스 생성을 위한 기반으로 프레임워크를
          선택하려면 복잡한 의사 결정이 필요합니다. 이 결정은 다양한 고려 사항을
          고려하며 이러한 복잡성의 상호 작용에 따라 결과가 결정됩니다. 특별한
          이유 없이 특정 프레임워크를 선택하는 것이 가능하지만, 그러한 대개
          신중한 평가와 조직의 목표 및 요구 사항에 대한 복잡한 의사 결정의
          결과물이라고 이야기 할 수 있습니다.
        </p>
        <div class="tech-title" id="anchor2">지난 3년간의 vue.js 활용기</div>
        <p class="tech-contents-text">
          마크베이스 개발팀은 지난 3년간 프론트엔드의 주요 프레임워크로 vue.js를
          사용해 왔습니다. 이 vue.js는 특히 CEMS라고 하는 에지 컴퓨팅 기반의
          클라우드 제품 핵심 사용자 인터페이스 부분의 핵심 기반 프레임워크로서
          사용자의 다양한 시각적 요구 사항을 만족시키기 위해 설계와 구현
          과정에서 대부분의 프론트엔드 개발자들이 학습해왔고, 이미 익숙해져
          있었습니다.
          <a class="tech-contents-link" href="https://www.cems.ai"
            >(https://www.cems.ai)</a
          >
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/neo-first-01.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          &lt;CEMS screenshot developed by Vue.js&gt;
        </p>
        <p class="tech-contents-text">
          그렇지만, 지난 1년간 마크베이스 네오라는 새로운 데이터베이스 제품을
          개발하면서 채택한 vue.js가 최고의 선택인지 의문이 들기 시작했습니다.
        </p>
        <div class="tech-title" id="anchor3">
          New Endeavors for Machbase Neo
        </div>
        <p class="tech-contents-text">
          우선 마크베이스 네오를 설명을 드려야겠네요.
          <a class="tech-contents-link" href="https://neo.machbase.com"
            >(https://neo.machbase.com)</a
          >. 이 제품은 시계열 데이터베이스 제품이지만, 미래의 기술 트렌드를
          추구하는 All-In-One 개념의 제품으로서 사용자가 이 제품만으로 데이터의
          저장과 추출뿐만 아니라, 데이터의 수집과 변환 그리고, 내장된 다양한
          서버인 MQTT, SSH, HTTP, gRPC 등을 통해 불필요한 부가 프로세스의 설치와
          관리의 비용을 대폭 줄이는 것을 목표로 개발되었습니다.
        </p>
        <p class="tech-contents-text">
          특히, 이 제품은 오픈소스로서 누구가 접근해서 그 구조와 동작원리를
          이해할 수 있으며, 내부에 세계에서 가장 빠른 TPC 랭킹 1위의 마크베이스
          TSDB가 내장되어 있습니다.
        </p>
        <p class="tech-contents-text">
          <a
            class="tech-contents-link"
            href="https://github.com/machbase/neo-server"
            >(https://github.com/machbase/neo-server)</a
          >
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/neo-first-02.png"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          즉, 네오를 활용하는 고객이 해당 데이터를 별도의 시각화 도구가 필요
          없이 다양한 차트를 그리고, 모든 작업을 웹 기반으로 할 수 있도록 하기
          위해 vue.js라는 프론트엔드 프레임워크를 사용하고 있습니다.
        </p>
        <p class="tech-contents-text">
          그런데, 개발이 진행되면 될수록 vue.js에 대한 장단점에서 단점이 점점 더
          커지게 되었습니다. 우선 이 프레임워크의 장단점을 기술해 보겠습니다.
        </p>
        <div class="tech-contents-title">Vue.js 장점:</div>
        <p class="tech-contents-text">
          1. 쉬운 학습 난이도: Vue.js는 완만한 학습 곡선을 제공하므로 다양한
          기술 수준을 가진 개발자가 접근할 수 있습니다.
        </p>
        <p class="tech-contents-text">
          2. 유연성 및 다용도성: Vue.js는 유연한 구조를 제공하므로 개발자는 이를
          기존 프로젝트에 통합하거나 필요에 따라 프레임워크의 특정 부분을 사용할
          수 있습니다.
        </p>
        <p class="tech-contents-text">
          3. 반응형 데이터 바인딩: 프레임워크의 반응형 데이터 바인딩은 모델과 뷰
          간의 데이터 동기화 프로세스를 단순화합니다.
        </p>
        <p class="tech-contents-text">
          4. 구성 요소 기반 아키텍처: Vue.js는 구성 요소 기반 접근 방식을
          촉진하여 모듈식 개발 및 재사용성을 촉진합니다.
        </p>
        <div class="tech-contents-title">Vue.js의 단점:</div>
        <p class="tech-contents-text">
          1. 덜 성숙한 생태계: React와 같은 프레임워크에 비해 Vue.js는
          라이브러리 및 도구로 구성된 더 작은 생태계를 가지고 있어 잠재적으로
          고급 기능에 대한 옵션이 제한됩니다.
        </p>
        <p class="tech-contents-text">
          2. 제한된 기업 지원: Vue.js는 React 또는 Angular에 비해 기업 지원이
          적으므로 장기적인 지속 가능성 및 업데이트에 영향을 미칠 수 있습니다.
        </p>
        <p class="tech-contents-text">
          3. 성능 문제: 애플리케이션이 확장됨에 따라 Vue.js는 특히 복잡하고 깊게
          중첩된 구성 요소를 처리할 때 성능 문제에 직면할 수 있습니다.
        </p>
        <p class="tech-contents-text">
          4. 소규모 커뮤니티: Vue.js의 소규모 사용자 커뮤니티로 인해 문제 해결
          속도가 느려지고 문제 해결을 위한 리소스가 줄어들 수 있습니다.
        </p>
        <p class="tech-contents-text">
          장점에도 불구하고 이러한 단점이 점점 더 부각되면서 우리는 Vue.js를
          Machbase Neo의 프런트엔드 개발에 있어 진화하는 요구 사항에 가장 적합한
          것으로 재검토하게 되었습니다.
        </p>
        <p class="tech-contents-text">
          물론, 특히 개발이 진행됨에 따라 우리는 단점 1과 3이 개발 시간과 비용에
          점점 더 많은 영향을 미치고 있다는 것을 깨달았습니다. 새로운 기능을
          도입해야 하는 필요성으로 인해 기존 구성 요소에 의존할 수 없고 새로운
          구성 요소를 개발해야 하는 상황이 자주 발생했습니다. 이는 프로젝트의
          복잡성과 리소스 요구 사항을 더욱 가중시켰습니다.
        </p>
        <p class="tech-contents-text">
          게다가 기능이 성장하면서 웹 기반 UI 성능의 질적인 저하가 느껴지기
          시작했습니다. 이러한 인식은 사용자마다 다를 수 있다는 점을 인정하는
          것이 중요하지만, 더 많은 기능이 통합됨에 따라 원활하고 응답성이 뛰어난
          사용자 경험을 유지할 수 있는 능력에 대한 우려가 제기되었습니다.
        </p>
        <p class="tech-contents-text">
          물론 대안으로 고려하고 있는 React의 장단점을 살펴보겠습니다.
        </p>
        <div class="tech-contents-title">React의 장점:</div>
        <p class="tech-contents-text">
          1. 활발한 개발 커뮤니티: eact는 다양한 요구 사항을 해결하기 위해
          다양한 라이브러리 선택을 제공하는 매우 활발한 개발 커뮤니티의 이점을
          누리고 있습니다.
        </p>
        <p class="tech-contents-text">
          2. 효율적인 가상 DOM: React의 깔끔하고 효율적인 가상 DOM 구조는 더
          빠른 렌더링 속도에 기여합니다.
        </p>
        <p class="tech-contents-text">
          3. 신속한 개선 및 반복: React는 빈번한 업데이트와 개선을 통해 시간이
          지남에 따라 기능과 성능이 향상됩니다.
        </p>
        <div class="tech-contents-title">React의 단점:</div>
        <p class="tech-contents-text">
          1. 어려운 학습 난이도: React는 Vue에 비해 상대적으로 가파른 학습
          곡선을 가지고 있습니다.
        </p>
        <p class="tech-contents-text">
          2. 아키텍처로 인한 복잡성: React의 아키텍처로 인해 일부 복잡한 코딩
          시나리오가 발생할 수 있으며, 이는 특정 단위 개발 작업 중에 문제를
          일으킬 수 있습니다.
        </p>
        <p class="tech-contents-text">
          3. 지속적인 학습 필요: 지속적인 아키텍처 개선과 구조적 변화를 위해서는
          모범 사례를 따라잡기 위한 지속적인 학습이 필요합니다.
        </p>
        <p class="tech-contents-text">
          위에 단점에서 기술한 것과 같이 배우는데 꽤 오랜 시간이 걸리고,
          난이도가 높다는 것이 문제이기는 하지만, 일단 한번 익숙해지면, 장점의
          1번과 같이 정말 다양한 라이브러리의 제공을 통해 개발 시간을 단축하고,
          결과적으로 개발 비용을 낮출 수 있다는 점이 매우 매력적이었습니다.
          특히, 장점의 2번과 같이 실제로 바꾸어서 테스트를 해 보았을 때, 반응
          속도가 몇 배나 빨라질 수 있다는 가능성을 보았거든요.
        </p>
        <div class="tech-title" id="anchor4">
          마크베이스 네오 8.0에서 vue.js를 React로 대체하다!
        </div>
        <p class="tech-contents-text">
          내부적으로 기술 서베이를 마친 후에는 React를 채택하는 UI에 대한
          대대적인 재개발이 이루어졌습니다. 이 작업은 그렇게 오래 걸리지는
          않았으며, 대략 1~2개월 정도 걸린 것 같습니다. 물론, UI의 외부도 꽤
          바뀌었습니다만, 기본 기능은 큰 차이가 없습니다.
        </p>
        <div class="tech-contents-title">기존의 Machbase Neo 1.7 UI</div>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/neo-first-03.png" alt="" />
        </div>
        <p class="tech-contents-link-text">기존의 Machbase Neo 1.7 UI</p>
        <div class="tech-contents-title">새로운 Machbase Neo 8.0 UI</div>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/neo-first-04.png" alt="" />
        </div>
        <p class="tech-contents-link-text">새로운 Machbase Neo 8.0 UI</p>
        <div class="tech-contents-title">React를 통해 무엇이 좋아졌나요?</div>
        <p class="tech-contents-text">
          다음은 개발자에게 직접 전해 들은 react를 통해 좋아진 점들에 대한
          리스트입니다만, 직접 써 보니, 이전보다 응답 성능이 2~3배 이상 올라간
          것 같습니다. 50마일로 달리는 세단을 타다가 200마일로 달리는
          람보르기니를 직접 운전하는 느낌이랄까요?
        </p>
        <ul class="tech-ul">
          <li>
            <b>성능향상</b>: 우선적으로 느끼기에 VD의 최적화가 잘되어 있어서,
            렌더링 시 속도가 빠릅니다.
          </li>
          <li>
            <b>개발 시간 단축</b>: 프로젝트의 사이즈가 커질수록 투입되는 개발
            시간이 Vue.js보다 좋습니다.
          </li>
          <li>
            <b>풍부한 커뮤니티</b> : 개발 시에 필요한 자료의 양이 많다 보니,
            문제가 생기면 해결 방법을 찾는데 효율적입니다.
          </li>
          <li>
            <b>자유도</b> : 코드 자율성이 높아 개발자의 실력에 따라, 조금 더
            짧고 간결한 코드를 작성할 수 있습니다.
          </li>
          <li>
            <b>컴포넌트 재활용성</b> : hooks 사용을 통한 재사용 컴포넌트 개발이
            효율적입니다.
          </li>
          <li>
            <b>개발 용이성</b> : React의 method 방식 사용으로 lifecycle이 매우
            간결화되어 있습니다.
          </li>
        </ul>
        <div class="tech-title" id="anchor5">결론</div>
        <p class="tech-contents-text">
          이 내용은 마크베이스 네오 개발팀의 정말 주관적인 의견입니다. 그래서,
          다양한 개발 조직에서는 다른 의견을 가질 수 있고, 아마도 각각의
          프레임워크는 그 사용처에 따라 장단점이 달라질 수 있을 것 같습니다.
          그런 이유로 이 문서의 내용을 전적으로 믿지 마시고, 직접 개발하고,
          테스트하신 후에 나름의 결론을 가지시기를 권유 드립니다. 어쨌거나,
          마크베이스 네오 팀은 개발 속도도 빨라지고, 무엇보다 반응 속도가
          쾌적해진 현재의 상황에 매우 만족하고 있습니다.
        </p>
        <p class="tech-contents-text">
          이러한 경험이 다른 커뮤니티에도 많은 도움이 되기를 바라며, 이만
          줄입니다.
        </p>
        <p class="tech-contents-text">감사합니다.</p>
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
          <a href="https://www.slideshare.net/machbasekr" target="_blank"
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
          <a href="https://www.slideshare.net/machbasekr" target="_blank"
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
