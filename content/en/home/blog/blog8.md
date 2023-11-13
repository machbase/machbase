---
title: Blog
description: "Time Series Database Architecture and Performance Comparison_Machbase and MongoDB when Processing Sensor Data"
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
      Time Series Database Architecture and Performance Comparison_Machbase and
      MongoDB when Processing Sensor Data
    </h4>
    <div class="blog-date">
      <div>
        <span>by Grey Shim / 14 Sep 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">Introduction</li></a
      >
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">
          Comparison of features and architectures of time-series sensor data
        </li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">
          Sensor data index vs B+Tree
        </li>
      </a>
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">
          Compare input and simple query performance
        </li>
      </a>
      <a href="#anchor5">
        <li class="tech-list-li" id="tech-list-li">Conclusion</li>
      </a>
    </ul>
    <div class="tech-contents">
      <div>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/blog8-1.webp" alt="" />
        </div>
        <p class="tech-contents-link-text"></p>
        <p class="tech-title" id="anchor1">Introduction</p>
        <p class="tech-contents-text">
          In this post, we will take some time to look at the architectural
          differences between Machbase and MongoDB and compare their performance
          in processing time-series sensor data. When developing a sensor data
          processing system, there is a strong tendency to choose a DBMS that
          the developer is familiar with. However, I would also like to describe
          the fact that there are unknown difficulties in data processing if
          developed using familiar tools without considering the characteristics
          of time series sensor data.
        </p>
        <div class="tech-contents-title">Machbase</div>
        <p class="tech-contents-text">
          Machbase is a DBMS developed for fast input, search, and statistics of
          time-series sensor data. It supports edge devices such as Raspberry
          Pi, as well as general single-server and multi-server clusters. It has
          features and architecture specialized for processing time-series
          sensor data and machine log data. Details regarding the architecture
          of Machbase continue below.
        </p>
        <div class="tech-contents-title">MongoDB</div>
        <p class="tech-contents-text">
          MongoDB is a document-based database engine that can store and
          retrieve schema-less data in the form of JSON, so it is very
          conveniently used in the web-related field. It is not very suitable
          for time-series sensor data applications, but since semiconductor
          production process data is created in the form of XML in production
          facilities, it seems to be used in many cases due to the convenience
          of use in this case.
        </p>
        <div class="tech-title" id="anchor2">
          Comparison of features and architectures of time-series sensor data
        </div>
        <p class="tech-contents-text">
          Time-series sensor data is a type of data in which the amount of unit
          data is small and continuously increases over time without being
          updated. It is a form in which only the value of the data per sensor
          is continuously changed in chronological order. As the number of
          installed sensors increases and the data collection cycle tends to
          shorten, the amount of data generated per unit time increases
          enormously.
        </p>
        <p class="tech-contents-text">
          Due to the mass generation of time series sensor data, it is
          challenging to develop systems for data storage and processing in
          situations where data needs to be kept for a long time. Retrieval of
          such data is often performed using time and sensor identifiers as
          keys, and input performance is critical for real-time processing.
        </p>
        <p class="tech-contents-text">
          In the next section, we will take a closer look at the comparison of
          different systems in this situation.
        </p>
        <div class="tech-contents-title">Schema vs schema-less</div>
        <p class="tech-contents-text">
          Machbase requires a schema definition, which is defined in SQL DDL by
          a relational model, while MongoDB does not require a schema.
        </p>
        <p class="tech-contents-text">
          It is a very common technique to define user-related configuration
          data for a website in the form of JSON and process it in a web
          application. MongoDB is very convenient for entering this data into
          MongoDB without modification, and for quickly retrieving this data by
          user ID. MongoDB stores data in the form of binary JSON. Take a look
          at the example below.
        </p>
        <div class="tech-code-box">
          <span>Bson:</span><br />
          \x16\x00\x00\x00&nbsp;&nbsp;<span class="green"
            >// total document size</span
          ><br />
          \x02&nbsp;&nbsp;<span class="green">// 0x02 = type String</span><br />
          hello\x00&nbsp;&nbsp;<span class="green">// field name</span><br />
          \x06\x00\x00\x00world\x00&nbsp;&nbsp;<span class="green"
            >// field value (size of value, value, null terminator)</span
          ><br />
          \x00&nbsp;&nbsp;<span class="green"
            >// 0x00 = type EOO ('end of object')</span
          ><br />
        </div>
        <p class="tech-contents-link-text">&lt; Source Wikiped ></p>
        <p class="tech-contents-text">
          Unstructured data is very simplified compared to textual JSON data,
          but for each attribute, it expresses the type, name, and length of the
          attribute. Because there is no schema, columns that were present in
          previous data may not be present in this data, and the length of the
          data is always in flux. To find the attribute you’re looking for,
          you’d have to read the entire BSON document, and it might not exist,
          or the attribute might be of a different type.
        </p>
        <p class="tech-contents-text">
          Schema data, on the other hand, always has constant column names and
          the same column type. You know right away where the column data you
          want is without having to parse the entire record.
        </p>
        <p class="tech-contents-text">
          Real-time sensor data is often treated as structured data. This data
          has pre-set column values and can be represented and processed in a
          fixed schema, which makes it efficient to use a structured data model.
        </p>
        <p class="tech-contents-text">Of course, MongoDB is also possible.</p>
        <p class="tech-contents-text">
          Here’s a quick comparison between structured and unstructured data:
        </p>
        <div class="tech-img-wrap">
          <img class="tech-img" src="../../img/blog8-2.webp" alt="" />
        </div>
        <p class="tech-contents-text">
          To convert unstructured data into structured data, you need to design
          a data model using an entity-relationship (ER) model, convert the raw
          data into appropriate tables, and enter it. However, this conversion
          process can make it difficult to accurately represent the data in
          certain cases.
        </p>
        <p class="tech-contents-text">
          On the other hand, unstructured databases like MongoDB are convenient
          because the data can be used as it is without any transformation.
          However, when searching unstructured data or performing statistics,
          real-time parsing of the data is required to obtain the column values
          of the desired data. This can cause performance degradation, and
          techniques such as distributed processing may need to be applied to
          address these performance issues. This can lead to additional server
          and cost issues.
        </p>
        <p class="tech-contents-text">
          When dealing with structured data, schema models provide a significant
          performance boost for processing large amounts of data because they
          can read directly from the data without parsing. When the data
          structure is structured, such as real-time time series data, the
          structured data model is much more efficient than MongoDB’s
          unstructured data model.
        </p>
        <div class="tech-contents-title">SQL vs No-sql</div>
        <p class="tech-contents-text">
          Machbase supports SQL as a data query language, and MongoDB has its
          own query methods. This section examines the differences between the
          two.
        </p>
        <p class="tech-contents-text">
          Typically, schema data is queried using a structured query language
          (SQL). No-SQL is also widely used these days, and each product handles
          it differently, so I’ll only describe MongoDB’s query language rather
          than provide a comprehensive description.
        </p>
        <p class="tech-contents-text">
          As mentioned earlier, MongoDB is optimized for applications like web
          services. In a web service, data is represented as JSON, and a set of
          this data is mapped to a collection object (a table in the relational
          data model). The main operation is to find the specific data you want
          by key value — a very simple query and most web services can cover
          pretty much what you want by entering data and finding the data by key
          value.
        </p>
        <div class="tech-code-box">
          <span>db.</span><span class="orange">collection.find</span>( {
          _id:<span class="blue">5</span>} )
        </div>
        <p class="tech-contents-text">
          You can extend the search condition clause further by listing the
          desired conditions in the Find method. This looks very natural in the
          object model.
        </p>
        <p class="tech-contents-text">
          What about time series data? For time series data, the most common
          query is to get data with a specific sensor ID over a specific time
          period. Of course, MongoDB can do this, but when you compare the two
          queries, you start to see differences.
        </p>
        <div class="tech-contents-title">Machbase Query (SQL)</div>
        <div class="tech-code-box">
          <span class="red">SELECT</span>&nbsp;*<br />
          <span class="red">FROM</span>&nbsp;tag<br />
          <span class="red">WHERE</span>&nbsp;name =
          <span class="orange">'EQ0^TAG287'</span><br />
          &nbsp;&nbsp;&nbsp;&nbsp;<span class="red">AND</span
          >&nbsp;time&nbsp;<span class="red">BETWEEN</span> to_date (<span
            class="orange"
            >'2018-01-01 00:00:00'</span
          >)<br />
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="red"
            >AND</span
          >
          to_date (<span class="orange">'2018-01-01 00:00:00'</span>) )
        </div>
        <p class="tech-contents-text">
          It’s very declarative and easy to understand: Get a day’s worth of
          data with a specific sensor identifier.
        </p>
        <div class="tech-contents-title">MongoDB Query</div>
        <div class="tech-code-box">
          <span>db.sensor.find(</span><span class="green">{name</span>:<span
            class="orange"
            >"EQ0^TAG287"</span
          >,<br />
          <span class="green">time</span>: {
          <span class="blue">$gte</span>:ISODate(<span class="orange"
            >"2018-01-01T00:00:00Z"</span
          >),<br />
          <span class="blue">$lt</span>:ISODate(<span class="orange"
            >"2018-01-02T00:00:00Z"</span
          >)}}).count()
        </div>
        <p class="tech-contents-text">
          Has the query language become a bit verbose and complex? Is it still
          relatively easy to use?
        </p>
        <div class="tech-contents-title">Statistics</div>
        <p class="tech-contents-text">
          Due to the large volume of time-series sensor data, it is often
          necessary to compute statistics on an hourly basis and visualize those
          values. Machbase automatically generates hourly statistics for this
          purpose, a feature referred to as “automatic Rollup execution,” which
          I will explain later. Using this statistical data, it is easy to
          obtain the desired hourly statistics, and it is also possible to
          retrieve statistical data using SQL.
        </p>
        <div class="tech-code-box">
          <span class="red">SELECT</span
          ><span class="green"> /*+ ROLLUP(TAG, hour, max) */ </span>time,
          <span class="red">value as</span> max<br />
          <span class="red">FROM</span> TAG<br />
          <span class="red">FROM</span> name =
          <span class="ornage">'EQ1^TAG1024'</span>
          <span class="red"> AND</span> time
          <span class="red">BETWEEN</span> to_date(<span class="orange"
            >'2018-01-01 00:00:00'</span
          >)<br />
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="red"
            >AND</span
          >
          to_date (<span class="orange">'2018-01-01 23:59:59'</span>) )<br />
          <span class="red">ORDER BY</span> time<br />
        </div>
        <p class="tech-contents-text">
          Using the ROLLUP hint, we’ve shown a precomputed statistic without
          actually performing the statistic.
        </p>
        <p class="tech-contents-text">
          MongoDB can execute a similar query. Now query becomes very complex.
        </p>
        <div class="tech-code-box">
          <span>db.sensor.aggregate(</span><br />[<br />
          { <span class="green">$match </span>: {<span class="green">name</span
          >:<span class="orange">"EQ1^TAG1024"</span>,<span class="green"
            >time</span
          >: { <span class="green">$gte</span>:ISODate(<span class="ornage"
            >"2018-01-01T00:00:00Z"</span
          >),<br />
          <span class="green">$lt</span>:ISODate(<span class="orange"
            >"2018-01-02T00:00:00Z"</span
          >)}}},<br />
          { <span class="green">$project</span> : {<br />
          &nbsp;&nbsp;&nbsp;&nbsp;_id : <span class="blue">0</span>,<br />
          &nbsp;&nbsp;<span class="red">"time"</span>:
          <span class="blue">1</span>,<br />
          <span class="red">"value"</span>: <span class="blue">1</span>,<br />
          }<br />
          },<br />
          { <span class="green">$group</span> : {<br />
          <span class="red">"_id"</span>: { <br />
          <span class="red">"year"</span>: { <span class="green">$year</span> :
          <span>"$time"</span>},<br />
          <span class="red">"month"</span>: {
          <span class="green">$month</span> : <span>"$time"</span>},<br />
          <span class="red">"day"</span>: {
          <span class="green">$dayOfMonth</span> : <span>"$time"</span>},<br />
          <span class="red">"hour"</span>: { <span class="green">$hour</span> :
          <span>"$time"</span>},<br />
          },<br />
          <span class="red">"maxValue"</span>: {
          <span class="green">$max</span> : <span>"$value"</span>},<br />
          <span class="red">"count"</span>: { <span class="green">$sum</span> :
          <span class="blue">1</span>}<br />
          }<br />
          },<br />
          { <span class="green">$sort</span>: { <br />
          <span class="red">"_id.year"</span>:
          <span class="blue">1</span>,<br />
          <span class="red">"_id.month"</span>:
          <span class="blue">1</span>,<br />
          <span class="red">"_id.day"</span>: <span class="blue">1</span>,<br />
          <span class="red">"_id.hour"</span>:
          <span class="blue">1</span>,<br />
          }<br />
          }<br />
          ])
        </div>
        <p class="tech-contents-text">
          Ease of use is a matter of personal opinion, but when expressing
          statistics or complex conditional statements, MongoDB tends to make
          queries very verbose.
        </p>
        <p class="tech-contents-text">
          In time-series sensor data processing, queries involving hourly
          statistics are heavily used. Therefore, as queries become more
          complex, it can be expected that creating queries in MongoDB may
          become significantly more challenging than anticipated.
        </p>
        <div class="tech-title" id="anchor3">Sensor data index vs B+Tree</div>
        <p class="tech-contents-text">
          A B+Tree index, which is also commonly used in RDBMSs, looks like
          this.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog8-3.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          Each key is entered into a leaf node, where the key values are
          sequentially accessible as a linked list.
        </p>
        <p class="tech-contents-text">
          The algorithm is designed in such a way that when data is inserted and
          there is no more space in the leaf nodes, upper-level nodes are added.
          This design ensures that the tree does not become skewed to one side
          regardless of the distribution of input key values. For this reason,
          this structure is reasonably good for single-condition search
          performance on disk-based RDBMSs.
        </p>
        <p class="tech-contents-text">
          However, can it also solve well for two-dimensional problems, such as
          time-series sensor data, where time and sensor identifiers must be
          considered simultaneously?
        </p>
        <p class="tech-contents-text">
          Meanwhile, the sensor data index in Machbase has a special structure,
          sorted by time and sensor identifier.
        </p>
        <p class="tech-contents-text">
          For time series sensor data, most queries are based on time range and sensor ID, so we have implemented an index structure that is optimized for these queries as much as possible. Here’s a comparison of the features of these two indexes
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog8-4.webp"
            alt=""
          />
        </div>
        <ul class="tech-ul">
          <li>
            B+Tree indexes can lead to poor input performance when entering
            large amounts of data.
          </li>
          <li>
            B+Tree indexing involves frequent Structure Modification Operations
            (SMOs) when data is inserted rapidly. To maintain the consistency
            between data insertion and read operations (index search), locking
            occurs during SMOs, which can affect either a portion or the
            entirety of the tree. Of course, during this time, ongoing input
            operations from other sessions may be temporarily halted.
          </li>
          <li>
            B+Tree indexes are optimized for search in environments with tens to
            hundreds of millions of inputs and infrequent, partial updates. It
            performs well in web-related applications where MongoDB is often
            used, but it cannot perform well enough in time-series sensor data
            environments where large amounts of data are input at high rates.
          </li>
          <li>
            When searching using a B+Tree index, the index is stored in the form
            of &lt;key value, record identifier>. In some cases, you may want to
            record data by key value, which is known as a clustered index.
            MongoDB does not provide clustered indexes. Once you have traversed
            the key values to get the record identifiers, you read the desired
            records from the data file by their record identifiers. At this
            point, a random read operation to disk occurs.
          </li>
          <li>
            In the example below, if we indexed by time, there would be a lot of
            sensor data between the two-time ranges. Assuming the desired data
            is red squares, the red squares within the two-time ranges are not
            clustered, so we sequentially traverse the leaf nodes of the B+Tree
            index, obtain each RID, and perform a random read each time. As the
            number of sensors increases and the data collection interval becomes
            shorter, the number of index records that need to be visited by the
            index sequential search increases, and more random read operations
            occur. This is why even if you create a B+Tree index, you won’t get
            the data retrieval speed you want.
          </li>
        </ul>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog8-5.webp"
            alt=""
          />
        </div>
        <ul class="tech-ul">
          <li>
            On the other hand, Machbase’s sensor data index creates index files
            by partitioning them by time. Each index file stores data sorted by
            &lt;sensor ID, time, sensor value>, and the index partition keeps
            information about the minimum and maximum time values for that
            partition in memory. Therefore, index partitions that do not contain
            the time values you want to search for are excluded from the search.
          </li>
          <li>
            In addition to improved search performance due to index
            partitioning, partitioned indexes can achieve the same performance
            even with very large data inputs. This is because, unlike B+Tree,
            newly entered data is only reflected in the last recorded index
            partition and does not change the index partitions created in the
            past. For this reason, Machbase is implemented to work well in
            parallel, even if input, indexing, and searching are performed in
            parallel.
          </li>
          <li>
            Returning to the topic of searching, once the key value is located
            within the selected index partition, filtering based on the target
            time conditions can be done quickly. The data with the same key
            values are sorted in chronological order, allowing for efficient
            filtering. Since all the desired results, such as specific sensor
            data values by time, are recorded within the same index, the search
            can be performed with short-range sequential reads.
          </li>
        </ul>
        <p class="tech-contents-text">
          Comparing the two indexing architectures, we can see that the time
          series sensor data index solves all the problems that B+Tree has when
          applied to time series data processing.
        </p>
        <div class="tech-title" id="anchor4">
          Compare input and simple query performance
        </div>
        <p class="tech-contents-text">
          It’s easy to predict that Machbase will perform better with time
          series sensor data due to the formal schema structure and sensor
          data-specific indexes described earlier.
        </p>
        <p class="tech-contents-text">
          Tests were run in the following environments
        </p>
        <ul class="tech-ul">
          <li>
            I imported the previously prepared CSV file (107GB) using dedicated
            tools for each product, such as CSV loader and Mongo import.
          </li>
          <li>Indexing on tag name and timestamp</li>
          <li>4Core Xeon CPU, 32GB RAM, SSD</li>
        </ul>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog8-6.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          You can see that MongoDB was slow to enter data, consuming more
          resources, while the database entered data at more than eight times
          the speed.
        </p>
        <p class="tech-contents-text">
          Next, the schema structure and index differences produced the
          following results for simple search performance.
        </p>
        <div class="tech-contents-title">
          Performance of simple search queries
        </div>
        <p class="tech-contents-text">
          A query which retrieves all 1-day data for a given day.
        </p>
        <div class="tech-code-box">
          <span class="red">SELECT</span><span> count(*) </span
          ><span class="red">FROM</span> ( <br />
          <span class="red">&nbsp;&nbsp;&nbsp;&nbsp;SELECT</span> *
          <span class="red">FROM</span> tag<br />
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="red"
            >WHERE</span
          >
          name = <span class="ornage">'EQ0^TAG287' </span>
          <span class="red">AND</span> time
          <span class="red">between</span> to_date (<span class="orange"
            >'2018-01-01 00:00:00'</span
          >)<br />
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="red"
            >AND</span
          >
          to_date (<span class="orange">'2018-01-01 23:59:59'</span>)<br />
        </div>
        <div class="tech-code-box">
          <span>db.sensor.find(</span><span class="green">{name</span>:<span
            class="orange"
            >"EQ0^TAG287"</span
          >,<br />
          <span class="green">time</span>: {
          <span class="blue">$gte</span>:ISODate(<span class="orange"
            >"2018-01-01T00:00:00Z"</span
          >),<br />
          <span class="blue">$lt</span>:ISODate(<span class="orange"
            >"2018-01-02T00:00:00Z"</span
          >)}}).count()
        </div>
        <p class="tech-contents-text">
          The following results were obtained from the performance of the above
          two queries.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog8-7.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          The result is a performance difference of over 200x between the two
          DBs. You can see that the time series sensor data index in the
          machbase has made a difference.
        </p>
        <div class="tech-contents-title">
          Generating automatic rollups of sensor data vs. real-time statistics
        </div>
        <p class="tech-contents-text"></p>
        <p class="tech-contents-text">
          Because sensor data stores so much data, visualizing long-term
          statistics (overall trends over 10 years of data) requires a large
          amount of data reading and statistical computation.
        </p>
        <p class="tech-contents-text">
          In visualization applications, fast statistical extraction is
          essential because if the data takes too long to read, it cannot be
          displayed interactively (zooming in and out, moving through periods,
          etc.). Even if you can quickly retrieve the data you want to
          visualize, if you have hundreds of millions of data points, displaying
          them over time will again require massive computation.
        </p>
        <p class="tech-contents-text">
          If you can set up statistics on a time basis in advance, you can run
          statistical queries based on time values very quickly. Machbase
          provides the ability to automatically generate statistics on time
          series sensor data, store them, and quickly retrieve them through
          queries.
        </p>
        <p class="tech-contents-text">
          The results of running the same statistical query on Machbase and
          MongoDB are as follows. It should be noted that MongoDB does not
          support SQL, which makes the query language very complicated.
        </p>
        <p class="tech-contents-text">
          The following query retrieves the maximum value per minute for a
          particular sensor over a day. Machbase uses the following tips to help
          you retrieve the statistical data you have entered.
        </p>
        <div class="tech-code-box">
          <span class="red">SELECT</span
          ><span class="green"> /*+ ROLLUP(TAG, hour, max) */ </span>time,
          <span class="red">value as</span> max<br />
          <span class="red">FROM</span> TAG<br />
          <span class="red">FROM</span> name =
          <span class="ornage">'EQ1^TAG1024'</span>
          <span class="red"> AND</span> time
          <span class="red">BETWEEN</span> to_date(<span class="orange"
            >'2018-01-01 00:00:00'</span
          >)<br />
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="red"
            >AND</span
          >
          to_date (<span class="orange">'2018-01-01 23:59:59'</span>) )<br />
          <span class="red">ORDER BY</span> time<br />
        </div>
        <p class="tech-contents-text">
          MongoDB runs by passing the following JSON to the query language.
        </p>
        <div class="tech-code-box">
          <span>db.sensor.aggregate(</span><br />[<br />
          { <span class="green">$match </span>: {<span class="green">name</span
          >:<span class="orange">"EQ1^TAG1024"</span>,<span class="green"
            >time</span
          >: { <span class="green">$gte</span>:ISODate(<span class="ornage"
            >"2018-01-01T00:00:00Z"</span
          >),<br />
          <span class="green">$lt</span>:ISODate(<span class="orange"
            >"2018-01-02T00:00:00Z"</span
          >)}}},<br />
          { <span class="green">$project</span> : {<br />
          &nbsp;&nbsp;&nbsp;&nbsp;_id : <span class="blue">0</span>,<br />
          &nbsp;&nbsp;<span class="red">"time"</span>:
          <span class="blue">1</span>,<br />
          <span class="red">"value"</span>: <span class="blue">1</span>,<br />
          }<br />
          },<br />
          { <span class="green">$group</span> : {<br />
          <span class="red">"_id"</span>: { <br />
          <span class="red">"year"</span>: { <span class="green">$year</span> :
          <span>"$time"</span>},<br />
          <span class="red">"month"</span>: {
          <span class="green">$month</span> : <span>"$time"</span>},<br />
          <span class="red">"day"</span>: {
          <span class="green">$dayOfMonth</span> : <span>"$time"</span>},<br />
          <span class="red">"hour"</span>: { <span class="green">$hour</span> :
          <span>"$time"</span>},<br />
          },<br />
          <span class="red">"maxValue"</span>: {
          <span class="green">$max</span> : <span>"$value"</span>},<br />
          <span class="red">"count"</span>: { <span class="green">$sum</span> :
          <span class="blue">1</span>}<br />
          }<br />
          },<br />
          { <span class="green">$sort</span>: { <br />
          <span class="red">"_id.year"</span>:
          <span class="blue">1</span>,<br />
          <span class="red">"_id.month"</span>:
          <span class="blue">1</span>,<br />
          <span class="red">"_id.day"</span>: <span class="blue">1</span>,<br />
          <span class="red">"_id.hour"</span>:
          <span class="blue">1</span>,<br />
          }<br />
          }<br />
          ])
        </div>
        <p class="tech-contents-text">
          The performance results are as follows.
        </p>
        <div class="tech-img-wrap">
          <img
            class="tech-img tech-margin-bottom"
            src="../../img/blog8-8.webp"
            alt=""
          />
        </div>
        <p class="tech-contents-text">
          You can see the performance difference of almost 400x.
        </p>
        <div class="tech-title" id="anchor5">Conclusion</div>
        <p class="tech-contents-text">
          We looked at how Machbase and MongoDB differ from an architectural
          point of view, and the performance impact We found that while MongoDB
          is very convenient for environments like web applications, and we were
          able to get good performance out of it, it has an architecture that
          provides indexes that are not ideal for time series sensor data
          applications.
        </p>
        <p class="tech-contents-text">
          Smart factories and smart cities, which have become a hot topic in
          recent years, not only generate large amounts of sensor data but also
          a lot of concerns and attempts to process it. I have written this
          article in the hope that Machbase can be a good solution at the heart
          of the problem.
        </p>
        <p class="tech-contents-text">
          I’ll leave it at that, with the promise of a comparison with a larger
          database of time-series sensor data when I get the chance.
        </p>
        <p class="tech-contents-text">Thank you.</p>
        <p class="tech-contents-text">Kwanghoon Shim, CRO of Machbase</p>
      </div>
    </div>
  </div>
</section>
{{< home_footer_blog_en >}}
