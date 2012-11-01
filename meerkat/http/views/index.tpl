<!DOCTYPE html>

<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ -->
<!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en"> <![endif]-->
<!--[if IE 7]>    <html class="no-js lt-ie9 lt-ie8" lang="en"> <![endif]-->
<!--[if IE 8]>    <html class="no-js lt-ie9" lang="en"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en"> <!--<![endif]-->

<head>
  <meta charset="utf-8" />

  <!-- Set the viewport width to device width for mobile -->
  <meta name="viewport" content="width=device-width" />

  <title>Meerkat</title>

  <!-- Included CSS Files, use foundation.css if you do not want minified code -->
  <link rel="stylesheet" href="static/stylesheets/foundation.min.css">
  <link rel="stylesheet" href="static/stylesheets/app.css">

  <!-- Custom Modernizr for Foundation -->
  <script src="static/javascripts/foundation/modernizr.foundation.js"></script>
</head>

<body>
  <!-- Page Layout HTML here -->
  <header>
    <div class="row">
        <div class="twelve columns">
            <h1><img src="static/images/logo.png" /> Meerkat</h1>
        </div>
    </div>
  </header>
  <section class="row">
    <h2>Probes</h2>
      %for probe in scheduler.probes:
        <div class="probe row">
            {{probe.id}}
        </div>
      %end
  </section>

  <!-- Latest version of jQuery -->
  <script src="static/javascripts/jquery.js"></script>

  <!-- Included JS Files (Minified) -->
  <script src="static/javascripts/foundation.min.js"></script>

  <!-- Initialize JS Plugins -->
  <script src="static/javascripts/app.js"></script>
</body>
</html>
