<!DOCTYPE html>

<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ -->
<!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en"> <![endif]-->
<!--[if IE 7]>    <html class="no-js lt-ie9 lt-ie8" lang="en"> <![endif]-->
<!--[if IE 8]>    <html class="no-js lt-ie9" lang="en"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en"> <!--<![endif]-->

<head>
  <meta charset="utf-8" />

  <!-- Set the viewport width to device width for mobile -->
  <!--
  <meta name="viewport" content="width=800" />
  -->

  <title>Meerkat</title>

  <!-- Included CSS Files -->
  <link rel="stylesheet" href="/static/css/bootstrap.min.css">
  <link rel="stylesheet" href="/static/css/meerkat.css">
  <link href='http://fonts.googleapis.com/css?family=Lato:300,400' rel='stylesheet' type='text/css'>

  <!-- Custom Modernizr for Foundation -->
  <!--
  <script src="/static/javascripts/foundation/modernizr.foundation.js"></script>
  -->
</head>

<body>
  <div id="loading"><img src="/static/img/loading.gif" alt="loading.."/></div>

  <header class="navbar" id="header">
    <div class="navbar-inner">
      <h1>meerkat</h1>
    </div>
  </header>
  <div class="container" id="container">
    <div id="alert" class="alert alert-error">
        <button type="button" class="close" data-dismiss="alert">×</button>
        <strong class="title"></strong>
        <pre class="body"></pre>
    </div>
    <section class="row" id="master">
      <h2>
        <i class="icon-info-sign"></i>
        info
      </h2>
      <div id="system-tools" class="row">
        <div class="inner">
          <a href="data" class="btn" id="masterDownload"><i class="icon-list-alt"></i> Download data</a>
          <button class="btn" id="missionControlRegister"><i class="icon-bullhorn"></i> Ping mission control</button>
          <button class="btn" id="joinClickWifi"><i class="icon-globe"></i> Join click wifi</button>
          <button class="btn" id="joinCityWifi"><i class="icon-globe"></i> Join city wifi</button>
          <button class="btn" id="getGPSProcs"><i class="icon-globe"></i> Get GPS procs</button>
          <button class="btn btn-warning" id="kickstartGPS"><i class="icon-globe icon-white"></i> Kickstart GPS</button>
          <button class="btn btn-warning" id="cleanupGPS"><i class="icon-globe icon-white"></i> Clean up GPS</button>
        </div>
      </div>
      <div class="section-body row">
        <div id="img-holder">
            <div id="capture-img">
              <a href="/static/img/capture/manual_capture.jpg"><img src="/static/img/capture/manual_capture.jpg"/></a>
            </div>
            <div id="latest-img">
              <a href="/static/img/capture/latest.jpg"><img src="/static/img/capture/latest.jpg"/></a>
            </div>
        </div>

        <dl class="dl-horizontal">
          <dt class="status">status</dt>
          <dd class="status"><!-- [on/off] --></dd>
          <dt class="ip_address">ip address</dt>
          <dd class="ip_address"><!-- [ip.address] --></dd>
          <dt class="ip_address2">ip address 2</dt>
          <dd class="ip_address2"><!-- [ip.address2] --></dd>
          <dt class="net_interfaces">net interfaces</dt>
          <dd class="net_interfaces"><!-- [net_interfaces] --></dd>
          <dt class="cur_essid">current ESSID</dt>
          <dd class="cur_essid"><!-- [cur_essid] --></dd>
          <dt class="host">host</dt>
          <dd class="host"><!-- [host] --></dd>
          <dt class="uptime">uptime</dt>
          <dd class="uptime"><!-- [1:23] --></dd>
          <dt class="load_average">load average</dt>
          <dd class="load_average"><!-- [1.23] --></dd>
          <dt class="sys_temperature">system temp.</dt>
          <dd class="sys_temperature"><!-- [12.34] --></dd>
          <dt class="gpu_temperature">gpu temp.</dt>
          <dd class="gpu_temperature"><!-- [12.34] --></dd>
          <dt class="data_size">data size</dt>
          <dd class="data_size"><!-- [xMB] --></dd>
          <dt class="image_data_size">image data size</dt>
          <dd class="image_data_size"><!-- [xMB] --></dd>
          <dt class="free_space">free space</dt>
          <dd class="free_space"><!-- [yMB] --></dd>
          <dt class="available_memory">available RAM</dt>
          <dd class="available_memory"><!-- [xKB] --></dd>
          <dt class="free_memory">free RAM</dt>
          <dd class="free_memory"><!-- [yKB] --></dd>
          <dt class="lodation">location</dt>
          <dd class="location"><span class="lat"></span>, <span class="lon"></span></dd>
          <dt class="mission_control">mission control</dt>
          <dd class="mission_control"><a href=""><!--[mission control url]--></a></dd>
        </dl>
        <div id="tools" class="row">
          <div class="inner">
            <button type="button" class="btn btn-info refresh" id="masterRefresh"><i class="icon-refresh icon-white"></i> Refresh</button>
            <button type="button" class="btn btn-info" id="masterCapture"><i class="icon-camera icon-white"></i> Capture photo</button>
          </div>
        </div>
      </div>

    </section>
    <section class="row" id="probes">
      <h2>
        <i class="icon-eye-open"></i>
        probes
        <button type="button" class="btn pull-right" id="masterToggle"><i class="icon-off icon-white"></i> <span class="lbl">ON/OFF</span></button>
      </h2>
      <div class="section-body">
        <!--START:PROBE -->
        <div class="probe row" id="probe.label">
          <h3>
            <i class="icon-chevron-right"></i>
            <span class="probe-label">probe.label</span>
            <button type="button" class="probeToggle btn btn-small pull-right"><i class="icon-off icon-white"></i> <span class="lbl">ON/OFF</span></button>
          </h3>
          <div class="probe-body">
            <div class="row status probe-section">
              <h4><i class="icon-info-sign"></i> info</h4>
              <dl class="dl-horizontal">
                <dt class="status">status</dt>
                <dd class="status"><!-- [on/off] --></dd>
                <dt class="interval">interval</dt>
                <dd class="interval"><!-- [interval] --></dd>
                <dt class="duration">duration</dt>
                <dd class="duration"><!-- [duration] --></dd>
                <dt class="command">command</dt>
                <dd class="command"><!-- [command] --></dd>
                <dt class="last_error">last error</dt>
                <dd class="last_error"><pre><!-- [error] --></pre></dd>
              </dl>
              <button type="button" class="probeRefresh btn btn-info refresh"><i class="icon-refresh icon-white"></i> refresh</button>
            </div>
            <div class="row data probe-section">
              <h4><i class="icon-th-list"></i> last data</h4>
              <!-- data table here -->
              <div class="dbody">
              </div>
            </div>
            <div class="row filters probe-section">
              <h4><i class="icon-wrench"></i> filters</h4>
              <!-- filters here -->
              <ol>
                <li></li>
              </ol>
            </div>
            <div class="row error-filters probe-section">
              <h4><i class="icon-wrench"></i> error filters</h4>
              <!-- error filters here -->
              <ol>
                <li></li>
              </ol>
            </div>
          </div>
        </div>
        <!--END:PROBE -->
      </div>
    </section>
    <section class="row" id="log">
      <h2>
        <i class="icon-list"></i> log
        <button type="button" id="logRefresh" class="btn btn-info refresh pull-right"><i class="icon-refresh icon-white"></i> refresh</button>
      </h2>
      <div class="section-body">
        <!-- log here -->
        <pre>
        </pre>
      </div>
    </section>
  </div>
  <footer>
    <p>
    <i class="icon-hand-right"></i> Konrad Markus/HIIT &lt;<a href="mailto:konrad.markus@hiit.fi">konrad.markus@hiit.fi</a>&gt;
    </p>
  </footer>

  <!-- Included JS Files -->
  <script src="/static/js/bootstrap.min.js"></script>
  <script src="/static/js/jquery.js"></script>
  <script src="/static/js/pure_min.js"></script>
  <script src="/static/js/json-to-table.js"></script>
  <script src="/static/js/meerkat.js"></script>
</body>
</html>
