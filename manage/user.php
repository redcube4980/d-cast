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

//Database接続
$dbo = dbconnect( $dbInst, $dbUser, $dbPass );
if( ! $dbo ){
	die("<br>\nシステム異常により処理が中断されました。システム担当者までご連絡下さい。");
}

//サニタイジング
$varCOOKIE = sanitize($_COOKIE, 'aKV');
$varSESSION = sanitize($_SESSION, 'aKV');
$varGET = sanitize($_GET, 'aKV');
$varPOST = sanitize($_POST, 'aKV');
//英数字のAscik化が望ましくないば項目は以下で個別処理

//初期設定済(ユーザー登録の有無)確認
if( ! initializedcheck( $dbo ) ){
	$title = "管理者ユーザー登録";
$repass = <<< EOF
				<tr>
					<td>PassWord(確認):</td>
					<td><input type="password" id="inp_repassword" name="inp_repassword" /></td>
				</tr>

EOF;
$script = <<< EOF
	$('#btnRegist').prop('disabled', true);
	$('input').blur(function(){
		if( $('#inp_password').val() !== '' && $('#inp_repassword').val() !== '' && $('#inp_id').val() !== '' && $('#inp_password').val() == $('#inp_repassword').val() ){
			$('#btnRegist').prop('disabled', false);
		} else {
			$('#btnRegist').prop('disabled', true);
		}
	});


EOF;
	$btnReset = "";
} else if( logincheck( $varSESSION['loginid'], $varSESSION['password'], $dbo ) ){ //ログイン確認
	$title = "ユーザーID変更";
	$repass = "";
	$script = "";
$btnReset = <<< EOF
						<button type="button" id="btnBack" class="btn btn-info btn-sm">メニューに戻る</button>

EOF;
} else {
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

<title><?php echo $title; ?> -大同キャスティングス</title>
<link rel="stylesheet" type="text/css" href="/css/common.css">
<link rel="stylesheet" type="text/css" href="/css/manage.css">
<?php link_jquery(); ?>
<?php link_bootstrap(); ?>
</head>
<body>
<div id="wrap">
	<div id="contUser">
		<h1><? echo $title; ?></h1>
		<form id="frmRegist" name="frmRegist">
			<table id="tblUserReg">
				<tr>
					<td>ID:</td>
					<td><input type="text" id="inp_id" name="inp_id" /></td>
				</tr>
				<tr>
					<td>PassWord:</td>
					<td><input type="password" id="inp_password" name="inp_password" /></td>
				</tr>
<?php echo $repass; ?>
				<tr>
					<td colspan="2">
						<img id="imgIndicator" src="images/indicator.gif" alt="登録中" /><button type="button" id="btnRegist" class="btn btn-primary">登　　録</button>&nbsp;&nbsp;
<?php echo $btnReset; ?>
					</td>
				</tr>
			</table>
			<div id="err-0" class="errMessage">※データ処理中に不明なエラーが発生しました。お手数をお掛けしますが暫く経ってから再度ご登録下さい。</div>
			<div id="err-1" class="errMessage">※入力されたユーザーIDに誤りがあります。登録をご希望のユーザーIDを、英数字と「_」「-」3～12文字にてご指定下さい。</div>
			<div id="err-2" class="errMessage">※入力されたパスワードに誤りがあります。登録をご希望のパスワードを、英数字5～18文字にてご指定下さい。</div>
			<div id="err-4" class="errMessage">※入力されたユーザーIDとパスワードの組み合わせに誤りがあります。</div>
			<div id="err-8" class="errMessage">※トランザクションに異常が発生しました。お手数をお掛けしますが暫く経ってから再度ご登録下さい。</div>
			<div id="err-16" class="errMessage">※データ処理中にエラーが発生しました。お手数をお掛けしますが暫く経ってから再度ご登録下さい。</div>
			<div id="msg-1" class="resMessage">※登録が完了しました。</div>
		</form>
<script language="javascript">
$(function(){
<?php echo $script; ?>
	$('#btnRegist').on('click' ,function(){
		$('#imgIndicator').css('display', 'inline');
		$('#btnRegist').css('display', 'none');
		$('.errMessage, .resMessage').css('display', 'none');
		var postdata = $("#frmRegist").serialize();
		var promiss = ajaxProc(postdata);
		promiss.done(function(){
			if( ret.result == -3 ){
				$('#err-1, #err-2').css('display', 'block');
			} else if( ret.result <= 0 ){
				$('#err' + ret.result).css('display', 'block');
			} else {
				$('#msg-1').css('display', 'block');
			}
			$('#imgIndicator').css('display', 'none');
			$('#btnRegist').css('display', 'inline');
		});
		function ajaxProc(postdata) {
			var defer = $.Deferred();;
			var jqxhr = $.ajax({
				type: "POST",
				url: 'userchk.php',
				data: postdata,
				dataType: 'json'
			}).always(function(msg){
				ret = msg;
				defer.resolve();
			});
			return defer;
		}
	});
	$('#btnBack').on('click', function(){
		location.href = './';
	});
});
</script>
	</div>
</div>
</body>
</html>
