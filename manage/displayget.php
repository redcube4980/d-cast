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

//トランザクション処理,現在の登録内容を取得
try {
	$dbo->beginTransaction();
	$preparedSQL = "select * from DCAST_DISPLAY_MST;";
	$query = $dbo->prepare($preparedSQL);
	$query->execute();
	if( $query->rowCount() > 1 ){
		$query->closeCursor(); //クエリーの再利用可能化
		$preparedSQL = "TRUNCATE DCAST_DISPLAY_MST";
		$query = $dbo->prepare($preparedSQL);
		$query->execute();
		$query->closeCursor(); //クエリーの再利用可能化
		$ret['result'] = -16;
		$ret['template'] = '';
	} else if( $query->rowCount() == 1 ){
		$datas = $query->fetchAll( PDO::FETCH_ASSOC );
		$query->closeCursor(); //クエリーの再利用可能化
		$ret = $datas[0];
		$ret['result'] = 1;
	} else {
		$ret['result'] = 1;
		$ret['template'] = '0';
	}
} catch( PDOException $e ){
	$dbo->rollback();
	$ret['result'] = -16;
	$ret['template'] = '';
	echo json_encode($ret);
	exit(0);
}

echo json_encode($ret);
exit(0);
