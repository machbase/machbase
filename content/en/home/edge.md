---
title: Edge Computing and Time series database
description: "Edge Computing refers to the practice of processing data closer to its source, right at the edge of the network, rather than sending all data to centralized cloud servers for analysis."
images:
  - /namecard/og_img.jpg
---

<head>
  <link rel="stylesheet" type="text/css" href="../css/common.css" />
  <link rel="stylesheet" type="text/css" href="../css/style.css" />
</head>
<body>
 {{< home_menu_sub_en >}}
  <section class="product_sction0 section0">
    <div>
      <h2 class="sub_page_title">Tech Paper</h2>
      <p class="sub_page_titletext">
        “ Discover the top DBMS suites for edge computing and take your data
        processing to the next level ”
      </p>
    </div>
  </section>
  <section>
    <div class="tech-inner">
      <h4 class="sub_title main_margin_top">
        Edge Computing and Time series database
      </h4>
      <div class="bar"><img src="../img/bar.png" /></div>
      <div class="tech-contents">
        <div>
          <div class="tech-title">Why Edge Computing?</div>
          <p class="tech-contents-text">
            In recent years, Edge Computing has emerged as a pivotal
            technological concept, transforming the way we process and manage
            data. This paradigm shift has gained immense significance due to the
            growing proliferation of Internet of Things (IoT) devices and the
            increasing need for real-time, localized data processing. Edge
            Computing refers to the practice of processing data closer to its
            source, right at the "edge" of the network, rather than sending all
            data to centralized cloud servers for analysis. This approach brings
            several advantages, and this is where your software, a specialized
            time-series database engine, plays a crucial role.
          </p>
          <p class="tech-contents-title">The Importance of Edge Computing:</p>
          <ul class="tech-ul">
            <li>
              Low Latency and Real-time Processing: Applications that require
              real-time decision-making, such as industrial automation,
              autonomous vehicles, and remote monitoring, cannot afford the
              latency involved in sending data to distant data centers. Edge
              Computing reduces this delay by processing data locally, enabling
              quick responses.
            </li>
            <li>
              Bandwidth Efficiency: Transmitting large volumes of raw data to
              centralized cloud servers demands substantial bandwidth. Edge
              Computing reduces the amount of data transferred by sending only
              relevant, processed information, optimizing network usage and
              cost.
            </li>
            <li>
              Privacy and Security: Edge Computing addresses concerns about data
              privacy and security by keeping sensitive data localized. This
              mitigates potential risks associated with transmitting sensitive
              information over public networks.
            </li>
            <li>
              Offline Functionality: Edge Computing allows devices to operate
              autonomously even when connectivity to the cloud is lost. This is
              crucial for scenarios where continuous functionality is essential.
            </li>
            <li>
              Scalability: With the rapid growth of IoT devices, centralized
              cloud processing might become a bottleneck. Edge Computing
              distributes the processing load, ensuring scalability without
              overwhelming cloud resources.
            </li>
          </ul>
        </div>
        <div>
          <div class="tech-title">
            The Role of Time-Series Database Engines in Edge Computing
          </div>
          <p class="tech-contents-text">
            Time-series data, which records values over time, is prevalent in
            IoT applications—temperature readings, stock prices, energy
            consumption, etc. Time-series database engines excel at efficiently
            storing, retrieving, and analyzing such data.
          </p>
          <p class="tech-contents-title">
            Here's how they contribute to Edge Computing:
          </p>
          <ul class="tech-ul">
            <li>
              Data Storage and Retrieval: Time-series databases are optimized
              for high-throughput storage and retrieval of time-stamped data.
              This ensures quick access to historical and real-time data,
              crucial for decision-making at the edge.
            </li>
            <li>
              Aggregation and Analysis: These databases allow you to perform
              complex analyses on time-series data, even in resource-constrained
              environments. Aggregations, downsampling, and statistical
              computations can provide meaningful insights.
            </li>
            <li>
              Compression: With edge devices often having limited storage,
              time-series databases offer data compression techniques, enabling
              efficient storage of vast amounts of data in constrained
              environments.
            </li>
            <li>
              Data Contextualization: Time-series databases enable
              contextualizing data by associating it with relevant metadata.
              This contextual information enhances the value of the data
              collected from edge devices.
            </li>
            <li>
              Event Triggering: Time-series databases can support
              event-triggering mechanisms, enabling real-time alerts and actions
              based on predefined conditions, directly enhancing the
              responsiveness of edge applications.
            </li>
          </ul>
          <p class="tech-contents-text">
            The rise of Edge Computing is closely tied to the proliferation of
            IoT devices and the need for efficient, real-time data processing.
            Ability to manage time-series data efficiently aligns perfectly with
            the demands of Edge Computing, enabling localized processing, quick
            decision-making, and optimized resource usage. As industries
            continue to adopt and leverage Edge Computing, Time series DBMS
            stands at the forefront of enabling this transformative
            technological trend.
          </p>
        </div>
        <div>
          <div class="tech-title">
            Edge Computing and Data Processing Requirements
          </div>
          <p class="tech-contents-text">
            How much data do you need to process at the edge, and how fast?<br /><br />The
            clearer the answer to this question, the more likely it is that the
            vision of the future presented by Edge Computing will be at the
            customer's level.<br /><br />
            As an extreme example, the data processing requirements for edge
            devices for real-time monitoring and management of NC (Numerical
            Control) equipment are about 1T Bytes of data every two weeks. To
            translate this value more precisely, it needs to digest 872,628
            bytes per second.<br /><br />Converting this to the average size of
            real-world sensor data (about 20 bytes), we calculate that it should
            be able to store about 400,000+ events per second.<br /><br />Not
            only does the edge device need to ingest 400,000+ sensor data per
            second, but it also needs to store it in a secondary storage device
            for real-time analysis.<br /><br />Furthermore, if the environment
            requires the edge device to support high availability, it will
            require a higher level of data processing technology.<br /><br />In
            the end, different industries will have different types of data,
            different forms of data, and different amounts of data, and the
            requirements in various forms will become more and more stringent
            over time.
          </p>
        </div>
        <div>
          <div class="tech-title">Machbase and Edge Computing</div>
          <p class="tech-contents-text">
            As a real-time time series database, Machbase already offers a
            standard edition for ultra-fast data processing on edge
            computing.<br /><br />It can store 400,000 sensor data per second on
            a Raspberry PI 4, while utilizing CPU and disk usage very
            efficiently.<br /><br />Even if it is an edge device, Machbase with
            big data technology can store data to the storage limit, and the
            search and analysis of big data is excellent.<br /><br />Depending
            on your future roadmap, you can build a cluster on multiple edge
            devices, which means that your edge computing needs for high
            performance and high availability are well supported. To summarize
            Machbase's performance<br />
          </p>
          <p class="tech-contents-title">In ingestion point of view</p>
          <ul class="tech-ul">
            <li>In edge Device (ARM 2 core) : up to 500,000 rec/sec</li>
            <li>In single Server (INTEL 8 core) : up to 2,500,000 rec/sec</li>
            <li>In Cluster (16 node) : up to 100,000,000 rec/sec</li>
          </ul>
          <p class="tech-contents-title">In extraction point of view</p>
          <ul class="tech-ul">
            <li>
              0.1 seconds for extracting 10,000 random time ranges from a 400
              billion data store
            </li>
          </ul>
          <p class="tech-contents-title">In compression point of view</p>
          <ul class="tech-ul">
            <li>4TB store : around 1 trillion record</li>
          </ul>
          <p class="tech-contents-text">
            As you can see, Machbase already fulfills a great data processing
            requirement for edge computing, and if you want to evaluate the
            product in more detail, download and test it.
          </p>
        </div>
      </div>
    </div>
  </section>
</body>
{{< home_footer_sub_en >}}
