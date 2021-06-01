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
$varGET = sanitize($_GET, 'aKV');
$varPOST = sanitize($_POST, 'aKV');
//英数字のAsci化が望ましくないば項目は以下で個別処理

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

?>
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1480">

<title>管理画面ログイン -大同キャスティングス</title>
<link rel="stylesheet" type="text/css" href="/css/common.css">
<link rel="stylesheet" type="text/css" href="/css/manage.css">
<?php link_jquery(); ?>
<?php link_bootstrap(); ?>
</head>
<body>
<div id="wrap">
	<div id="contLogin">
		<h1>管理画面 ログイン</h1>
		<form id="frmLogin" name="frmLogin">
			<table id="tblLogin">
				<tr>
					<td>ID:</td>
					<td><input type="text" id="inp_id" name="inp_id" /></td>
				</tr>
				<tr>
					<td>PassWord:</td>
					<td><input type="password" id="inp_password" name="inp_password" /></td>
				</tr>
				<tr>
					<td colspan="2">
						<img id="imgIndicator" src="images/indicator.gif" alt="ログイン処理中" /><button type="button" id="btnLogin" class="btn btn-primary">ログイン</button>
					</td>
				</tr>
			</table>
			<div id="msgLogin">※IDとパスワードの組み合わせに誤りがあります。<br>入力されたIDもしくはパスワードまたはその両方に誤りがあります。</div>
		</form>
<script language="javascript">
$(function(){
	$('#btnLogin').on('click' ,function(){
		$('#imgIndicator').css('display', 'inline');
		$('#btnLogin').css('display', 'none');
		$('#msgLogin').css('display', 'none');
		var postdata = $("#frmLogin").serialize();
		var promiss = ajaxProc(postdata);
		promiss.done(function(){
			if( ret.result == true ){
				$('#imgIndicator').css('display', 'none');
				$('#btnLogin').css('display', 'inline');
				location.href = "./";
			} else {
				$('#imgIndicator').css('display', 'none');
				$('#btnLogin').css('display', 'inline');
				$('#msgLogin').css('display', 'inline');
			}
		});
		function ajaxProc(postdata) {
			var defer = $.Deferred();;
			var jqxhr = $.ajax({
				type: "POST",
				url: 'loginchk.php',
				data: postdata,
				dataType: 'json'
			}).always(function(msg){
				ret = msg;
				defer.resolve();
			});
			return defer;
		}
	});
});
</script>
	</div>
</div>
</body>
</html>