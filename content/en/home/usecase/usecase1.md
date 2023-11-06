---
title: Use Case
description: "Hyundai Global Services is a company that provides real-time ship operation information to ship owners and performs onshore control services for ships manufactured by Hyundai Heavy Industries."
images:
  - /namecard/og_img.jpg
---

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" type="text/css" href="../../css/common.css" />
  <link rel="stylesheet" type="text/css" href="../../css/style.css" />
</head>
{{< home_menu_blog_en >}}
<section class="usecase_section0">
  <div>
    <h2 class="sub_page_title">Use Case</h2>
    <p class="sub_page_titletext">
      Machbase products are the choice of the world's leading companies and are
      in use in countless locations.
    </p>
  </div>
</section>
<section>
  <div class="tech-inner">
    <section>
      <div class="tech-inner">
        <h4 class="blog-title">[Machbase Use Case]Ship Management - Hyundai Global Services</h4>
        <ul class="tech-list-ul">
          <a href="#anchor1">
            <li class="tech-list-li" id="tech-list-li">Company Profile</li></a
          >
          <a href="#anchor2">
            <li class="tech-list-li" id="tech-list-li">Challenges</li></a
          >
          <a href="#anchor3">
            <li class="tech-list-li" id="tech-list-li">Reason for Selection</li>
          </a>
          <a href="#anchor4">
            <li class="tech-list-li" id="tech-list-li">Solution</li></a
          >
          <a href="#anchor5">
            <li class="tech-list-li" id="tech-list-li">Application Result</li>
          </a>
        </ul>
        <div class="tech-contents">
          <div>
            <div class="tech-img-wrap">
              <img
                class="tech-img"
                src="../../img/usecase_hyundai.png"
                alt=""
              />
            </div>
            <p class="tech-contents-link-text">
              Machbase solution Architecture
            </p>
            <p class="tech-title" id="anchor1">Company Profile</p>
            <p class="tech-contents-text">
              Hyundai Global Services is a company that provides real-time ship
              operation information to ship owners and performs onshore control
              services for ships manufactured by Hyundai Heavy Industries.
            </p>
            <p class="tech-title" id="anchor2">Challenges</p>
            <p class="tech-contents-text">
              to thousands of sensors are attached to the engines of ships,
              generating data in real time. Due to the nature of ships in
              operation, network communication is limited, so the data is
              transmitted using satellite communication, and the data is sent to
              the server in the form of a single CSV file.
            </p>
            <p class="tech-contents-text">
              At this time, there is an issue with storing the original CSV
              file, which is parsed and entered in real time according to the
              database’s storage schema. This is because CSV files collected
              from hundreds of ships must be processed in real time and data
              must be accumulated smoothly for a long period of time.
            </p>
            <p class="tech-title" id="anchor3">Reason for Selection</p>
            <p class="tech-contents-text">
              Hyundai Global Services selected Machbase through a comparison
              with InfluxDB in terms of performance and features.
            </p>
            <p class="tech-contents-text">
              They judged the excellent data processing performance of the
              Machbase developed in C language, stable system operation through
              redundancy, convenience of application development through SQL
              support, and operational technical support and maintenance as
              strengths.
            </p>
            <p class="tech-title" id="anchor4">Solution</p>
            <p class="tech-contents-text">
              Machbase developed a data collector that maps CSV files to the
              rules provided by Hyundai Global Services, preprocesses the data,
              and stores it in the DB. We also secured high availability by
              redundantly configuring the production DB and the backup DB.
            </p>
            <p class="tech-title" id="anchor5">Application Result</p>
            <p class="tech-contents-text">
              Machbase’s schema structure for time-series data allows it to
              flexibly respond to the addition of new ships or sensors without
              making changes to the existing schema, so it has been used with
              the same initial settings even as it has expanded from a few dozen
              ships in the beginning to hundreds of ships today.
            </p>
            <p class="tech-contents-text">
              Not only has the provision of real-time monitoring services made
              it possible to provide additional services to shipowners, but as
              data is collected and stored seamlessly, it is possible to develop
              new business insights through big data analysis through long-term
              data accumulation.
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</section>
{{< home_footer_blog_en >}}
{{< home_lang_en >}}
