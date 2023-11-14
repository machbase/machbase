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
      A solution to ESG issues: Time Series Database
    </h4>
    <div class="blog-date">
      <div>
        <span>by Timothy Cha / 11 Nov 2023</span>
      </div>
    </div>
    <ul class="tech-list-ul">
      <a href="#anchor1">
        <li class="tech-list-li" id="tech-list-li">Introduction</li></a
      >
      <a href="#anchor2">
        <li class="tech-list-li" id="tech-list-li">
          Environmental issues associated with data centers
        </li>
      </a>
      <a href="#anchor3">
        <li class="tech-list-li" id="tech-list-li">Solutions</li>
      </a>
      <a href="#anchor4">
        <li class="tech-list-li" id="tech-list-li">
          Time series database engines as a solution to ESG issues
        </li>
      </a>
      <a href="#anchor5">
        <li class="tech-list-li" id="tech-list-li">Conclusion</li>
      </a>
    </ul>
    <div class="tech-contents">
      <p class="tech-title" id="anchor1">Introduction</p>
      <p class="tech-contents-text">
        With the advent of the digital age, every aspect of our lives generates
        and requires data. As a result, data is considered a core business
        asset, and the ability to effectively collect, manage, analyze and
        utilize data, as well as building the core infrastructure for it, is
        becoming increasingly important.
      </p>
      <p class="tech-contents-text">
        Advances in data analytics, particularly using big data, and advances in
        artificial intelligence (AI) and its machine learning (ML) algorithms
        are driving this trend.
      </p>
      <p class="tech-contents-text">
        However, this infrastructure, particularly data centers, raises a number
        of ESG and environmental concerns.
      </p>
      <p class="tech-contents-text">
        In this article, we look at what environmental issues are being raised
        and what solutions are being discussed.
      </p>
      <div class="tech-title" id="anchor2">
        Environmental issues associated with data centers
      </div>
      <p class="tech-contents-text">
        Managing data requires a variety of equipment, including servers,
        storage and networking equipment.
      </p>
      <p class="tech-contents-text">
        Most companies that deal directly or indirectly with data have a room
        called a server room where this equipment is stored, and IT companies
        that specialize in data have large facilities called data centers. You
        can think of a data center as a hotel for computers, with all the
        different equipment we’ve been talking about — servers, storage,
        networking equipment, and so on.
      </p>
      <p class="tech-contents-text">
        As data becomes more important and necessary, this infrastructure, the
        data centre, grows in size and its environmental impact increases.
      </p>
      <p class="tech-contents-text">Here’s how it breaks down</p>
      <p class="tech-contents-title">Electricity Energy consumption</p>
      <div class="tech-img-wrap">
        <img
          class="tech-img "
          src="../../img/blog11-1.png"
          alt=""
        />
      </div>
      <p class="tech-contents-link-text">
        Inside a customer data suite at Union Station. Image: Global Access
        Point. Public domain. 2008
      </p>
      <p class="tech-contents-text">
        One of the first issues that comes to mind when talking about data
        centers is power consumption. While electricity is unavoidable when
        using electronics, the environmental impact of data centres is more
        significant than most people realize.
      </p>
      <p class="tech-contents-text">
        Basically, just keeping hundreds of thousands of pieces of electronics
        running requires a lot of electricity, but there are additional reasons
        why it’s a burden on the environment.
      </p>
      <p class="tech-contents-text">1. 24-hour operations</p>
      <p class="tech-contents-text">
        Data centers operate around the clock. This is because many applications
        require real-time processing, and in a global business environment,
        services must be continuously available regardless of location or time.
        Other reasons include the need to optimize the use of resources based on
        the time of day.
      </p>
      <p class="tech-contents-text">2. Maintaining temperature and humidity</p>
      <p class="tech-contents-text">
        The core equipment in a data centre, such as computer servers, storage
        systems and networking equipment, generate heat as they operate, but
        they work best at a constant temperature range, and excessive
        temperature rises can cause damage to components, so it’s important to
        keep them cool to maintain a constant temperature.
      </p>
      <p class="tech-contents-text">
        In addition to managing temperature, it is also important to manage
        humidity, as high humidity increases the likelihood of condensation (dew
        point), which allows moisture to penetrate electronic components,
        causing short circuits and corrosion, while low humidity makes it easier
        to generate static electricity. Static electricity can affect electronic
        equipment and cause data loss or hardware damage.
      </p>
      <p class="tech-contents-text">3. Redundancy</p>
      <p class="tech-contents-text">
        Redundancy is a method of ensuring the reliability and availability of a
        system by installing and operating redundant versions of key components
        within a data center.
      </p>
      <p class="tech-contents-text">
        Data centres are built with redundancy in mind, which is why they have
        more equipment and use twice as much power. The reason for redundancy is
        that redundancy is almost the only solution in the event of failure of
        critical equipment, accidents caused by various disasters and even the
        security of the entire system.
      </p>
      <p class="tech-contents-text">
        On the other hand, let’s look at how much power these data centers use.
      </p>
      <p class="tech-contents-text">
        It is estimated that the power consumption per square meter of a data
        centre is about 1,000 kWh, which is 10 to 50 times more per square meter
        than a typical commercial office, and the power consumption of a large
        data center with tens of thousands of servers is equivalent to the power
        consumption of 50,000 households.
      </p>
      <p class="tech-contents-text">
        The current electricity consumption of 147 data centers (3,337 GWh)
        alone consumes almost half the annual electricity production of one
        nuclear power plant (7,000 GWh), and the expansion of two or three
        nuclear power plants would need to be considered to meet future
        electricity needs.
      </p>
      <p class="tech-contents-title">Water use</p>
      <div class="tech-img-wrap">
        <img
          class="tech-img "
          src="../../img/blog11-2.png"
          alt=""
        />
      </div>
      <p class="tech-contents-link-text">
        Steam rises above cooling towers at the Google Dalles data center in
        Oregon. Google photo
      </p>
      <p class="tech-contents-text">
        Data center water use is also an issue. The amount of water used in data
        centers is staggering. In 2011, Google reported that 16.2 billion liters
        of water were used in Google data centers worldwide, which is about the
        same amount of water used by 29 golf courses in the southwestern United
        States.
      </p>
      <p class="tech-contents-text">
        DWater is used in data centers for cooling, to prevent servers from
        overheating, and for generators to supplement power in emergencies.
      </p>
      <p class="tech-contents-text">
        In addition to conventional cooling, various cooling methods have been
        developed, such as running coolant through the grids of server racks,
        but regardless of the method, water is used in the cooling tower cooling
        system.
      </p>
      <p class="tech-contents-text">
        On the other hand, data centers install back-up power generators, which
        are rarely used because they are used to back up power in the event of a
        blackout, but when they are used they use steam to turn turbines to
        generate electricity, which requires large amounts of water.
      </p>
      <p class="tech-contents-title">Electronic and toxic waste</p>
      <div class="tech-img-wrap">
        <img
          class="tech-img "
          src="../../img/blog11-3.png"
          alt=""
        />
      </div>
      <p class="tech-contents-link-text">
        This amazing pile of English e-waste awaits recycling. Photograph by
        Stefan Czapski, courtesy Geograph. CC-BY-SA-2.0
        <a
          class="tech-contents-link"
          href="https://blog.education.nationalgeographic.org/"
          >https://blog.education.nationalgeographic.org/</a
        >
      </p>
      <p class="tech-contents-text">
        A hyperscale data center is generally defined as one with at least
        100,000 servers in 22,500 square meters of space.
      </p>
      <p class="tech-contents-text">
        There will be 628 hyperscale data centers in the world by 2021 (source:
        Cisco), and there are also hyperscale data centers with more than
        100,000 servers in Korea, such as LG U+’s Pyeongchon data center and
        Naver’s Sejong data center.
      </p>
      <p class="tech-contents-text">
        The problem is that hundreds of thousands of servers in data centers
        have a lifespan of only four to five years, and according to the US
        Environmental Protection Agency (EPA), e-waste, or discarded electronic
        equipment, is classified as toxic waste. (70% of toxic waste is
        e-waste).
      </p>
      <p class="tech-contents-text">
        This is because electronics use toxic chemicals such as brominated flame
        retardants, lead, mercury, cadmium and beryllium.
      </p>
      <p class="tech-contents-text">
        According to a recent United Nations report, 53.6 million tonnes of
        e-waste will be discarded globally in 2019, with only 17.4% recycled and
        82.6% landfilled or incinerated. In addition, due to strict
        environmental regulations and high disposal costs, most e-waste is
        exported to developing countries such as China, India and Africa,
        meaning that e-waste pollutes the entire planet.
      </p>
      <p class="tech-contents-title">Heat, noise and electromagnetic waves</p>
      <p class="tech-contents-text">
        Although less serious than the first three, data centers themselves
        generate a lot of heat. The enormous amount of energy used to keep the
        temperature inside the data center down through cooling means that a lot
        of heat is generated inside the data center and released to the outside.
        This is problematic from a global warming perspective.
      </p>
      <p class="tech-contents-text">
        In addition, the huge amount of electromagnetic waves generated by
        hundreds of thousands of servers and the noise generated by the many
        electronic devices and air conditioners can affect not only people’s
        lives but also the ecosystem.
      </p>
      <div class="tech-title" id="anchor3">Solutions</div>
      <p class="tech-contents-text">
        The main solutions to the above problems are to
      </p>
      <p class="tech-contents-title">
        Minimizing the power required for cooling
      </p>
      <div class="tech-img-wrap">
        <img
          class="tech-img "
          src="../../img/blog11-4.png"
          alt=""
        />
      </div>
      <p class="tech-contents-link-text">
        Project Natick —
        <a
          class="tech-contents-link"
          href="https://natick.research.microsoft.com/"
          >https://natick.research.microsoft.com/</a
        >
      </p>
      <p class="tech-contents-text">
        Various methods are being used to minimize the amount of electricity
        used for cooling.
      </p>
      <p class="tech-contents-text">
        Temperature control, particularly cooling, is the most power-intensive
        part of the data centre, accounting for 40–55% of total power
        consumption, so it is arguably the most important part of reducing
        overall power consumption.
      </p>
      <p class="tech-contents-text">
        Google has reported a 10% reduction in power consumption using water
        cooling compared to conventional cooling, and many other companies are
        working to reduce power consumption using a variety of cooling methods.
      </p>
      <p class="tech-contents-text">
        Meta (Facebook) built its pan-European data center in Luleå, Sweden,
        which is cooler year-round to reduce cooling costs, and Microsoft is
        experimenting with putting data centers under the sea with Project
        Natick.
      </p>
      <p class="tech-contents-text">
        In South Korea, LG Uplus’ Anyang data center in Pyeongchon and Naver’s
        Chuncheon data center are also actively using outdoor air cooling to
        reduce the amount of electricity used for cooling.
      </p>
      <p class="tech-contents-title">Data Centre Optimisation</p>
      <div class="tech-img-wrap">
        <img
          class="tech-img "
          src="../../img/blog11-5.webp"
          alt=""
        />
      </div>
      <p class="tech-contents-link-text">Image creator from Microsoft Bing</p>
      <p class="tech-contents-text">
        Another issue that should be examined is how to reduce energy
        consumption by optimizing various equipment such as servers and storage
        in the data center.
      </p>
      <p class="tech-contents-text">
        This is because when operating a data centre, applications installed on
        servers may become obsolete over time, or servers may become unused
        because service subscriptions are discontinued, leaving them unattended
        and consuming power.
      </p>
      <p class="tech-contents-text">
        According to infrastructure management company Cormant, these servers,
        also known as zombie servers, make up 10 to 30 percent of the servers in
        a data center.
      </p>
      <p class="tech-contents-text">
        By better management, removing zombie servers, consolidating and
        virtualizing servers, and reducing storage equipment through data
        erasure, you can save a significant amount of energy simply by reducing
        unnecessary equipment.
      </p>
      <p class="tech-contents-title">Improving power efficiency</p>
      <div class="tech-img-wrap">
        <img
          class="tech-img "
          src="../../img/blog11-6.png"
          alt=""
        />
      </div>
      <p class="tech-contents-link-text">
        Comparison of AC and HVDC power feed systems in a datacenter or
        communications building.(NTT Technical Review)
      </p>
      <p class="tech-contents-text">
        In order to reliably operate the various facilities in a data center
        over a 24-hour period, many basic facilities are required, such as
        backup batteries, power generation units and highly reliable air
        conditioning systems for cooling equipment. It is also being
        investigated whether power can be saved by improving the structure and
        method of powering these facilities.
      </p>
      <p class="tech-contents-text">
        A typical example is DC power. Since servers use DC internally,
        supplying power directly as DC can save power by eliminating the need
        for AC to DC conversion in the server’s internal power supply.
        Typically, there is a loss of around 10% per power conversion, so DC
        power requires fewer power conversions than AC power, so in principle
        efficiency can be improved.
      </p>
      <p class="tech-contents-text">
        In addition, the replacement of conventional generators with alternative
        power solutions such as fuel cells is being investigated to minimize
        carbon emissions and other costs.
      </p>
      <div class="tech-title" id="anchor4">
        Time series database engines as a solution to ESG issues
      </div>
      <p class="tech-contents-text">
        In recent years, ESG has emerged as an important concept.
      </p>
      <p class="tech-contents-text">
        ESG is a concept that refers to the three aspects of environment,
        society and governance, and is used to assess whether a company fulfills
        its social responsibility and pursues sustainable management.
      </p>
      <p class="tech-contents-text">
        The reason why ESG has become important is that, as regulations on
        corporate ESG have been strengthened, ESG performance has a significant
        impact on the valuation of companies.
      </p>
      <p class="tech-contents-text">
        From an ESG perspective, time series database engines can provide
        solutions for the environment in a different way than the previous
        three.
      </p>
      <p class="tech-contents-text">
        Time series data is data whose values correspond to the passage of time,
        such as sensor data, and a time series database engine is a software
        system optimized for storing and serving this type of data.
      </p>
      <p class="tech-contents-text">
        This means that if you need to process time series data, such as sensor
        data, you can use a time series database engine to do so with much less
        equipment than a traditional database engine.
      </p>
      <p class="tech-contents-text">
        This is a very significant solution that can reduce the amount of power
        and water required for operation and cooling, as well as reducing waste.
      </p>
      <p class="tech-contents-text">
        Machbase’s time series database engine has been rated the world’s best
        in a price/performance evaluation test by the Transaction Processing
        Performance Council (TPC), an internationally recognised performance
        evaluation organization, and has demonstrated a performance difference
        of nearly 6x over Hadoop in the US.
      </p>
      <div class="tech-img-wrap">
        <img
          class="tech-img "
          src="../../img/blog11-7.webp"
          alt=""
        />
      </div>
      <p class="tech-contents-link-text">
        <a
          class="tech-contents-link"
          href="https://www.tpc.org/tpcx-iot/results/tpcxiot_price_perf_results5.asp?version=2"
          >https://www.tpc.org/tpcx-iot/results/tpcxiot_price_perf_results5.asp?version=2</a
        >
      </p>
      <p class="tech-contents-text">
        In this test, the cost of meeting the same performance criteria was
        $329.75 for Hadoop and $54.85 for Machbase.
      </p>
      <p class="tech-contents-text">
        This almost sixfold difference is due to the superior performance of the
        database engine itself and the simplicity of the architecture.
      </p>
      <p class="tech-contents-text">
        For example, in a project with Electronics and Telecommunications
        Research Institute(ETRI) of Korea, Machbase has demonstrated that a
        system using Hadoop can be simplified to Machbase.
      </p>
      <div class="tech-img-wrap">
        <img
          class="tech-img "
          src="../../img/blog11-8.png"
          alt=""
        />
      </div>
      <p class="tech-contents-link-text">Before: Hadoop</p>
      <div class="tech-img-wrap">
        <img
          class="tech-img "
          src="../../img/blog11-9.png"
          alt=""
        />
      </div>
      <p class="tech-contents-link-text">After: Machbase TSDB</p>
      <p class="tech-contents-text">
        In this case, a project to build an energy big data platform to collect
        electricity big data and develop deep learning algorithms, Machbase has
        demonstrated that applying a time series database engine instead of
        Hadoop can simplify the platform architecture, which not only reduces
        the cost and time to build hardware, but also reduces the physical size
        of the overall facility.
      </p>
      <div class="tech-title" id="anchor5">Conclusion</div>
      <p class="tech-contents-text">
        The importance of the environment and energy cannot be overstated. The
        fact that sustainable development indicators, known as ESG, are actually
        being used to assess the investment value of companies shows that
        environmental issues are directly related to the survival of companies.
      </p>
      <p class="tech-contents-text">
        The growth of data and the facilities to store it is inevitable. But
        minimizing its environmental impact will be a question of how we do it.
      </p>
      <p class="tech-contents-text">
        Although not a panacea, it is a proven fact that in areas where time
        series data is used, the impact on the environment can be minimized
        through the use of time series database engines.
      </p>
      <p class="tech-contents-text">
        Among the DBMSs currently in development, the Machbase time series data
        engine has been formally proven to minimize the facilities associated
        with time series data.
      </p>
      <p class="tech-contents-text">
        If you are concerned about the global environment and ESG issues, I
        encourage you to take a look at how Machbase’s time series database
        engine can help you minimize your environmental impact.
      </p>
    </div>
  </div>
</section>
{{< home_footer_blog_en >}}
