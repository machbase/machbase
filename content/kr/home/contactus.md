---
title: Contact US
description: "해당 양식을 작성하여 제출해 주시면 최대한 빨리 연락드리겠습니다."
images:
  - /namecard/og_img.jpg
---

<head>
  <link rel="stylesheet" type="text/css" href="../css/common.css" />
  <link rel="stylesheet" type="text/css" href="../css/style.css" />
</head>
<body>
  {{< home_menu_sub_kr >}}
  <div>
    <section class="contact_section0">
      <h2 class="sub_page_title">Contact US</h2>
      <p class="sub_page_titletext">
        If you fill out the form and submit it, we will contact you as soon as
        possible
      </p>
    </section>
    <section class="section1">
      <div class="contact_inner">
        <form
          id="contactForm"
          action="https://machbase.com/contact"
          method="post"
          enctype="utf-8"
        >
          <div class="sub_titlebox">
            <h4 class="sub_page_sub_title">Contact Form</h4>
            <div class="bar"><img src="../img/bar.png" /></div>
          </div>
          <div class="contact-long-div">
            <span class="input-span">성함*</span>
            <label>
              <input
                class="long-input"
                type="text"
                name="name"
                id="fullName"
                placeholder="성함을 입력해주세요"
            /></label>
          </div>
          <div class="contact-short-div-wrap">
            <div class="contact-short-div">
              <span class="input-span">이메일*</span>
              <input
                class="short-input"
                type="text"
                name="email"
                id="emailAddress"
              />
            </div>
            <div class="contact-short-div">
              <span class="input-span">국가*</span>
              <select
                class="short-input"
                id="countrySelect"
                name="country"
              ></select>
            </div>
          </div>
          <div>
            <span class="input-span">문의 유형*</span>
            <div class="radio-input-wrap">
              <div class="radio-div">
                <input
                  class="radio-input"
                  type="radio"
                  checked
                  name="title"
                  value="Sales"
                />
                <span>세일즈</span>
              </div>
              <div class="radio-div">
                <input
                  class="radio-input"
                  type="radio"
                  name="title"
                  value="Marketing"
                />
                <span>마케팅</span>
              </div>
              <div class="radio-div">
                <input
                  class="radio-input"
                  type="radio"
                  name="title"
                  value="Partners"
                />
                <span>파트너</span>
              </div>
              <div class="radio-div">
                <input
                  class="radio-input"
                  type="radio"
                  name="title"
                  value="Media Contact"
                />
                <span>언론홍보</span>
              </div>
            </div>
          </div>
          <div>
            <span class="input-span">문의 내용*</span>
            <textarea
              class="contact_input"
              id="helpText"
              type="text"
              name="contents"
            ></textarea>
          </div>
          <div>
            <div class="check_cont">
              <input
                type="checkbox"
                id="privacyCheckbox"
                class="checkbox"
                value="Send"
              />
              <p>
                <a id="openModalBtn" class="policy">개인정보처리방침</a>
                에 동의합니다
              </p>
              <div id="modalDiv" class="modal">
                <div class="modal-content">
                  <div class="modal_title">
                    <p class="policy_title">개인정보 처리방침</p>
                    <p id="closeModalBtn" class="close">&times;</p>
                  </div>
                  <p class="policy_text">
                    본 개인정보취급방침은 본 방침이 게시된 웹사이트에서
                    제공되거나 수집되는 정보의 처리에 대해 설명합니다. 또한,
                    타사 웹사이트 또는 플랫폼에 있는 회사의 애플리케이션을
                    사용함으로써 제공되거나 수집되는 정보의 처리에 대해
                    설명합니다.
                  </p>
                  <p class="policy_text">
                    회사는 이용자의 개인정보를 중요시하며, 개인정보취급방침을
                    통하여 회사가 이용자로부터 제공받은 개인정보를 어떠한 용도와
                    방식으로 이용하고 있으며, 개인정보 보호를 위해 어떠한 조치를
                    취하고 있는지 알려드립니다.
                  </p>
                  <p class="policy_text">
                    본 방침은 2015 년 월 일부터 시행되며, 이를 개정하는 경우
                    웹사이트 공지사항(또는 서면, 팩스, 이메일 등의 개별공지)을
                    통하여 공지하겠습니다.
                  </p>
                  <p class="policy_text">
                    1. 수집하는 정보 및 수집방법<br />(1) 수집하는 개인정보의
                    항목 회사가 수집하는 개인정보의 항목은 다음과 같습니다.
                  </p>
                  <p class="policy_text">
                    • 이용자가 제공하는 정보<br />
                    회사는 이용자가 직접 제공하는 정보를 수집할 수 있습니다.<br />
                    [개인정보취급방침 부록 &lt;1-1&gt; '개인정보 항목' 취사선택]
                  </p>
                  <p class="policy_text">
                    • 이용자가 서비스를 사용할 때 수집하는 정보<br />회사는
                    이용자가 직접 제공하는 정보 이외에도, 이용자가 회사의
                    서비스를 사용하는 과정에서 정보를 수집할 수 있습니다.
                    <br />[개인정보취급방침 부록 &lt;1-2&gt; '개인정보 항목'
                    취사선택]
                  </p>
                  <p class="policy_text">
                    (2) 수집방법<br />
                    회사는 이용자의 정보를 다음과 같은 방법으로 수집합니다.
                    [개인정보취급방침 부록 &lt;2&gt; '수집 방법' 취사선택]
                  </p>
                  <p class="policy_text">
                    2. 수집한 정보의 이용<br />
                    회사는 수집한 이용자의 정보를 다음과 같은 목적으로
                    이용합니다.<br />[개인정보취급방침 부록 &lt;3&gt; '수집
                    정보의 이용' 취사선택]
                  </p>
                  <p class="policy_text">
                    본 개인정보취급방침에 명시된 목적과 다른 용도로 정보를
                    이용할 경우, 회사는 이용자의 동의를 구하도록 하겠습니다.
                  </p>
                  <p class="policy_text">
                    3. 수집한 정보의 공유<br />
                    회사는 다음의 경우를 제외하고 이용자의 개인정보를 제 3
                    자에게 공유하지 않습니다.<br />
                    • 회사의 계열사, 파트너, 서비스 제공업체에 대한 공유<br />
                    [개인정보취급방침 부록 &lt;4-1&gt; '수집 정보의 이용'
                    취사선택]
                  </p>
                  <p class="policy_text">
                    •이용자가 사전에 동의하는 경우<br />
                    [개인정보취급방침 부록 &lt;4-2&gt;'수집 정보의 공유'
                    취사선택]
                  </p>
                  <p class="policy_text">• 법률상 필요한 경우</p>
                  <p class="policy_text">- 법령상 공개하도록 요구되는 경우</p>
                  <p class="policy_text">
                    - 수사 목적으로 법령에 정해진 절차와 방법에 따라 수사기관의
                    요구가 있는 경우
                  </p>
                  <p class="policy_text">
                    4. 쿠키, 비콘 및 기타(Cookies, Beacons and Similar
                    Technologies)<br />
                    회사는 '쿠키(cookies)' 또는 '웹 비콘(web beacons)' 등을
                    통하여 비개인적인 집합정보를 수집할 수 있습니다. 쿠키란
                    회사의 웹사이트를 운영하는데 이용되는 서버가 이용자의
                    브라우저에 보내는 아주 작은 텍스트 파일로, 이용자의 컴퓨터
                    하드디스크에 저장됩니다.
                  </p>
                  <p class="policy_text">
                    웹 비콘은 웹사이트 또는 이메일 상에 있는 소량의 코드입니다.
                    웹 비콘을 사용하여 이용자가 특정 웹이나 이메일 콘텐츠와 상호
                    작용했는지 여부를 알 수 있습니다.
                  </p>
                  <p class="policy_text">
                    이러한 기능은 서비스를 평가하고 개선하여 이용자 경험을 맞춤
                    설정하는 데 유용하게 이용되어, 이용자에게 더 향상된 서비스를
                    제공합니다.
                  </p>
                  <p class="policy_text">
                    T회사가 수집하는 쿠키의 항목 및 수집 목적은 다음과
                    같습니다.<br />
                    [개인정보취급방침 부록 &lt;5&gt; '수집하는 쿠키' 취사선택]
                  </p>
                  <p class="policy_text">
                    이용자는 쿠키 설치에 대한 선택권을 가지고 있습니다. 따라서
                    웹브라우저에서 옵션을 설정함으로써 모든 쿠키를 허용하거나,
                    쿠키가 저장될 때마다 확인을 거치거나, 아니면 모든 쿠키의
                    저장을 거부할 수도 있습니다. 단, 이용자께서 쿠키 설치를
                    거부하였을 경우 회사가 제공하는 일부 서비스에 어려움이 있을
                    수 있습니다.
                  </p>
                  <p class="policy_text">
                    5. 이용자의 접근권한과 선택권<br />
                    이용자 또는 법정대리인은 정보의 주체로서 회사의 개인정보
                    수집, 사용, 공유와 관련하여 다음과 같은 선택권을 행사할 수
                    있습니다.
                  </p>
                  <p class="policy_text">
                    • 개인정보에 대한 접근권한<br />
                    • 개인정보의 정정 또는 삭제<br />
                    • 개인정보 처리의 일시 정지<br />
                    • 기존에 제공한 동의의 철회의 요청<br />
                  </p>
                  <p class="policy_text">
                    이를 위하여 웹페이지의 '회원정보 수정' 메뉴를 이용하시거나,
                    대표전화 또는 회사 담당부서(또는 개인정보 관리책임자)에게
                    서면, 전화 또는 이메일로 연락하시면 지체 없이
                    조치하겠습니다. 다만 회사는 법률에 명시된 타당한 사유 또는
                    그에 상응하는 사유가 있는 경우에만 그러한 요청을 거부할 수
                    있습니다.
                  </p>
                  <p class="policy_text">
                    6. 보안<br />회사는 이용자의 개인정보에 대한 보안을 매우
                    중요하게 생각합니다. 회사는 이용자 개인정보의 무단 접근,
                    공개, 사용 및 수정을 막기 위해 다음과 같은 보안 조치를
                    구축하고 있습니다. [개인정보취급방침 부록 &lt;6&gt;
                    '보안조치' 취사선택]
                  </p>
                  <p class="policy_text">
                    7. 어린이 개인정보 보호<br />회사는 원칙적으로 13 세 미만
                    또는 관할 법률상 이에 상응하는 최소 연령의 어린이로부터
                    정보를 수집하지 않습니다. 회사의 웹사이트, 제품과 서비스
                    등은 원칙적으로 일반인을 대상으로 한 웹 사이트입니다. 회사의
                    웹사이트 또는 애플리케이션에는 연령 제한 기능이 있어서
                    어린이가 이용할 수 없도록 하고 있으며, 그러한 기능을 통해
                    어린이로부터 고의로 개인정보를 수집하지 않습니다.
                  </p>
                  <p class="policy_text">
                    (어린이 개인정보를 수집하는 경우 추가) 다만 회사가 부득이
                    서비스 이용을 위하여 13 세 미만 또는 관할 법률상 이에
                    상응하는 최소 연령의 어린이의 개인정보를 수집할 때에는,
                    어린이 개인정보 보호를 위해 다음과 같은 절차를 추가적으로
                    거치게 됩니다.
                  </p>
                  <p class="policy_text">
                    • 어린이 개인정보 수집 또는 회사의 제품, 서비스 정보를
                    어린이에게 직접 발송하기 위한 보호자 동의 획득<br />
                    • 수집한 개인정보 항목, 목적, 공유 여부를 포함한 회사의
                    어린이 개인정보보호 방침에 대하여 보호자에게 통보<br />
                    • 법정대리인에게 해당 아동의 개인정보에 대한 액세스 /
                    개인정보의 정정 또는 삭제 / 개인정보 처리의 일시 정지 /
                    기존에 제공한 동의의 철회를 요청할 수 있는 권한의 부여<br />•
                    온라인 활동의 참여에 필요한 것 이상의 개인정보 수집의 제한
                  </p>
                  <p class="policy_text">
                    8. 개인정보취급방침의 변경<br />
                    회사는 회사의 본 방침을 수시로 수정 내지 변경할 권리를
                    보유합니다. 회사가 본 방침을 변경하는 경우 웹사이트
                    공지사항(또는 서면, 팩스, 이메일 등의 개별공지)을 통하여
                    공지하며, 관계법에서 요구하는 경우에는 이용자의 동의를
                    구하게 됩니다.
                  </p>
                  <p class="policy_text">
                    9. 기타<br />
                    [개인정보취급방침 부록 &lt;7&gt; '데이터 전송' 취사선택]<br />
                    [개인정보취급방침 부록 &lt;8&gt;'제 3 자 사이트 및 서비스'
                    취사선택]<br />
                    [개인정보취급방침 부록&lt;9&gt; '캘리포니아 거주자에 대한
                    안내' 취사선택]<br />
                    [개인정보취급방침 부록 &lt;10&gt; '한국인 거주자에 대한
                    안내' 취사선택]
                  </p>
                  <p class="policy_text">
                    10. 회사 담당부서<br />
                    회사는 이용자의 개인정보를 보호하고 개인정보와 관련한 불만을
                    처리하기 위하여 아래와 같이 관련 부서를 지정하고 있습니다.
                    본 방침에 대하여 의문 사항 있거나 회사가 보유한 이용자의
                    정보를 업데이트하고자 하는 경우, 아래 연락처로 회사에
                    연락하시기 바랍니다.
                  </p>
                  <p class="policy_text">
                    • 회사 담당부서 : <br />
                    주소 : 9F, 3M Tower, 10 Teheran-ro 20-gil, Gangnam-gu,
                    Seoul<br />
                    전화번호: +82-02-2038-4606<br />
                    E-mail: support@machbase.com <br />
                    최종갱신일 : September, 2023
                  </p>
                  <p class="policy_title">개인정보취급방침 부록</p>
                  <p class="policy_text">&lt;1-1&gt; 개인정보 항목</p>
                  <table class="policy_table">
                    <tr class="table_title">
                      <th>서비스명</th>
                      <th>수집 항목(예시)</th>
                    </tr>
                    <tr>
                      <td>인터넷 회원제 서비스</td>
                      <td>
                        ∘ 이름, 이메일 주소, ID, 전화번호, 우편주소, 국가정보,
                        암호화된 동일인 식별정보(CI), 중복가입확인정보(DI) 등
                        <br />∘ 미성년자인 경우 법정대리인 정보(법정대리인의
                        이름, 생년월일, CI, DI 등)
                      </td>
                    </tr>
                    <tr>
                      <td>온라인 결제 서비스</td>
                      <td>
                        ∘ 이름, 주소, 전화 번호, 이메일 주소 등<br />
                        ∘ 계좌번호, 카드번호 등의 결제정보<br />∘ 배송 주소지,
                        수령인 이름, 수령인 연락처 등의 배송정보<br />∘ 입찰,
                        구매, 판매 등 정보
                      </td>
                    </tr>
                    <tr>
                      <td>소셜 네트워크 서비스</td>
                      <td>
                        ∘ 이름, 이메일 주소, ID, 전화 번호, 우편주소, 국가정보,
                        주소록(지인) 등<br />∘ 사진 촬영 장소, 파일 생성 날짜 등
                        정보<br />∘ 회원이 보거나 이용하는 콘텐츠의 유형, 회원의
                        활동 빈도나 기간 등 회원의 서비스 이용에 관한 정보
                      </td>
                    </tr>
                  </table>
                  <p class="policy_text">&lt;1-2&gt; 개인정보 항목</p>
                  <table class="policy_table">
                    <tr class="table_title">
                      <th>목록</th>
                      <th>수집 항목(예시)</th>
                    </tr>
                    <tr>
                      <td>기기정보</td>
                      <td>
                        ∘ 기기 식별자, 운영 체제, 하드웨어 버전, 기기 설정,
                        전화번호 등
                      </td>
                    </tr>
                    <tr>
                      <td>로그정보</td>
                      <td>
                        ∘ 로그데이터, 이용시간, 이용자가 입력한 검색어, 인터넷
                        프로토콜 주소, 쿠키 및 웹비콘 등
                      </td>
                    </tr>
                    <tr>
                      <td>위치정보</td>
                      <td>
                        ∘ GPS, 블루투스 또는 와이파이 신호를 통한 구체적인
                        지리적 위치를 포함한 기기 위치에 대한 정보 등(법으로
                        허용되는 지역에 한함)
                      </td>
                    </tr>
                    <tr>
                      <td>기타정보</td>
                      <td>
                        ∘ 이용자의 서비스 사용에 있어 선호도, 광고 환경,
                        방문하는 페이지 등
                      </td>
                    </tr>
                  </table>
                  <p class="policy_text">&lt;2&gt; 수집 방법</p>
                  <p class="policy_text">
                    • 웹페이지, 서면양식, 팩스, 전화, 이메일, 생성정보 수집 툴
                    등<br />
                    • 협력회사로부터의 제공
                  </p>
                  <p class="policy_text">&lt;3&gt; 수집 정보의 이용</p>
                  <p class="policy_text">
                    • 회원관리, 본인확인 등 <br />
                    • 허가받지 않은 서비스 이용과 부정 이용 등의 탐지 및 방지<br />
                    • 이용자가 요구하는 서비스 제공에 관한 계약 이행, 요금 정산
                    등<br />
                    • 기존서비스 개선, 신규서비스 개발 등<br />
                    • 회사 사이트 또는 애플리케이션의 기능 또는 정책 변경사항의
                    알림<br />
                    • 기타 이용자의 사전 동의에 의한 이용(예를 들어, 마케팅
                    광고에 활용 등)<br />
                    • 연락처에 등록된 지인 검색•알림•자동 등록, 지인일 가능성이
                    있는 다른 이용자의 검색과 알림<br />
                    • 회원의 서비스 이용에 대한 통계, 통계학적 특성에 따른
                    서비스 제공 및 광고 게재<br />
                    • 홍보성 이벤트 정보 제공 및 참여 기회 제공<br />
                    • 준거법 또는 법적 의무의 준수<br />
                  </p>
                  <p class="policy_text">&lt;4-1&gt; 수집 정보의 공유</p>
                  <p class="policy_text">
                    ∘ 회사를 대신하여 결제 처리, 주문 이행, 제품 배송, 분쟁
                    해결(결제 및 배송 분쟁 포함) 등 서비스를 회사의 계열사,
                    파트너, 서비스 제공업체가 수행하는 경우
                  </p>
                  <p class="policy_text">&lt;4-2&gt; 수집 정보의 공유</p>
                  <p class="policy_text">
                    ∘ 이용자의 개인정보를 특정 업체와 공유하여 해당 업체의 제품
                    및 서비스에 대한 정보를 제공받기로 이용자가 선택하는 경우<br />
                    ∘ 이용자의 개인정보를 소셜 네트워킹 사이트와 같은 타사
                    사이트 또는 플랫폼과 공유하도록 이용자가 선택하는 경우
                    <br />
                    ∘ 기타 이용자가 사전에 동의한 경우<br />
                  </p>
                  <p class="policy_text">&lt;5&gt; 수집하는 쿠키</p>
                  <table class="policy_table">
                    <tr class="table_title">
                      <th>카테고리</th>
                      <th>쿠키를 사용하는 이유 및 추가 정보</th>
                    </tr>
                    <tr>
                      <td>반드시 필요한 쿠키</td>
                      <td>
                        이 쿠키는 이용자가 회사의 웹사이트 기능을 이용하는 데
                        필수적인 쿠키입니다. 이 쿠키를 허용하지 않으면
                        장바구니와 전자청구서와 같은 서비스가 제공될 수
                        없습니다. 이 쿠키는 마케팅에 사용하거나 사용자가
                        인터넷에서 방문한 사이트를 기억하는 데 사용될 수 있는
                        정보를 수집하지 않습니다.<br />
                        (반드시 필요한 쿠키의 예시)<br />∘ 웹 브라우저 세션 동안
                        다른 페이지를 검색할 때 주문 양식에 입력한 정보를
                        기억<br />∘ 상품 및 체크아웃 페이지인 경우 주문한
                        서비스를 기억<br />∘ 웹사이트에 로그인 여부를 확인<br />∘
                        회사가 웹사이트의 작동 방식을 변경할 때 이용자가 회사
                        웹사이트의 올바른 서비스에 연결되었는지 확인<br />∘
                        서비스의 특정 어플리케이션 또는 특정 서버로 사용자를
                        연결
                      </td>
                    </tr>
                    <tr>
                      <td>수행 쿠키</td>
                      <td>
                        이 쿠키는 이용자가 가장 자주 방문하는 페이지 정보와 같이
                        이용자가 회사 웹사이트를 어떻게 이용하고 있는지에 대한
                        정보를 수집합니다. 이 데이터는 회사 웹사이트를
                        최적화시키고 이용자가 좀 더 간편하게 웹사이트를 검색할
                        수 있도록 도와줍니다. 이 쿠키는 이용자가 누구인지에 대한
                        정보를 수집하지 않습니다. 이 쿠키가 수집하는 모든 정보는
                        종합적으로 처리되므로 익명성이 보장됩니다.
                        <br />
                        (수행 쿠키의 예시) <br />
                        ∘ 웹 분석 : 웹 사이트를 사용하는 방법에 대한 통계를
                        제공<br />
                        ∘ 광고 반응 요금 : 회사의 광고가 주는 효과를 확인<br />
                        ∘ 제휴사 추적 : 회사 방문자 중 하나가 제휴사의 웹
                        사이트를 방문한 것에 대해 제휴사에게 익명으로 피드백을
                        제공<br />
                        ∘ 오류 관리 : 발생하는 오류를 측정하여 웹 사이트를
                        개선하는 데 도움<br />
                        ∘ 디자인 테스트 : 회사의 웹 사이트의 다른 디자인을
                        테스트<br />
                      </td>
                    </tr>
                    <tr>
                      <td>기능 쿠키</td>
                      <td>
                        이 쿠키는 서비스를 제공하거나 방문을 개선하기 위해
                        설정을 기억하는 데 사용됩니다. 이 쿠키로 수집된 정보는
                        이용자를 개별적으로 파악하지 않습니다. <br />
                        (기능 쿠키의 예시)<br />
                        ∘ 레이아웃, 텍스트 크기, 기본 설정, 색상 등과 같이
                        적용한 설정을 기억<br />
                        ∘ 회사의 설문 조사에 고객이 응하는 경우 이를 기억<br />
                      </td>
                    </tr>
                    <tr>
                      <td>대상 쿠키</td>
                      <td>
                        이 쿠키는 '좋아요' 버튼 및 '공유' 버튼과 같은 제 3 자가
                        제공하는 서비스와 연결됩니다. 제 3 자는 이용자가 회사의
                        웹사이트를 방문한 것을 인지하여 이러한 서비스를
                        제공합니다. <br />
                        (대상 쿠키의 예시) <br />
                        ∘ 소셜 네트워크로 연결하여, 해당 소셜 네트워크가
                        이용자의 방문 정보를 사용하여 나중에 다른 웹사이트에서
                        이용자를 대상으로 홍보<br />
                        ∘ 이용자가 관심이 있을 수 있는 광고를 제시할 수 있도록
                        이용자 방문정보를 광고 대행사에 제공<br />
                      </td>
                    </tr>
                  </table>
                  <p class="policy_text">&lt;6&gt; 보안조치</p>
                  <p class="policy_text">
                    • 개인정보의 암호화 <br />
                    - 이용자의 개인정보를 암호화된 통신구간을 이용하여 전송<br />
                    - 비밀번호 등 중요정보는 암호화하여 보관<br />
                    • 해킹 등에 대비한 대책 <br />
                    - 해킹이나 컴퓨터 바이러스 등에 의해 이용자의 개인정보가
                    유출되거나 훼손되는 것을 막기 위해 외부로부터 접근이 통제된
                    구역에 시스템을 설치 <br />
                    • 내부관리계획의 수립 및 시행<br />
                    • 접근통제장치의 설치 및 운영 <br />
                    • 접속기록의 위조, 변조 방지를 위한 조치<br />
                  </p>
                  <p class="policy_text">&lt;7&gt; 데이터 전송</p>
                  <p class="policy_text">
                    회사는 전 세계를 무대로 영업함으로 본 개인정보취급방침에
                    명시된 목적을 위해 타국에 위치한 회사나 타사에 이용자의
                    개인정보를 제공할 수 있습니다. 개인정보가 전송, 보유 또는
                    처리되는 곳에 대해서는 회사가 개인정보 보호를 위한 합당한
                    조치를 취합니다.
                  </p>
                  <p class="policy_text">
                    (US 사용인 경우 추가 가능) 또한, 유럽연합에서 얻은
                    개인정보를 사용 또는 공개 시 회사는 미국 상무부에서 정한
                    세이프 하버 원칙을 준수하거나 유럽연합 집행기관에서 승인한
                    표준 계약 조항 사용, 또는 적절한 안전장치 보장을 위해
                    유럽연합 규정 내에서 다른 방안을 강구하거나 이용자의 동의를
                    구합니다.
                  </p>
                  <p class="policy_text">&lt;8&gt; 제 3 자 사이트 및 서비스</p>
                  <p class="policy_text">
                    회사의 웹 사이트, 제품, 서비스 등은 제 3 자의 웹사이트,
                    제품, 서비스 등의 링크를 포함할 수 있습니다. 링크된 제 3 자
                    사이트의 개인정보취급방침이 회사의 정책과 다룰 수 있습니다.
                    따라서 이용자들은 링크된 제 3 자 사이트의 개인정보취급방침을
                    추가적으로 검토하셔야 합니다.
                  </p>
                  <p class="policy_text">
                    &lt;9&gt; 캘리포니아 거주자에 대한 안내
                  </p>
                  <p class="policy_text">
                    캘리포니아에 거주하시는 분이라면 특정 권리사항이 추가될 수
                    있습니다. 회사는 캘리포니아 온라인 프라이버시 보호법을
                    준수하기 위해 회원의 개인정보를 보호하기 위해 필요한
                    예방책을 마련합니다.
                  </p>
                  <p class="policy_text">
                    이용자는 개인정보가 누출되었을 경우 정보유출 확인을 요청할
                    수 있습니다. 또한 회사 웹사이트의 모든 이용자는 개인 계정에
                    접속하여 정보 수정 메뉴를 이용하여 언제든지 정보를 변경할 수
                    있습니다.
                  </p>
                  <p class="policy_text">
                    또한 회사는 웹 사이트 방문자를 추적하지 않습니다. 또한 '추적
                    방지' 신호도 사용하지 않습니다. 회사는 이용자의 동의 없이
                    광고 서비스를 통해 개인 식별 정보를 수집하고 타사에 제공하지
                    않습니다.
                  </p>
                  <p class="policy_text">
                    &lt;10&gt; 한국인 거주자에 대한 안내
                  </p>
                  <p class="policy_text">
                    회사는 대한민국 정보통신망법 및 개인정보보호법이 요구하는 몇
                    가지 추가 공개 사항을 다음과 같이 안내합니다.
                  </p>
                  <p class="policy_text">
                    (1) 수집하는 정보 <br />
                    회사가 수집하는 개인정보의 항목은 다음과 같습니다.
                    <br />
                    • 필수항목 예시
                  </p>
                  <table class="policy_table">
                    <tr class="table_title">
                      <th>서비스명</th>
                      <th>수집 항목(예시)</th>
                    </tr>
                    <tr>
                      <td>인터넷 회원제 서비스</td>
                      <td>
                        ∘ 이름, 이메일 주소, ID, 전화번호, 우편주소, 국가정보,
                        암호화된 동일인 식별정보(CI), 중복가입확인정보(DI) 등
                        <br />∘ 미성년자인 경우 법정대리인 정보(법정대리인의
                        이름, 생년월일, CI, DI 등)
                      </td>
                    </tr>
                    <tr>
                      <td>온라인 결제 서비스</td>
                      <td>
                        ∘ 이름, 주소, 전화 번호, 이메일 주소 등<br />
                        ∘ 신용카드 결제시 : 카드사 명, 카드번호, 카드유효기간
                        등<br />
                        ∘ 이동전화 소액결제시 : 이동전화번호, 결제승인번호 등<br />
                        ∘ 계좌이체 결제시 : 은행명, 계좌번호, 계좌비밀번호 등<br />
                        ∘ 무통장 입금시 : 송금인명, 연락처등<br />
                        ∘ 배송 주소지, 수령인 이름, 수령인 연락처 등의
                        배송정보<br />
                        ∘ 입찰, 구매, 판매 등 정보<br />
                      </td>
                    </tr>
                    <tr>
                      <td>소셜 네트워크 서비스</td>
                      <td>
                        ∘ 이름, 이메일 주소, ID, 전화 번호, 우편주소, 국가정보,
                        주소록(지인) 등<br />
                        ∘ 사진 촬영 장소, 파일 생성 날짜 등 정보<br />
                        ∘ 회원이 보거나 이용하는 콘텐츠의 유형, 회원의 활동
                        빈도나 기간 등 회원의 서비스 이용에 관한 정보<br />
                      </td>
                    </tr>
                    <tr>
                      <td class="policy_left" colspan="2">
                        서비스 이용과정에서 아래와 같은 정보들이 자동으로
                        생성되어 수집될 수 있습니다.<br />
                        ∘ 기기정보(기기 식별자, 운영 체제, 하드웨어 버전, 기기
                        설정, 전화번호 등)<br />
                        ∘ 로그정보(로그데이터, 이용시간, 이용자가 입력한 검색어,
                        인터넷 프로토콜 주소, 쿠키 및 웹비콘 등)<br />
                        ∘ 위치정보(GPS, 블루투스 또는 와이파이 신호를 통한
                        구체적인 지리적 위치를 포함한 기기 위치에 대한 정보
                        등)<br />
                        ∘ 기타 생성정보<br />
                      </td>
                    </tr>
                  </table>
                  <p class="policy_text">
                    • 선택항목 예시 <br />
                    이용자는 선택항목 수집 및 이용에 동의를 거부하실 수 있으며,
                    동의를 거부하시더라도 서비스 이용에 제한은 없습니다.
                  </p>
                  <table class="policy_table">
                    <tr class="table_title">
                      <th>수집 목적</th>
                      <th>수집 항목(예시)</th>
                    </tr>
                    <tr>
                      <td>이용자 분석</td>
                      <td>
                        ∘ 가입하신 사유, 직업, 결혼여부, 결혼기념일, 관심
                        카테고리, SNS 계정정보 등
                      </td>
                    </tr>
                    <tr>
                      <td>맞춤화된 광고의 제공</td>
                      <td>
                        ∘ 마케팅활동 내용 및 결과, 이벤트참여 내용 및 결과 등
                      </td>
                    </tr>
                    <tr>
                      <td>급한 고지사항 전달</td>
                      <td>
                        ∘ 타 계약의 체결ᆞ유지ᆞ이행ᆞ관리ᆞ행사참여 등과 관련하여
                        이용자가 제공한 정보
                      </td>
                    </tr>
                    <tr>
                      <td>마케팅</td>
                      <td>
                        ∘ 이용자의 서비스 사용에 있어 선호도, 광고 환경,
                        방문하는 페이지 등
                      </td>
                    </tr>
                  </table>
                  <p class="policy_text">
                    • (민감정보 수집의 경우 추가) 민감정보 예시 <br />
                    회사는 민감정보의 수집이 반드시 필요할 경우에는 관련 법령에
                    따라 적법한 절차를 거쳐서 수집합니다. 회사가 수집하는
                    민감정보는 다음과 같습니다.
                  </p>
                  <p class="policy_text">
                    ∘ 사상·신념<br />
                    ∘ 노동조합·정당의 가입·탈퇴<br />
                    ∘ 정치적 견해 <br />
                    ∘ 건강, 성생활 등에 관한 정보<br />
                    ∘ 유전자검사 등의 결과로 얻어진 유전정보
                    <br />
                    ∘ 형의 선고·면제 및 선고유예, 보호감호, 치료감호, 보호관찰,
                    선고유예의 실효, 집행유예의 취소 등 범죄경력에 관한 정보<br />
                  </p>
                  <p class="policy_text">
                    (2) 수집한 개인정보의 위탁 <br />
                    회사는 서비스 이행을 위해 아래와 같이 개인정보 처리 업무를
                    외부 전문업체에 위탁하여 처리하고 있습니다. 개인정보
                    처리위탁은 개별 서비스 별로 그 이행을 위해 필요한 경우에
                    한해 각 위탁업체에 대해 이루어집니다.<br />
                    회사가 개인정보의 처리를 위탁하는 경우에는 개인정보 보호의
                    안전을 기하기 위하여 개인정보보호 관련 지시 엄수, 개인정보에
                    대한 비밀유지, 제 3 자 제공의 금지 및 사고시의 책임부담,
                    위탁기간, 처리 종료 후의 개인정보의 반환 또는 파기 등을
                    명확히 규정하고, 위탁업체가 개인정보를 안전하게 처리하도록
                    감독합니다.
                  </p>
                  <table class="policy_table">
                    <tr class="table_title">
                      <th>수탁업체의 명칭</th>
                      <th>위탁하는 업무(서비스)의 내용</th>
                    </tr>
                    <tr>
                      <td>AAA</td>
                      <td>고객상담</td>
                    </tr>
                  </table>
                  <p class="policy_text">
                    (3) 개인정보의 제 3 자 제공에 대한 세부사항 <br />
                    회사는 아래의 경우를 제외하고 이용자의 개인정보를 제 3
                    자에게 공개하거나 제공하지 않습니다.
                  </p>
                  <table class="policy_table">
                    <tr class="table_title">
                      <th>제공 받는 자</th>
                      <th>제공 받는 자의 이용목적</th>
                      <th>제공 항목</th>
                      <th>제공받는 자의 보유 및 이용기간</th>
                    </tr>
                    <tr>
                      <td>BBB</td>
                      <td>제휴 서비스 제공</td>
                      <td>ID, 이름, 나이</td>
                      <td>목적이 달성시까지 또는 법이 요구하는 기간까지</td>
                    </tr>
                  </table>
                  <p class="policy_text">
                    (4) 개인정보의 보유 및 이용기간<br />
                    회사는 이용자의 개인정보의 수집 및 이용 목적이 달성되는
                    경우, 개인정보에 대한 법적∙경영적 필요가 해소되는 경우, 또는
                    이용자가 요청하는 경우, 이용자의 개인정보를 지체 없이
                    파기합니다. 다만 관계법령의 규정에 의하여 보존할 필요가 있는
                    경우 회사는 관계법령에서 정한 일정한 기간 동안 회원정보를
                    보관합니다. 관계 법령에 따라 보관해야 하는 정보는 다음과
                    같습니다.
                  </p>
                  <div class="policy_box">
                    <p class="policy_box_text">
                      ∘ 계약 또는 청약철회 등에 관련 기록: 5 년(전자상거래
                      등에서의 소비자보호에 관한 법률)<br />
                      ∘ 대금결제 및 재화 등의 공급에 관한 기록: 5 년 (전자상거래
                      등에서의 소비자보호에 관한 법률) <br />
                      ∘ 소비자의 불만 또는 분쟁처리에 관한 기록: 3 년
                      (전자상거래 등에서의 소비자보호에 관한 법률)<br />
                      ∘ 신용정보의 수집/처리 및 이용 등에 관한 기록: 3 년
                      (신용정보의 이용 및 보호에 관한 법률)<br />
                      ∘ 표시/광고에 관한 기록: 6 개월 (전자상거래 등에서의
                      소비자보호에 관한 법률)<br />
                      ∘ 이용자의 인터넷 등 로그기록/이용자의 접속지 추적자료: 3
                      개월 (통신비밀보호법)<br />
                      ∘ 그 외의 통신사실 확인자료: 12 개월 (통신비밀보호법)<br />
                    </p>
                  </div>
                  <p class="policy_text">
                    (5) 개인정보의 파기 절차 및 파기방법 <br />
                    회사는 원칙적으로 개인정보 수집 및 이용목적이 달성된 후에는
                    해당 정보를 지체 없이 파기합니다. 다만 관계법령에 의해
                    보관해야 하는 정보는 법령이 정한 기간 동안 보관한 후
                    파기합니다. 이때 별도로 저장 관리되는 개인정보는 법령에 정한
                    경우가 아니고서는 절대 다른 용도로 이용되지 않습니다. 개인
                    정보가 수록된 종이 기록은 파쇄 또는 소각하고, 전자 파일에
                    저장된 개인 정보는 기술적으로 복원이 불가능한 방법을
                    이용하여 삭제합니다.
                  </p>
                  <p class="policy_text">
                    (6) 개인정보 보호를 위한 기술적, 관리적, 물리적 조치 <br />
                    회사는 이용자의 개인정보를 취급함에 있어 개인정보가 분실,
                    도난, 누출, 변조 또는 훼손되지 않도록 안전성 확보를 위하여
                    다음과 같은 기술적, 관리적, 물리적 조치를 강구하고 있습니다.
                  </p>
                  <table class="policy_table">
                    <tr class="table_title">
                      <th>항목</th>
                      <th>예시</th>
                    </tr>
                    <tr>
                      <td>기술적 조치</td>
                      <td>
                        ∘ 개인정보 암호화 전송을 위한 보안서버 활용<br />∘
                        비밀정보 암호화 조치<br />∘ 접근통제장치의 설치 및
                        운영<br />∘ 내부관리계획의 수립 및 시행
                      </td>
                    </tr>
                    <tr>
                      <td>관리적 조치</td>
                      <td>
                        ∘ 개인정보 보호 책임자 지적<br />
                        ∘ 개인정보취급자 교육<br />
                        ∘ 내부관리계획의 수립 및 시행<br />
                        ∘ 추측하기 어려운 비밀번호 작성 규칙 수립<br />
                        ∘ 개인정보처리시스템에 대한 접근기록의 안전한 보관<br />
                        ∘ 개인정보처리시스템에 대한 접근권한 차별화<br />
                      </td>
                    </tr>
                    <tr>
                      <td>물리적 조치</td>
                      <td>
                        ∘ 개인정보를 보관 시설에 대한 출입통제 절차 수립 및 운영
                        <br />
                        ∘ 개인정보가 포함된 서류나 보조기억매체 등은 잠금장치가
                        부착되어 있는 안전한 장소에 보관
                      </td>
                    </tr>
                  </table>
                </div>
                <div @click="closeModal" class="modal_wrap"></div>
              </div>
            </div>
            <div class="submit-wrap">
              <button id="submitBtn" class="contact_button">제출</button>
            </div>
          </div>
        </form>
      </div>
    </section>
  </div>
  {{< home_footer_sub_kr >}}
</body>
<script>
  const fullNameInput = document.getElementById("fullName");
  const emailAddressInput = document.getElementById("emailAddress");
  const countrySelect = document.getElementById("countrySelect");
  const helpText = document.getElementById("helpText");
  const privacyCheckbox = document.getElementById("privacyCheckbox");
  const submitButton = document.getElementById("submitBtn");
  function validateEmail(email) {
    const re =
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
  }
  function validateForm() {
    const fullName = document.getElementById("fullName");
    const email = document.getElementById("emailAddress");
    const country = document.getElementById("countrySelect");
    const message = document.getElementById("helpText");
    const privacyPolicy = document.getElementById("privacyCheckbox");
    const radios = document.getElementsByClassName("radio-input");
    var why = "";
    for (var i = 0; i < radios.length; i++) {
      if (radios[i].checked) {
        why = radios[i].value;
        break;
      }
    }
    if (!fullName.value) {
      alert("성함을 입력해주세요.");
      return false;
    }
    if (!email.value) {
      alert("E-mail을 입력해주세요.");
      return false;
    }
    if (!validateEmail(email.value)) {
      alert("Email형식이 유효하지 않습니다.");
      return false;
    }
    if (!country.value) {
      alert("국가를 선택해주세요");
      return false;
    }
    if (why === "" || why === undefined) {
      alert("문의 유형을 선택해주세요");
      return false;
    }
    if (!message.value) {
      alert("문의 내용을 입력해주세요.");
      return false;
    }
    if (!privacyPolicy.checked) {
      alert("개인정보처리방침에 동의해주세요");
      return false;
    }
    alert("감사합니다.");
    return true;
  }
  submitButton.addEventListener("click", function (event) {
    const contactForm = document.getElementById("contactForm");
    event.preventDefault();
    if (validateForm()) {
      contactForm.submit();
    }
  });
  const openModalBtn = document.getElementById("openModalBtn");
  const modal = document.getElementById("modalDiv");
  const closeModalBtn = document.getElementById("closeModalBtn");
  openModalBtn.addEventListener("click", function () {
    modal.style.display = "block";
  });
  closeModalBtn.addEventListener("click", function () {
    modal.style.display = "none";
  });
  window.addEventListener("click", function (event) {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });
  const countries = {
    KR: {
      "2digitCode": "KR",
      "3digitCode": "KOR",
      ISONumbericCode: 410,
      CountryNameKR: "대한민국",
      CountryNameEN: "KOREA, REPUBLIC OF",
      CountryNameOriginal: "한국",
    },
    AF: {
      "2digitCode": "AF",
      "3digitCode": "AFG",
      ISONumbericCode: 4,
      CountryNameKR: "아프가니스탄",
      CountryNameEN: "AFGHANISTAN",
      CountryNameOriginal: "افغانستان",
    },
    AL: {
      "2digitCode": "AL",
      "3digitCode": "ALB",
      ISONumbericCode: 8,
      CountryNameKR: "알바니아",
      CountryNameEN: "ALBANIA",
      CountryNameOriginal: "Shqipëria",
    },
    AQ: {
      "2digitCode": "AQ",
      "3digitCode": "ATA",
      ISONumbericCode: 10,
      CountryNameKR: "남극",
      CountryNameEN: "ANTARCTICA",
      CountryNameOriginal: "Antarctica",
    },
    DZ: {
      "2digitCode": "DZ",
      "3digitCode": "DZA",
      ISONumbericCode: 12,
      CountryNameKR: "알제리",
      CountryNameEN: "ALGERIA",
      CountryNameOriginal: "الجزائر",
    },
    AS: {
      "2digitCode": "AS",
      "3digitCode": "ASM",
      ISONumbericCode: 16,
      CountryNameKR: "아메리칸사모아",
      CountryNameEN: "AMERICAN SAMOA",
      CountryNameOriginal: "American Samoa",
    },
    AD: {
      "2digitCode": "AD",
      "3digitCode": "AND",
      ISONumbericCode: 20,
      CountryNameKR: "안도라",
      CountryNameEN: "ANDORRA",
      CountryNameOriginal: "Andorra",
    },
    AO: {
      "2digitCode": "AO",
      "3digitCode": "AGO",
      ISONumbericCode: 24,
      CountryNameKR: "앙골라",
      CountryNameEN: "ANGOLA",
      CountryNameOriginal: "Angola",
    },
    AG: {
      "2digitCode": "AG",
      "3digitCode": "ATG",
      ISONumbericCode: 28,
      CountryNameKR: "앤티가 바부다",
      CountryNameEN: "ANTIGUA AND BARBUDA",
      CountryNameOriginal: "Antigua and Barbuda",
    },
    AZ: {
      "2digitCode": "AZ",
      "3digitCode": "AZE",
      ISONumbericCode: 31,
      CountryNameKR: "아제르바이잔",
      CountryNameEN: "AZERBAIJAN",
      CountryNameOriginal: "Azərbaycan",
    },
    AR: {
      "2digitCode": "AR",
      "3digitCode": "ARG",
      ISONumbericCode: 32,
      CountryNameKR: "아르헨티나",
      CountryNameEN: "ARGENTINA",
      CountryNameOriginal: "Argentina",
    },
    AU: {
      "2digitCode": "AU",
      "3digitCode": "AUS",
      ISONumbericCode: 36,
      CountryNameKR: "오스트레일리아",
      CountryNameEN: "AUSTRALIA",
      CountryNameOriginal: "Australia",
    },
    AT: {
      "2digitCode": "AT",
      "3digitCode": "AUT",
      ISONumbericCode: 40,
      CountryNameKR: "오스트리아",
      CountryNameEN: "AUSTRIA",
      CountryNameOriginal: "Österreich",
    },
    BS: {
      "2digitCode": "BS",
      "3digitCode": "BHS",
      ISONumbericCode: 44,
      CountryNameKR: "바하마",
      CountryNameEN: "BAHAMAS",
      CountryNameOriginal: "Bahamas",
    },
    BH: {
      "2digitCode": "BH",
      "3digitCode": "BHR",
      ISONumbericCode: 48,
      CountryNameKR: "바레인",
      CountryNameEN: "BAHRAIN",
      CountryNameOriginal: "البحرين",
    },
    BD: {
      "2digitCode": "BD",
      "3digitCode": "BGD",
      ISONumbericCode: 50,
      CountryNameKR: "방글라데시",
      CountryNameEN: "BANGLADESH",
      CountryNameOriginal: "বাংলাদেশ",
    },
    AM: {
      "2digitCode": "AM",
      "3digitCode": "ARM",
      ISONumbericCode: 51,
      CountryNameKR: "아르메니아",
      CountryNameEN: "ARMENIA",
      CountryNameOriginal: "Հայաստան",
    },
    BB: {
      "2digitCode": "BB",
      "3digitCode": "BRB",
      ISONumbericCode: 52,
      CountryNameKR: "바베이도스",
      CountryNameEN: "BARBADOS",
      CountryNameOriginal: "Barbados",
    },
    BE: {
      "2digitCode": "BE",
      "3digitCode": "BEL",
      ISONumbericCode: 56,
      CountryNameKR: "벨기에",
      CountryNameEN: "BELGIUM",
      CountryNameOriginal: "België",
    },
    BM: {
      "2digitCode": "BM",
      "3digitCode": "BMU",
      ISONumbericCode: 60,
      CountryNameKR: "버뮤다",
      CountryNameEN: "BERMUDA",
      CountryNameOriginal: "Bermuda",
    },
    BT: {
      "2digitCode": "BT",
      "3digitCode": "BTN",
      ISONumbericCode: 64,
      CountryNameKR: "부탄",
      CountryNameEN: "BHUTAN",
      CountryNameOriginal: "འབྲུག་ཡུལ",
    },
    BO: {
      "2digitCode": "BO",
      "3digitCode": "BOL",
      ISONumbericCode: 68,
      CountryNameKR: "볼리비아",
      CountryNameEN: "BOLIVIA",
      CountryNameOriginal: "Bolivia",
    },
    BA: {
      "2digitCode": "BA",
      "3digitCode": "BIH",
      ISONumbericCode: 70,
      CountryNameKR: "보스니아 헤르체고비나",
      CountryNameEN: "BOSNIA HERCEGOVINA",
      CountryNameOriginal: "Bosna i Hercegovina",
    },
    BW: {
      "2digitCode": "BW",
      "3digitCode": "BWA",
      ISONumbericCode: 72,
      CountryNameKR: "보츠와나",
      CountryNameEN: "BOTSWANA",
      CountryNameOriginal: "Botswana",
    },
    BV: {
      "2digitCode": "BV",
      "3digitCode": "BVT",
      ISONumbericCode: 74,
      CountryNameKR: "부베 섬",
      CountryNameEN: "BOUVET ISLAND",
      CountryNameOriginal: "Bouvet Island",
    },
    BR: {
      "2digitCode": "BR",
      "3digitCode": "BRA",
      ISONumbericCode: 76,
      CountryNameKR: "브라질",
      CountryNameEN: "BRAZIL",
      CountryNameOriginal: "Brasil",
    },
    BZ: {
      "2digitCode": "BZ",
      "3digitCode": "BLZ",
      ISONumbericCode: 84,
      CountryNameKR: "벨리즈",
      CountryNameEN: "BELIZE",
      CountryNameOriginal: "Belize",
    },
    IO: {
      "2digitCode": "IO",
      "3digitCode": "IOT",
      ISONumbericCode: 86,
      CountryNameKR: "영국령 인도양 지역",
      CountryNameEN: "BRITISH INDIAN OCEAN TERRITORY",
      CountryNameOriginal: "British Indian Ocean Territory",
    },
    SB: {
      "2digitCode": "SB",
      "3digitCode": "SLB",
      ISONumbericCode: 90,
      CountryNameKR: "솔로몬 제도",
      CountryNameEN: "SOLOMON ISLANDS",
      CountryNameOriginal: "Solomon Islands",
    },
    VG: {
      "2digitCode": "VG",
      "3digitCode": "VGB",
      ISONumbericCode: 92,
      CountryNameKR: "영국령 버진아일랜드",
      CountryNameEN: "VIRGIN ISLANDS, BRITISH",
      CountryNameOriginal: "Virgin Islands, British",
    },
    BN: {
      "2digitCode": "BN",
      "3digitCode": "BRN",
      ISONumbericCode: 96,
      CountryNameKR: "브루나이",
      CountryNameEN: "BRUNEI DARUSSALAM",
      CountryNameOriginal: "Brunei Darussalam",
    },
    BG: {
      "2digitCode": "BG",
      "3digitCode": "BGR",
      ISONumbericCode: 100,
      CountryNameKR: "불가리아",
      CountryNameEN: "BULGARIA",
      CountryNameOriginal: "България",
    },
    MM: {
      "2digitCode": "MM",
      "3digitCode": "MMR",
      ISONumbericCode: 104,
      CountryNameKR: "미얀마",
      CountryNameEN: "MYANMAR",
      CountryNameOriginal: "Myanmar(Burma)",
    },
    BI: {
      "2digitCode": "BI",
      "3digitCode": "BDI",
      ISONumbericCode: 108,
      CountryNameKR: "부룬디",
      CountryNameEN: "BURUNDI",
      CountryNameOriginal: "Uburundi",
    },
    BY: {
      "2digitCode": "BY",
      "3digitCode": "BLR",
      ISONumbericCode: 112,
      CountryNameKR: "벨라루스",
      CountryNameEN: "BELARUS",
      CountryNameOriginal: "Белару́сь",
    },
    KH: {
      "2digitCode": "KH",
      "3digitCode": "KHM",
      ISONumbericCode: 116,
      CountryNameKR: "캄보디아",
      CountryNameEN: "CAMBODIA",
      CountryNameOriginal: "Kampuchea",
    },
    CM: {
      "2digitCode": "CM",
      "3digitCode": "CMR",
      ISONumbericCode: 120,
      CountryNameKR: "카메룬",
      CountryNameEN: "CAMEROON",
      CountryNameOriginal: "Cameroun",
    },
    CA: {
      "2digitCode": "CA",
      "3digitCode": "CAN",
      ISONumbericCode: 124,
      CountryNameKR: "캐나다",
      CountryNameEN: "CANADA",
      CountryNameOriginal: "Canada",
    },
    CV: {
      "2digitCode": "CV",
      "3digitCode": "CPV",
      ISONumbericCode: 132,
      CountryNameKR: "카보베르데",
      CountryNameEN: "CAPE VERDE",
      CountryNameOriginal: "Cabo Verde",
    },
    KY: {
      "2digitCode": "KY",
      "3digitCode": "CYM",
      ISONumbericCode: 136,
      CountryNameKR: "케이맨 제도",
      CountryNameEN: "CAYMAN ISLANDS",
      CountryNameOriginal: "Cayman Islands",
    },
    CF: {
      "2digitCode": "CF",
      "3digitCode": "CAF",
      ISONumbericCode: 140,
      CountryNameKR: "중앙아프리카 공화국",
      CountryNameEN: "CENTRAL AFRICAN REPUBLIC",
      CountryNameOriginal: "République Centrafricaine",
    },
    LK: {
      "2digitCode": "LK",
      "3digitCode": "LKA",
      ISONumbericCode: 144,
      CountryNameKR: "스리랑카",
      CountryNameEN: "SRI LANKA",
      CountryNameOriginal: "Sri Lanka",
    },
    TD: {
      "2digitCode": "TD",
      "3digitCode": "TCD",
      ISONumbericCode: 148,
      CountryNameKR: "차드",
      CountryNameEN: "CHAD",
      CountryNameOriginal: "Tchad",
    },
    CL: {
      "2digitCode": "CL",
      "3digitCode": "CHL",
      ISONumbericCode: 152,
      CountryNameKR: "칠레",
      CountryNameEN: "CHILE",
      CountryNameOriginal: "Chile",
    },
    CN: {
      "2digitCode": "CN",
      "3digitCode": "CHN",
      ISONumbericCode: 156,
      CountryNameKR: "중화인민공화국",
      CountryNameEN: "CHINA",
      CountryNameOriginal: "中国",
    },
    TW: {
      "2digitCode": "TW",
      "3digitCode": "TWN",
      ISONumbericCode: 158,
      CountryNameKR: "중화민국",
      CountryNameEN: "TAIWAN",
      CountryNameOriginal: "台灣",
    },
    CX: {
      "2digitCode": "CX",
      "3digitCode": "CXR",
      ISONumbericCode: 162,
      CountryNameKR: "크리스마스 섬",
      CountryNameEN: "CHRISTMAS ISLAND",
      CountryNameOriginal: "Christmas Island",
    },
    CC: {
      "2digitCode": "CC",
      "3digitCode": "CCK",
      ISONumbericCode: 166,
      CountryNameKR: "코코스 제도",
      CountryNameEN: "COCOS ISLANDS",
      CountryNameOriginal: "Cocos Islands",
    },
    CO: {
      "2digitCode": "CO",
      "3digitCode": "COL",
      ISONumbericCode: 170,
      CountryNameKR: "콜롬비아",
      CountryNameEN: "COLOMBIA",
      CountryNameOriginal: "Colombia",
    },
    KM: {
      "2digitCode": "KM",
      "3digitCode": "COM",
      ISONumbericCode: 174,
      CountryNameKR: "코모로",
      CountryNameEN: "COMOROS",
      CountryNameOriginal: "Comores",
    },
    YT: {
      "2digitCode": "YT",
      "3digitCode": "MYT",
      ISONumbericCode: 175,
      CountryNameKR: "마요트",
      CountryNameEN: "MAYOTTE",
      CountryNameOriginal: "Mayotte",
    },
    CG: {
      "2digitCode": "CG",
      "3digitCode": "COG",
      ISONumbericCode: 178,
      CountryNameKR: "콩고 공화국",
      CountryNameEN: "CONGO",
      CountryNameOriginal: "Congo",
    },
    CD: {
      "2digitCode": "CD",
      "3digitCode": "COD",
      ISONumbericCode: 180,
      CountryNameKR: "콩고 민주 공화국",
      CountryNameEN: "DEMOCRATIC REPUBLIC OF THE CONGO",
      CountryNameOriginal: "Congo, Democratic Republic of the",
    },
    CK: {
      "2digitCode": "CK",
      "3digitCode": "COK",
      ISONumbericCode: 184,
      CountryNameKR: "쿡 제도",
      CountryNameEN: "COOK ISLANDS",
      CountryNameOriginal: "Cook Islands",
    },
    CR: {
      "2digitCode": "CR",
      "3digitCode": "CRI",
      ISONumbericCode: 188,
      CountryNameKR: "코스타리카",
      CountryNameEN: "COSTA RICA",
      CountryNameOriginal: "Costa Rica",
    },
    HR: {
      "2digitCode": "HR",
      "3digitCode": "HRV",
      ISONumbericCode: 191,
      CountryNameKR: "크로아티아",
      CountryNameEN: "CROATIA",
      CountryNameOriginal: "Hrvatska",
    },
    CU: {
      "2digitCode": "CU",
      "3digitCode": "CUB",
      ISONumbericCode: 192,
      CountryNameKR: "쿠바",
      CountryNameEN: "CUBA",
      CountryNameOriginal: "Cuba",
    },
    CY: {
      "2digitCode": "CY",
      "3digitCode": "CYP",
      ISONumbericCode: 196,
      CountryNameKR: "키프로스",
      CountryNameEN: "CYPRUS",
      CountryNameOriginal: "Κυπρος",
    },
    CZ: {
      "2digitCode": "CZ",
      "3digitCode": "CZE",
      ISONumbericCode: 203,
      CountryNameKR: "체코",
      CountryNameEN: "CZECH REPUBLIC",
      CountryNameOriginal: "Česko",
    },
    BJ: {
      "2digitCode": "BJ",
      "3digitCode": "BEN",
      ISONumbericCode: 204,
      CountryNameKR: "베냉",
      CountryNameEN: "BENIN",
      CountryNameOriginal: "Bénin",
    },
    DK: {
      "2digitCode": "DK",
      "3digitCode": "DNK",
      ISONumbericCode: 208,
      CountryNameKR: "덴마크",
      CountryNameEN: "DENMARK",
      CountryNameOriginal: "Danmark",
    },
    DM: {
      "2digitCode": "DM",
      "3digitCode": "DMA",
      ISONumbericCode: 212,
      CountryNameKR: "도미니카 연방",
      CountryNameEN: "DOMINICA",
      CountryNameOriginal: "Dominica",
    },
    DO: {
      "2digitCode": "DO",
      "3digitCode": "DOM",
      ISONumbericCode: 214,
      CountryNameKR: "도미니카 공화국",
      CountryNameEN: "DOMINICAN REPUBLIC",
      CountryNameOriginal: "Dominican Republic",
    },
    EC: {
      "2digitCode": "EC",
      "3digitCode": "ECU",
      ISONumbericCode: 218,
      CountryNameKR: "에콰도르",
      CountryNameEN: "ECUADOR",
      CountryNameOriginal: "Ecuador",
    },
    SV: {
      "2digitCode": "SV",
      "3digitCode": "SLV",
      ISONumbericCode: 222,
      CountryNameKR: "엘살바도르",
      CountryNameEN: "EL SALVADOR",
      CountryNameOriginal: "El Salvador",
    },
    GQ: {
      "2digitCode": "GQ",
      "3digitCode": "GNQ",
      ISONumbericCode: 226,
      CountryNameKR: "적도 기니",
      CountryNameEN: "EQUATORIAL GUINEA",
      CountryNameOriginal: "Guinea Ecuatorial",
    },
    ET: {
      "2digitCode": "ET",
      "3digitCode": "ETH",
      ISONumbericCode: 231,
      CountryNameKR: "에티오피아",
      CountryNameEN: "ETHIOPIA",
      CountryNameOriginal: "Ityop'iya",
    },
    ER: {
      "2digitCode": "ER",
      "3digitCode": "ERI",
      ISONumbericCode: 232,
      CountryNameKR: "에리트레아",
      CountryNameEN: "ERITREA",
      CountryNameOriginal: "Ertra",
    },
    EE: {
      "2digitCode": "EE",
      "3digitCode": "EST",
      ISONumbericCode: 233,
      CountryNameKR: "에스토니아",
      CountryNameEN: "ESTONIA",
      CountryNameOriginal: "Eesti",
    },
    FO: {
      "2digitCode": "FO",
      "3digitCode": "FRO",
      ISONumbericCode: 234,
      CountryNameKR: "페로 제도",
      CountryNameEN: "FAROE ISLANDS",
      CountryNameOriginal: "Faroe Islands",
    },
    FK: {
      "2digitCode": "FK",
      "3digitCode": "FLK",
      ISONumbericCode: 238,
      CountryNameKR: "포클랜드 제도",
      CountryNameEN: "FALKLAND ISLANDS",
      CountryNameOriginal: "Falkland Islands",
    },
    GS: {
      "2digitCode": "GS",
      "3digitCode": "SGS",
      ISONumbericCode: 239,
      CountryNameKR: "사우스조지아 사우스샌드위치 제도",
      CountryNameEN: "SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS",
      CountryNameOriginal: "South Georgia and the South Sandwich Islands",
    },
    FJ: {
      "2digitCode": "FJ",
      "3digitCode": "FJI",
      ISONumbericCode: 242,
      CountryNameKR: "피지",
      CountryNameEN: "FIJI",
      CountryNameOriginal: "Fiji",
    },
    FI: {
      "2digitCode": "FI",
      "3digitCode": "FIN",
      ISONumbericCode: 246,
      CountryNameKR: "핀란드",
      CountryNameEN: "FINLAND",
      CountryNameOriginal: "Suomi",
    },
    AX: {
      "2digitCode": "AX",
      "3digitCode": "ALA",
      ISONumbericCode: 248,
      CountryNameKR: "올란드 제도",
      CountryNameEN: "ALAND ISLANDS",
      CountryNameOriginal: "Aland Islands",
    },
    FR: {
      "2digitCode": "FR",
      "3digitCode": "FRA",
      ISONumbericCode: 250,
      CountryNameKR: "프랑스",
      CountryNameEN: "FRANCE",
      CountryNameOriginal: "France",
    },
    GF: {
      "2digitCode": "GF",
      "3digitCode": "GUF",
      ISONumbericCode: 254,
      CountryNameKR: "프랑스령 기아나",
      CountryNameEN: "FRENCH GUIANA",
      CountryNameOriginal: "French Guiana",
    },
    PF: {
      "2digitCode": "PF",
      "3digitCode": "PYF",
      ISONumbericCode: 258,
      CountryNameKR: "프랑스령 폴리네시아",
      CountryNameEN: "FRENCH POLYNESIA",
      CountryNameOriginal: "French Polynesia",
    },
    TF: {
      "2digitCode": "TF",
      "3digitCode": "ATF",
      ISONumbericCode: 260,
      CountryNameKR: "프랑스령 남부와 남극 지역",
      CountryNameEN: "FRENCH SOUTHERN TERRITORIES",
      CountryNameOriginal: "French Southern Territories",
    },
    DJ: {
      "2digitCode": "DJ",
      "3digitCode": "DJI",
      ISONumbericCode: 262,
      CountryNameKR: "지부티",
      CountryNameEN: "DJIBOUTI",
      CountryNameOriginal: "Djibouti",
    },
    GA: {
      "2digitCode": "GA",
      "3digitCode": "GAB",
      ISONumbericCode: 266,
      CountryNameKR: "가봉",
      CountryNameEN: "GABON",
      CountryNameOriginal: "Gabon",
    },
    GE: {
      "2digitCode": "GE",
      "3digitCode": "GEO",
      ISONumbericCode: 268,
      CountryNameKR: "조지아",
      CountryNameEN: "GEORGIA",
      CountryNameOriginal: "საქართველო",
    },
    GM: {
      "2digitCode": "GM",
      "3digitCode": "GMB",
      ISONumbericCode: 270,
      CountryNameKR: "감비아",
      CountryNameEN: "GAMBIA",
      CountryNameOriginal: "Gambia",
    },
    PS: {
      "2digitCode": "PS",
      "3digitCode": "PSE",
      ISONumbericCode: 275,
      CountryNameKR: "팔레스타인",
      CountryNameEN: "PALESTINE",
      CountryNameOriginal: "Palestinian Territories",
    },
    DE: {
      "2digitCode": "DE",
      "3digitCode": "DEU",
      ISONumbericCode: 276,
      CountryNameKR: "독일",
      CountryNameEN: "GERMANY",
      CountryNameOriginal: "Deutschland",
    },
    GH: {
      "2digitCode": "GH",
      "3digitCode": "GHA",
      ISONumbericCode: 288,
      CountryNameKR: "가나",
      CountryNameEN: "GHANA",
      CountryNameOriginal: "Ghana",
    },
    GI: {
      "2digitCode": "GI",
      "3digitCode": "GIB",
      ISONumbericCode: 292,
      CountryNameKR: "지브롤터",
      CountryNameEN: "GIBRALTAR",
      CountryNameOriginal: "Gibraltar",
    },
    KI: {
      "2digitCode": "KI",
      "3digitCode": "KIR",
      ISONumbericCode: 296,
      CountryNameKR: "키리바시",
      CountryNameEN: "KIRIBATI",
      CountryNameOriginal: "Kiribati",
    },
    GR: {
      "2digitCode": "GR",
      "3digitCode": "GRC",
      ISONumbericCode: 300,
      CountryNameKR: "그리스",
      CountryNameEN: "GREECE",
      CountryNameOriginal: "Ελλάς",
    },
    GL: {
      "2digitCode": "GL",
      "3digitCode": "GRL",
      ISONumbericCode: 304,
      CountryNameKR: "그린란드",
      CountryNameEN: "GREENLAND",
      CountryNameOriginal: "Greenland",
    },
    GD: {
      "2digitCode": "GD",
      "3digitCode": "GRD",
      ISONumbericCode: 308,
      CountryNameKR: "그레나다",
      CountryNameEN: "GRENADA",
      CountryNameOriginal: "Grenada",
    },
    GP: {
      "2digitCode": "GP",
      "3digitCode": "GLP",
      ISONumbericCode: 312,
      CountryNameKR: "과들루프",
      CountryNameEN: "GUADELOUPE",
      CountryNameOriginal: "Guadeloupe",
    },
    GU: {
      "2digitCode": "GU",
      "3digitCode": "GUM",
      ISONumbericCode: 316,
      CountryNameKR: "괌",
      CountryNameEN: "GUAM",
      CountryNameOriginal: "Guam",
    },
    GT: {
      "2digitCode": "GT",
      "3digitCode": "GTM",
      ISONumbericCode: 320,
      CountryNameKR: "과테말라",
      CountryNameEN: "GUATEMALA",
      CountryNameOriginal: "Guatemala",
    },
    GN: {
      "2digitCode": "GN",
      "3digitCode": "GIN",
      ISONumbericCode: 324,
      CountryNameKR: "기니",
      CountryNameEN: "GUINEA",
      CountryNameOriginal: "Guinée",
    },
    GY: {
      "2digitCode": "GY",
      "3digitCode": "GUY",
      ISONumbericCode: 328,
      CountryNameKR: "가이아나",
      CountryNameEN: "GUYANA",
      CountryNameOriginal: "Guyana",
    },
    HT: {
      "2digitCode": "HT",
      "3digitCode": "HTI",
      ISONumbericCode: 332,
      CountryNameKR: "아이티",
      CountryNameEN: "HAITI",
      CountryNameOriginal: "Haïti",
    },
    HM: {
      "2digitCode": "HM",
      "3digitCode": "HMD",
      ISONumbericCode: 334,
      CountryNameKR: "허드 맥도널드 제도",
      CountryNameEN: "HEARD AND MC DONALD ISLANDS",
      CountryNameOriginal: "Heard Island and McDonald Islands",
    },
    VA: {
      "2digitCode": "VA",
      "3digitCode": "VAT",
      ISONumbericCode: 336,
      CountryNameKR: "바티칸 시국",
      CountryNameEN: "VATICAN CITY STATE",
      CountryNameOriginal: "Città del Vaticano",
    },
    HN: {
      "2digitCode": "HN",
      "3digitCode": "HND",
      ISONumbericCode: 340,
      CountryNameKR: "온두라스",
      CountryNameEN: "HONDURAS",
      CountryNameOriginal: "Honduras",
    },
    HK: {
      "2digitCode": "HK",
      "3digitCode": "HKG",
      ISONumbericCode: 344,
      CountryNameKR: "홍콩",
      CountryNameEN: "HONG KONG",
      CountryNameOriginal: "Hong Kong",
    },
    HU: {
      "2digitCode": "HU",
      "3digitCode": "HUN",
      ISONumbericCode: 348,
      CountryNameKR: "헝가리",
      CountryNameEN: "HUNGARY",
      CountryNameOriginal: "Magyarország",
    },
    IS: {
      "2digitCode": "IS",
      "3digitCode": "ISL",
      ISONumbericCode: 352,
      CountryNameKR: "아이슬란드",
      CountryNameEN: "ICELAND",
      CountryNameOriginal: "Ísland",
    },
    IN: {
      "2digitCode": "IN",
      "3digitCode": "IND",
      ISONumbericCode: 356,
      CountryNameKR: "인도",
      CountryNameEN: "INDIA",
      CountryNameOriginal: "India",
    },
    ID: {
      "2digitCode": "ID",
      "3digitCode": "IDN",
      ISONumbericCode: 360,
      CountryNameKR: "인도네시아",
      CountryNameEN: "INDONESIA",
      CountryNameOriginal: "Indonesia",
    },
    IR: {
      "2digitCode": "IR",
      "3digitCode": "IRN",
      ISONumbericCode: 364,
      CountryNameKR: "이란",
      CountryNameEN: "IRAN",
      CountryNameOriginal: "ایران",
    },
    IQ: {
      "2digitCode": "IQ",
      "3digitCode": "IRQ",
      ISONumbericCode: 368,
      CountryNameKR: "이라크",
      CountryNameEN: "IRAQ",
      CountryNameOriginal: "العراق",
    },
    IE: {
      "2digitCode": "IE",
      "3digitCode": "IRL",
      ISONumbericCode: 372,
      CountryNameKR: "아일랜드",
      CountryNameEN: "IRELAND",
      CountryNameOriginal: "Ireland",
    },
    IL: {
      "2digitCode": "IL",
      "3digitCode": "ISR",
      ISONumbericCode: 376,
      CountryNameKR: "이스라엘",
      CountryNameEN: "ISRAEL",
      CountryNameOriginal: "ישראל",
    },
    IT: {
      "2digitCode": "IT",
      "3digitCode": "ITA",
      ISONumbericCode: 380,
      CountryNameKR: "이탈리아",
      CountryNameEN: "ITALY",
      CountryNameOriginal: "Italia",
    },
    CI: {
      "2digitCode": "CI",
      "3digitCode": "CIV",
      ISONumbericCode: 384,
      CountryNameKR: "코트디부아르",
      CountryNameEN: "COTE D'IVOIRE",
      CountryNameOriginal: "Côte d'Ivoire",
    },
    JM: {
      "2digitCode": "JM",
      "3digitCode": "JAM",
      ISONumbericCode: 388,
      CountryNameKR: "자메이카",
      CountryNameEN: "JAMAICA",
      CountryNameOriginal: "Jamaica",
    },
    JP: {
      "2digitCode": "JP",
      "3digitCode": "JPN",
      ISONumbericCode: 392,
      CountryNameKR: "일본",
      CountryNameEN: "JAPAN",
      CountryNameOriginal: "日本",
    },
    KZ: {
      "2digitCode": "KZ",
      "3digitCode": "KAZ",
      ISONumbericCode: 398,
      CountryNameKR: "카자흐스탄",
      CountryNameEN: "KAZAKHSTAN",
      CountryNameOriginal: "Қазақстан",
    },
    JO: {
      "2digitCode": "JO",
      "3digitCode": "JOR",
      ISONumbericCode: 400,
      CountryNameKR: "요르단",
      CountryNameEN: "JORDAN",
      CountryNameOriginal: "الاردن",
    },
    KE: {
      "2digitCode": "KE",
      "3digitCode": "KEN",
      ISONumbericCode: 404,
      CountryNameKR: "케냐",
      CountryNameEN: "KENYA",
      CountryNameOriginal: "Kenya",
    },
    KP: {
      "2digitCode": "KP",
      "3digitCode": "PRK",
      ISONumbericCode: 408,
      CountryNameKR: "조선민주주의인민공화국",
      CountryNameEN: "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF",
      CountryNameOriginal: "조선",
    },
    KW: {
      "2digitCode": "KW",
      "3digitCode": "KWT",
      ISONumbericCode: 414,
      CountryNameKR: "쿠웨이트",
      CountryNameEN: "KUWAIT",
      CountryNameOriginal: "الكويت",
    },
    KG: {
      "2digitCode": "KG",
      "3digitCode": "KGZ",
      ISONumbericCode: 417,
      CountryNameKR: "키르기스스탄",
      CountryNameEN: "KYRGYZSTAN",
      CountryNameOriginal: "Кыргызстан",
    },
    LA: {
      "2digitCode": "LA",
      "3digitCode": "LAO",
      ISONumbericCode: 418,
      CountryNameKR: "라오스",
      CountryNameEN: "LAO PEOPLE'S DEMOCRATIC REPUBLIC",
      CountryNameOriginal: "ນລາວ",
    },
    LB: {
      "2digitCode": "LB",
      "3digitCode": "LBN",
      ISONumbericCode: 422,
      CountryNameKR: "레바논",
      CountryNameEN: "LEBANON",
      CountryNameOriginal: "لبنان",
    },
    LS: {
      "2digitCode": "LS",
      "3digitCode": "LSO",
      ISONumbericCode: 426,
      CountryNameKR: "레소토",
      CountryNameEN: "LESOTHO",
      CountryNameOriginal: "Lesotho",
    },
    LV: {
      "2digitCode": "LV",
      "3digitCode": "LVA",
      ISONumbericCode: 428,
      CountryNameKR: "라트비아",
      CountryNameEN: "LATVIA",
      CountryNameOriginal: "Latvija",
    },
    LR: {
      "2digitCode": "LR",
      "3digitCode": "LBR",
      ISONumbericCode: 430,
      CountryNameKR: "라이베리아",
      CountryNameEN: "LIBERIA",
      CountryNameOriginal: "Liberia",
    },
    LY: {
      "2digitCode": "LY",
      "3digitCode": "LBY",
      ISONumbericCode: 434,
      CountryNameKR: "리비아",
      CountryNameEN: "LIBYAN ARAB JAMAHIRIYA",
      CountryNameOriginal: "ليبيا",
    },
    LI: {
      "2digitCode": "LI",
      "3digitCode": "LIE",
      ISONumbericCode: 438,
      CountryNameKR: "리히텐슈타인",
      CountryNameEN: "LIECHTENSTEIN",
      CountryNameOriginal: "Liechtenstein",
    },
    LT: {
      "2digitCode": "LT",
      "3digitCode": "LTU",
      ISONumbericCode: 440,
      CountryNameKR: "리투아니아",
      CountryNameEN: "LITHUANIA",
      CountryNameOriginal: "Lietuva",
    },
    LU: {
      "2digitCode": "LU",
      "3digitCode": "LUX",
      ISONumbericCode: 442,
      CountryNameKR: "룩셈부르크",
      CountryNameEN: "LUXEMBOURG",
      CountryNameOriginal: "Lëtzebuerg",
    },
    MO: {
      "2digitCode": "MO",
      "3digitCode": "MAC",
      ISONumbericCode: 446,
      CountryNameKR: "마카오",
      CountryNameEN: "MACAU",
      CountryNameOriginal: "Macao",
    },
    MG: {
      "2digitCode": "MG",
      "3digitCode": "MDG",
      ISONumbericCode: 450,
      CountryNameKR: "마다가스카르",
      CountryNameEN: "MADAGASCAR",
      CountryNameOriginal: "Madagasikara",
    },
    MW: {
      "2digitCode": "MW",
      "3digitCode": "MWI",
      ISONumbericCode: 454,
      CountryNameKR: "말라위",
      CountryNameEN: "MALAWI",
      CountryNameOriginal: "Malawi",
    },
    MY: {
      "2digitCode": "MY",
      "3digitCode": "MYS",
      ISONumbericCode: 458,
      CountryNameKR: "말레이시아",
      CountryNameEN: "MALAYSIA",
      CountryNameOriginal: "Malaysia",
    },
    MV: {
      "2digitCode": "MV",
      "3digitCode": "MDV",
      ISONumbericCode: 462,
      CountryNameKR: "몰디브",
      CountryNameEN: "MALDIVES",
      CountryNameOriginal: "ގުޖޭއްރާ ޔާއްރިހޫމްޖ",
    },
    ML: {
      "2digitCode": "ML",
      "3digitCode": "MLI",
      ISONumbericCode: 466,
      CountryNameKR: "말리",
      CountryNameEN: "MALI",
      CountryNameOriginal: "Mali",
    },
    MT: {
      "2digitCode": "MT",
      "3digitCode": "MLT",
      ISONumbericCode: 470,
      CountryNameKR: "몰타",
      CountryNameEN: "MALTA",
      CountryNameOriginal: "Malta",
    },
    MQ: {
      "2digitCode": "MQ",
      "3digitCode": "MTQ",
      ISONumbericCode: 474,
      CountryNameKR: "마르티니크",
      CountryNameEN: "MARTINIQUE",
      CountryNameOriginal: "Martinique",
    },
    MR: {
      "2digitCode": "MR",
      "3digitCode": "MRT",
      ISONumbericCode: 478,
      CountryNameKR: "모리타니",
      CountryNameEN: "MAURITANIA",
      CountryNameOriginal: "موريتانيا",
    },
    MU: {
      "2digitCode": "MU",
      "3digitCode": "MUS",
      ISONumbericCode: 480,
      CountryNameKR: "모리셔스",
      CountryNameEN: "MAURITIUS",
      CountryNameOriginal: "Mauritius",
    },
    MX: {
      "2digitCode": "MX",
      "3digitCode": "MEX",
      ISONumbericCode: 484,
      CountryNameKR: "멕시코",
      CountryNameEN: "MEXICO",
      CountryNameOriginal: "México",
    },
    MC: {
      "2digitCode": "MC",
      "3digitCode": "MCO",
      ISONumbericCode: 492,
      CountryNameKR: "모나코",
      CountryNameEN: "MONACO",
      CountryNameOriginal: "Monaco",
    },
    MN: {
      "2digitCode": "MN",
      "3digitCode": "MNG",
      ISONumbericCode: 496,
      CountryNameKR: "몽골",
      CountryNameEN: "MONGOLIA",
      CountryNameOriginal: "Монгол Улс",
    },
    MD: {
      "2digitCode": "MD",
      "3digitCode": "MDA",
      ISONumbericCode: 498,
      CountryNameKR: "몰도바",
      CountryNameEN: "MOLDOVA, REPUBLIC OF",
      CountryNameOriginal: "Moldova",
    },
    ME: {
      "2digitCode": "ME",
      "3digitCode": "MNE",
      ISONumbericCode: 499,
      CountryNameKR: "몬테네그로",
      CountryNameEN: "MONTENEGRO",
      CountryNameOriginal: "Црна Гора",
    },
    MS: {
      "2digitCode": "MS",
      "3digitCode": "MSR",
      ISONumbericCode: 500,
      CountryNameKR: "몬트세랫",
      CountryNameEN: "MONTSERRAT",
      CountryNameOriginal: "Montserrat",
    },
    MA: {
      "2digitCode": "MA",
      "3digitCode": "MAR",
      ISONumbericCode: 504,
      CountryNameKR: "모로코",
      CountryNameEN: "MOROCCO",
      CountryNameOriginal: "المغرب",
    },
    MZ: {
      "2digitCode": "MZ",
      "3digitCode": "MOZ",
      ISONumbericCode: 508,
      CountryNameKR: "모잠비크",
      CountryNameEN: "MOZAMBIQUE",
      CountryNameOriginal: "Moçambique",
    },
    OM: {
      "2digitCode": "OM",
      "3digitCode": "OMN",
      ISONumbericCode: 512,
      CountryNameKR: "오만",
      CountryNameEN: "OMAN",
      CountryNameOriginal: "عمان",
    },
    NA: {
      "2digitCode": "NA",
      "3digitCode": "NAM",
      ISONumbericCode: 516,
      CountryNameKR: "나미비아",
      CountryNameEN: "NAMIBIA",
      CountryNameOriginal: "Namibia",
    },
    NR: {
      "2digitCode": "NR",
      "3digitCode": "NRU",
      ISONumbericCode: 520,
      CountryNameKR: "나우루",
      CountryNameEN: "NAURU",
      CountryNameOriginal: "Naoero",
    },
    NP: {
      "2digitCode": "NP",
      "3digitCode": "NPL",
      ISONumbericCode: 524,
      CountryNameKR: "네팔",
      CountryNameEN: "NEPAL",
      CountryNameOriginal: "नेपाल",
    },
    NL: {
      "2digitCode": "NL",
      "3digitCode": "NLD",
      ISONumbericCode: 528,
      CountryNameKR: "네덜란드",
      CountryNameEN: "NETHERLANDS",
      CountryNameOriginal: "Nederland",
    },
    AN: {
      "2digitCode": "AN",
      "3digitCode": "ANT",
      ISONumbericCode: 530,
      CountryNameKR: "네덜란드령 안틸레스",
      CountryNameEN: "NETHERLANDS ANTILLES",
      CountryNameOriginal: "Netherlands Antilles",
    },
    AW: {
      "2digitCode": "AW",
      "3digitCode": "ABW",
      ISONumbericCode: 533,
      CountryNameKR: "아루바",
      CountryNameEN: "ARUBA",
      CountryNameOriginal: "Aruba",
    },
    NC: {
      "2digitCode": "NC",
      "3digitCode": "NCL",
      ISONumbericCode: 540,
      CountryNameKR: "누벨칼레도니",
      CountryNameEN: "NEW CALEDONIA",
      CountryNameOriginal: "New Caledonia",
    },
    VU: {
      "2digitCode": "VU",
      "3digitCode": "VUT",
      ISONumbericCode: 548,
      CountryNameKR: "바누아투",
      CountryNameEN: "VANUATU",
      CountryNameOriginal: "Vanuatu",
    },
    NZ: {
      "2digitCode": "NZ",
      "3digitCode": "NZL",
      ISONumbericCode: 554,
      CountryNameKR: "뉴질랜드",
      CountryNameEN: "NEW ZEALAND",
      CountryNameOriginal: "New Zealand",
    },
    NI: {
      "2digitCode": "NI",
      "3digitCode": "NIC",
      ISONumbericCode: 558,
      CountryNameKR: "니카라과",
      CountryNameEN: "NICARAGUA",
      CountryNameOriginal: "Nicaragua",
    },
    NE: {
      "2digitCode": "NE",
      "3digitCode": "NER",
      ISONumbericCode: 562,
      CountryNameKR: "니제르",
      CountryNameEN: "NIGER",
      CountryNameOriginal: "Niger",
    },
    NG: {
      "2digitCode": "NG",
      "3digitCode": "NGA",
      ISONumbericCode: 566,
      CountryNameKR: "나이지리아",
      CountryNameEN: "NIGERIA",
      CountryNameOriginal: "Nigeria",
    },
    NU: {
      "2digitCode": "NU",
      "3digitCode": "NIU",
      ISONumbericCode: 570,
      CountryNameKR: "니우에",
      CountryNameEN: "NIUE",
      CountryNameOriginal: "Niue",
    },
    NF: {
      "2digitCode": "NF",
      "3digitCode": "NFK",
      ISONumbericCode: 574,
      CountryNameKR: "노퍽 섬",
      CountryNameEN: "NORFOLK ISLAND",
      CountryNameOriginal: "Norfolk Island",
    },
    NO: {
      "2digitCode": "NO",
      "3digitCode": "NOR",
      ISONumbericCode: 578,
      CountryNameKR: "노르웨이",
      CountryNameEN: "NORWAY",
      CountryNameOriginal: "Norge",
    },
    MP: {
      "2digitCode": "MP",
      "3digitCode": "MNP",
      ISONumbericCode: 580,
      CountryNameKR: "북마리아나 제도",
      CountryNameEN: "NORTHERN MARIANA ISLANDS",
      CountryNameOriginal: "Northern Mariana Islands",
    },
    UM: {
      "2digitCode": "UM",
      "3digitCode": "UMI",
      ISONumbericCode: 581,
      CountryNameKR: "미국령 군소 제도",
      CountryNameEN: "UNITED STATES MINOR OUTLYING ISLANDS",
      CountryNameOriginal: "United States minor outlying islands",
    },
    FM: {
      "2digitCode": "FM",
      "3digitCode": "FSM",
      ISONumbericCode: 583,
      CountryNameKR: "미크로네시아 연방",
      CountryNameEN: "MICRONESIA",
      CountryNameOriginal: "Micronesia",
    },
    MH: {
      "2digitCode": "MH",
      "3digitCode": "MHL",
      ISONumbericCode: 584,
      CountryNameKR: "마셜 제도",
      CountryNameEN: "MARSHALL ISLANDS",
      CountryNameOriginal: "Marshall Islands",
    },
    PW: {
      "2digitCode": "PW",
      "3digitCode": "PLW",
      ISONumbericCode: 585,
      CountryNameKR: "팔라우",
      CountryNameEN: "PALAU",
      CountryNameOriginal: "Belau",
    },
    PK: {
      "2digitCode": "PK",
      "3digitCode": "PAK",
      ISONumbericCode: 586,
      CountryNameKR: "파키스탄",
      CountryNameEN: "PAKISTAN",
      CountryNameOriginal: "پاکستان",
    },
    PA: {
      "2digitCode": "PA",
      "3digitCode": "PAN",
      ISONumbericCode: 591,
      CountryNameKR: "파나마",
      CountryNameEN: "PANAMA",
      CountryNameOriginal: "Panamá",
    },
    PG: {
      "2digitCode": "PG",
      "3digitCode": "PNG",
      ISONumbericCode: 598,
      CountryNameKR: "파푸아 뉴기니",
      CountryNameEN: "PAPUA NEW GUINEA",
      CountryNameOriginal: "Papua New Guinea",
    },
    PY: {
      "2digitCode": "PY",
      "3digitCode": "PRY",
      ISONumbericCode: 600,
      CountryNameKR: "파라과이",
      CountryNameEN: "PARAGUAY",
      CountryNameOriginal: "Paraguay",
    },
    PE: {
      "2digitCode": "PE",
      "3digitCode": "PER",
      ISONumbericCode: 604,
      CountryNameKR: "페루",
      CountryNameEN: "PERU",
      CountryNameOriginal: "Perú",
    },
    PH: {
      "2digitCode": "PH",
      "3digitCode": "PHL",
      ISONumbericCode: 608,
      CountryNameKR: "필리핀",
      CountryNameEN: "PHILIPPINES",
      CountryNameOriginal: "Pilipinas",
    },
    PN: {
      "2digitCode": "PN",
      "3digitCode": "PCN",
      ISONumbericCode: 612,
      CountryNameKR: "핏케언 제도",
      CountryNameEN: "PITCAIRN",
      CountryNameOriginal: "Pitcairn",
    },
    PL: {
      "2digitCode": "PL",
      "3digitCode": "POL",
      ISONumbericCode: 616,
      CountryNameKR: "폴란드",
      CountryNameEN: "POLAND",
      CountryNameOriginal: "Polska",
    },
    PT: {
      "2digitCode": "PT",
      "3digitCode": "PRT",
      ISONumbericCode: 620,
      CountryNameKR: "포르투갈",
      CountryNameEN: "PORTUGAL",
      CountryNameOriginal: "Portugal",
    },
    GW: {
      "2digitCode": "GW",
      "3digitCode": "GNB",
      ISONumbericCode: 624,
      CountryNameKR: "기니비사우",
      CountryNameEN: "GUINEA-BISSAU",
      CountryNameOriginal: "Guiné-Bissau",
    },
    TL: {
      "2digitCode": "TL",
      "3digitCode": "TLS",
      ISONumbericCode: 626,
      CountryNameKR: "동티모르",
      CountryNameEN: "EAST TIMOR",
      CountryNameOriginal: "Timor-Leste",
    },
    PR: {
      "2digitCode": "PR",
      "3digitCode": "PRI",
      ISONumbericCode: 630,
      CountryNameKR: "푸에르토리코",
      CountryNameEN: "PUERTO RICO",
      CountryNameOriginal: "Puerto Rico",
    },
    QA: {
      "2digitCode": "QA",
      "3digitCode": "QAT",
      ISONumbericCode: 634,
      CountryNameKR: "카타르",
      CountryNameEN: "QATAR",
      CountryNameOriginal: "قطر",
    },
    RE: {
      "2digitCode": "RE",
      "3digitCode": "REU",
      ISONumbericCode: 638,
      CountryNameKR: "레위니옹",
      CountryNameEN: "REUNION",
      CountryNameOriginal: "Reunion",
    },
    RO: {
      "2digitCode": "RO",
      "3digitCode": "ROU",
      ISONumbericCode: 642,
      CountryNameKR: "루마니아",
      CountryNameEN: "ROMANIA",
      CountryNameOriginal: "România",
    },
    RU: {
      "2digitCode": "RU",
      "3digitCode": "RUS",
      ISONumbericCode: 643,
      CountryNameKR: "러시아",
      CountryNameEN: "RUSSIAN FEDERATION",
      CountryNameOriginal: "Россия",
    },
    RW: {
      "2digitCode": "RW",
      "3digitCode": "RWA",
      ISONumbericCode: 646,
      CountryNameKR: "르완다",
      CountryNameEN: "RWANDA",
      CountryNameOriginal: "Rwanda",
    },
    SH: {
      "2digitCode": "SH",
      "3digitCode": "SHN",
      ISONumbericCode: 654,
      CountryNameKR: "세인트헬레나",
      CountryNameEN: "ST. HELENA",
      CountryNameOriginal: "Saint Helena",
    },
    KN: {
      "2digitCode": "KN",
      "3digitCode": "KNA",
      ISONumbericCode: 659,
      CountryNameKR: "세인트키츠 네비스",
      CountryNameEN: "SAINT KITTS AND NEVIS",
      CountryNameOriginal: "Saint Kitts and Nevis",
    },
    AI: {
      "2digitCode": "AI",
      "3digitCode": "AIA",
      ISONumbericCode: 660,
      CountryNameKR: "앵귈라",
      CountryNameEN: "ANGUILLA",
      CountryNameOriginal: "Anguilla",
    },
    LC: {
      "2digitCode": "LC",
      "3digitCode": "LCA",
      ISONumbericCode: 662,
      CountryNameKR: "세인트루시아",
      CountryNameEN: "SAINT LUCIA",
      CountryNameOriginal: "Saint Lucia",
    },
    PM: {
      "2digitCode": "PM",
      "3digitCode": "SPM",
      ISONumbericCode: 666,
      CountryNameKR: "생피에르 미클롱",
      CountryNameEN: "ST. PIERRE AND MIQUELON",
      CountryNameOriginal: "Saint Pierre and Miquelon",
    },
    VC: {
      "2digitCode": "VC",
      "3digitCode": "VCT",
      ISONumbericCode: 670,
      CountryNameKR: "세인트빈센트 그레나딘",
      CountryNameEN: "SAINT VINCENT AND THE GRENADINES",
      CountryNameOriginal: "Saint Vincent and the Grenadines",
    },
    SM: {
      "2digitCode": "SM",
      "3digitCode": "SMR",
      ISONumbericCode: 674,
      CountryNameKR: "산마리노",
      CountryNameEN: "SAN MARINO",
      CountryNameOriginal: "San Marino",
    },
    ST: {
      "2digitCode": "ST",
      "3digitCode": "STP",
      ISONumbericCode: 678,
      CountryNameKR: "상투메 프린시페",
      CountryNameEN: "SAO TOME AND PRINCIPE",
      CountryNameOriginal: "São Tomé and Príncipe",
    },
    SA: {
      "2digitCode": "SA",
      "3digitCode": "SAU",
      ISONumbericCode: 682,
      CountryNameKR: "사우디아라비아",
      CountryNameEN: "SAUDI ARABIA",
      CountryNameOriginal: "المملكة العربية السعودية",
    },
    SN: {
      "2digitCode": "SN",
      "3digitCode": "SEN",
      ISONumbericCode: 686,
      CountryNameKR: "세네갈",
      CountryNameEN: "SENEGAL",
      CountryNameOriginal: "Sénégal",
    },
    RS: {
      "2digitCode": "RS",
      "3digitCode": "SRB",
      ISONumbericCode: 688,
      CountryNameKR: "세르비아",
      CountryNameEN: "SERBIA",
      CountryNameOriginal: "Србија",
    },
    SC: {
      "2digitCode": "SC",
      "3digitCode": "SYC",
      ISONumbericCode: 690,
      CountryNameKR: "세이셸",
      CountryNameEN: "SEYCHELLES",
      CountryNameOriginal: "Seychelles",
    },
    SL: {
      "2digitCode": "SL",
      "3digitCode": "SLE",
      ISONumbericCode: 694,
      CountryNameKR: "시에라리온",
      CountryNameEN: "SIERRA LEONE",
      CountryNameOriginal: "Sierra Leone",
    },
    SG: {
      "2digitCode": "SG",
      "3digitCode": "SGP",
      ISONumbericCode: 702,
      CountryNameKR: "싱가포르",
      CountryNameEN: "SINGAPORE",
      CountryNameOriginal: "Singapura",
    },
    SK: {
      "2digitCode": "SK",
      "3digitCode": "SVK",
      ISONumbericCode: 703,
      CountryNameKR: "슬로바키아",
      CountryNameEN: "SLOVAKIA",
      CountryNameOriginal: "Slovensko",
    },
    VN: {
      "2digitCode": "VN",
      "3digitCode": "VNM",
      ISONumbericCode: 704,
      CountryNameKR: "베트남",
      CountryNameEN: "VIET NAM",
      CountryNameOriginal: "Việt Nam",
    },
    SI: {
      "2digitCode": "SI",
      "3digitCode": "SVN",
      ISONumbericCode: 705,
      CountryNameKR: "슬로베니아",
      CountryNameEN: "SLOVENIA",
      CountryNameOriginal: "Slovenija",
    },
    SO: {
      "2digitCode": "SO",
      "3digitCode": "SOM",
      ISONumbericCode: 706,
      CountryNameKR: "소말리아",
      CountryNameEN: "SOMALIA",
      CountryNameOriginal: "Soomaaliya",
    },
    ZA: {
      "2digitCode": "ZA",
      "3digitCode": "ZAF",
      ISONumbericCode: 710,
      CountryNameKR: "남아프리카 공화국",
      CountryNameEN: "SOUTH AFRICA",
      CountryNameOriginal: "South Africa",
    },
    ZW: {
      "2digitCode": "ZW",
      "3digitCode": "ZWE",
      ISONumbericCode: 716,
      CountryNameKR: "짐바브웨",
      CountryNameEN: "ZIMBABWE",
      CountryNameOriginal: "Zimbabwe",
    },
    ES: {
      "2digitCode": "ES",
      "3digitCode": "ESP",
      ISONumbericCode: 724,
      CountryNameKR: "스페인",
      CountryNameEN: "SPAIN",
      CountryNameOriginal: "España",
    },
    SS: {
      "2digitCode": "SS",
      "3digitCode": "SSD",
      ISONumbericCode: 728,
      CountryNameKR: "남수단",
      CountryNameEN: "REPUBLIC OF SOUTH SUDAN",
      CountryNameOriginal: "South Sudan",
    },
    EH: {
      "2digitCode": "EH",
      "3digitCode": "ESH",
      ISONumbericCode: 732,
      CountryNameKR: "서사하라",
      CountryNameEN: "WESTERN SAHARA",
      CountryNameOriginal: "الصحراء الغربية",
    },
    SD: {
      "2digitCode": "SD",
      "3digitCode": "SDN",
      ISONumbericCode: 736,
      CountryNameKR: "수단",
      CountryNameEN: "SUDAN",
      CountryNameOriginal: "السودان",
    },
    SR: {
      "2digitCode": "SR",
      "3digitCode": "SUR",
      ISONumbericCode: 740,
      CountryNameKR: "수리남",
      CountryNameEN: "SURINAME",
      CountryNameOriginal: "Suriname",
    },
    SJ: {
      "2digitCode": "SJ",
      "3digitCode": "SJM",
      ISONumbericCode: 744,
      CountryNameKR: "스발바르 얀마옌",
      CountryNameEN: "SVALBARD AND JAN MAYEN ISLANDS",
      CountryNameOriginal: "Svalbard and Jan Mayen",
    },
    SZ: {
      "2digitCode": "SZ",
      "3digitCode": "SWZ",
      ISONumbericCode: 748,
      CountryNameKR: "스와질란드",
      CountryNameEN: "SWAZILAND",
      CountryNameOriginal: "Swaziland",
    },
    SE: {
      "2digitCode": "SE",
      "3digitCode": "SWE",
      ISONumbericCode: 752,
      CountryNameKR: "스웨덴",
      CountryNameEN: "SWEDEN",
      CountryNameOriginal: "Sverige",
    },
    CH: {
      "2digitCode": "CH",
      "3digitCode": "CHE",
      ISONumbericCode: 756,
      CountryNameKR: "스위스",
      CountryNameEN: "SWITZERLAND",
      CountryNameOriginal: "Schweiz",
    },
    SY: {
      "2digitCode": "SY",
      "3digitCode": "SYR",
      ISONumbericCode: 760,
      CountryNameKR: "시리아",
      CountryNameEN: "SYRIAN ARAB REPUBLIC",
      CountryNameOriginal: "سوريا",
    },
    TJ: {
      "2digitCode": "TJ",
      "3digitCode": "TJK",
      ISONumbericCode: 762,
      CountryNameKR: "타지키스탄",
      CountryNameEN: "TAJIKISTAN",
      CountryNameOriginal: "Тоҷикистон",
    },
    TH: {
      "2digitCode": "TH",
      "3digitCode": "THA",
      ISONumbericCode: 764,
      CountryNameKR: "타이",
      CountryNameEN: "THAILAND",
      CountryNameOriginal: "ราชอาณาจักรไทย",
    },
    TG: {
      "2digitCode": "TG",
      "3digitCode": "TGO",
      ISONumbericCode: 768,
      CountryNameKR: "토고",
      CountryNameEN: "TOGO",
      CountryNameOriginal: "Togo",
    },
    TK: {
      "2digitCode": "TK",
      "3digitCode": "TKL",
      ISONumbericCode: 772,
      CountryNameKR: "토켈라우",
      CountryNameEN: "TOKELAU",
      CountryNameOriginal: "Tokelau",
    },
    TO: {
      "2digitCode": "TO",
      "3digitCode": "TON",
      ISONumbericCode: 776,
      CountryNameKR: "통가",
      CountryNameEN: "TONGA",
      CountryNameOriginal: "Tonga",
    },
    TT: {
      "2digitCode": "TT",
      "3digitCode": "TTO",
      ISONumbericCode: 780,
      CountryNameKR: "트리니다드 토바고",
      CountryNameEN: "TRINIDAD AND TOBAGO",
      CountryNameOriginal: "Trinidad and Tobago",
    },
    AE: {
      "2digitCode": "AE",
      "3digitCode": "ARE",
      ISONumbericCode: 784,
      CountryNameKR: "아랍에미리트",
      CountryNameEN: "UNITED ARAB EMIRATES",
      CountryNameOriginal: "الإمارات العربيّة المتّحدة",
    },
    TN: {
      "2digitCode": "TN",
      "3digitCode": "TUN",
      ISONumbericCode: 788,
      CountryNameKR: "튀니지",
      CountryNameEN: "TUNISIA",
      CountryNameOriginal: "تونس",
    },
    TR: {
      "2digitCode": "TR",
      "3digitCode": "TUR",
      ISONumbericCode: 792,
      CountryNameKR: "터키",
      CountryNameEN: "TURKEY",
      CountryNameOriginal: "Türkiye",
    },
    TM: {
      "2digitCode": "TM",
      "3digitCode": "TKM",
      ISONumbericCode: 795,
      CountryNameKR: "투르크메니스탄",
      CountryNameEN: "TURKMENISTAN",
      CountryNameOriginal: "Türkmenistan",
    },
    TC: {
      "2digitCode": "TC",
      "3digitCode": "TCA",
      ISONumbericCode: 796,
      CountryNameKR: "터크스 케이커스 제도",
      CountryNameEN: "TURKS AND CAICOS ISLANDS",
      CountryNameOriginal: "Turks and Caicos Islands",
    },
    TV: {
      "2digitCode": "TV",
      "3digitCode": "TUV",
      ISONumbericCode: 798,
      CountryNameKR: "투발루",
      CountryNameEN: "TUVALU",
      CountryNameOriginal: "Tuvalu",
    },
    UG: {
      "2digitCode": "UG",
      "3digitCode": "UGA",
      ISONumbericCode: 800,
      CountryNameKR: "우간다",
      CountryNameEN: "UGANDA",
      CountryNameOriginal: "Uganda",
    },
    UA: {
      "2digitCode": "UA",
      "3digitCode": "UKR",
      ISONumbericCode: 804,
      CountryNameKR: "우크라이나",
      CountryNameEN: "UKRAINE",
      CountryNameOriginal: "Україна",
    },
    MK: {
      "2digitCode": "MK",
      "3digitCode": "MKD",
      ISONumbericCode: 807,
      CountryNameKR: "마케도니아 공화국",
      CountryNameEN: "REPUBLIC OF MACEDONIA",
      CountryNameOriginal: "Македонија",
    },
    EG: {
      "2digitCode": "EG",
      "3digitCode": "EGY",
      ISONumbericCode: 818,
      CountryNameKR: "이집트",
      CountryNameEN: "EGYPT",
      CountryNameOriginal: "مصر",
    },
    GB: {
      "2digitCode": "GB",
      "3digitCode": "GBR",
      ISONumbericCode: 826,
      CountryNameKR: "영국",
      CountryNameEN: "UNITED KINGDOM",
      CountryNameOriginal: "United Kingdom",
    },
    GG: {
      "2digitCode": "GG",
      "3digitCode": "GGY",
      ISONumbericCode: 831,
      CountryNameKR: "건지 섬",
      CountryNameEN: "GUERNSEY",
      CountryNameOriginal: "Guernsey",
    },
    JE: {
      "2digitCode": "JE",
      "3digitCode": "JEY",
      ISONumbericCode: 832,
      CountryNameKR: "저지 섬",
      CountryNameEN: "JERSEY",
      CountryNameOriginal: "Jersey",
    },
    IM: {
      "2digitCode": "IM",
      "3digitCode": "IMN",
      ISONumbericCode: 833,
      CountryNameKR: "맨 섬",
      CountryNameEN: "ISLE OF MAN",
      CountryNameOriginal: "Isle of Man",
    },
    TZ: {
      "2digitCode": "TZ",
      "3digitCode": "TZA",
      ISONumbericCode: 834,
      CountryNameKR: "탄자니아",
      CountryNameEN: "TANZANIA, UNITED REPUBLIC OF",
      CountryNameOriginal: "Tanzania",
    },
    US: {
      "2digitCode": "US",
      "3digitCode": "USA",
      ISONumbericCode: 840,
      CountryNameKR: "미국",
      CountryNameEN: "UNITED STATES",
      CountryNameOriginal: "United States",
    },
    VI: {
      "2digitCode": "VI",
      "3digitCode": "VIR",
      ISONumbericCode: 850,
      CountryNameKR: "미국령 버진아일랜드",
      CountryNameEN: "VIRGIN ISLANDS, U.S.",
      CountryNameOriginal: "Virgin Islands, U.S.",
    },
    BF: {
      "2digitCode": "BF",
      "3digitCode": "BFA",
      ISONumbericCode: 854,
      CountryNameKR: "부르키나파소",
      CountryNameEN: "BURKINA FASO",
      CountryNameOriginal: "Burkina Faso",
    },
    UY: {
      "2digitCode": "UY",
      "3digitCode": "URY",
      ISONumbericCode: 858,
      CountryNameKR: "우루과이",
      CountryNameEN: "URUGUAY",
      CountryNameOriginal: "Uruguay",
    },
    UZ: {
      "2digitCode": "UZ",
      "3digitCode": "UZB",
      ISONumbericCode: 860,
      CountryNameKR: "우즈베키스탄",
      CountryNameEN: "UZBEKISTAN",
      CountryNameOriginal: "O'zbekiston",
    },
    VE: {
      "2digitCode": "VE",
      "3digitCode": "VEN",
      ISONumbericCode: 862,
      CountryNameKR: "베네수엘라",
      CountryNameEN: "VENEZUELA",
      CountryNameOriginal: "Venezuela",
    },
    WF: {
      "2digitCode": "WF",
      "3digitCode": "WLF",
      ISONumbericCode: 876,
      CountryNameKR: "왈리스 퓌튀나",
      CountryNameEN: "WALLIS AND FUTUNA ISLANDS",
      CountryNameOriginal: "Wallis and Futuna",
    },
    WS: {
      "2digitCode": "WS",
      "3digitCode": "WSM",
      ISONumbericCode: 882,
      CountryNameKR: "사모아",
      CountryNameEN: "SAMOA",
      CountryNameOriginal: "Samoa",
    },
    YE: {
      "2digitCode": "YE",
      "3digitCode": "YEM",
      ISONumbericCode: 887,
      CountryNameKR: "예멘",
      CountryNameEN: "YEMEN, REPUBLIC OF",
      CountryNameOriginal: "اليمن",
    },
    ZM: {
      "2digitCode": "ZM",
      "3digitCode": "ZMB",
      ISONumbericCode: 894,
      CountryNameKR: "잠비아",
      CountryNameEN: "ZAMBIA",
      CountryNameOriginal: "Zambia",
    },
  };
  const selectElement = document.getElementById("countrySelect");
  for (const code in countries) {
    const option = document.createElement("option");
    option.value = code;
    option.textContent = countries[code].CountryNameEN;
    selectElement.appendChild(option);
  }

</script>
