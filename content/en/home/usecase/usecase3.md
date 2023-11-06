---
title: Use Case
description: "Mando Brose is a company specializing in automotive motors, founded in 2011 as a joint venture between Korea’s Mando Corporation and Germany’s Brose, a global auto parts company. It supplies ‘brushless electric motors’ for intelligent chassis systems in the global automotive industry and supplies motors for EPS (electric power steering) to major Korean automakers."
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
        <h4 class="blog-title">
          [Machbase Use Case]Manufacturing - Mando Brose
        </h4>
        <ul class="tech-list-ul">
          <a href="#anchor1">
            <li class="tech-list-li" id="tech-list-li">Company Profile</li> </a
          ><a href="#anchor2">
            <li class="tech-list-li" id="tech-list-li">Challenges</li></a
          >
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
              <img class="tech-img" src="../../img/usecase_mando.png" alt="" />
            </div>
            <p class="tech-contents-link-text">
              Machbase solution Architecture
            </p>
            <p class="tech-title" id="anchor1">Company Profile</p>
            <p class="tech-contents-text">
              Mando Brose is a company specializing in automotive motors,
              founded in 2011 as a joint venture between Korea’s Mando
              Corporation and Germany’s Brose, a global auto parts company.
            </p>
            <p class="tech-contents-text">
              It supplies ‘brushless electric motors’ for intelligent chassis
              systems in the global automotive industry and supplies motors for
              EPS (electric power steering) to major Korean automakers.
            </p>
            <p class="tech-title" id="anchor2">Challenges</p>
            <p class="tech-contents-text">
              The company wanted to build a facility status monitoring system by
              collecting data from production facilities in real time, and
              needed to collect multiple PLC data for each production line and
              monitor the status of each line. In addition, alarms and process
              progress data needed to be communicated through an interface with
              the existing MES system and displayed on the MES screen.
            </p>
            <p class="tech-title" id="anchor3">Reason for Selection</p>
            <p class="tech-contents-text">
              Machbase has Edge Master, an edge computing solution based on a
              time series database, so we were able to build a data collection
              infrastructure in a short period of time by simply installing the
              package without any additional development. We also proposed a
              solution to prevent data loss even if there is a failure such as a
              network disconnection because the time series database can be
              embedded in the edge device to collect and store data in the first
              place.
            </p>
            <p class="tech-contents-text">
              They were using Mensch and Mitsubishi PLCs, and Edge Master has
              its own data collection application that supports those protocols,
              so it was easy to set up and collect PLC data.
            </p>
            <p class="tech-title" id="anchor4">Solution</p>
            <p class="tech-contents-text">
              A total of seven edge devices were built with Machbase time series
              DB and deployed for each production line. The data collected by
              the edge devices was automatically transmitted to the central
              server in real time for storage. Alarms and progress data required
              by the MES were transmitted from the edge devices through an
              interface with MS-SQL.
            </p>
            <p class="tech-title" id="anchor5">Application Result</p>
            <p class="tech-contents-text">
              With alarms and progress data available in the MES system, process
              status can be monitored in real time. In addition, facility data
              can be analyzed in big data, laying the foundation for quality
              analysis and facility predictive maintenance.
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</section>
{{< home_footer_blog_en >}}
{{< home_lang_en >}}
