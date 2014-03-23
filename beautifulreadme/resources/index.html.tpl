<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="shortcut icon" href="../../assets/ico/favicon.ico">
    <title>{{ title }}</title>
    <!--<link href="static/css/bootstrap.min.css" rel="stylesheet">-->
    <link href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css" rel="stylesheet">
    <link href="static/css/blog.css" rel="stylesheet">
    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
    <style type="text/css">
    /* Override some bootstrap.css / blog.css styles */
    pre {
        word-wrap: normal;
    }

    .blog-footer {
        margin-top: 50px;
    }

    h2 {
        margin-top: 30px;
    }
    {{ customcss }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="blog-header">
        <h1 class="blog-title">{{ title }}</h1>
        <p class="lead blog-description">{{ description }}</p>
      </div>
      <div class="row">
        <div class="col-sm-8 blog-main">
        {{ body }}
        </div><!-- /.blog-main -->
        <!-- No affix sidebar for now, seems to be problematic (cf. issue tracker)
        <div data-spy="affix" data-offset-top="60" data-offset-bottom="200" class="col-sm-3 col-sm-offset-1 blog-sidebar">
        -->
        <div class="col-sm-3 col-sm-offset-1 blog-sidebar">
          <div class="sidebar-module sidebar-module-inset">
            <h4>About</h4>
            <p>{{ about }}</p>
          </div>
        {{ sidebar }}
        </div><!-- /.blog-sidebar -->
      </div><!-- /.row -->
    </div><!-- /.container -->
    <div class="blog-footer">
      <p><a href="#">Back to top</a></p>
      <p>{{ copyright }}</p>
      {% if attribution -%}
      <p>Created with <a href="http://gehrcke.de/beautiful-readme">beautiful-readme</a>.</p>
      {% endif -%}
    </div>
    <!--
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
    <script src="static/js/bootstrap.min.js"></script>
    -->
    {% if google_analytics_id -%}
    {#
      Define GA snippet. Official version from
      https://developers.google.com/analytics/devguides/collection/gajs/asyncTracking
      TODO: use optimized versin from HTML5 boilerplate project:
      https://github.com/h5bp/html5-boilerplate/issues/1444
    #}
    <script type="text/javascript">
      var _gaq = _gaq || [];i
      _gaq.push(['_setAccount', '{{ google_analytics_id }}']);
      _gaq.push(['_trackPageview']);
      (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      })();
    </script>
    {% endif -%}
  </body>
</html>
