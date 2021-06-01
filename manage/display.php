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
//英数字のAsci化が望ましくないば項目は以下で個別処理

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

<title>表示画面管理 -大同キャスティングス</title>
<link rel="stylesheet" type="text/css" href="/css/common.css">
<link rel="stylesheet" type="text/css" href="/css/manage.css">
<?php link_jquery(); ?>
<?php link_bootstrap(); ?>
</head>
<body>
<div id="wrap">
	<div id="contDisp">
		<h1>表示画面管理</h1>
		<form id="frmDisplay" name="frmDisplay">
			<table id="tblDispReg">
				<tr>
					<td>現在の表示内容</td>
					<td id="display_present">
						<img id="dispIndicator" src="images/indicator.gif" alt="処理中" />
						<span class="display_present" id="p5">新卒・プレエントリー・中途採用受付</span>
						<span class="display_present" id="p6">中途・プレエントリー受付</span>
						<span class="display_present" id="p4">新卒・プレエントリー受付</span>
						<span class="display_present" id="p3">新卒・中途採用エントリー受付</span>
						<span class="display_present" id="p7">プレエントリーのみ受付</span>
						<span class="display_present" id="p2">新卒採用のみ受付</span>
						<span class="display_present" id="p1">中途採用のみ受付</span>
						<span class="display_present" id="p0">エントリー受付なし</span>
						<span class="display_present" id="p-1">データ取得失敗</span>
					</td>
				</tr>
				<tr>
					<td>変更後の表示内容</td>
					<td>
						<select id="inp_display" name="inp_display">
							<option value="5">新卒・プレエントリー・中途採用受付</option>
							<option value="6">中途・プレエントリー受付</option>
							<option value="4">新卒・プレエントリー受付</option>
							<option value="3">新卒・中途採用エントリー受付</option>
							<option value="7">プレエントリーのみ受付</option>
							<option value="2">新卒採用のみ受付</option>
							<option value="1">中途採用のみ受付</option>
							<option value="0">エントリー受付なし</option>
						</select>
					</td>
				</tr>
				<tr>
					<td colspan="2">
						<img id="imgIndicator" src="images/indicator.gif" alt="登録中" /><button type="button" id="btnRegist" class="btn btn-primary">登　　録</button>&nbsp;&nbsp;
						<button type="button" id="btnBack" class="btn btn-info btn-sm">メニューに戻る</button>
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
	updateDisplay();

	$('#btnRegist').on('click' ,function(){
		$('#imgIndicator').css('display', 'inline');
		$('#btnRegist').css('display', 'none');
		$('.errMessage, .resMessage').css('display', 'none');
		var postdata = $("#frmDisplay").serialize();
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
			updateDisplay();
		});
		function ajaxProc(postdata) {
			var defer = $.Deferred();;
			var jqxhr = $.ajax({
				type: "POST",
				url: 'displaychk.php',
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

//登録内容を取得
function updateDisplay(){
	var promiss = ajaxProcList();
	promiss.done(function(){
		if( ret.result == 1 ){
			$('.display_present').css('display', 'none');
			$('#p' + ret.template ).css('display', 'inline');
			$('#dispIndicator').css('display', 'none');
		} else {
			$('.display_present' + ret.template ).css('display', 'none');
			$('#p-1').css('display', '');
			$('#dispIndicator').css('display', 'none');
		}
	});
}
function ajaxProcList() {
	var defer = $.Deferred();
	var jqxhr = $.ajax({
		type: "POST",
		url: 'displayget.php',
		dataType: 'json'
	}).always(function(msg){
		ret = msg;
		defer.resolve();
	});
	return defer;
}
</script>
	</div>
</div>
</body>
</html>
