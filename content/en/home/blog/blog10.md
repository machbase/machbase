---
title: Blog
description: "How to make Sensor Data send directly to a Database via MQTT?"
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
      How to make Sensor Data send directly to a Database via MQTT?
    </h4>
    <div class="blog-date">
      <div>
        <span>by Eirny Kwon / 2 Nov 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">Introduction</li></a
      >
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">
          Features of the MQTT protocol
        </li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">
          Structure of MQTT packets
        </li>
      </a>
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">
          MQTT and IoT applications
        </li>
      </a>
      <a href="#anchor5">
        <li class="tech-list-li" id="tech-list-li">
          Machbase and Machbase Neo
        </li>
      </a>
      <a href="#anchor6">
        <li class="tech-list-li" id="tech-list-li">Conclusion</li>
      </a>
    </ul>
    <div class="tech-contents">
      <p class="tech-contents-text">
        The MQTT protocol is an OASIS open standard (ISO/IEC 2092).
      </p>
      <div>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/blog10-1.jpg" alt="" />
        </div>
        <p class="tech-contents-link-text">
          Photo by
          <a
            class="tech-contents-link"
            href="https://unsplash.com/ko/@markusspiske?utm_medium=referral&utm_source=medium"
            >Markus Spiske</a
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
          In 1999, an early version of the protocol was written by Andy
          Stanford-Crack (IBM) and Alan Nipper (then at Eurotech) and used to
          monitor pipelines with Supervisory Control and Data Acquisition
          (SCADA) control systems. The design goal was to be bandwidth
          efficient, lightweight, and minimize battery consumption, as the
          systems of the time were heterogeneous and supported only their
          proprietary protocols, so they could not interoperate with each other,
          but had to be connected via satellite links, which were prohibitively
          expensive at the time.
        </p>
        <p class="tech-contents-text">
          The “MQ” in “MQTT” historically comes from the IBM MQ (Message
          Queuing) product line, which was called MQ (then MQSeries). Despite
          the name “Queue”, the protocol only defines the PUBLISH-SUBSCRIBE
          message transfer and does not specify a queue. The 3.1 version of the
          specification published by IBM states that MQTT is short for “MQ
          Telemetry Transport”, but subsequent versions published by OASIS refer
          to the protocol simply as “MQTT”.
        </p>
        <p class="tech-contents-text">
          Despite the name of the OASIS technical committee being “OASIS Message
          Queuing Telemetry Transport Technical Committee”, it was defined at a
          2013 technical committee meeting that “MQTT” should not stand for
          anything. [OASIS_MQTT_TC_minutes_25042013.pdf (oasis-open.org)]<a
            class="tech-link"
            href="https://www.oasis-open.org/committees/download.php/49028/OASIS_MQTT_TC_minutes_25042013.pdf"
            >(https://www.oasis-open.org/committees/download.php/49028/OASIS_MQTT_TC_minutes_25042013.pdf)</a
          >
        </p>
        <p class="tech-contents-text">
          In 2013, IBM submitted MQTT v3.1 with minor changes to OASIS, and on
          29 October 2014, OASIS released version 3.1.1 after taking over
          stewardship of the standard from IBM. MQTT version 5 was released on 7
          March 2019. It can be considered a significant upgrade with new
          features.
        </p>
        <p class="tech-contents-text">
          Note that the MQTT for Sensor Networks (MQTT-SN) specification is a
          variant of MQTT that targets battery-powered embedded devices on
          non-TCP/IP networks (e.x. Zigbee).
        </p>
        <div class="tech-title" id="anchor2">Features of the MQTT protocol</div>
        <p class="tech-contents-text">
          1. Connection-oriented <br />
          A client requesting a connection with an MQTT server is designed to
          establish a TCP/IP socket and then stay connected and send messages
          until it explicitly disconnects or is disconnected due to network
          issues.
        </p>
        <p class="tech-contents-text">
          2. Publish-Subscribe<br />
          In the publish-subscribe model of topic-based messages, there is no
          direct transmission or reception of messages between clients, and all
          messages can only be linked through a server (or broker).
        </p>
        <p class="tech-contents-text">
          3. Quality of Service (QoS)<br />
          When sending a message to a target topic, you can set the QoS to 0, 1,
          or 2.<br />
          - 0 : Maximum one transmission, no guarantee of message delivery.<br />
          - 1 : Guarantees at least one delivery, but the same message may be
          sent multiple times.<br />
          - 2 : Guarantees that the message is sent exactly once with no
          duplicates.
        </p>
        <p class="tech-contents-text">
          4. Types of messages<br />
          The following messages are defined in the MQTT specification.<br />
          - CONNECT, CONNACK<br />
          - DISCONNECT<br />
          - PUBLISH, PUBACK, PUBREC, PUBREL, PUBCOMP<br />
          - SUBSCRIBE, SUBACK<br />
          - UNSUBSCRIBE, UNSUBACK<br />
          - PINGREQ, PINGRESP<br />
        </p>
        <p class="tech-contents-text">
          MQTT messages are used in a wide variety of applications, from
          enterprise applications to gaming and entertainment, because they have
          little overhead (two-byte fixed headers and variable-length headers,
          except for the topic path), support QoS, and provide flexibility for a
          wide range of applications. In particular, it is becoming the standard
          for telemetry transmission in the IoT.
        </p>
        <div class="tech-title" id="anchor3">Structure of MQTT packets</div>
        <p class="tech-contents-text">
          A packet consists of a fixed 2-byte header that must always exist, a
          header that can vary in size, followed by the payload as shown below.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-2.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          The first four bits indicate the type of packet. They are defined as
          follows.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-3.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          The lower four bits then display additional flags in the control
          command. Only the defined values should be used in messages other than
          the PUBLISH message.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-4.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          The basic message sequence for an application using MQTT is shown in
          the figure below. The Clients, Publisher, and Subscriber, send a
          CONNECT message to the server, Broker, and Broker returns CONNECT in
          response. The Subscriber makes a SUBSCRIBE request to the topic of
          interest and the response is a SUBACK. PUBLISH is a message sent by
          the publisher to the target topic or by the broker to the subscriber,
          and if QoS 1, the receiver acknowledges receipt with PUBACK.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-5.jpg"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          The following fields may be included in a CONNECT message.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-6.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          When the server responds to a client’s CONNECT request with CONNACK,
          the response code has the following meaning
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-7.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          Sending and receiving server-to-client messages is done via PUBLISH
          messages. The following fields can be set.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-8.webp"
            alt=""
          />
        </div>
        <div class="tech-title" id="anchor4">MQTT and IoT applications</div>
        <p class="tech-contents-text">
          At a simplified level, most applications of MQTT in the IoT space look
          like the image below.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-9.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          Telemetry data collected from sensors is sent to a pre-arranged MQTT
          broker topic in a format such as JSON or CSV, and the server-side
          application subscribing to the topic receives the message from the
          broker and stores it in a database, and the application accesses the
          database to retrieve or process the data as needed.
        </p>
        <p class="tech-contents-text">
          This is probably the most common and familiar architecture and may
          seem obvious. However, over the course of many IoT projects, both
          large and small, we’ve seen the problems that this structure brings,
          and they usually boil down to the following.
        </p>
        <p class="tech-contents-title">Issue 1) Availability of MQTT Broker</p>
        <p class="tech-contents-text">
          There are several quality MQTT brokers out there, including open
          source. These brokers are mature and work well on their own. Having
          implemented these brokers in various types of IoT projects, I have
          found that the availability of the MQTT broker is directly dependent
          on the availability of the entire IoT service. Since all data is
          communicated through the broker, the availability of the overall
          service can never exceed the availability of the MQTT broker used,
          which means that the development and operational know-how of the
          chosen broker is the most important factor in determining the quality
          of the overall service. Accumulating sufficient technical skills on an
          easily accessible open-source broker has become as much or more of an
          effort than making the application you’re trying to develop stable,
          and what was once a secondary component has become a key one.
        </p>
        <p class="tech-contents-title">Issue 2) Managing “redundant” storage</p>
        <p class="tech-contents-text">
          The purpose of an MQTT Broker is to ensure that messages sent by
          sensors (Publishers) are delivered correctly and without loss to
          ingesting applications that are subscribing to the topic. In this
          context, “lossless delivery” means that the broker itself must first
          store the messages it receives in some form of memory. The store and
          forward strategy is a common design strategy for all message brokers,
          not just MQTT. The ingestion application, which receives the messages
          forwarded by the broker, transforms them into a serviceable structure
          and stores them (in a database such as an RDBMS or NoSQL). Once the
          system is deployed, two types of storage (MQTT’s storage and the
          application’s storage) must be managed to keep the service running
          reliably and to cope with failures. And when new types of sensors are
          added or data types are added, the collection application must be
          further developed or modified.
        </p>
        <p class="tech-contents-text">
          As a result, every IoT service developer or system architect starts
          with the question: Do I always have to bear the burden of managing
          “redundant” storage with the operation of an MQTT broker? and ends up
          with the question: How can I efficiently process large amounts of IoT
          data? to the question of how to efficiently process large amounts of
          IoT data.
        </p>
        <div class="tech-title" id="anchor5">Machbase and Machbase Neo</div>
        <p class="tech-contents-text">
          What if the sensor sends telemetry data directly to the database via
          MQTT? It would look something like this.
        </p>
        <p class="tech-contents-text">Traditional architecture:</p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-9.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          Leveraging the MQTT interface as Machbase sees it:
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-10.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          The existence of this type of database solves the problem of managing
          MQTT broker operations and managing redundant storage operations to
          prevent message loss. Additionally, the need for a collection
          application could be eliminated. Sensors would continue to send
          telemetry data via MQTT and applications could retrieve the required
          data via the HTTP Restful API provided by the database or via the
          standard database interface of the programming language (JDBC, ODBC,
          Go Driver…).
        </p>
        <p class="tech-contents-text">
          Machbase Neo is the result of this approach.(<a
            class="tech-link"
            href="https://machbase.com/neo"
            >https://machbase.com/neo</a
          >)
        </p>
        <p class="tech-contents-text">
          Machbase is the world’s №1 performance database, certified by tpc.org
          (see TPCx-IoT V2,
          <a
            class="tech-link"
            href="https://www.tpc.org/tpcx-iot/results/tpcxiot_perf_results5.asp?version=2"
            >https://www.tpc.org/tpcx-iot/results/tpcxiot_perf_results5.asp?version=2</a
          >), and machbase-neo combines Machbase with IoT-oriented convenience
          features such as an MQTT server. All features are distributed in a
          single executable file, so it can be installed by simply copying the
          file, and the UX is implemented to suit the development workflow of
          IoT developers.
        </p>
        <p class="tech-contents-text">
          For the sake of brevity, we’ll take a quick look at Machbase-neo’s
          MQTT interface for storing data from sensors. For more details, you
          can refer to the documentation and tutorials on the official site(<a
            class="tech-link"
            href="https://machbase.com/neo"
            >(https://machbase.com/neo)</a
          >) For the sake of demonstration, we’ll be testing MQTT with the
          mosquito_pub command, so you’ll need to have the mosquito-client tool
          installed first. And machbase-neo can be downloaded from the site or
          by running the command below. (Note: Windows users should download it
          directly from the release page on the site).
        </p>
        <div class="tech-code-box">
          <span
            >$ sh -c "$(curl -fsSL https://machbase.com/install.sh)"</span
          >
        </div>
        <p class="tech-contents-text">
          Unzip the downloaded archive and copy the “machbase-neo” executable to
          your desired location. Complete the installation.
        </p>
        <p class="tech-contents-text">
          When you run machbase-neo serve, it creates a database and runs as
          shown below. As shown on the screen, the MQTT server is opened on port
          5653 and the HTTP server on port 5654.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog10-11.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          Then use the command below to create the tables we need for the demo.
        </p>
        <div class="tech-code-box">
          <span
            >$ curl -o - http://127.0.0.1:5654/db/query \<br />
            &nbsp;&nbsp;&nbsp;&nbsp;--data-urlencode \<br />
            &nbsp;&nbsp;&nbsp;&nbsp;"q=create tag table EXAMPLE (name
            varchar(40) primary key, time datetime basetime, value
            double)"</span
          >
        </div>
        <p class="tech-contents-text">
          Now we can mimic the sensor sending data to MQTT with mosquito_pub as
          shown below. If you look at the topic path, you can see that the table
          name EXAMPLE is used.
        </p>
        <div class="tech-code-box">
          <span
            >$ mosquitto_pub -h 127.0.0.1 -p 5653 \<br />
            &nbsp;&nbsp;&nbsp;&nbsp;-t db/append/EXAMPLE \<br />
            &nbsp;&nbsp;&nbsp;&nbsp;-m '[ "my-car", 1670380342000000000, 32.1
            ]'</span
          >
        </div>
        <p class="tech-contents-text">
          Applications can retrieve data entered via HTTP.
        </p>
        <div class="tech-code-box">
          <span
            >$ curl -o - http://127.0.0.1:5654/db/query \<br />
            &nbsp;&nbsp;&nbsp;&nbsp;--data-urlencode "q=select * from EXAMPLE"
          </span>
        </div>
        <div class="tech-title" id="anchor6">Conclusion</div>
        <p class="tech-contents-text">
          I believe Machbase Neo(<a
            class="tech-link"
            href="https://machbase.com/neo"
            >(https://machbase.com/neo)</a
          >) is a good example of how the technology accumulated in the
          development of time series databases can help solve the problems of
          developers in the IoT space. I hope this article will be useful for
          many developers and I invite you to visit our GitHub(<a
            class="tech-link"
            href="https://github.com/machbase/neo-server"
            >(https://github.com/machbase/neo-server)</a
          >) for more information and to help and contribute to the community.
        </p>
        <p class="tech-contents-text">by Eirny Kwon</p>
      </div>
    </div>
  </div>
</section>
{{< home_footer_blog_en >}}
