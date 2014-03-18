<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="shortcut icon" href="../../assets/ico/favicon.ico">
    <title>$title</title>
    <link href="static/css/bootstrap.min.css" rel="stylesheet">
    <link href="static/css/blog.css" rel="stylesheet">
    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
    <style type="text/css">
    /* Override some bootstrap.css / blog.css styles */

    /* Add styles */
    .section {
        margin-top: 30px;
    }
    </style>
  </head>
  <body>
    <!--
    <div class="blog-masthead">
      <div class="container">
        <nav class="blog-nav">
          <a class="blog-nav-item active" href="#">Home</a>
          <a class="blog-nav-item" href="#">New features</a>
          <a class="blog-nav-item" href="#">Press</a>
          <a class="blog-nav-item" href="#">New hires</a>
          <a class="blog-nav-item" href="#">About</a>
        </nav>
      </div>
    </div>
    -->
    <div class="container">
      <div class="blog-header">
        <h1 class="blog-title">$title</h1>
        <p class="lead blog-description">$description</p>
      </div>
      <div class="row">
        <div class="col-sm-8 blog-main">
        $body
        </div><!-- /.blog-main -->
        <div class="col-sm-3 col-sm-offset-1 blog-sidebar">
          <div class="sidebar-module sidebar-module-inset">
            <h4>About</h4>
            <p>$about</p>
          </div>
        $sidebar
        </div><!-- /.blog-sidebar -->
      </div><!-- /.row -->
    </div><!-- /.container -->
    <div class="blog-footer">
      <p>$copyright</p>
      <p><a href="#">Back to top</a></p>
    </div>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <script src="../../dist/js/bootstrap.min.js"></script>
    <!-- I think these scripts are not required for now.
    <script src="../../assets/js/docs.min.js"></script>
    -->
    $googleanalytics
  </body>
</html>
