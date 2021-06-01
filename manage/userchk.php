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
if( initializedcheck($dbo) && ! logincheck( $varSESSION['loginid'], $varPOST['inp_password'], $dbo, true ) ){
	$ret['result'] = -4;
	echo json_encode($ret);
	exit(0);
}

//入力値確認 ID,Password
$ret['result'] = 0;
$match_len = mb_ereg("[a-zA-Z0-9_-]{3,12}", $varPOST['inp_id'], $match);
if( count($match) != 1 || $match[0] != $varPOST['inp_id'] ) $ret['result'] += -1;
$match_len = mb_ereg("[a-zA-Z0-9]{5,18}", $varPOST['inp_password'], $match);
if( count($match) != 1 || $match[0] != $varPOST['inp_password'] ) $ret['result'] += -2;
if( $ret['result'] != 0 ){
	echo json_encode($ret);
	exit(0);
}

//トランザクション処理,全件削除後登録
try {
	$dbo->beginTransaction();
	$preparedSQL = "TRUNCATE DCAST_USER_MST";
	$query = $dbo->prepare($preparedSQL);
	$query->execute();
	$query->closeCursor(); //クエリーの再利用可能化
	$preparedSQL = "insert into DCAST_USER_MST (account, passwordhash, updatedate) values (:account, :passwordhash, :updatedate);";
	$query = $dbo->prepare($preparedSQL);
	$query->bindParam( ':account', $varPOST['inp_id'], PDO::PARAM_STR);
	$passwordhash = pwd_hash($varPOST['inp_password']);
	$query->bindParam( ':passwordhash', $passwordhash, PDO::PARAM_STR);
	$query->bindParam( ':updatedate', $dateString, PDO::PARAM_STR);
	$query->execute();
	//ID更新後は、セッション変数に保存
	$_SESSION['loginid'] = $varPOST['inp_id'];
	$_SESSION['password'] = $varPOST['inp_password'];
	if( $query->rowCount() != 1 ){
		$dbo->rollback();
		$ret['result'] = -8;
	} else {
		$dbo->commit();
		$ret['result'] = 1;
	}
} catch( PDOException $e ){
	$dbo->rollback();
	$ret['result'] = -16;
	echo json_encode($ret);
	exit(0);
}

echo json_encode($ret);
exit(0);
