---
title: Use Case
description: "Lotte Chilsung is a non-alcoholic beverage manufacturer that produces a variety of products including soda, tea, and fruit juice."
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
          [Machbase Use Case]Manufacturing - Lotte Chilsung
        </h4>
        <ul class="tech-list-ul">
          <a href="#anchor1">
            <li class="tech-list-li" id="tech-list-li">Company Profile</li> </a
          ><a href="#anchor2">
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
              <img class="tech-img" src="../../img/uscase_lotte.png" alt="" />
            </div>
            <p class="tech-contents-link-text">
              Machbase solution Architecture
            </p>
            <p class="tech-title" id="anchor1">Company Profile</p>
            <p class="tech-contents-text">
              Lotte Chilsung is a non-alcoholic beverage manufacturer that
              produces a variety of products including soda, tea, and fruit
              juice.
            </p>
            <p class="tech-title" id="anchor2">Challenges</p>
            <p class="tech-contents-text">
              SCADA system was built to collect data from beverage production
              facilities, and the alarm history of the facilities was collected
              and stored in MS-SQL. For digital transformation, Machbase was
              introduced to collect not only alarm history but also all tag data
              of production process equipment.
            </p>
            <p class="tech-contents-text">
              The performance of collecting and storing 200,000 data per second
              in real time was an important requirement, and periodic backup and
              instant retrieval of backed-up data were also needed.
            </p>
            <p class="tech-title" id="anchor3">Reason for Selection</p>
            <p class="tech-contents-text">
              Lotte Chilsung verified the product’s ability to collect 200,000
              data per second in real time through a proof of concept (PoC) and
              judged Machbase’s data entry performance, product quality, and
              seamless technical support as its strengths.
            </p>
            <p class="tech-title" id="anchor4">Solution</p>
            <p class="tech-contents-text">
              Due to the capacity limitations of the SSD disk, past data is
              backed up and stored on the HDD disk, and if necessary, the MOUNT
              function of the Machbase is used to immediately connect to the
              operating DB without the restore process to retrieve data.
            </p>
            <p class="tech-title" id="anchor5">Application Result</p>
            <p class="tech-contents-text">
              Big data analytics teams are extracting data stored in time series
              databases through JDBC or REST APIs and using data analysis tools
              such as R, Python, Grafana, and Tableau. for long-term trend
              analysis and quality cause analysis.
            </p>
            <p class="tech-contents-text">
              By being able to store and analyze the entire data generated in
              the production process at a low cost, we can expect to increase
              productivity by reducing the defect rate through analysis of the
              causes of defects in the production process and improving product
              quality.
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</section>
{{< home_footer_blog_en >}}
{{< home_lang_en >}}
