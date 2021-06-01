<?php

//処理文字コードの指定
mb_language("Japanese");
mb_internal_encoding("UTF-8");
mb_regex_encoding("UTF-8");

//Include,Require
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

$msg['result'] = 0;
//Database接続
$dbo = dbconnect( $dbInst, $dbUser, $dbPass );
if( ! $dbo ){
	echo json_encode($msg);
	exit(0);
}

//ログイン確認
if( ! logincheck( $varSESSION['loginid'], $varSESSION['password'], $dbo ) ){
	echo json_encode($msg);
	exit(0);
}

//現パスワード確認
if( ! logincheck( $varSESSION['loginid'], $varPOST['inp_password'], $dbo, true ) ){
	$ret['result'] = -4;
	echo json_encode($ret);
	exit(0);
}

if( $varPOST['inp_newpassword'] != $varPOST['inp_repassword'] ) $msg['result'] = -1;

$match_len = mb_ereg("[a-zA-Z0-9]{5,18}", $varPOST['inp_newpassword'], $match);
if( count($match) != 1 || $match[0] != $varPOST['inp_newpassword'] ) $msg['result'] = -2;

if( $msg['result'] != 0){
	echo json_encode($msg);
	exit(0);
}

//更新処理
$preparedSQL = "update DCAST_USER_MST set passwordhash = :passwordhash where account = :account";
$query = $dbo->prepare($preparedSQL);
$passwordhash = pwd_hash( $varPOST['inp_newpassword'] );
$query->bindParam( ':account', $varSESSION['loginid'], PDO::PARAM_STR );
$query->bindParam( ':passwordhash', $passwordhash, PDO::PARAM_STR );
$query->execute();
if( $query->rowCount() != 1 ){
	$msg['result'] = -8;
} else {
	//セッション変数に保存
	$_SESSION['password'] = $varPOST['inp_newpassword'];
	$msg['result'] = 1;
}

echo json_encode($msg);
exit(0);
