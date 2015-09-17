<!DOCTYPE html>
<html lang="<?php print $language->language; ?>" dir="<?php print $language->dir; ?>" <?php print $rdf_namespaces; ?>>
  <head>
    <?php print $head; ?>
  
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  
    <title><?php print $head_title ?></title>
 
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <?php print $styles; ?>
    <?php print $scripts; ?>

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/8.8.0/styles/solarized_light.min.css">
    <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/8.8.0/highlight.min.js"></script>
    
    
    <!--[if gte IE 10]><!--><link rel="stylesheet" href="{{ ROOT_URL }}/css/campl.css"><!--<![endif]-->
    <!--[if lte IE 9 ]>
      <link rel="stylesheet" href="{{ ROOT_URL }}/css/campl_legacy.css">
    <![endif]-->
    <script type="text/javascript" src="https://code.jquery.com/jquery-1.11.3.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.10.6/moment.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.10.6/locale/en-gb.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/js-cookie/2.0.3/js.cookie.js"></script>
    {% for src, dst in JS %}
    <script type="text/javascript" src="{{ ROOT_URL }}/js/{{ dst }}"></script>
    {% endfor %}
    <script type="text/javascript" src="//use.typekit.com/hyb5bko.js"></script>
    <script type="text/javascript">
      try {
        Typekit.load();
      } catch (e) {
      }
    </script>
  </head>
  <body class="offcanvas offcanvas-left theme-turquoise <?php print $classes; ?>" <?php print $attributes ?>>
    <?php print $page_top; ?>
    
    <?php print $page; ?>
    
    <?php print $scripts; ?>
    
    <?php print $page_bottom; ?>
  </body>
</html>