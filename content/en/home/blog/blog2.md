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
          <a href="/home"><img src="../../img/logo_machbase.png" alt="" /></a>
        </li>
        <li class="menu-a products-menu-wrap" id="productsMenuWrap">
          <div>
            <a
              class="menu_active_border"
              id="menuActiveBorder"
              href="/home/tsdb"
              >Products</a
            >
            <div class="dropdown" id="dropdown">
              <a class="dropdown-link" href="/home/tsdb">TSDB</a>
              <a class="dropdown-link" href="/home/mos">MOS</a>
              <a
                class="dropdown-link"
                href="https://www.cems.ai/home-eng/"
                target="_blank"
                >CEMS</a
              >
            </div>
          </div>
        </li>
        <li class="menu-a"><a href="/home/blog">Blog</a></li>
        <li class="menu-a"><a href="/home/customers">Customers</a></li>
        <li class="menu-a"><a href="/home/usecase">Use Case</a></li>
        <li class="menu-a"><a href="/home/company">Company</a></li>
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
        <li class="menu-a"><a href="/home/download">Download</a></li>
        <li class="menu-a">
          <a href="https://support.machbase.com/hc/en-us">Support</a>
        </li>
         <li class="menu-a"><a href="/home/contactus">Contact US</a></li>
        <li class="menu-a"><select id="languageSelector" onchange="changeLanguage()">
        <option value="en">English</option>
        <option value="kr">한국어</option>
    </select></li>
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
        <a class="tablet-logo" href="/home"
          ><img src="../../img/logo_machbase.png" alt=""
        /></a>
      </div>
      <li></li>
      <li class="products-toggle">Products</li>
      <li>
        <div class="products-content">
          <div class="products-sub"><a href="/home/tsdb">TSDB</a></div>
          <div class="products-num"><a href="/home/mos">MOS</a></div>
          <div class="products-cems">
            <a href="https://www.cems.ai/home-eng/" target="_blank">CEMS</a>
          </div>
        </div>
      </li>
      <li><a href="/home/blog">Blog</a></li>
      <li><a href="/home/customers">Customers</a></li>
      <li><a href="/home/usecase">Use Cases</a></li>
      <li><a href="/home/company">Company</a></li>
      <li class="docs-toggle">Document</li>
      <li>
        <div class="docs-content">
          <div class="docs-sub"><a href="/neo" target="_blank">Neo</a></div>
          <div class="docs-num"><a href="/dbms" target="_blank">Classic</a></div>
        </div>
      </li>
      <li><a href="/home/download">Download</a></li>
      <li><a href="https://support.machbase.com/hc/en-us">Support</a></li>
         <li><a href="/home/download">Contact US</a></li>
     <li class="menu-a"><select id="languageSelector2" onchange="changeLanguage2()">
        <option value="en">English</option>
        <option value="kr">한국어</option>
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
      Why did Machbase Neo switch its front-end framework from Vue.js to React?
    </h4>
    <div class="blog-date">
      <div>
        <span>by Andrew Kim / 1 Sep 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">
          About Frontend Framework
        </li></a
      >
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">
          Three Years of Vue.js Journey: Reflections and Lessons Learned
        </li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">
          New Endeavors for Machbase Neo
        </li>
      </a>
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">
          Switching from Vue.js to React in Machbase Neo 8.0!
        </li>
      </a>
      <a href="#anchor5">
        <li class="tech-list-li" id="tech-list-li">Conclusion</li>
      </a>
    </ul>
    <div class="tech-contents">
      <div>
        <div class="tech-title" id="anchor1">About Frontend Framework</div>
        <p class="tech-contents-text">
          Designing and developing the web-based front-end portion in today’s
          software landscape is undoubtedly challenging and intricate. However,
          it stands as one of the most crucial aspects, encompassing user
          interfaces that directly engage users. For this reason, the choice of
          framework for developing user interfaces within a particular company’s
          development organization is a complex outcome of various factors.
          These factors include diverse knowledge backgrounds, distinct
          requirements, cultural and individual characteristics, as well as the
          company’s philosophy.
        </p>
        <p class="tech-contents-text">
          As a result, selecting a framework as the foundation for creating user
          interfaces involves intricate decision-making. This decision takes
          into account a multitude of considerations, with outcomes that are
          shaped by the interplay of these complexities. While it’s possible to
          choose a specific framework without any specific reason, such
          decisions are often rooted in careful evaluation and alignment with
          the organization’s goals and needs.
        </p>
        <div class="tech-title" id="anchor2">
          Three Years of Vue.js Journey: Reflections and Lessons Learned
        </div>
        <p class="tech-contents-text">
          The Machbase development team has been using Vue.js as the primary
          framework for the front-end over the past three years. This Vue.js
          framework has served as a core foundation for the user interface of
          our cloud product, known as CEMS, which is based on edge computing.
          Throughout the design and implementation process, the framework has
          been instrumental in meeting various visual requirements of users.
          Most of our front-end developers have learned and become familiar with
          Vue.js, using it to satisfy a diverse array of visual demands.
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
          However, over the past year, as we developed a new database product
          called Machbase Neo, doubts have arisen about whether Vue.js, which we
          adopted, remains the optimal choice.
        </p>
        <div class="tech-title" id="anchor3">
          New Endeavors for Machbase Neo
        </div>
        <p class="tech-contents-text">
          First, let me provide a description of Machbase Neo
          <a class="tech-contents-link" href="https://neo.machbase.com"
            >(https://neo.machbase.com)</a
          >. This product is a time-series database solution, but it goes beyond
          traditional boundaries by embracing an All-In-One concept that aligns
          with future technological trends. Machbase Neo aims to streamline the
          entire data management process for users. This includes not only data
          storage and retrieval, but also data collection, transformation, and
          integration. The product is designed to significantly reduce the costs
          associated with installing and managing various auxiliary processes
          through built-in servers like MQTT, SSH, HTTP, and gRPC.
        </p>
        <p class="tech-contents-text">
          Notably, Machbase Neo stands out as an open-source solution, allowing
          anyone to access and understand its structure and operational
          principles. At its core, the product incorporates the world’s fastest
          TPC benchmark ranking, with Machbase TSDB as the backbone, delivering
          exceptional performance and efficiency.
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
          In essence, to empower customers utilizing Neo, we employ the Vue.js
          front-end framework to enable them to create various charts and
          perform all tasks within a web-based environment without the need for
          separate visualization tools.
        </p>
        <p class="tech-contents-text">
          However, as development progressed, the drawbacks of Vue.js became
          more pronounced. Let’s outline the pros and cons of this framework.
        </p>
        <div class="tech-contents-title">Pros of Vue.js:</div>
        <p class="tech-contents-text">
          1. Easy Learning Curve: Vue.js offers a gentle learning curve, making
          it accessible to developers with varying skill levels.
        </p>
        <p class="tech-contents-text">
          2. Flexible and Versatile: Vue.js provides a flexible structure,
          allowing developers to integrate it into existing projects or use
          specific parts of the framework as needed.
        </p>
        <p class="tech-contents-text">
          3. Reactive Data Binding: The framework’s reactive data binding
          simplifies the process of synchronizing data between the model and the
          view.
        </p>
        <p class="tech-contents-text">
          4. Component-Based Architecture: Vue.js promotes a component-based
          approach, facilitating modular development and reusability.
        </p>
        <div class="tech-contents-title">Cons of Vue.js:</div>
        <p class="tech-contents-text">
          1. Less Mature Ecosystem: Compared to frameworks like React, Vue.js
          has a smaller ecosystem of libraries and tools, potentially limiting
          options for advanced functionality.
        </p>
        <p class="tech-contents-text">
          2. Limited Corporate Backing: Vue.js has less corporate support
          compared to React or Angular, which might impact long-term
          sustainability and updates.
        </p>
        <p class="tech-contents-text">
          3. Performance Challenges: As applications scale, Vue.js can face
          performance issues, especially when handling complex and deeply nested
          components.
        </p>
        <p class="tech-contents-text">
          4. Smaller Community: The smaller user community of Vue.js might lead
          to slower issue resolution and fewer resources for troubleshooting.
        </p>
        <p class="tech-contents-text">
          Despite its benefits, the increasing prominence of these drawbacks has
          led us to reconsider Vue.js as the best fit for our evolving needs in
          the development of Machbase Neo’s front-end.
        </p>
        <p class="tech-contents-text">
          Absolutely, particularly as development progressed, we realized that
          drawbacks 1 and 3 have been increasingly impacting development time
          and costs. The need to introduce new features often led to situations
          where we couldn’t rely on existing components and had to develop new
          ones. This further added to the complexity and resource requirements
          of the project.
        </p>
        <p class="tech-contents-text">
          Furthermore, as functionality grew, we began to sense a qualitative
          decline in the web-based UI performance. It’s important to acknowledge
          that this perception could vary among users, but it raised concerns
          about the ability to maintain a smooth and responsive user experience
          as more features were incorporated.
        </p>
        <p class="tech-contents-text">
          Certainly, let’s take a look at the pros and cons of React, which
          you’ve been considering as an alternative:
        </p>
        <div class="tech-contents-title">Pros of React:</div>
        <p class="tech-contents-text">
          1. Active Development Community: React benefits from a highly active
          development community, offering a wide array of library choices to
          address different needs.
        </p>
        <p class="tech-contents-text">
          2. Efficient Virtual DOM: React’s clean and efficient virtual DOM
          structure contributes to faster rendering speeds.
        </p>
        <p class="tech-contents-text">
          3. Rapid Improvement and Iteration: React sees frequent updates and
          improvements, leading to enhanced features and performance over time.
        </p>
        <div class="tech-contents-title">Cons of React:</div>
        <p class="tech-contents-text">
          1. Higher Learning Curve: React has a relatively steeper learning
          curve compared to Vue.
        </p>
        <p class="tech-contents-text">
          2. Complexity due to Architecture: Some complex coding scenarios can
          arise due to React’s architecture, which might pose challenges during
          specific unit development tasks.
        </p>
        <p class="tech-contents-text">
          3. Continuous Learning Required: Ongoing architectural enhancements
          and structural changes demand continuous learning to keep up with best
          practices.
        </p>
        <p class="tech-contents-text">
          As mentioned in the drawbacks, while React may require a longer
          learning curve and present higher difficulty, once familiarity is
          established, the availability of a wide range of libraries (as
          mentioned in the first advantage) can significantly reduce development
          time and subsequently lower costs. Notably, the potential for
          significant performance improvements, as highlighted in the second
          advantage, became a compelling factor during testing, indicating that
          switching to React might yield faster response times by several folds.
        </p>
        <div class="tech-title" id="anchor4">
          Switching from Vue.js to React in Machbase Neo 8.0!
        </div>
        <p class="tech-contents-text">
          After conducting an internal technology survey, a substantial
          redevelopment of the UI was undertaken to adopt React following the
          decision. This effort, while not overly time-consuming, took
          approximately 1 to 2 months to complete. Although the external
          appearance of the UI underwent significant changes, the core
          functionality remains largely unchanged.
        </p>
        <div class="tech-contents-title">Machbase Neo 1.7 UI</div>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/neo-first-03.png" alt="" />
        </div>
        <p class="tech-contents-link-text">Machbase Neo 1.7 UI</p>
        <div class="tech-contents-title">Machbase Neo 8.0 UI</div>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/neo-first-04.png" alt="" />
        </div>
        <p class="tech-contents-link-text">Machbase Neo 8.0 UI</p>
        <div class="tech-contents-title">
          What improvements have been achieved in React?
        </div>
        <p class="tech-contents-text">
          Here’s a list of improvements experienced directly by developers
          through React, though using it feels like the response performance has
          improved by more than 2 to 3 times compared to before. It’s like going
          from driving a sedan at 50 miles per hour to driving a Lamborghini at
          200 miles per hour.
        </p>
        <ul class="tech-ul">
          <li>
            <b>Performance Boost</b>: First and foremost, there’s a noticeable
            improvement in rendering speed, primarily due to well-optimized
            Virtual DOM (VD) handling.
          </li>
          <li>
            <b>Reduced Development Time</b>: As the project size increases, the
            development time invested is more efficient compared to Vue.js.
          </li>
          <li>
            <b>Robust Community</b>: The abundance of resources in the
            development community makes it efficient to find solutions when
            issues arise.
          </li>
          <li>
            <b>Flexibility</b>: Higher code autonomy allows developers to write
            shorter and more concise code based on their skills.
          </li>
          <li>
            <b>Component Reusability</b>: Developing reusable components through
            the use of hooks is efficient and effective.
          </li>
          <li>
            <b>Development Simplicity</b>: The method-based approach of React
            simplifies lifecycles, making development smoother.
          </li>
        </ul>
        <div class="tech-title" id="anchor5">Conclusion</div>
        <p class="tech-contents-text">
          The content provided reflects the subjective perspective of the
          Machbase Neo development team. Different development organizations may
          hold varying opinions, and the strengths and weaknesses of each
          framework can differ based on their use cases. For this reason, we
          strongly advise not to take this document as absolute truth but to
          conduct your own development, testing, and draw your own conclusions.
        </p>
        <p class="tech-contents-text">
          Regardless, the Machbase Neo team is highly satisfied with the current
          situation, where development speed has increased, and most
          importantly, response times have become more pleasant. We hope that
          these experiences may prove helpful to other communities. With that,
          we conclude.
        </p>
        <p class="tech-contents-text">Thank you.</p>
      </div>
    </div>
  </div>
</section>
<footer>
  <div class="footer_inner">
    <div class="footer-logo">
      <img class="footer-logo-img" src="../../img/machbase-logo-w.png" />
      <a href="/home/contactus">
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
          <a href="https://medium.com/machbase" target="_blank"
            ><img class="sns-img" src="../../img/medium.png"
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
          <a href="https://medium.com/machbase" target="_blank"
            ><img class="sns-img" src="../../img/medium.png"
          /></a>
        </div>
      </div>
      <a href="/home/contactus">
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
    if (userLang !== "ko") {
      sessionStorage.setItem("lang", userLang);
      language = "en";
    } else {
      sessionStorage.setItem("lang", "ko");
      language = "kr";
      location.href = location.origin + "/kr" + location.pathname;
    }
  }
  function changeLanguage() {
    var languageSelector = document.getElementById("languageSelector");
    var selectedLanguage = languageSelector.value;
    if (selectedLanguage === "kr") {
      location.href = location.origin + "/kr" + location.pathname;
    } 
}
  function changeLanguage2() {
    var languageSelector = document.getElementById("languageSelector2");
    var selectedLanguage = languageSelector.value;
    if (selectedLanguage === "kr") {
      location.href = location.origin + "/kr" + location.pathname;
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
