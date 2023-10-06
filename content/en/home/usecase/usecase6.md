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
          <a href="/home"><img src="../../img/machbase_logo_b.png" alt="" /></a>
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
                href="https://www.cems.ai/"
                target="_blank"
                >CEMS</a
              >
            </div>
          </div>
        </li>
        <li class="menu-a"><a href="/">Docs</a></li>
        <li class="menu-a"><a href="/home/blog">Blog</a></li>
        <li class="menu-a"><a href="/home/customers">Customers</a></li>
        <li class="menu-a"><a href="/home/usecase">Use Case</a></li>
        <li class="menu-a"><a href="/home/company">Company</a></li>
      </ul>
    </div>
    <div class="menu-right">
      <ul class="menu-right-ul">
        <li class="menu-a"><a href="/home/download">Download</a></li>
        <li class="menu-a"><a href="https://support.machbase.com/hc/en-us">Support</a></li>
        <li class="menu-a"><a href="/home/contactus">Contact US</a></li>
      </ul>
    </div>
  </div>
</nav>
 <section class="usecase_section0">
        <div>
            <h1 class="sub_page_title">Use Case</h1>
            <p class="sub_page_titletext">Machbase products are the choice of the world's leading companies and are in use in countless locations.</p>
        </div>
    </section>
    <section>
        <div class="tech-inner">
            <section>
                <div class="tech-inner">
                    <h4 class="blog-title">[Machbase Use Case] Insurance - Carrot Insurance</h4>
                    <ul class="tech-list-ul">
                    <a href="#anchor1">
                        <li class="tech-list-li" id="tech-list-li">Company Profile</li>
                        </a><a href="#anchor2">
                        <li class="tech-list-li" id="tech-list-li">Challenges</li>
                        </a>
                        <a href="#anchor3">
                        <li class="tech-list-li" id="tech-list-li">Reason for Selection</li>
                        </a>
                        <a href="#anchor4">
                        <li class="tech-list-li" id="tech-list-li">Solution</li>
                        </a>
                        <a href="#anchor5">
                        <li class="tech-list-li" id="tech-list-li">Application Result</li>
                        </a>
                    </ul>
                    <div class="tech-contents">
                        <div>
                            <div class="tech-img-wrap">
                                <img class="tech-img" src="../img/usecase_carrot.png" alt="" />
                            </div>
                            <p class="tech-contents-link-text">Machbase solution Architecture</p>
                            <p class="tech-title" id="anchor1">Company Profile</p>
                            <p class="tech-contents-text">
                                As Korea’s first digital non-life insurer, Carrot Insurance is redefining insurance by launching new products and services based on technology and data, and is
                                experiencing rapid growth as an insurtech platform. In auto insurance, they are actively engaged in per-mile auto insurance.
                            </p>
                            <p class="tech-title" id="anchor2">Challenges</p>
                            <p class="tech-contents-text">
                                Carrot plugin, whose main business is a product that measures the mileage of a vehicle by mounting its own IoT product to the vehicle’s cigarette lighter and charges
                                insurance premiums based on the mileage, needed to build a stable infrastructure without service interruption even if a failure occurs to collect real-time data on
                                vehicle operation information, and also needed to build a system that secures data collection performance even if the number of subscribers increases.
                            </p>
                            <p class="tech-title" id="anchor3">Reason for Selection</p>
                            <p class="tech-contents-text">
                                The database has a Cluster. Edition that enables distributed storage and distributed processing of data using multiple servers, and the performance to enter and store
                                hundreds of thousands of data per second was guaranteed. Above all, fast and smooth technical support is necessary for stable service, and they judged technical support
                                as a strength compared to open source.
                            </p>
                            <p class="tech-title" id="anchor4">Solution</p>
                            <p class="tech-contents-text">
                                They used cloud instances for data rather than physical servers, and built a Machbase cluster using three instances. Both the master and data nodes were redundant to
                                prevent SPOF (Single Point Of Failure) and configured for automatic fail-over in case of failure. HA and scale-out are also supported, enabling a stable service 24
                                hours a day, 365 days a year.
                            </p>
                            <p class="tech-title" id="anchor5">Application Result</p>
                            <p class="tech-contents-text">
                                At the beginning of the service, the system was built for less than 100,000 subscribers, but after a considerable period of time, the number of subscribers has
                                increased to 800,000.
                            </p>
                            <p class="tech-contents-text">
                                Despite this, the stable cluster operation has made it possible to collect real-time information on subscribers’ vehicle driving and charge insurance premiums based on
                                it.
                            </p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    </section>
<footer>
  <div class="footer_inner">
    <div class="footer-logo">
      <img class="footer-logo-img" src="../../img/machbase_logo_w.png" />
      <a href="/home/contactus">
      <button class="contactus">
        Contact Us
      </button>
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
    <div class="logo">
      <img class="footer-logo-img" src="../../img/machbase_logo_w.png" />
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
      <button class="contactus">
        Contact US
      </button>
      </a>
    </div>
  </div>
  <div class="machbase_right">
    <p>@2023 MACHBASE All rights reserved.</p>
  </div>
</footer>
