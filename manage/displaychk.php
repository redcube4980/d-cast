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

//入力値の確認
$match_len = mb_ereg("[0-9]{1}", $varPOST['inp_display'], $match);
if ( count($match) == 1 && $match[0] == $varPOST['inp_display'] ) {
} else {
	$ret['resultX'] = 1;
	$ret['result'] = -16;
	echo json_encode($ret);
	exit(0);
}

//トランザクション処理,全件削除後登録
try {
	$dbo->beginTransaction();
	$preparedSQL = "TRUNCATE DCAST_DISPLAY_MST";
	$query = $dbo->prepare($preparedSQL);
	$query->execute();
	$query->closeCursor(); //クエリーの再利用可能化
	$preparedSQL = "insert into DCAST_DISPLAY_MST (template, updatedate) values (:template, :updatedate);";
	$query = $dbo->prepare($preparedSQL);
	$query->bindParam( ':template', $varPOST['inp_display'], PDO::PARAM_STR);
	$query->bindParam( ':updatedate', $dateString, PDO::PARAM_STR);
	$query->execute();
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
