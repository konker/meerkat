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
  <link rel="stylesheet" href="static/css/bootstrap.min.css">
  <link rel="stylesheet" href="static/css/meerkat.css">

  <!-- Custom Modernizr for Foundation -->
  <!--
  <script src="static/javascripts/foundation/modernizr.foundation.js"></script>
  -->
</head>

<body>
  <!-- Page Layout HTML here -->
  <header class="navbar navbar-inverse navbar-fixed-top" id="header">
    <div class="navbar-inner">
      <h1>meerkat control</h1>
    </div>
  </header>
  <div class="container" id="container">
    <div id="alert" class="alert alert-error">
        <button type="button" class="close" data-dismiss="alert">×</button>
        <strong class="title"></strong>
        <span class="body"></span>
    </div>
    <section class="row" id="nodes">
      <h2>
        <i class="icon-eye-open"></i>
        nodes
        <button type="button" class="btn btn-warning refresh pull-right" id="nodesRefresh"><i class="icon-refresh icon-white"></i> Refresh</button>
      </h2>
      <div class="section-body">
        <!-- nodes -->
      </div>
    </section>
    <section class="row" id="log">
      <h2>
        <i class="icon-list"></i> log
        <button type="button" id="logRefresh" class="btn btn-warning refresh pull-right"><i class="icon-refresh icon-white"></i> refresh</button>
      </h2>
      <div class="section-body">
        <!-- log here -->
        <pre>
        </pre>
      </div>
    </section>
  </div>
  <div id="templates">
      <!--START:NODE -->
      <div class="node row" id="node.label">
        <h3>
          <i class="icon-chevron-right"></i>
          <span class="node-label">node.label</span>
          <button type="button" class="nodeToggle btn btn-small pull-right"><i class="icon-off icon-white"></i> <span class="lbl">ON/OFF</span></button>
        </h3>
        <div class="node-body">
          <div class="row status node-section">
            <h4><i class="icon-info-sign"></i> info</h4>
            <dl class="dl-horizontal">
              <dt class="status">status</dt>
              <dd class="status"><!-- [on/off] --></dd>
            </dl>
            <div id="latest-img">
            <!--
              <a href="static/img/latest.jpg"><img src="static/img/latest.jpg"/></a>
            -->
            </div>
            <button type="button" class="nodeRefresh btn btn-warning refresh"><i class="icon-refresh icon-white"></i> refresh</button>
          </div>
        </div>
      </div>
      <!--END:NODE -->
  </div>
  <footer>
    <p>
    <i class="icon-hand-right"></i> Konrad Markus/HIIT &lt;<a href="mailto:konrad.markus@hiit.fi">konrad.markus@hiit.fi</a>&gt;
    </p>
  </footer>

  <!-- Included JS Files -->
  <script src="static/js/bootstrap.min.js"></script>
  <script src="static/js/jquery.js"></script>
  <script src="static/js/pure_min.js"></script>
  <script src="static/js/json-to-table.js"></script>
  <script src="static/js/meerkat.js"></script>
</body>
</html>
