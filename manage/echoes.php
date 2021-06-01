<?php

function link_jquery(){
echo <<< EOF
<!-- jQuery & UI -->
<script src="/jquery3/jquery.js"></script>
<link rel="stylesheet" type="text/css" href="/jquery3/ui/jquery-ui.min.css">
<link rel="stylesheet" type="text/css" href="/jquery3/ui/jquery-ui.structure.min.css">
<link rel="stylesheet" type="text/css" href="/jquery3/ui/jquery-ui.theme.min.css">
<script src="/jquery3/ui/jquery-ui.min.js"></script>
<!-- jQueryUI DatePicker i18n JA -->
<script src="/jquery3/ui/i18n/datepicker-ja.js"></script>

EOF;
}

function link_bootstrap(){
echo <<< EOF
<!-- Bootstrap -->
<script src="/bootstrap/js/bootstrap.min.js"></script>
<link rel="stylesheet" type="text/css" href="/bootstrap/css/bootstrap.min.css">
<link rel="stylesheet" type="text/css" href="/bootstrap/css/bootstrap-theme.min.css">

EOF;
}

?>
