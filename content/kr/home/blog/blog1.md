---
title: Blog
description: "당신의 개발 Know-how를 기록하는 새로운 방법"
---

<head>
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
    <h4 class="blog-title">당신의 개발 Know-how를 기록하는 새로운 방법</h4>
    <div class="blog-date">
      <div>
        <span>by James Lee / 7 Sep 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">개요</li></a
      >
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">
          WorkWorksheet 작성 언어 - Markdown
        </li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">Neo Markdown 문법</li>
      </a>
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">Worksheet 관리</li>
      </a>
      <a href="#anchor5">
        <li class="tech-list-li" id="tech-list-li">결론</li>
      </a>
    </ul>
    <div class="tech-contents">
      <div>
        <p class="tech-title" id="anchor1">개요</p>
        <p class="tech-contents-text">
          <b
            >Machbase Neo는 Machbase time series database를 기반으로 사용자
            편의성을 극대화한 All-in-one package 솔루션입니다.</b
          >
        </p>
        <p class="tech-contents-text">
          Machbase Neo에 대한 자세한 내용은 웹사이트
          <a class="tech-contents-link" href="https://machbase.com/neo"
            >https://machbase.com/neo</a
          >을 참고하면 됩니다.
        </p>
        <p class="tech-contents-text">
          Machbase Neo 기능 중에 문서를 작성할 수 있는 worksheet 라는 기능이
          있다. 단순히 정적인 문서를 작성하는 것이 아니라 SQL 구문 등은 직접
          실행해서 결과를 문서상에 표시할 수 있기 때문에 Interactive 하게 내용을
          이해할 수 있습니다.
        </p>
        <p class="tech-contents-text">
          또한 작성된 worksheet 을 통해 Machbase Neo 사용법 등을 사용자 간
          공유할 수 있어서 서로 간의 정보교류의 수단으로도 활용할 수 있습니다.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/neo-worksheet-1.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          &lt; Machbase Neo worksheet 실행 메뉴 >
        </p>
        <p class="tech-title" id="anchor2">Worksheet 작성 언어 — Markdown</p>
        <p class="tech-contents-text">
          Markdown 문법을 이용하여 worksheet를 작성한다. Markdown은 일반 텍스트
          기반의 경량 마크업 언어로 태그 등을 이용하여 문서나 데이터의 구조 등을
          표시하는 언어이다. 주로 텍스트만으로 서식 있는 문서를 작성할 때
          사용되며, 문법이 간단하고 쉬어서 약간의 학습으로 누구나 문서를 작성할
          수 있습니다.
        </p>
        <p class="tech-contents-text">
          Markdown은 Github, Notion, Discord 등 다양한 서비스 플랫폼에서
          지원하고 있으며 대부분의 텍스트 에디터 환경에서 작성 및 수정이
          가능합니다.
        </p>
        <p class="tech-contents-text">
          다만 파일이나 이미지가 문서 내에 바로 임베딩되지 않기 때문에서 별도의
          서버에 업로드하고 나서 파일 URL을 입력해야 합니다.
        </p>
        <p class="tech-title" id="anchor3">Neo Markdown 문법</p>
        <p class="tech-contents-text">
          일반적인 Markdown 문법은 여기
          <a class="tech-contents-link" href="https://www.markdownguide.org/basic-syntax/"
            >(https://www.markdownguide.org/basic-syntax/)</a
          >.
        </p>
        <p class="tech-contents-text">
          Machbase Neo에서는 SQL 구문을 실행할 수 있는 버튼이 있어 SQL쿼리문을
          실행하면 실제로 Neo TSDB에서 SQL 쿼리문을 실행하고 그 결과를 화면에
          표시할 수 있는 기능이 있습니다.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/neo-worksheet-2.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          &lt; Machbase Neo worksheet에서 SQL 구문 실행 화면 예시 >
        </p>
        <p class="tech-contents-text">
          예를 들어, 작성 입력창에서 SQL 구문을 작성하고 문서 타입을 Markdown이
          아닌 SQL로 선택하면 됩니다. 그리고 실행 아이콘을 클릭하면 해당 SQL
          문이 실제로 수행이 되고 그 결과값을 아랫부분에 표시하게 됩니다. 단순히
          static 문서를 read 하는 것이 아니라 interactive 하게 TSDB와 연동해서
          동작 여부를 확인할 수 있습니다.
        </p>
        <p class="tech-contents-text">
          SQL 문장뿐만 아니라 Machbase Neo에서 제공하는 TQL 문법도 바로 실행이
          가능하고 그 결과를 화면에 표시하게 됩니다.
        </p>
        <p class="tech-title" id="anchor4">Worksheet 관리</p>
        <p class="tech-contents-text">
          작성된 Worksheet은 저장하게 되면 Neo가 설치된 경로에 wrk 확장자 파일로
          저장됩니다.
        </p>
        <p class="tech-contents-text">
          작성된 파일을 다른 사용자에게 공유하면 Machbase Neo의 Worksheet에서
          바로 오픈하여 읽어볼 수 있습니다. Machbase Neo를 설치하면 워크시트를
          사용하여 이미 작성된 튜토리얼 문서를 볼 수 있습니다.
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/neo-worksheet-3.png" alt="" />
        </div>
        <p class="tech-contents-link-text">
          &lt; Machbase Neo built-in worksheet example >
        </p>
        <p class="tech-contents-text">
          Machbase Neo 메인화면에서 Drop&Open 영역에 해당 파일을 마우스로 drag &
          drop 하면 문서가 오픈됩니다.
        </p>
        <p class="tech-title" id="anchor5">결론</p>
        <p class="tech-contents-text">
          Machbase Neo Worksheet 기능은 텍스트 기반의 Markdown 언어를 통해
          간단하고 쉽게 문서를 작성하고 관리할 수 있는 기능이다.
        </p>
        <p class="tech-contents-text">
          Machbase Neo 사용법 또는 가이드 문서를 작성하고 다른 사용자가
          worksheet 문서를 read 하면서 쉽게 따라 해볼 수 있다. 특히 SQL 구문,
          TQL 구문은 문서상에서 바로 실행해서 결과를 확인해 볼 수 있기 때문에
          초보자도 Machbase Neo 상에서 쉽게 따라 해보면서 내용을 파악할 수 있다.
        </p>
      </div>
    </div>
  </div>
</section>
{{< home_footer_blog_kr >}}
{{< home_lang_kr >}}
