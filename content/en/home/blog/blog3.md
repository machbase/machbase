---
title: Blog
description: "Semiconductor Production Data using MACHBASE(Time-Series Database)"
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
      Semiconductor Production Data using MACHBASE(Time-Series Database)
    </h4>
    <div class="blog-date">
      <div>
        <span>by Grey Shim / 21 Aug 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">Introduction</li></a
      >
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">
          Problems with data processing
        </li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">
          Definition of Target Data for Search
        </li>
      </a>
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">
          Data Preprocessing for Machbase TAG Table
        </li>
      </a>
      <a href="#anchor5">
        <li class="tech-list-li" id="tech-list-li">Data Retrieval</li>
      </a>
      <a href="#anchor6">
        <li class="tech-list-li" id="tech-list-li">Conclusion</li>
      </a>
    </ul>
    <div class="tech-contents">
      <div>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/manage_1.jpg" alt="" />
        </div>
        <p class="tech-contents-link-text">
          Photo by
          <a
            class="tech-contents-link"
            href="https://unsplash.com/ko/@jonassvidras?utm_source=medium&utm_medium=referral"
            >Jonas Svidras</a
          >
          on
          <a
            class="tech-contents-link"
            href="https://unsplash.com/ko?utm_source=medium&utm_medium=referral"
            >Unsplash</a
          >
        </p>
        <p class="tech-title" id="anchor1">Introduction</p>
        <p class="tech-contents-text">
          Semiconductor production data consists of a combination of information
          from various sensors attached to manufacturing equipment and details
          about the produce chip. This data is substantial, and depending on the
          frequency at which sensors transmit information, the production data
          for just one semiconductor wafer can reach several gigabytes.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/manage_2.jpg"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          Semiconductor production data is being recorded in the format
          described above. This data is transformed into XML files and stored in
          systems like Hadoop, which is a NoSQL big data processing system, for
          analysis. Alternatively, the mentioned data is also processed by
          storing it in the form of XML-formatted BLOB columns within a
          relational database management system (RDBMS).
        </p>
        <p class="tech-contents-text">
          In reality, the data from each sensor is included within the wafer XML
          files, making it unsuitable for examining the trends of sensor values
          over time.
        </p>
        <div class="tech-title" id="anchor2">Problems with data processing</div>
        <p class="tech-contents-text">
          The method of recording sensor data based on the production item (as
          described in the introduction) has encountered various issues in
          practical situations. These issues are commonly encountered in the
          processing of large volumes of sensor data, and we will once again
          examine them here.
        </p>
        <p class="tech-contents-text">
          · <b>Using Hadoop</b>, handling massive and rapid data input is not an
          issue. However, when it comes to reading sensor data for desired
          statistical analysis, it takes too much time, making real-time
          analysis unfeasible. Introducing tools like Spark can enhance search
          performance, but setting up a large-scale cluster is necessary,
          leading to significant hardware investment costs.
        </p>
        <p class="tech-contents-text">
          · <b>RDBMS</b> encounters issues with slow data input speeds, causing
          problems when trying to input the desired amount of data. While
          certain appliances can improve input speeds to a certain extent,
          substantial costs are involved, and a satisfactory level is still not
          achieved.
        </p>
        <p class="tech-contents-text">
          To address these challenges, we have been recently experimenting with
          using a specialized database for time-series sensor data called
          “Machbase” to handle data processing. In this post, we will explore
          how to configure the database structure of Machbase to achieve fast
          data input and enable users to perform the desired data searches.
        </p>
        <div class="tech-title" id="anchor3">
          Definition of Target Data for Search
        </div>
        <p class="tech-contents-text">
          The Machbase Tag table efficiently stores sensor values on an hourly
          basis, allowing for swift searches based on sensor tag identifiers and
          time ranges. This characteristic also extends to the sensor data of a
          myriad of aquariums. However, when it comes to storing and retrieving
          production information (such as which wafer each sensor was producing
          at a specific time, and the recipe employed at that moment), the
          performance of this Tag table faces limitations. An example of the
          search interface desired by the customers is as follows:
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/manage_3.jpg"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          In this illustration, the customer wants to visualize sensor data or
          display statistical values for each sensor without specifying a
          particular sensor tag or time range. To do this, he selects the
          equipment module where the sensor is installed instead of a specific
          time range, and the lot number or wafer number of the produced wafers.
          To expedite this data retrieval, we need to input the semiconductor
          production wafer data through further processing.
        </p>
        <div class="tech-title" id="anchor4">
          Data Preprocessing for Machbase TAG Table
        </div>
        <p class="tech-contents-text">
          As mentioned earlier, semiconductor production data recorde in a
          manner where sensor data is dependent on specific wafers or lot
          products. However, for better performance in Markbase, it’s beneficial
          to separate sensor data from process data. Therefore, data needs to
          transform into the following format.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/manage_4.jpg"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          In the figure above, for each production lot, the time it enters and
          exits each machine and the corresponding lot number is recorded. This
          information is stored in the table “Lot_eq_start_end”. We define this
          table as process data (PROCESS_DATA).
        </p>
        <p class="tech-contents-text">
          Since each sensor is installed on a specific piece of equipment, the
          tag identifier of each sensor is retrievable in relation to that piece
          of production equipment. This sensor tag is considered metadata. An
          E-R diagram representation of these relationships is shown below.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/manage_5.jpg"
            alt=""
          />
        </div>
        <div class="tech-title" id="anchor5">Data Retrieval</div>
        <p class="tech-contents-text">
          Now that we have metadata for searching sensor tag IDs by equipment
          and process data for the manufactured products, the desired outcome
          can be achieved by joining the three tables together.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/manage_6.jpg"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          In Machbase, when conducting a search based on specific equipment and
          lot criteria for 1 million tags and a total of 10 billion records, we
          can retrieve a total of 900,000 search results in less than 0.1
          seconds. This observes on hardware with 4 cores and 32GB SSD.
          Furthermore, it confirmes that maintaining consistent performance is
          possible even when scaling up the total volume of data.
        </p>
        <div class="tech-title" id="anchor6">Conclusion</div>
        <p class="tech-contents-text">
          We have examined the limitations of using Hadoop and RDBMS for
          processing semiconductor production data and the solutions provided by
          time-series DBMS. Markbase’s time-series DBMS offers exceptional
          high-speed capabilities for data input, retrieval, and analysis,
          surpassing the constraints of conventional data processing systems in
          semiconductor production. We have also explored the data processing
          and retrieval methods necessary when applying Markbase.
        </p>
        <p class="tech-contents-text">
          This approach holds value not only for semiconductor production but
          also for various other industries. If there are additional technical
          details or advancements in the future, I will address them in separate
          posts.
        </p>
        <p class="tech-contents-text">Thank you.</p>
        <p class="tech-contents-text">Kwanghoon Shim, CRO of Machbase</p>
      </div>
    </div>
  </div>
</section>
{{< home_footer_blog_en >}}
{{< home_lang_en >}}
