<?php

//処理文字コードの指定
mb_language("Japanese");
mb_internal_encoding("UTF-8");
mb_regex_encoding("UTF-8");

//Include,Require
include_once("echoes.php");
include_once("subroutine.php");
include_once("dbinfo.php");

//時刻取得
$dateSerial = time();
$dateString = date('Y/m/d H:i:s', $dateSerial);

//CookieによるSession管理Start
session_set_cookie_params(0);
session_start();

//サニタイジング
$varCOOKIE = sanitize($_COOKIE, 'aKV');
$varSESSION = sanitize($_SESSION, 'aKV');

//Database接続
$dbo = dbconnect( $dbInst, $dbUser, $dbPass );
if( ! $dbo ){
	die("<br>\nシステム異常により処理が中断されました。システム担当者までご連絡下さい。");
}

//初期設定済(ユーザー登録の有無)確認
if( ! initializedcheck( $dbo ) ){
	header ("HTTP/1.1 302 Found");
	header ("Location: ./user.php");
	exit(0);
}

//ログイン確認
if( ! logincheck( $varSESSION['loginid'], $varSESSION['password'], $dbo ) ){
	header ("HTTP/1.1 302 Found");
	header ("Location: ./login.php");
	exit(0);
}

?>
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1480">

<title>管理画面-大同キャスティングス</title>
<link rel="stylesheet" type="text/css" href="/css/common.css">
<link rel="stylesheet" type="text/css" href="/css/manage.css">
<?php link_jquery(); ?>
<?php link_bootstrap(); ?>
</head>
<body>
<div id="wrap">
	<div id="contMenu">
		<h1>管理画面</h1>
		<p><button type="button" id="btnDisplay" class="btn btn-info">画面表示管理</button></p>
		<!--<p><button type="button" id="btnMail" class="btn btn-info">メールアドレス管理</button></p>-->
		<p><button type="button" id="btnUser" class="btn btn-info">ユーザー名変更</button></p>
		<p><button type="button" id="btnChange" class="btn btn-info">パスワード変更</button></p>
<script language="javascript">
$(function(){
	$('#btnDisplay').on('click', function(){
		location.href = 'display.php';
	});
	$('#btnMail').on('click', function(){
		location.href = 'mail.php';
	});
	$('#btnUser').on('click', function(){
		location.href = 'user.php';
	});
	$('#btnChange').on('click', function(){
		location.href = 'changepassword.php';
	});
});
</script>
	</div>
</div>
</body>
</html>
