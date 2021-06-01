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

<title>パスワード変更 -木曽駒高原宇山カントリークラブ</title>
<link rel="stylesheet" type="text/css" href="/css/common.css">
<link rel="stylesheet" type="text/css" href="/css/manage.css">
<? link_jquery(); ?>
<? link_bootstrap(); ?>
</head>
<body>
<div id="wrap">
	<div id="contChange">
		<h1>パスワード変更</h1>
		<form id="frmChange" name="frmChange">
			<table id="tblLogin">
				<tr>
					<td>PassWord(現):</td>
					<td><input type="password" id="inp_password" name="inp_password" /></td>
				</tr>
				<tr>
					<td>PassWord(新):</td>
					<td><input type="password" id="inp_newpassword" name="inp_newpassword" /></td>
				</tr>
				<tr>
					<td>PassWord(新，確認用):</td>
					<td><input type="password" id="inp_repassword" name="inp_repassword" /></td>
				</tr>
				<tr>
					<td colspan="2">
						<button type="button" id="btnChange" class="btn btn-primary">パスワード変更</button>&nbsp;&nbsp;
						<button type="button" id="btnBack" class="btn btn-info btn-sm">メニューに戻る</button>
					</td>
				</tr>
			</table>
			<div id="err-0" class="errMessage">※データ処理中に不明なエラーが発生しました。お手数をお掛けしますが暫く経ってから再度ご登録下さい。</div>
			<div id="err-1" class="errMessage">※入力された新パスワードと新パスワード(確認用)が一致しません。</div>
			<div id="err-2" class="errMessage">※入力された新パスワードに誤りがあります。登録をご希望のパスワードを、英数字5～18文字にてご指定下さい。</div>
			<div id="err-4" class="errMessage">※入力された現パスワードに誤りがあります。</div>
			<div id="err-8" class="errMessage">※トランザクションに異常が発生しました。お手数をお掛けしますが暫く経ってから再度ご登録下さい。</div>
			<div id="msg-1" class="resMessage">※パスワード変更が完了しました。</div>
		</form>
<script language="javascript">
$(function(){
	$('#btnChange').on('click' ,function(){
		$('#imgIndicator').css('display', 'inline');
		$('.errMessage, .resMessage').css('display', 'none');
		var postdata = $("#frmChange").serialize();
		var promiss = ajaxProc(postdata);
		promiss.done(function(){
			if( ret.result <= 0 ){
				$('#err' + ret.result).css('display', 'block');
			} else {
				$('#msg-1').css('display', 'block');
			}
			$('#btnRegist').css('display', 'inline');
			$('#imgIndicator').css('display', 'none');
		});
		function ajaxProc(postdata) {
			var defer = $.Deferred();;
			var jqxhr = $.ajax({
				type: "POST",
				url: 'changepasswordchk.php',
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