---
---

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" type="text/css" href="./css/common.css" />
  <link rel="stylesheet" type="text/css" href="./css/style.css" />
</head>
<nav>
  <div class="homepage-menu-wrap">
    <div class="menu-left">
      <ul class="menu-left-ul">
        <li class="menu-logo">
          <a href="/home"><img src="./img/machbase_logo_b.png" alt="" /></a>
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
<section class="section1 main_section1 main_wrap">
  <div class="main_wraper">
    <div class="main_titlebox">
      <h1 class="main_title">
        Mach Speed<br />
        Horizontally Scalable<br />Time series database.
      </h1>
      <h2 class="main_titletext">
        “ Machbase is the world’s fastest timeseries database.
      </h2>
      <p class="main_titletext_under">
        It’s an ideal solution for environments that
      </p>
      <p class="main_titletext_under">
        require scalability, from edge devices with limited resources<br />
        to clusters processing massive amounts of data."
      </p>
      <h2 class="main_tablet_subtitle">
        “ Machbase is the world’s fastest timeseries database. It’s an ideal
        solution for environments that require scalability, from edge devices
        with limited resources to clusters processing massive amounts of data."
      </h2>
    </div>
    <div class="chart_wrap">
      <div class="chart">
        <a href="https://neo.machbase.com/" target="_blank"
          ><img class="main_chart" src="./img/neo_main2.png" alt=""
        /></a>
      </div>
      <div class="chart_hover">
        <a href="https://neo.machbase.com/" target="_blank"
          ><img class="main_chart" src="./img/Neo_hover2.png" alt=""
        /></a>
      </div>
    </div>
    <div class="tablet_chart_wrap">
      <div class="tablet_chart">
        <a href="https://neo.machbase.com/" target="_blank"
          ><img class="main_chart" src="./img/neo_main.png" alt=""
        /></a>
      </div>
      <div class="tablet_chart_hover">
        <a href="https://neo.machbase.com/" target="_blank"
          ><img class="main_chart" src="./img/Neo_hover.png" alt=""
        /></a>
      </div>
    </div>
  </div>
</section>
<section class="section2 main_section2">
  <div>
    <h4 class="sub_title main_margin_top">Why Machbase?</h4>
    <div class="bar"><img src="./img/bar.png" /></div>
  </div>
  <div class="main_why_wrap">
    <div class="main_why_box">
      <div class="main_why_title_box">
        <p class="main_why_title">The World-best Performance</p>
        <img class="main_img" src="./img/main_best.png" />
      </div>
      <div class="main_why_contents_box">
        <ul>
          <li class="main_why_contents">
            TPCx IoT Performance Ranked #1 Worldwide since November 2019(IoT
            sensor data processing performance of 5 million IOP on January 2023)
          </li>
          <li class="main_why_contents">
            10x lower CPU/memory investment than Hadoop
          </li>
          <li class="main_why_contents">
            Dozens of times more compression efficiency than traditional RDBMS
            and Hadoop
          </li>
          <li class="main_why_contents">
            Support for Different Operating Systems and CPUs
          </li>
        </ul>
      </div>
      <div class="main_why_more_box">
        <p class="main_why_more">
          <span>
            <router-link
              class="main_why_more"
              :to="{ path: '/Company', hash: '#performance' }"
              >View More<ArrowSvg
            /></router-link>
          </span>
        </p>
      </div>
    </div>
    <div class="main_why_box">
      <div class="main_why_title_box">
        <p class="main_why_title">Edge Computing</p>
        <img class="main_img" src="./img/main_edge.png" />
      </div>
      <div class="main_why_contents_box">
        <ul>
          <li class="main_why_contents">
            Data insertion performance exceeding 400,000/sec on Raspberry Pi 4
          </li>
          <li class="main_why_contents">
            Best performance on any device, from edge devices to clusters
          </li>
          <li class="main_why_contents">
            The highest scalability with a simple architecture
          </li>
          <li class="main_why_contents">
            Provides an efficient way to develop learning and inference
            applications between DBMS and AI applications
          </li>
        </ul>
      </div>
      <div class="main_why_more_box">
        <p class="main_why_more">
          <span>
            <a target="" class="main_why_more" href="/edge">
              View More<ArrowSvg />
            </a>
          </span>
        </p>
      </div>
    </div>
    <div class="main_why_box">
      <div class="main_why_title_box">
        <p class="main_why_title">Solving Developer Pain Points</p>
        <img class="main_img" src="./img/main_time.png" />
      </div>
      <div class="main_why_contents_box">
        <ul>
          <li class="main_why_contents">
            Provide a powerful built-in data transformation language (TQL).
          </li>
          <li class="main_why_contents">Provide worksheet functionality.</li>
          <li class="main_why_contents">Provide visualization.</li>
          <li class="main_why_contents">Support embedded broker</li>
          <li class="main_why_contents">Support standard security features.</li>
        </ul>
      </div>
      <div class="main_why_more_box">
        <span>
          <a
            class="main_why_more"
            :to="{ path: '/Products', hash: '#scroll2' }"
            >View More<ArrowSvg
          /></a>
        </span>
      </div>
    </div>
  </div>
</section>
<section class="main_section3">
  <div class="termianl_top">
    <h4 class="sub_title section3_subtitle">Machbase TSDB (Neo)</h4>
    <div class="bar"><img src="./img/bar.png" /></div>
    <!--[ Download & Install]</p> -->
  </div>
  <div class="test-wp-wrap">
    <div class="test-wrap">
      <button class="left-btn" data-target="download">Download</button>
      <button class="left-btn" data-target="start">Start Up</button>
      <button class="left-btn" data-target="create">Create Table</button>
      <button class="left-btn" data-target="insert">Insert</button>
      <button class="left-btn" data-target="select">Select</button>
    </div>
    <div class="home_table_wrap">
      <div class="terminal_wrap">
        <!-- [ Download & Install ] -->
        <div id="download">
          <div class="btn_wrap">
            <button class="btn1" data-target="download1">Linux / Mac</button>
            <button class="btn1" data-target="download2">Windows</button>
            <button class="btn1" data-target="download4">All releases</button>
          </div>
          <div class="main_container">
            <div id="download1">
              <div class="download_item">
                <div class="none_text">
                  <span class="green"># Download pakcage</span><br />
                </div>
                <div class="dol_rel">
                  <span class="yellow dol">$</span>
                  <p class="dol_p">
                    sh -c "$(curl -fsSL https://neo.machbase.com/install.sh)"
                  </p>
                  <button class="text_copy_btn">
                    <img class="copy_btn" src="./img/ic_copy.png" />
                  </button>
                </div>
              </div>
              <div class="download_item">
                <div class="none_text">
                  <span class="green"># Unarchive</span><br />
                </div>
                <div class="dol_rel">
                  <span class="yellow dol">$</span>
                  <p class="dol_p">unzip machbase-neo-*.zip</p>
                  <button class="text_copy_btn1">
                    <img class="copy_btn" src="./img/ic_copy.png" />
                  </button>
                </div>
              </div>
            </div>
            <div id="download2" class="hidden">
              <p class="ternal_margin_top">
                <span class="green"
                  >&lt;Click on the link below to download&gt;</span
                ><br />
                <a
                  class="orange home_visited"
                  target="_blank"
                  v-bind:href="latestNeoURI"
                  >machbase-neo-{{ latestNeo }}-windows-amd64.zip</a
                >
              </p>
            </div>
            <div id="download4" class="hidden">
              <p class="ternal_margin_top">
                <span class="green">&lt;Download from releases&gt;</span><br />
                <a
                  class="orange home_visited"
                  target="_blank"
                  href="https://neo.machbase.com/releases/"
                  >https://neo.machbase.com/releases/</a
                >
              </p>
            </div>
          </div>
        </div>
        <div id="start" class="hidden">
          <div class="btn_wrap">
            <button class="btn5" data-target="start1">Start Up</button>
          </div>
          <div class="main_container">
            <div id="start2">
              <div class="none_text">
                <span class="green"># Start</span><br />
              </div>
              <div class="dol_rel">
                <span class="yellow dol">$</span>
                <p class="dol_p">machbase-neo serve</p>
                <button
                  @click="copyCode(`machbase-neo serve`)"
                  class="copy-btn btn_up"
                >
                  Copy
                </button>
              </div>
            </div>
            <div id="start1" class="hidden">
              <div class="none_text">
                <span class="green"># Start</span><br />
              </div>
              <div class="dol_rel">
                <span class="yellow dol">$</span>
                <p class="dol_p">machbase-neo serve</p>
                <button
                  @click="copyCode(`machbase-neo serve`)"
                  class="copy-btn btn_up"
                >
                  Copy
                </button>
              </div>
            </div>
          </div>
        </div>
        <div id="create" class="hidden">
          <div class="btn_wrap">
            <button class="btn6" data-target="create1">Neo Shell</button>
            <button class="btn6" data-target="create2">Curl</button>
          </div>
          <div class="main_container">
            <div id="create3">
              <p class="ternal_margin_top">
                <span
                  ><span class="yellow">machbase-neo</span> shell sql \<br />
                  &nbsp;&nbsp;<span class="blue"
                    >'create tag table EXAMPLE (\<br />
                    &nbsp;&nbsp;&nbsp;&nbsp;name varchar(40) primary key, \<br />
                    &nbsp;&nbsp;&nbsp;&nbsp;time datetime basetime, \<br />
                    &nbsp;&nbsp;&nbsp;&nbsp;value double \<br />
                    &nbsp;&nbsp;)'</span
                  ></span
                >
              </p>
              <button
                @click="copyCode(this.codes['createShell'])"
                class="copy-btn3"
              >
                Copy
              </button>
            </div>
            <div id="create1" class="hidden">
              <p class="ternal_margin_top">
                <span
                  ><span class="yellow">machbase-neo</span> shell sql \<br />
                  &nbsp;&nbsp;<span class="blue"
                    >'create tag table EXAMPLE (\<br />
                    &nbsp;&nbsp;&nbsp;&nbsp;name varchar(40) primary key, \<br />
                    &nbsp;&nbsp;&nbsp;&nbsp;time datetime basetime, \<br />
                    &nbsp;&nbsp;&nbsp;&nbsp;value double \<br />
                    &nbsp;&nbsp;)'</span
                  ></span
                >
              </p>
              <button
                @click="copyCode(this.codes['createShell'])"
                class="copy-btn3"
              >
                Copy
              </button>
            </div>
            <div id="create2" class="hidden">
              <p class="ternal_margin_top">
                <span
                  >curl
                  <span class="orange">http://127.0.0.1:5654/db/query</span>
                  \<br />
                  &nbsp;&nbsp;&nbsp;&nbsp;<span class="orange"
                    >--data-urlencode</span
                  >
                  \<br />
                  &nbsp;&nbsp;&nbsp;&nbsp;<span class="orange"
                    >"q=create tag table EXAMPLE (name varchar(40) primary key,
                    time datetime basetime, value double)"</span
                  ></span
                >
              </p>
              <button
                @click="copyCode(this.codes['createCurl'])"
                class="copy-btn3"
              >
                Copy
              </button>
            </div>
          </div>
        </div>
        <div id="insert" class="hidden">
          <div class="btn_wrap">
            <button class="btn3" data-target="read7">Neo Shell</button>
            <button class="btn3" data-target="read1">Curl</button>
            <button class="btn3" data-target="read2">Python</button>
            <button class="btn3" data-target="read3">JavaScript</button>
            <button class="btn3" data-target="read4">Go</button>
            <button class="btn3" data-target="read5">C#</button>
          </div>
          <div class="main_container">
            <div id="read6">
              <p class="ternal_margin_top">
                <span class="yellow">machbase-neo</span> shell sql \<br />
                &nbsp;<span class="blue"
                  >"insert into EXAMPLE values('temperature',
                  1670380342000000000, 12.3456)"</span
                >
              </p>
              <button
                @click="copyCode(this.codes['insertShell'])"
                class="copy-btn"
              >
                Copy
              </button>
            </div>
            <div id="read7" class="hidden">
              <p class="ternal_margin_top">
                <span class="yellow">machbase-neo</span> shell sql \<br />
                &nbsp;<span class="blue"
                  >"insert into EXAMPLE values('temperature',
                  1670380342000000000, 12.3456)"</span
                >
              </p>
              <button
                @click="copyCode(this.codes['insertShell'])"
                class="copy-btn"
              >
                Copy
              </button>
            </div>
            <div id="read1" class="hidden">
              <p class="ternal_margin_top">
                curl
                <span class="orange">http://127.0.0.1:5654/db/query</span>
                \<br />
                &nbsp;&nbsp;<span class="orange">--data-urlencode</span> \<br />
                &nbsp;&nbsp;<span class="orange"
                  >"q=insert into EXAMPLE values('temperature',
                  1670380342000000000, 12.3456)"</span
                >
              </p>
              <button
                @click="copyCode(this.codes['insertCurl'])"
                class="copy-btn"
              >
                Copy
              </button>
            </div>
            <div id="read2" class="hidden">
              <p class="ternal_margin_top">
                <span class="red">import </span>
                <span class="blue"
                  >requests<br />
                  csvdata</span
                >
                =
                <span class="orange"
                  >"temperature,1670380342000000000,12.3456"<br
                /></span>
                <span class="blue">response</span> =
                <span class="blue">requests</span>.<span class="yellow"
                  >post</span
                >(<br />
                <span class="orange"
                  >&nbsp;&nbsp;&nbsp;&nbsp;"http://127.0.0.1:5654/db/write/EXAMPLE?heading=false",</span
                >
                <br />
                <span class="blue">&nbsp;&nbsp;&nbsp;&nbsp;data</span>=<span
                  class="blue"
                  >csvdata</span
                >,
                <br />
                <span class="blue">&nbsp;&nbsp;&nbsp;&nbsp;headers</span>={<span
                  class="orange"
                  >'Content-Type': 'text/csv'</span
                >})
              </p>
              <button
                @click="copyCode(this.codes['insertPy'])"
                class="copy-btn"
              >
                Copy
              </button>
            </div>
            <div id="read3" class="hidden">
              <p class="ternal_margin_top">
                <span class="blue">q</span> =
                <span class="orange">"select * from example"</span><br />
                <span class="blue">fetch</span>(<span class="orange"
                  >`http://127.0.0.1:5654/db/query?q=$</span
                >{<span class="blue">encodeURIComponent</span>(<span
                  class="blue"
                  >q</span
                >)<span class="orange">}`</span>)<br />
                &nbsp;&nbsp;.<span class="yellow">then</span>(<span
                  class="yellow"
                  >res</span
                >
                => {<br />
                &nbsp;&nbsp;&nbsp;<span class="red">return </span>
                <span class="blue">res</span>.<span class="yellow">json</span
                >();<br />
                &nbsp;&nbsp;})<br />
                &nbsp;&nbsp;.<span class="yellow">then</span>(<span
                  class="yellow"
                  >data</span
                >
                => {<br />
                &nbsp;&nbsp;&nbsp;<span class="blue">console</span>.<span
                  class="yellow"
                  >log</span
                >(<span class="blue">data</span>)<br />
                &nbsp;&nbsp;});
              </p>
              <button
                @click="copyCode(this.codes['insertJs'])"
                class="copy-btn"
              >
                Copy
              </button>
            </div>
            <div id="read4" class="hidden">
              <p class="ternal_margin_top">
                <span class="blue">package</span> main<br />
                <span class="blue">import</span> (<br />
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span
                  class="orange"
                  >"net/http"<br />
                  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"bytes"<br />
                  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"strings"<br /> </span
                >)<br />
                <span class="blue">func</span>
                <span class="yellow">main</span>() {<br />
                &nbsp;&nbsp;&nbsp;&nbsp;<span class="blue">rows</span> :=
                []<span class="green">string</span>{
                <span class="orange"
                  >"temperature,1670380342000000000,12.3456"</span
                >}<br />
                &nbsp;&nbsp;&nbsp;&nbsp;http.<span class="yellow">Post</span
                >(<br />
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span
                  class="orange"
                  >"http://127.0.0.1:5654/db/write/EXAMPLE?heading=false"</span
                >,<br />
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span
                  class="orange"
                  >"text/csv"</span
                >,<br />
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;bytes.<span
                  class="yellow"
                  >NewBufferString</span
                >(strings.<span class="yellow">Join</span>(rows,
                <span class="orange">"\n"</span>))) }
              </p>
              <button
                @click="copyCode(this.codes['insertGo'])"
                class="copy-btn"
              >
                Copy
              </button>
            </div>
            <div id="read5" class="hidden">
              <p class="ternal_margin_top">
                <span class="red">using </span>
                <span class="blue">HttpClient client</span> =
                <span class="red">new</span>();<br />
                <br />
                <span class="red">var </span>
                <span class="yellow">payload</span> =
                <span class="red">new </span>
                <span class="blue">System.Net.Http.StringContent</span>(<br />
                &nbsp;&nbsp;&nbsp;&nbsp;<span class="orange"
                  >@"temperature,1677033057000000000,21.1<br />
                  &nbsp;&nbsp;&nbsp;&nbsp;humidity,1677033057000000000,0.53"</span
                >,<br />
                &nbsp;&nbsp;&nbsp;&nbsp;<span class="red">new </span>
                <span class="blue"
                  >System.Net.Http.Headers.MediaTypeHeaderValue</span
                >(<span class="orange">"text/csv"</span>));<br />
                <br />
                <span class="red">var </span>
                <span class="yellow">rsp</span> =
                <span class="red">await </span>
                <span class="blue">client.PostAsync</span>(<br />
                &nbsp;&nbsp;&nbsp;&nbsp;<span class="orange"
                  >"http://127.0.0.1:5654/db/write/example?heading=false"</span
                >, <span class="blue">payload</span><br />
                );<br />
              </p>
              <button @click="copyCode(this.codes['insertC'])" class="copy-btn">
                Copy
              </button>
            </div>
          </div>
        </div>
        <div id="select" class="hidden">
          <div class="btn_wrap">
            <button class="btn4" data-target="div7">Neo Shell</button>
            <button class="btn4" data-target="div1">Curl</button>
            <button class="btn4" data-target="div2">Python</button>
            <button class="btn4" data-target="div3">JavaScript</button>
            <button class="btn4" data-target="div4">Go</button>
            <button class="btn4" data-target="div5">C#</button>
          </div>
          <div class="main_container">
            <div id="div6">
              <p class="ternal_margin_top">
                <span class="yellow">machbase-neo</span> shell sql
                <span class="blue">'select * from EXAMPLE'</span>
              </p>
              <button
                @click="copyCode(`machbase-neo shell sql 'select * from EXAMPLE'`)"
                class="copy-btn"
              >
                Copy
              </button>
            </div>
            <div id="div7" class="hidden">
              <p class="ternal_margin_top">
                <span class="yellow">machbase-neo</span> shell sql
                <span class="blue">'select * from EXAMPLE'</span>
              </p>
              <button
                @click="copyCode(`machbase-neo shell sql 'select * from EXAMPLE'`)"
                class="copy-btn"
              >
                Copy
              </button>
            </div>
            <div id="div1" class="hidden">
              <p class="ternal_margin_top">
                curl
                <span class="orange">http://127.0.0.1:5654/db/query</span>
                \<br />
                &nbsp;&nbsp;<span class="orange"
                  >--data-urlencode "q=select * from EXAMPLE"</span
                >
              </p>
              <button
                @click="copyCode(this.codes['selectCurl'])"
                class="copy-btn"
              >
                Copy
              </button>
            </div>
            <div id="div2" class="hidden">
              <p class="ternal_margin_top">
                <span class="red">import </span>
                <span class="blue">requests</span><br />
                <span class="blue">params</span> = {<span class="orange"
                  >"q"</span
                >:<span class="orange">"select * from example"</span>,
                <span class="orange">"format":"csv"</span>,
                <span class="orange">"heading":"false"</span>} <br />
                <span class="blue">response</span> =
                <span class="blue">requests</span>.<span class="yellow"
                  >get</span
                >(<span class="orange">"http://127.0.0.1:5654/db/query"</span>,
                <span class="blue">params</span>)<br />
                print(<span class="blue">response</span>.<span class="yellow"
                  >text</span
                >)<br />
              </p>
              <button
                @click="copyCode(this.codes['selectPy'])"
                class="copy-btn"
              >
                Copy
              </button>
            </div>
            <div id="div3" class="hidden">
              <p class="ternal_margin_top">
                <span class="blue">q</span> =
                <span class="orange">"select * from example"</span><br />
                <span class="blue">fetch</span>(<span class="orange"
                  >`http://127.0.0.1:5654/db/query?q=$</span
                >{<span class="blue">encodeURIComponent</span>(<span
                  class="blue"
                  >q</span
                >)<span class="orange">}`</span>)<br />
                &nbsp;&nbsp;.<span class="yellow">then</span>(<span
                  class="yellow"
                  >res</span
                >
                => {<br />
                &nbsp;&nbsp;&nbsp;<span class="red">return </span>
                <span class="blue">res</span>.<span class="yellow">json</span
                >();<br />
                &nbsp;&nbsp;})<br />
                &nbsp;&nbsp;.<span class="yellow">then</span>(<span
                  class="yellow"
                  >data</span
                >
                => {<br />
                &nbsp;&nbsp;&nbsp;<span class="blue">console</span>.<span
                  class="yellow"
                  >log</span
                >(<span class="blue">data</span>)<br />
                &nbsp;&nbsp;});
              </p>
              <button
                @click="copyCode(this.codes['selectJs'])"
                class="copy-btn"
              >
                Copy
              </button>
            </div>
            <div id="div4" class="hidden">
              <p class="ternal_margin_top">
                <span class="blue">package</span> main<br />
                <span class="blue">import</span> (<br />
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span
                  class="orange"
                  >"net/http"<br />
                  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"io"</span
                ><br />)<br />
                <span class="blue">func</span>
                <span class="yellow">main</span>() {
                <br />&nbsp;&nbsp;&nbsp;&nbsp;<span class="blue">q</span> :=
                url.<span class="yellow">QueryEscape</span>(<span class="orange"
                  >"select * from example"</span
                >) <br />&nbsp;&nbsp;&nbsp;&nbsp;<span class="blue">rsp</span>,
                <span class="blue">_</span> := http.<span class="yellow"
                  >Get</span
                >(<span class="orange"
                  >"http://127.0.0.1:5654/db/query?format=csv&q="</span
                >+q)<br />
                &nbsp;&nbsp;&nbsp;&nbsp;<span class="blue">data</span>,
                <span class="blue">_</span> := io.<span class="yellow"
                  >ReadAll</span
                >(rsp.Body)<br />
                &nbsp;&nbsp;&nbsp;&nbsp;fmt.<span class="yellow">Println</span
                >(<span class="yellow">string</span>(data)) <br />}
              </p>
              <button
                @click="copyCode(this.codes['selectGo'])"
                class="copy-btn"
              >
                Copy
              </button>
            </div>
            <div id="div5" class="hidden">
              <p class="ternal_margin_top">
                <span class="red">using </span>
                <span class="blue">HttpClient client</span> =
                <span class="red">new</span>();<br />
                <br />
                <span class="red">var</span> <span class="blue">q</span> =
                <span class="blue">System.Net.WebUtility</span>.<span
                  class="yellow"
                  >UrlEncode</span
                >(<span class="orange">"select * from example"</span>);<br />
                <span class="red">var</span> <span class="blue">data</span> =
                <span class="red">await </span>
                <span class="blue">client</span>.<span class="yellow"
                  >GetStringAsync</span
                >(<br />
                &nbsp;&nbsp;&nbsp;&nbsp;"http://127.0.0.1:5654/db/query?format=csv&q="+q<br />
                );<br />
                <span class="blue">Console</span>.<span class="yellow"
                  >Write</span
                >(<span class="blue">data</span>);<br />
              </p>
              <button @click="copyCode(this.codes['selectC'])" class="copy-btn">
                Copy
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
<section class="section5 main_section5">
  <div>
    <h4 class="sub_title main_margin_top">Use Case</h4>
    <div class="bar"><img src="./img/bar.png" /></div>
  </div>
  <div class="main_usecase_wrap">
    <div class="main_usecase_box">
      <div class="main-usecase-img-wrap">
        <img
          class="main-usecase-img"
          alt="hyundai global"
          src="./img/hyundai_global.png"
        />
      </div>
      <div class="main_usecase_contents_box">
        <p class="main_usecase_contents">
          Machbase was able to provide a real-time monitoring service by
          collecting and storing CSV files containing data from sensors on ship
          engines through a schema structure that fits time series data.
        </p>
      </div>
      <div class="main_usecase_more_box">
        <p class="main_suecase_more">
          <span>
            <a class="main_usecase_more" href="/usecase-h">
              View More<ArrowSvg />
            </a>
          </span>
        </p>
      </div>
    </div>
    <div class="main_usecase_box">
      <div class="main-usecase-img-wrap2">
        <img class="main-usecase-img" alt="ETRI" src="./img/ETRI_logo.png" />
      </div>
      <div class="main_usecase_contents_box">
        <p class="main_usecase_contents">
          Using Machbase Time Series DB, we shortened the timeframe of a project
          to build an energy big data platform that collects and stores
          real-time power data to develop deep learning algorithms.
        </p>
      </div>
      <div class="main_usecase_more_box">
        <p class="main_usecase_more">
          <span>
            <a class="main_usecase_more" href="/usecase-e">
              View More<ArrowSvg />
            </a>
          </span>
        </p>
      </div>
    </div>
    <div class="main_usecase_box">
      <div class="main-usecase-img-wrap3">
        <img
          class="main-usecase-img"
          alt="carrot"
          src="./img/carrot-logo.png"
        />
      </div>
      <div class="main_usecase_contents_box3">
        <p class="main_usecase_contents">
          Machbase's reliable cluster operation has enabled Carrot's mileage
          insurance, which uses IoT devices, to collect real-time information on
          subscribers' vehicle operations and charge premiums based on that
          information.
        </p>
      </div>
      <div class="main_usecase_more_box">
        <span>
          <a class="main_usecase_more" href="/usecase-c"
            >View More<ArrowSvg />
          </a>
        </span>
      </div>
    </div>
  </div>
</section>
<section>
  <div>
    <h4 class="sub_title main_margin_top">Meet the Machbase Neo</h4>
    <div class="bar"><img src="./img/bar.png" /></div>
  </div>
  <div class="main_video">
    <iframe
      width="800"
      height="500"
      src="https://www.youtube.com/embed/1DR1TohMOc4?si=kNqjVRGDrmVhSaU3"
      title="YouTube video player"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      allowfullscreen
    ></iframe>
  </div>
</section>
<footer>
  <div class="footer_inner">
    <div class="footer-logo">
      <img src="./img/machbase_logo_w.png" />
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
            ><img src="./img/twitter.png"
          /></a>
        </div>
        <div>
          <a href="https://github.com/machbase" target="_blank"
            ><img src="./img/github.png"
          /></a>
        </div>
        <div>
          <a href="https://www.linkedin.com/company/machbase" target="_blank"
            ><img src="./img/linkedin.png"
          /></a>
        </div>
        <div>
          <a href="https://www.facebook.com/MACHBASE/" target="_blank"
            ><img src="./img/facebook.png"
          /></a>
        </div>
        <div>
          <a href="https://www.slideshare.net/machbase" target="_blank"
            ><img src="./img/slideshare.png"
          /></a>
        </div>
        <div>
          <a href="https://medium.com/machbase" target="_blank"
            ><img src="./img/medium.png"
          /></a>
        </div>
      </div>
    </div>
  </div>
  <div class="footer_tablet_inner">
    <div class="logo">
      <img src="./img/machbase_logo_w.png" />
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
            ><img src="./img/twitter.png"
          /></a>
        </div>
        <div>
          <a href="https://github.com/machbase" target="_blank"
            ><img src="./img/github.png"
          /></a>
        </div>
        <div>
          <a href="https://www.linkedin.com/company/machbase" target="_blank"
            ><img src="./img/linkedin.png"
          /></a>
        </div>
        <div>
          <a href="https://www.facebook.com/MACHBASE/" target="_blank"
            ><img src="./img/facebook.png"
          /></a>
        </div>
        <div>
          <a href="https://www.slideshare.net/machbase" target="_blank"
            ><img src="./img/slideshare.png"
          /></a>
        </div>
        <div>
          <a href="https://medium.com/machbase" target="_blank"
            ><img src="./img/medium.png"
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
